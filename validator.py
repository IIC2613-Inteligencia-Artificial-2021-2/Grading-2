import re

from enum import Enum
from logging import LogLevel
from termcolor import colored
from typing import Dict, List, Tuple, Set, Optional


PREDICATE = re.compile(r"^(?P<name>\w+)\((?P<args>.*)\)$")


class Validator:
    def __init__(self, solution: List[str]):
        # All predicates from the model
        self.solution = solution
        # All predicates that have been recognized
        self.parsed_predicates: Set[str] = set()

        self.valid: Optional[bool] = None
        self.logs: Optional[List[Tuple[LogLevel, str]]] = None

    def __str__(self) -> str:
        if not self.logs:
            return "Validator[(Uninitialized)]"

        return "Validator[\n{}\n]".format(
            "\n".join(
                [
                    "  {}: {}".format(key, value)
                    for (key, value) in [
                        ("solution", self.solution),
                        ("valid", self.valid),
                        (
                            "issues",
                            "\n".join(
                                [LogLevel.to_str(l, msg) for (l, msg) in self.logs]
                            ),
                        ),
                    ]
                ]
            )
        )

    def validate(self):
        if self.valid is not None:
            return

        self.logs = self.verify()

        ignored_predicates = set()
        for pred in self.solution:
            if pred in self.parsed_predicates:
                continue
            if (m := PREDICATE.search(pred)) is not None:
                predicate_name = m.group("name")
                ignored_predicates.add(predicate_name)
            else:
                raise Exception("Can't parse name for predicate '{}'".format(pred))

        if ignored_predicates:
            self.logs.append(
                (
                    LogLevel.WARNING,
                    "Ignored predicates: {}".format(sorted(list(ignored_predicates))),
                )
            )

        self.valid = True
        for (level, _) in self.logs:
            if level == LogLevel.ERROR:
                self.valid = False
                return

        self.logs.append((LogLevel.INFO, "No issues found!"))

    def verify(self) -> List[Tuple[LogLevel, str]]:
        return []

    def is_valid(self):
        if self.valid is None:
            self.validate()
        return self.valid

    def coloured_logs(self):
        if self.valid is None:
            self.validate()
        return [LogLevel.to_str(l, msg) for (l, msg) in self.logs]
