#!/usr/bin/env python

from logging import LogLevel
import judge
import os
import re

from pathlib import Path
from strips import StripsValidator


INSTANCES_PATH = judge.INSTANCES_PATH
OUTPUT_PATH = judge.OUTPUT_PATH


# Parse expressions
AT_POS = re.compile(r"^at\((?P<x>\d+)\)$")
IS_RED = re.compile(r"^isRed\((?P<t>\d+)\)$")

# PROBLEM
COORDS = re.compile(r"^x\((?P<t>\d+)\)$")

# ACTIONS
MOVE = re.compile(r"^move\((?P<args>.*)\)$")
WAIT = re.compile(r"^wait\((?P<args>.*)\)$")


class StatuesValidator(StripsValidator):
    def __init__(self, solution):
        super().__init__(solution)

        self.start_pos: int = -1
        self.end_pos: int = -1

        self.is_red: Set[int] = set()

        # Times at which we plan to move
        self.steps: List[int] = []
        # Times at which we plan to wait
        self.pauses: List[int] = []

        for f in self.start:
            if (m := AT_POS.search(f)) is not None:
                pos = int(m.group("x"))
                self.start_pos = pos

        if len(self.goal) == 0:
            raise Exception("No goals, are you using `#show` and hiding it?")

        for f in self.goal:
            if (m := AT_POS.search(f)) is not None:
                pos = int(m.group("x"))
                self.end_pos = pos

        self.unexpected_actions = set()
        for t, instant_plan in self.plan.items():
            for agent, actions in instant_plan.items():
                for a in actions:
                    # Move:
                    if a.name == "move":
                        self.steps.append(t)
                    # Wait: Consider some alternative names too
                    elif a.name in ["wait", "stay"]:
                        self.pauses.append(t)
                    else:
                        self.unexpected_actions.add(a.name)

        for pred in self.solution:
            skipped = False
            if (m := IS_RED.search(pred)) is not None:
                self.is_red.add(int(m.group("t")))
            elif (m := COORDS.search(pred)) is not None:
                pass
            else:
                skipped = True
            if not skipped:
                if pred not in self.parsed_predicates:
                    self.parsed_predicates.add(pred)

    def verify(self):
        logs = []

        if self.unexpected_actions:
            actions = sorted(list(self.unexpected_actions))
            logs.append(
                (
                    LogLevel.WARNING,
                    "Got unexpected actions: [{}]".format(actions),
                )
            )

        if len(self.start) != 1:
            logs.append(
                (
                    LogLevel.WARNING,
                    "Multiple starting positions may be defined.",
                )
            )
        if len(self.goal) != 1:
            logs.append(
                (
                    LogLevel.WARNING,
                    "Multiple goal positions may be defined.",
                )
            )

        if len(self.agents) != 1:
            logs.append(
                (
                    LogLevel.ERROR,
                    "Multiple agents defined.",
                )
            )

        for t, instant_plan in self.plan.items():
            for agent, actions in instant_plan.items():
                if len(actions) > 1:
                    logs.append(
                        (
                            LogLevel.ERROR,
                            "Multiple actions executed at time {}: {}".format(
                                t, actions
                            ),
                        )
                    )

        if self.start_pos != 0:
            logs.append((LogLevel.WARNING, "Start position does not start at 0!"))
        if self.start_pos > self.end_pos:
            logs.append(
                (
                    LogLevel.WARNING,
                    "Start position is to the right of the goal position.",
                )
            )

        if self.start_pos == self.end_pos:
            logs.append(
                (LogLevel.ERROR, "Start position is the same as the end position.")
            )

        for t in self.steps:
            if t in self.is_red:
                logs.append(
                    (
                        LogLevel.ERROR,
                        "At time={} the light is red, but a `move` was planned.".format(
                            t
                        ),
                    )
                )

        if len(self.steps) == 0 and self.start_pos != self.end_pos:
            logs.append((LogLevel.WARNING, "No steps taken. Is there something wrong?"))

        pos = self.start_pos
        for t in self.steps:
            pos += 1

        if pos != self.end_pos:
            logs.append(
                (
                    LogLevel.ERROR,
                    "Goal position was {}, but got to {} instead.".format(
                        self.end_pos, pos
                    ),
                )
            )

        return logs


class StatuesInstance(judge.Instance):
    def verify(self, solution):
        v = StatuesValidator(solution)
        return {
            "instance_summary": v.instance_summary(sep="\n" + " "*26),
            "valid": len(solution) > 0 and v.is_valid(),
            "logs": "\n                 > ".join(v.coloured_logs()),
        }


def main():
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    print("Output path: ", OUTPUT_PATH)

    for instance_dir in sorted(
        [INSTANCES_PATH / p.name for p in INSTANCES_PATH.glob("*/")]
    ):
        instance = StatuesInstance(
            instance_dir=instance_dir,
            assignment_path=judge.ASSIGNMENT_PATH,
            output_path=OUTPUT_PATH,
            is_single_agent=judge.SINGLE_AGENT,
        )

        instance.test()
        print(instance.results_str())


if __name__ == "__main__":
    main()
