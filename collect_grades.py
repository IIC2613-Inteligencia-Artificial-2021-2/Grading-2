#!/usr/bin/env python

import contextlib
import copy
import json
import os
import re
import statistics
from collections import ChainMap
from decimal import Decimal
from pathlib import Path


@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


def file_to_string(file_path):
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            return f.read()


W_DH = Decimal("1.0")
W_STATUES = Decimal("1.0")
W_BLOCKS = Decimal("1.0")
W_BLOCKS_MULTIAGENT = Decimal("1.0")
W_COFFEE = Decimal("1.0")
W_COFFEE_MULTIAGENT = Decimal("1.0")

SCORES = {
    # Constraint Satisfaction
    # =======================
    # Dependency-hell
    # ---------------
    # - [0.8] Escriba un programa que pueda determinar soluciones factibles. No
    #         es necesario que determine todas las soluciones posibles, pero
    #         debe encontrar soluciones cuando hay.
    "dh-0.json": Decimal("0.1") * W_DH,
    "dh-1.json": Decimal("0.2") * W_DH,
    "dh-2.json": Decimal("0.2") * W_DH,
    "dh-3.json": Decimal("0.3") * W_DH,
    # - [0.7] ¿Cómo aseguraría que se usan las librerías más nuevas posibles?
    #         Agregue reglas que exijan esto.
    # -
    # Planning
    # ========
    # Statues
    # -------
    # - [0.3] Cree un programa en ASP que pueda resolver instancias como esta.
    #         Puede considerar agregar parámetros a ~move~ para convertirlo en
    #         una función en vez de una constante.
    "statues-0.json": Decimal("0.1") * W_STATUES,
    "statues-1.json": Decimal("0.1") * W_STATUES,
    "statues-2.json": Decimal("0.1") * W_STATUES,
    # - [0.2] ¿Qué restricciones de integridad agregaría para revisar que el
    #         problema tiene solución sin necesidad de tratar de encontrar un
    #         plan y fallar?.
    # "planning_statues_secret_3_test.py": Decimal("0.1") * W_STATUES,
    # "planning_statues_secret_4_test.py": Decimal("0.1") * W_STATUES,
    # Blocks-World
    # ------------
    # - Single-agent
    # - [1] Modele el mundo de bloques de forma de poder resolver instancias
    #       como esta
    "blocks-simple-sussman.json": Decimal("0.2") * W_BLOCKS,
    "blocks-simple-seq-0.json": Decimal("0.2") * W_BLOCKS,
    "blocks-simple-seq-1.json": Decimal("0.2") * W_BLOCKS,
    "blocks-simple-parallel-0.json": Decimal("0.1") * W_BLOCKS,
    "blocks-simple-parallel-1.json": Decimal("0.1") * W_BLOCKS,
    "blocks-simple-parallel-2.json": Decimal("0.2") * W_BLOCKS,
    "blocks-simple-parallel-3.json": Decimal("0.2") * W_BLOCKS,
    # - Multi-agent
    # - [1] Si un robot tuviese varios brazos que puedan operar en paralelo y
    #       sin chocar podríamos pensar que son 2 agentes que colaboran para
    #       lograr un objetivo común.
    #       Implemente una versión para multiples brazos que pueda resolver
    #       instancias como esta.
    "blocks-multi-move-0.json": Decimal("0.1") * W_BLOCKS_MULTIAGENT,
    "blocks-multi-seq-0.json": Decimal("0.2") * W_BLOCKS_MULTIAGENT,
    "blocks-multi-seq-1.json": Decimal("0.2") * W_BLOCKS_MULTIAGENT,
    "blocks-multi-parallel-0.json": Decimal("0.2") * W_BLOCKS_MULTIAGENT,
    "blocks-multi-parallel-1.json": Decimal("0.3") * W_BLOCKS_MULTIAGENT,
    # Coffee
    # ------
    # - Single-agent
    # - [1.5] Solucione el problema de repartir café.
    "coffee-single-move-0.json": Decimal("0.2") * W_COFFEE,
    "coffee-single-delivery-0.json": Decimal("0.2") * W_COFFEE,
    "coffee-single-delivery-1.json": Decimal("0.2") * W_COFFEE,
    "coffee-single-delivery-2.json": Decimal("0.3") * W_COFFEE,
    "coffee-single-delivery-3.json": Decimal("0.3") * W_COFFEE,
    "coffee-single-delivery-4.json": Decimal("0.3") * W_COFFEE,
    # - Multi-agent
    # - [1] Muestre que su solución también funciona para varios agentes al
    #       extender ~agentAt(Room)~ y ~has(Drink)~.
    "coffee-multi-implicit_doors.json": Decimal("0.05") * W_COFFEE_MULTIAGENT,
    "coffee-multi-move-0.json": Decimal("0.05") * W_COFFEE_MULTIAGENT,
    "coffee-multi-move-1.json": Decimal("0.1") * W_COFFEE_MULTIAGENT,
    "coffee-multi-move-2.json": Decimal("0.1") * W_COFFEE_MULTIAGENT,
    "coffee-multi-delivery-0.json": Decimal("0.2") * W_COFFEE_MULTIAGENT,
    "coffee-multi-delivery-1.json": Decimal("0.2") * W_COFFEE_MULTIAGENT,
    "coffee-multi-delivery-2.json": Decimal("0.3") * W_COFFEE_MULTIAGENT,
}


