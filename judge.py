import argparse
import clingo
import json
import pprint
import time
from typing import Any, Dict, Optional, Sequence
import os
from termcolor import colored
from pathlib import Path


parser = argparse.ArgumentParser(description="Run tests.")
parser.add_argument(
    "--assignment_dir",
    help="Directory containing the assignment to grade.",
)
parser.add_argument(
    "--instances_dir",
    help="Directory containing one directory per instance and their tests.",
)
parser.add_argument(
    "--output_name",
    help="The name of the test outputs.",
)
parser.add_argument(
    "--output_dir",
    help="Directory where to store the outputs.",
)
parser.add_argument("--base_files", nargs="*", default=[])

parser.add_argument("--verbose", type=bool, nargs="?", const=True, default=False)
parser.add_argument("--single_agent", type=bool, nargs="?", const=True, default=False)

ARGS = parser.parse_args()
ASSIGNMENT_PATH = Path(ARGS.assignment_dir)
INSTANCES_PATH = Path(ARGS.instances_dir)
OUTPUT_NAME = ARGS.output_name
OUTPUT_PATH = Path(ARGS.output_dir)
SINGLE_AGENT = ARGS.single_agent
VERBOSE = ARGS.verbose


def parse_constants(test_path: Path):
    constants = dict()
    with open(test_path) as file:
        for line in file:
            if line.startswith("%%% "):
                line = line.rstrip()
                line = line[4:]
                [key, value] = line.split("=", maxsplit=1)
                constants[key] = value
    return constants


def colored_status(status, expected) -> str:
    color = "red"
    if status == expected:
        color = "green"
    return colored("{}s".format(status), color)


def colored_time(time) -> str:
    color = "white"
    if time > 2:
        color = "yellow"
    if time > 10:
        color = "red"
    return colored("{:.3f}s".format(time), color)


