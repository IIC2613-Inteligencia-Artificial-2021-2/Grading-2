#!/usr/bin/env python

from enum import Enum
from logging import LogLevel
from pathlib import Path
from termcolor import colored
from typing import Dict, Tuple, Set
from validator import Validator

import judge
import os
import pprint
import re


ASSIGNMENT_PATH = judge.ASSIGNMENT_PATH
INSTANCES_PATH = judge.INSTANCES_PATH
OUTPUT_PATH = judge.OUTPUT_PATH

# Parse expressions
PROGRAM_REGEX = re.compile(r"^program\((?P<p>.*)\)$")
VERSION_REGEX = re.compile(r"^version\((?P<l>.*),(?P<v>\d)\)$")
LOWER_BOUND_REGEX = re.compile(r"^requiresAtLeast\((?P<p>.*),(?P<l>.*),(?P<v>\d)\)$")
UPPER_BOUND_REGEX = re.compile(r"^requiresAtMost\((?P<p>.*),(?P<l>.*),(?P<v>\d)\)$")
INSTALLED_REGEX = re.compile(r"^installed\((?P<l>.*),(?P<v>\d)\)$")
SHOULD_DELETE_REGEX = re.compile(r"^shouldDelete\((?P<l>.*),(?P<v>\d)\)$")
SHOULD_INSTALL_REGEX = re.compile(r"^shouldInstall\((?P<l>.*),(?P<v>\d)\)$")
WANTS_REGEX = re.compile(r"^wants\((?P<p>.*)\)$")


def format_libs(libs):
    return ", ".join(["{}.so.{}".format(lib, v) for lib, v in libs])