def grade(github_user):
    passed_tests = sorted([p.name for p in Path("test_results/passed").rglob("*.json")])
    failed_tests = sorted([p.name for p in Path("test_results/failed").rglob("*.json")])
    all_tests = [p for p in Path("test_results/passed").rglob("*.json")] + [
        p for p in Path("test_results/failed").rglob("*.json")
    ]
    test_data = {test_path.name: None for test_path in all_tests}
    for test_path in all_tests:
        with open(test_path, "r") as json_file:
            test_data[test_path.name] = json.load(json_file)

    # "dh-0.json": {
    #    "instance": "tests/csat/dep_hell/instances/0/instance.lp",
    #    "positive_tests": {},
    #    "negative_tests": {},
    #    "instance_time": 0.052,
    #    "tested": true,
    #    "passed": true
    # }

    # Python3.8 does not support Union (operator |)
    scores = {t: str(Decimal(0.0)) for t in failed_tests}
    for passed_test in passed_tests:
        scores[passed_test] = str(SCORES[passed_test])

    # for instance_name, instance_data in test_data.items():
    #     print(instance_name)
    #     for name, test_data in instance_data["positive_tests"].items():
    #         print(name)
    #         print(test_data["args"])
    #         raise Exception("aoeu")
    return {
        "github_user": github_user,
        "commit": file_to_string("info_commit.txt").strip(),
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "test_data": {
            instance_name: {
                "instance": instance_data["instance"],
                "instance_time": instance_data["instance_time"],
                "tested": instance_data["tested"],
                "passed": instance_data["passed"],
                "pos_tests": {
                    name: {
                        # "args": test_data["args"],
                        "status": test_data["status"],
                        "time": test_data["time"],
                        "timeout": test_data["timeout"],
                        "verified": test_data["verified"],
                        # "verifications": test_data["verifications"],
                    }
                    for name, test_data in instance_data["positive_tests"].items()
                },
                "neg_tests": {
                    name: {
                        # "args": test_data["args"],
                        "status": test_data["status"],
                        "time": test_data["time"],
                        "timeout": test_data["timeout"],
                        "verified": test_data["verified"],
                        # "verifications": test_data["verifications"],
                    }
                    for name, test_data in instance_data["negative_tests"].items()
                },
            }
            for instance_name, instance_data in test_data.items()
        },
        "total_score": str(
            sum([SCORES[t] for t in passed_tests])
        ),  # `json` can't serialize Decimals...
        "scores": scores,
    }


REPO_PREFIX = "tarea-2-2021-2-"


def summarize(reports):
    scores = {test_name: [] for test_name in SCORES.keys()}
    for name, report in reports.items():
        for name in report["passed_tests"]:
            scores[name].append(SCORES[name])
        for name in report["failed_tests"]:
            scores[name].append(0.0)
    for test_name, ss in scores.items():
        if len(ss) == 0:
            print("Empty test: ", test_name)
            raise Exception("aoeuaoeu")
    f_scores = {
        test_name: [float(s) for s in dec_scores]
        for test_name, dec_scores in scores.items()
    }

    summary = {
        test_name: {
            "scores": sorted(f_scores[test_name]),
            "zeroes": sum([1 for s in test_scores if s == 0]),
            "non_zeroes": sum([1 for s in test_scores if s > 0]),
            "min": float(min(test_scores)),
            "max": float(max(test_scores)),
            "mean": float(statistics.mean(f_scores[test_name])),
            "median": float(statistics.median(test_scores)),
            "mode": float(statistics.mode(test_scores)),
            "quartiles": statistics.quantiles(f_scores[test_name], n=4),
            "quintiles": statistics.quantiles(f_scores[test_name], n=5),
            "deciles": statistics.quantiles(f_scores[test_name], n=10),
            "percentiles": statistics.quantiles(f_scores[test_name], n=100),
        }
        for test_name, test_scores in scores.items()
    }

    return summary


def main(argv):
    # program_name = argv[0]
    args = argv[1:]

    reports = dict()
    for assignment_path in args:
        assignment_dir = os.path.basename(assignment_path)
        if not assignment_dir.startswith(REPO_PREFIX):
            print("Skipping ", assignment_path)
            continue

        github_user = assignment_dir[len(REPO_PREFIX) :]
        with pushd(assignment_path):
            report = grade(github_user)
            reports[github_user] = report
            with open("report.json", "w") as json_file:
                json.dump(report, json_file)
                print("Wrote `report.json` for ", github_user)

    with open("full_report.json", "w") as json_file:
        json.dump(reports, json_file)
        print("Wrote `full_report.json`")

    summary = summarize(reports)
    with open("summary.json", "w") as json_file:
        json.dump(summary, json_file)
        print("Wrote `summary.json`")


if __name__ == "__main__":
    import sys

    main(sys.argv)
