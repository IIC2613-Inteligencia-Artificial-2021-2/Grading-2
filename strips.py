#!/usr/bin/env python

import fileinput
import re

from termcolor import colored
from typing import Set
from validator import Validator

# STRIPS
TIME = re.compile(r"^time\((?P<t>\d+)\)$")
START = re.compile(r"^start\((?P<f>.*)\)$")
GOAL = re.compile(r"^goal\((?P<f>.*)\)$")
FLUENT = re.compile(r"^fluent\((?P<f>.*)\)$")
FLUENT_DROPPED = re.compile(r"^fluent_dropped\((?P<f>.*)\)$")
AGENT = re.compile(r"^agent\((?P<agent>.*)\)$")
ACTION = re.compile(r"^action\((?P<action>.*)\)$")
ACTION_PPRE = re.compile(r"^action_ppre\((?P<action>.*)\)$")
ACTION_NPRE = re.compile(r"^action_npre\((?P<action>.*)\)$")
ACTION_ADD = re.compile(r"^action_add\((?P<action>.*)\)$")
ACTION_DEL = re.compile(r"^action_del\((?P<action>.*)\)$")
HOLDS = re.compile(r"^holds\((?P<t>\d+),(?P<f>.*)\)$")
EXEC_SINGLE = re.compile(r"^exec\((?P<time>\d+),(?P<action>.*)\)$")
EXEC_MULTI = re.compile(r"^exec\((?P<time>\d+),(?P<agent>\w+),(?P<action>.*)\)$")


PREDICATE = re.compile(r"^(?P<name>\w+)\((?P<args>.*)\)$")


class Action:
    def __init__(self, raw_action):
        self.name = "(unknown)"
        self.args = ""
        if (m := PREDICATE.search(raw_action)) is not None:
            self.name = m.group("name")
            self.args = m.group("args")

    def __repr__(self):
        return "{}({})".format(self.name, self.args)

    def __str__(self):
        return "Action[{}({})]".format(self.name, self.args)


class Agent:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Agent[{}]".format(self.name)

    def __str__(self):
        return "Agent[{}]".format(self.name)

    def __hash__(self):
        return hash(self.name)


class StripsValidator(Validator):
    def __init__(self, solution):
        super().__init__(solution)

        # Parse time first to use time as dictionary keys
        self.time: Set[int] = set()
        self.max_time = -1

        self.agents: Dict[str, Agent] = dict()
        for pred in self.solution:
            skipped = False
            if (m := AGENT.search(pred)) is not None:
                agent_name = m.group("agent")
                self.agents[agent_name] = Agent(agent_name)
                self.parsed_predicates.add(pred)
            else:
                skipped = True
            if not skipped:
                self.parsed_predicates.add(pred)

        self.default_agent: Optional[Agent] = None
        if len(self.agents) == 0:
            self.agents["defaultAgent"] = Agent("defaultAgent")

        for pred in self.solution:
            skipped = False
            if (m := TIME.search(pred)) is not None:
                t = int(m.group("t"))
                self.time.add(t)
                if t > self.max_time:
                    self.max_time = t
                self.parsed_predicates.add(pred)
            else:
                skipped = True
            if not skipped:
                self.parsed_predicates.add(pred)

        # Parse everything
        # In python `exec` is a reserved keyword, so we use `plan` instead.
        self.plan: List[Dict[Agent, Set[Action]]] = [
            {agent: set() for agent in self.agents.values()} for _ in self.time
        ]

        # Add the extra time unit for `holds`
        self.time.add(self.max_time + 1)

        self.actions: Set[str] = set()
        self.fluents: Set[str] = set()
        self.holds: List[Set[str]] = [set() for _ in self.time]
        self.start: List[str] = []
        self.goal: List[str] = []

        for pred in self.solution:
            skipped = False
            if (m := TIME.search(pred)) is not None:
                pass
            elif (m := AGENT.search(pred)) is not None:
                pass
            elif (m := FLUENT.search(pred)) is not None:
                f = m.group("f")
                self.fluents.add(f)
            elif (m := FLUENT_DROPPED.search(pred)) is not None:
                pass
            elif (m := ACTION.search(pred)) is not None:
                self.actions.add(m.group("action"))
            elif (m := ACTION_PPRE.search(pred)) is not None:
                pass
            elif (m := ACTION_NPRE.search(pred)) is not None:
                pass
            elif (m := ACTION_ADD.search(pred)) is not None:
                pass
            elif (m := ACTION_DEL.search(pred)) is not None:
                pass
            elif (m := START.search(pred)) is not None:
                f = m.group("f")
                self.start.append(f)
            elif (m := GOAL.search(pred)) is not None:
                f = m.group("f")
                self.goal.append(f)
            elif (m := EXEC_MULTI.search(pred)) is not None:
                agent = self.agents[m.group("agent")]
                time = int(m.group("time"))
                action = Action(m.group("action"))
                self.plan[time][agent].add(action)
            elif (m := EXEC_SINGLE.search(pred)) is not None:
                agent = self.agents["defaultAgent"]
                time = int(m.group("time"))
                action = Action(m.group("action"))
                self.plan[time][agent].add(action)
            elif (m := HOLDS.search(pred)) is not None:
                t = int(m.group("t"))
                f = m.group("f")
                self.holds[t].add(f)
            else:
                skipped = True
            if not skipped:
                self.parsed_predicates.add(pred)

    def verify(self):
        logs = super().verify()

        if len(self.time) == 0:
            logs.append((LogLevel.WARNING, "No time defined!"))
        if len(self.plan) == 0:
            logs.append(
                (LogLevel.WARNING, "Empty plan, No actions executed (`exec` is empty).")
            )

        return logs

    def instance_summary(self, sep=", "):
        return "Plan: [{}]".format(
            sep.join([
                "{}: {}".format(t, str(i_p))
                for t, i_p in enumerate(self.plan)
            ]),
        )
