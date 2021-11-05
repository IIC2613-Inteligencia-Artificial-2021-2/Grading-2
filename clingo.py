from typing import Dict, Optional, List
import subprocess
import time

from enum import Enum


DEFAULT_TIMEOUT = 20  # 20s


def read_answers(clingo_output):
    answer_line = False
    for line in clingo_output:
        if line.startswith("Answer: "):
            # Mark next line as an answer line
            answer_line = True
            continue

        if not answer_line:
            # Discard non-answer lines
            continue

        # Collect answer
        answer_line = False
        yield line.split()


class Status(Enum):
    # This is a simplified model of the real Statuses
    SATISFIABLE = 30
    UNSATISFIABLE = 20
    OK = 0
    UNKNOWN = -1
    TIMEOUT = -2
    SYNTAX_ERROR = -3

    @staticmethod
    def from_status_code(clingo_status_code: int):
        # https://github.com/potassco/guide/issues/18
        if clingo_status_code == 0:
            return Status.OK
        # 1: Run interrupted: No solution has been found so far
        elif clingo_status_code == 1:
            return Status.UNKNOWN
        # 10: Program is consistent / some consequences exist / query is true
        elif clingo_status_code == 10:
            return Status.SATISFIABLE
        # 11: Run interrupted: Program is consistent / some consequences exist
        elif clingo_status_code == 11:
            return Status.SATISFIABLE
        # 20: Program is inconsistent / query is false
        elif clingo_status_code == 20:
            return Status.UNSATISFIABLE
        # 30: Program is consistent, all possible solutions/consequences enumerated / some optima found
        elif clingo_status_code == 30:
            return Status.SATISFIABLE
        # 31: Run interrupted: Program is consistent / some optima found
        elif clingo_status_code == 31:
            return Status.SATISFIABLE
        # 62: Program is consistent / all possible optima found
        elif clingo_status_code == 62:
            return Status.SATISFIABLE
        # 65: Parsing failed
        elif clingo_status_code == 65:
            return Status.SYNTAX_ERROR
        # 128: Syntax error / command line arguments error
        elif clingo_status_code == 128:
            return Status.SYNTAX_ERROR
        return Status.UNKNOWN


def run(
    args: List[str],
    base_files: List[str] = [],
    timeout: int = DEFAULT_TIMEOUT,
    models: int = 1,
    constants: Optional[Dict] = None,
):
    constant_flags = []
    if constants:
        for key, value in constants.items():
            constant_flags.append("--const")
            constant_flags.append("{}={}".format(key, value))

    t0 = time.time()
    exec_args = (
        ["clingo"] + ["--models={}".format(models)] + constant_flags + base_files + args
    )
    exec_args_str = [str(s) for s in exec_args]

    try:
        x = subprocess.run(
            exec_args,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        status = Status.from_status_code(x.returncode)
        stdout_lines = list(x.stdout.splitlines())
        stderr_lines = list(x.stderr.splitlines())

        if status == Status.UNKNOWN:
            print("returncode: ", x.returncode)
            print("args: ", x.args)
            print("stdout: ", stdout_lines)
            print("stderr: ", stderr_lines)
            raise Exception("Found unknown clingo status code.")
        return {
            "args": exec_args_str,
            "time": time.time() - t0,
            "timeout": False,
            "status": status,
            "solutions": [sol for sol in read_answers(stdout_lines)],
            "stdout": stdout_lines,
            "stderr": stderr_lines,
        }
    except subprocess.TimeoutExpired as to:
        return {
            "args": exec_args_str,
            "time": time.time() - t0,
            "timeout": True,
            "status": Status.TIMEOUT,
            "solutions": [],
            "stdout": [],
            "stderr": [],
        }
    except Exception as e:
        return {
            "args": exec_args_str,
            "time": time.time() - t0,
            "timeout": True,
            "status": Status.UNKNOWN,
            "solutions": [],
            "stdout": [],
            "stderr": [],
        }
