#!/usr/bin/env python

import os
import re

from pathlib import Path

import judge

from logging import LogLevel
from strips import StripsValidator


INSTANCES_PATH = judge.INSTANCES_PATH
OUTPUT_PATH = judge.OUTPUT_PATH


# Parse expressions
ARM = re.compile(r"^arm\((?P<name>.*)\)$")
BLOCK = re.compile(r"^block\((?P<name>.*)\)$")

F_ON = re.compile(r"^on\((?P<a>\w+),(?P<b>\w+)\)$")

A_EXT_MOVE = re.compile(r"^(?P<src>.*),(?P<dst>.*),(?P<extra>.*)$")
A_MOVE = re.compile(r"^(?P<src>.*),(?P<dst>.*)$")


def over(dest, on):
    """Returns the item directly over of the destination"""
    if dest == "table":
        return None
    for a, b in on.items():
        if dest == b:
            return a
    return None


def check_safe_move(t, arm, a, b, on, logs):
    if (blocking := over(a, on)) is not None:
        # `blocking` is over `a`
        logs.append(
            (
                LogLevel.ERROR,
                "Arm '{}' is executing move({}, {}), but at t={} {} is blocking {}.".format(
                    arm, a, b, t, blocking, a
                ),
            )
        )

    if b == "table":
        # It's always ok to move things to the table.
        return

    if (blocking := over(b, on)) is not None:
        # `blocking` is over `b`
        logs.append(
            (
                LogLevel.ERROR,
                "Arm '{}' is executing move({}, {}), but at t={} {} is blocking {}.".format(
                    arm, a, b, t, blocking, b
                ),
            )
        )


class BlocksValidator(StripsValidator):
    def __init__(self, solution):
        super().__init__(solution)

        self.arm: Set[str] = set()
        self.blocks: Set[str] = set()

        for pred in self.solution:
            skipped = False
            if (m := ARM.search(pred)) is not None:
                self.arm.add(m.group("name"))
            elif (m := BLOCK.search(pred)) is not None:
                self.blocks.add(m.group("name"))
            else:
                skipped = True
            if not skipped:
                if pred not in self.parsed_predicates:
                    self.parsed_predicates.add(pred)

    def verify(self):
        logs = super().verify()
        if logs is None:
            logs = []

        # Simulation
        on: Dict[str, str] = dict()

        for f in self.start:
            if (m := F_ON.search(f)) is not None:
                a = m.group("a")
                b = m.group("b")
                on[a] = b

        for t, instant_plan in enumerate(self.plan):
            # Check
            moves = dict()
            for agent, actions in instant_plan.items():
                if len(actions) > 1:
                    logs.append(
                        (
                            LogLevel.WARNING,
                            "Arm '{}' is executing multiple actions at t={}: [{}]".format(
                                agent, t, actions
                            ),
                        )
                    )

                for action in actions:
                    if (m := A_EXT_MOVE.search(action.args)) is not None:
                        logs.append(
                            (
                                LogLevel.INFO,
                                "Arm '{}' is executing {} at t={}, but we can only parse move/2.".format(
                                    agent, action, t
                                ),
                            )
                        )
                    elif (m := A_MOVE.search(action.args)) is not None:
                        a = m.group("src")
                        b = m.group("dst")
                        moves[a] = b
                        check_safe_move(t, agent, a, b, on, logs)
                    else:
                        logs.append(
                            (
                                LogLevel.WARNING,
                                "`move/2` should be the only action. Can't parse '{}'".format(action),
                            )
                        )

            # Check independence of actions at this instant
            destinations = [b for _a, b in moves.items()]
            destinations_set = set(destinations)
            if len(destinations) != len(destinations_set):
                # There's duplicate destinations
                logs.append(
                    (
                        LogLevel.ERROR,
                        "There's conflicts at t={}.".format(t),
                    )
                )

                # Explain the conflict
                targets = dict()
                for a, b in moves.items():
                    if not b in targets:
                        targets[b] = a
                        continue
                    logs.append(
                        (
                            LogLevel.ERROR,
                            "Executing conflicting actions move({}, {}) and move({}, {}) at t={}.".format(
                                a, b, targets[b], b, t
                            ),
                        )
                    )

            # Execute actions from this instant. (even under errors)
            for a, b in moves.items():
                # `a` is now over `b` (and not over the older block/table).
                on[a] = b
                assert a != "table"

        return logs


class BlocksWorldInstance(judge.Instance):
    def verify(self, solution):
        v = BlocksValidator(solution)
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
        instance = BlocksWorldInstance(
            instance_dir=instance_dir,
            assignment_path=judge.ASSIGNMENT_PATH,
            output_path=OUTPUT_PATH,
            is_single_agent=judge.SINGLE_AGENT,
        )

        instance.test()
        print(instance.results_str())


if __name__ == "__main__":
    main()