class DependencyHellValidator(Validator):
    """A model of the Dependency Hell problem."""

    def __init__(self, solution):
        super().__init__(solution)

        # Existing programs
        self.programs: Set[str] = set()
        # Existing libraries and their versions
        self.libraries: Set[str] = set()
        self.lib_versions: Set[Tuple[str, int]] = set()

        # Needed programs
        self.wanted_programs: Set[str] = set()
        # Installed libraries
        self.installed_libraries: Set[Tuple[str, int]] = set()

        # Constraints
        self.lower_bounds: Set[Tuple[str, str, int]] = set()
        self.upper_bounds: Set[Tuple[str, str, int]] = set()

        # Goals
        self.desired_programs: Set[str] = set()

        # Suggestions
        self.should_delete: Set[Tuple[str, int]] = set()
        self.should_install: Set[Tuple[str, int]] = set()

        # Parse solution
        for pred in self.solution:
            skipped = False
            if (m := PROGRAM_REGEX.search(pred)) is not None:
                program = m.group("p")
                self.programs.add(program)
            elif (m := VERSION_REGEX.search(pred)) is not None:
                library = m.group("l")
                version = int(m.group("v"))
                self.libraries.add(library)
                self.lib_versions.add((library, version))
            elif (m := LOWER_BOUND_REGEX.search(pred)) is not None:
                program = m.group("p")
                library = m.group("l")
                version = int(m.group("v"))
                self.lower_bounds.add((program, library, version))
            elif (m := UPPER_BOUND_REGEX.search(pred)) is not None:
                program = m.group("p")
                library = m.group("l")
                version = int(m.group("v"))
                self.upper_bounds.add((program, library, version))
            elif (m := INSTALLED_REGEX.search(pred)) is not None:
                library = m.group("l")
                version = int(m.group("v"))
                self.installed_libraries.add((library, version))
            elif (m := SHOULD_DELETE_REGEX.search(pred)) is not None:
                library = m.group("l")
                version = int(m.group("v"))
                self.should_delete.add((library, version))
            elif (m := SHOULD_INSTALL_REGEX.search(pred)) is not None:
                library = m.group("l")
                version = int(m.group("v"))
                self.should_install.add((library, version))
            elif (m := WANTS_REGEX.search(pred)) is not None:
                program = m.group("p")
                self.desired_programs.add(program)
            else:
                skipped = True
            if not skipped:
                if pred not in self.parsed_predicates:
                    self.parsed_predicates.add(pred)

    def __str__(self) -> str:
        if self.valid is None:
            self.validate()
        return "DH[\n{}\n]".format(
            "\n".join(
                [
                    "  {}: {}".format(key, value)
                    for (key, value) in [
                        ("programs", ", ".join(sorted(self.programs))),
                        ("libraries", ", ".join(sorted(self.libraries))),
                        (
                            "lib versions",
                            ", ".join(
                                sorted(
                                    [
                                        "{} v{}".format(l, v)
                                        for l, v in self.lib_versions
                                    ]
                                )
                            ),
                        ),
                        (
                            "lower bounds",
                            ", ".join(
                                sorted(
                                    [
                                        "({}: {} v{})".format(p, l, v)
                                        for p, l, v in self.lower_bounds
                                    ]
                                )
                            ),
                        ),
                        (
                            "upper bounds",
                            ", ".join(
                                sorted(
                                    [
                                        "({}: {} v{})".format(p, l, v)
                                        for p, l, v in self.upper_bounds
                                    ]
                                )
                            ),
                        ),
                        (
                            "installed_libs",
                            ", ".join(
                                sorted(
                                    [
                                        "{} v{}".format(l, v)
                                        for l, v in self.installed_libraries
                                    ]
                                )
                            ),
                        ),
                        (
                            "delete",
                            ", ".join(
                                sorted(
                                    [
                                        "{} v{}".format(l, v)
                                        for l, v in self.should_delete
                                    ]
                                )
                            ),
                        ),
                        (
                            "install",
                            ", ".join(
                                sorted(
                                    [
                                        "{} v{}".format(l, v)
                                        for l, v in self.should_install
                                    ]
                                )
                            ),
                        ),
                        ("goal", ", ".join(sorted(self.desired_programs))),
                        ("valid", self.valid),
                        (
                            "issues",
                            "\n".join(self.coloured_logs()),
                        ),
                    ]
                ]
            )
        )

    def verify(self):
        logs = []

        # Simulate changes
        installed: Set[Tuple[str, int]] = set([lib for lib in self.installed_libraries])

        for del_lib in self.should_delete:
            if del_lib not in installed:
                logs.append(
                    (
                        LogLevel.ERROR,
                        "Asked to delete lib {}, but it's not installed".format(
                            del_lib
                        ),
                    )
                )
                continue
            installed.remove(del_lib)

        for add_lib in self.should_install:
            if add_lib in installed:
                logs.append(
                    (
                        LogLevel.WARNING,
                        "Asked to install lib {}, but it's already installed. This is odd, but allowed.".format(
                            del_lib
                        ),
                    )
                )
                continue
            installed.add(add_lib)

        for program in self.desired_programs:
            deps = set()

            for (l_p, lib, _) in self.lower_bounds:
                if program == l_p:
                    deps.add(lib)
            for (u_p, lib, _) in self.upper_bounds:
                if program == u_p:
                    deps.add(lib)

            for required_lib in deps:
                available_versions = sorted(
                    [
                        installed_version
                        for (installed_library, installed_version) in installed
                        if installed_library == required_lib
                    ]
                )

                if len(available_versions) == 0:
                    logs.append(
                        (
                            LogLevel.ERROR,
                            "Program {} needs library {}, but it's not installed.".format(
                                program, required_lib
                            ),
                        )
                    )
                    continue

                low = min(available_versions)
                high = max(available_versions)

                # NOTE: This should be indexed to avoid skipping most entries
                for (l_p, l_l, l_v) in self.lower_bounds:
                    if l_p != program:
                        continue
                    if l_l != required_lib:
                        continue
                    if l_v > low:
                        low = l_v
                for (u_p, u_l, u_v) in self.upper_bounds:
                    if u_p != program:
                        continue
                    if u_l != required_lib:
                        continue
                    if u_v < high:
                        high = u_v

                # `program` needs `required_lib` in a version \in [low, high]
                feasible_versions = [
                    version for version in available_versions if low <= version <= high
                ]
                if len(feasible_versions) == 0:
                    logs.append(
                        (
                            LogLevel.ERROR,
                            "Program {} needs library {} in a version in [{}, {}], but only these versions are available: {}".format(
                                program, required_lib, low, high, available_versions
                            ),
                        )
                    )

        return logs

    def instance_summary(self):
        return "Installed: [{}]  ShouldDelete: [{}]  ShouldInstall[{}]".format(
            format_libs(self.installed_libraries),
            format_libs(self.should_delete),
            format_libs(self.should_install),
        )


class DependencyHellInstance(judge.Instance):
    def verify(self, solution) -> Dict:
        dh = DependencyHellValidator(solution)
        return {
            "instance_summary": dh.instance_summary(),
            "valid": len(solution) > 0 and dh.is_valid(),
            "logs": "\n                 > ".join(dh.coloured_logs()),
        }


def main():
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    print("Output path: ", OUTPUT_PATH)

    for instance_dir in sorted(
        [INSTANCES_PATH / p.name for p in INSTANCES_PATH.glob("*/")]
    ):
        instance = DependencyHellInstance(
            instance_dir=instance_dir,
            assignment_path=ASSIGNMENT_PATH,
            output_path=OUTPUT_PATH,
        )

        instance.test()
        print(instance.results_str())


if __name__ == "__main__":
    main()
