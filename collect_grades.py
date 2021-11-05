#!/usr/bin/env python

import contextlib
import copy
import json
import os
import re
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


SCORES = {
    # Constraint Satisfaction
    # =======================
    # Dependency-hell
    # ---------------
    # - [0.8] Escriba un programa que pueda determinar soluciones factibles. No
    #         es necesario que determine todas las soluciones posibles, pero
    #         debe encontrar soluciones cuando hay.
    "dh-0.json": Decimal("0.1"),
    "dh-1.json": Decimal("0.2"),
    "dh-2.json": Decimal("0.2"),
    "dh-3.json": Decimal("0.3"),
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
    "statues-0.json": Decimal("0.1"),
    "statues-1.json": Decimal("0.1"),
    "statues-2.json": Decimal("0.1"),
    # - [0.2] ¿Qué restricciones de integridad agregaría para revisar que el
    #         problema tiene solución sin necesidad de tratar de encontrar un
    #         plan y fallar?.
    "planning_statues_secret_3_test.py": Decimal("0.1"),
    "planning_statues_secret_4_test.py": Decimal("0.1"),

    # Blocks-World
    # ------------
    # - Single-agent
    # - [1] Modele el mundo de bloques de forma de poder resolver instancias
    #       como esta
    "blocks-simple-0.json": Decimal("0.1"),
    "blocks-simple-1.json": Decimal("0.2"),
    "blocks-simple-2.json": Decimal("0.2"),
    "blocks-simple-3.json": Decimal("0.2"),
    "blocks-simple-4.json": Decimal("0.3"),
    # - Multi-agent
    # - [1] Si un robot tuviese varios brazos que puedan operar en paralelo y
    #       sin chocar podríamos pensar que son 2 agentes que colaboran para
    #       lograr un objetivo común.
    #       Implemente una versión para multiples brazos que pueda resolver
    #       instancias como esta.
    "blocks-multi-0.json": Decimal("0.1"),
    "blocks-multi-1.json": Decimal("0.2"),
    "blocks-multi-2.json": Decimal("0.2"),
    "blocks-multi-3.json": Decimal("0.2"),
    "blocks-multi-4.json": Decimal("0.3"),
    # Coffee
    # ------
    # - Single-agent
    # - [1.5] Solucione el problema de repartir café.
    "coffee-single-0.json": Decimal("0.1"),
    "coffee-single-1.json": Decimal("0.2"),
    "coffee-single-2.json": Decimal("0.3"),
    "coffee-single-3.json": Decimal("0.3"),
    "coffee-single-4.json": Decimal("0.3"),
    "coffee-single-5.json": Decimal("0.3"),
    # - Multi-agent
    # - [1] Muestre que su solución también funciona para varios agentes al
    #       extender ~agentAt(Room)~ y ~has(Drink)~.
    "coffee-multi-0.json": Decimal("0.1"),
    "coffee-multi-1.json": Decimal("0.2"),
    "coffee-multi-2.json": Decimal("0.3"),
    "coffee-multi-3.json": Decimal("0.4"),
}


def grade(github_user):
    passed_tests = sorted(
        [p.name for p in Path("test_results/passed").rglob("*.json")]
    )
    failed_tests = sorted(
        [p.name for p in Path("test_results/failed").rglob("*.json")]
    )

    # Python3.8 does not support Union (operator |)
    scores = {t: str(Decimal(0.0)) for t in failed_tests}
    for passed_test in passed_tests:
        scores[passed_test] = str(SCORES[passed_test])

    return {
        "github_user": github_user,
        "commit": file_to_string("info_commit.txt").strip(),
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "total_score": str(
            sum([SCORES[t] for t in passed_tests])
        ),  # `json` can't serialize Decimals...
        "scores": scores,
    }


REPO_PREFIX = "tarea-2-2021-2-"


def main(argv):
    # program_name = argv[0]
    args = argv[1:]

    full_report = {}
    for assignment_path in args:
        assignment_dir = os.path.basename(assignment_path)
        if not assignment_dir.startswith(REPO_PREFIX):
            print("Skipping ", assignment_path)
            continue

        github_user = assignment_dir[len(REPO_PREFIX) :]
        with pushd(assignment_path):
            report = grade(github_user)
            full_report[github_user] = report
            with open("report.json", "w") as json_file:
                json.dump(report, json_file)
                print("Wrote `report.json` for ", github_user)

    with open("full_report.json", "w") as json_file:
        json.dump(full_report, json_file)
        print("Wrote `full_report.json`")


if __name__ == "__main__":
    import sys

    main(sys.argv)