class Instance:
    def __init__(
        self,
        instance_dir: Path,
        assignment_path: Path,
        output_path: Path,
        is_single_agent=False,
    ):
        # assignments/tarea-2-2021-2-$GITHUB_USER/
        self.assignment_path: Path = assignment_path

        # tests/csat/dep_hell/instances/0/
        self.instance_dir: Path = instance_dir
        # 0
        self.instance_name: str = os.path.basename(instance_dir)

        # tests/csat/dep_hell/instances/0/instance.lp
        self.instance_path: Path = instance_dir / "instance.lp"

        # From the --output_dir flag
        # assignments/tarea-2-2021-2-$GITHUB_USER/test_results/blocks-multi
        self.output_path: Path = output_path

        self.passed_output_path: Path = output_path / "passed"
        self.failed_output_path: Path = output_path / "failed"

        self.positive_tests = sorted(
            [
                self.instance_dir / p.name
                for p in Path(self.instance_dir).glob("pos-*.lp")
            ]
        )
        self.negative_tests = sorted(
            [
                self.instance_dir / p.name
                for p in Path(self.instance_dir).glob("neg-*.lp")
            ]
        )

        self.is_single_agent = is_single_agent

        self.test_results: Dict[str, Any] = dict()

    def __str__(self) -> str:
        return "Instance[assignment_path='{}', instance_dir='{}', instance_path='{}', output_path='{}]".format(
            str(self.assignment_path),
            str(self.instance_dir),
            str(self.instance_path),
            str(self.output_path),
        )

    def results_str(self) -> str:
        if self.test_results is None:
            return "{} has not been tested yet.".format(str(self.instance_dir))

        test_color = "red"
        if self.test_results["tested"] and self.test_results["passed"]:
            test_color = "green"
        s = "{}:\n".format(colored(str(self.instance_dir), test_color))

        # Show positive tests and validate them.
        for name, test in self.test_results["positive_tests"].items():
            s += "  + {}: {} (sols: {} time: {})\n".format(
                name,
                colored_status(test["status"],
                               expected=clingo.Status.SATISFIABLE),
                len(test["solutions"]),
                colored_time(test["time"]),
            )
            # Command
            s += "      {}\n".format(" ".join([str(a) for a in test["args"]]))

            # Models
            if len(test["solutions"]) == 0:
                s += "     ! no models\n"
            for i, (sol, ver) in enumerate(
                zip(test["solutions"], test["verifications"])
            ):
                color = "red"
                if ver["valid"]:
                    color = "green"
                if VERBOSE:
                    s += "      * model {}: {}\n".format(
                        i, colored(", ".join(sol), color)
                    )
                    s += "                 $ {}\n".format(ver["instance_summary"])
                else:
                    s += "      * model {}: $ {}\n".format(
                        i, colored(ver["instance_summary"], color)
                    )
                s += "                 > {}\n".format(ver["logs"])

        # Show negative tests they should have no solutions.
        for name, test in self.test_results["negative_tests"].items():
            s += "  - {}: {} (sols: {} time: {})\n".format(
                name,
                colored_status(test["status"],
                               expected=clingo.Status.UNSATISFIABLE),
                len(test["solutions"]),
                colored_time(test["time"]),
            )
            # Command
            s += "      {}\n".format(" ".join([str(a) for a in test["args"]]))

            # Models
            if len(test["solutions"]) > 0:
                s += "     ! Negative tests should have no models.\n"
            for i, (sol, ver) in enumerate(
                zip(test["solutions"], test["verifications"])
            ):
                if VERBOSE:
                    s += "      * model {}: {}\n".format(
                        i, colored(", ".join(sol), "red")
                    )
                else:
                    s += "      * model {}: $ {}\n".format(
                        i, colored(ver["instance_summary"], "red")
                    )
                s += "                 > {}\n".format(ver["logs"])

        return s[0:-1]

    def _run_clingo(self, test_path: Path, models: int, constants: Dict):
        run = clingo.run(
            [
                str(self.instance_path),
                str(test_path),
            ],
            base_files=ARGS.base_files,
            models=models,
            constants=constants,
        )

        if run["status"] == clingo.Status.UNKNOWN:
            print("="*100)
            print(colored(" ".join(run["args"]), "yellow"))
            print(colored(run, "magenta"))
            print("="*100)

        return run

    def verify(self, solution) -> Dict[str, Any]:
        return {
            "instance_summary": "",
            "valid": True,
            "logs": [],
        }

    def run_and_verify(self, test_path: Path):
        constants = parse_constants(test_path)

        models = 1
        if "MODELS" in constants:
            models = int(constants.pop("MODELS"))

        results = self._run_clingo(test_path, models, constants)
        results["verifications"] = [self.verify(sol) for sol in results["solutions"]]
        results["verified"] = all([ver["valid"] for ver in results["verifications"]])
        return results

    def test(self) -> Dict:
        if self.test_results:
            return self.test_results

        t0 = time.time()
        self.test_results = {
            "instance": str(self.instance_path),
            "positive_tests": {
                str(test): self.run_and_verify(test) for test in self.positive_tests
            },
            "negative_tests": {
                str(test): self.run_and_verify(test) for test in self.negative_tests
            },
        }
        self.test_results["instance_time"] = time.time() - t0

        self.test_results["tested"] = (
            len(self.test_results["positive_tests"])
            + len(self.test_results["negative_tests"])
            > 0
        )

        # All positive tests need to be SATISFIABLE and pass the verification.
        pos_tests_pass = all(
            run["status"] == clingo.Status.SATISFIABLE and run["verified"]
            for run in self.test_results["positive_tests"].values()
        )
        # All negative tests need to be UNSATISFIABLE
        neg_tests_pass = all(
            run["status"] == clingo.Status.UNSATISFIABLE
            for run in self.test_results["negative_tests"].values()
        )
        self.test_results["passed"] = pos_tests_pass and neg_tests_pass

        run_output: Path = self.failed_output_path
        if self.test_results["passed"]:
            run_output = self.passed_output_path
        instance_name = os.path.basename(self.instance_dir)
        run_output = run_output / (OUTPUT_NAME + "-" + instance_name + ".json")

        print(colored("Writing '{}'".format(run_output), "cyan"))

        with open(run_output, 'w') as f:
            json.dump({
                "instance": self.test_results["instance"],
                "positive_tests": {
                    str(k): {
                        "args": [str(part) for part in v["args"]],
                        "status": str(v["status"]),
                        "time": v["time"],
                        "timeout": v["timeout"],
                        "solutions": v["solutions"],
                        "stdout": v["stdout"],
                        "stderr": v["stderr"],
                        "verified": v["verified"],
                        "verifications": v["verifications"],
                    }
                    for k, v in self.test_results["positive_tests"].items()
                },
                "negative_tests": {
                    str(k): {
                        "args": [str(part) for part in v["args"]],
                        "status": str(v["status"]),
                        "time": v["time"],
                        "timeout": v["timeout"],
                        "solutions": v["solutions"],
                        "stdout": v["stdout"],
                        "stderr": v["stderr"],
                        "verified": v["verified"],
                        "verifications": v["verifications"],
                    }
                    for k, v in self.test_results["negative_tests"].items()
                },
                "instance_time": self.test_results["instance_time"],
                "tested": self.test_results["tested"],
                "passed": self.test_results["passed"],
            }, f)

        return self.test_results
