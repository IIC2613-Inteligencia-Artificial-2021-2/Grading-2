#!/usr/bin/env python

import os
import re

from pathlib import Path
from typing import Dict

import judge

from strips import StripsValidator


INSTANCES_PATH = judge.INSTANCES_PATH
OUTPUT_PATH = judge.OUTPUT_PATH


# Parse expressions
DOOR = re.compile(r"^door\((?P<name>.*)\)$")
ROOM = re.compile(r"^room\((?P<name>.*)\)$")
OFFICE = re.compile(r"^office\((?P<name>.*)\)$")
KITCHEN = re.compile(r"^kitchen\((?P<name>.*)\)$")
DRINK = re.compile(r"^drink\((?P<name>.*)\)$")
CONNECTED = re.compile(r"^connected\((?P<src>.*),(?P<dst>.*),(?P<door>.*)\)$")


class Drink:
    def __init__(self, name):
        self.name = name


class Room:
    def __init__(self, name):
        self.name = name
        self.drinks: Set[Drink] = set()
        self.neighbors: Set[Room] = set()


class Office(Room):
    def __init__(self, name):
        super().__init__(name)


class Kitchen(Room):
    def __init__(self, name):
        super().__init__(name)


class Door:
    def __init__(self, name, room1, room2):
        self.name = name
        self.is_open = False
        self.rooms: Tuple[Door, Door] = (room1, room2)

    def open(self):
        pass


class Agent:
    def __init__(self, name):
        self.name = name
        self.drinks: Set[Drink] = set()


class CoffeeValidator(StripsValidator):
    def __init__(self, solution):
        super().__init__(solution)

        self.door_names: Set[str] = set()
        self.rooms: Dict[str, Room] = dict()
        self.drinks: Dict[str, Drink] = dict()

        for pred in self.solution:
            skipped = False
            if (m := DOOR.search(pred)) is not None:
                self.door_names.add(m.group("name"))
            elif (m := ROOM.search(pred)) is not None:
                name = m.group("name")
                self.rooms[name] = Room(name)
            elif (m := OFFICE.search(pred)) is not None:
                name = m.group("name")
                self.rooms[name] = Office(name)
            elif (m := KITCHEN.search(pred)) is not None:
                name = m.group("name")
                self.rooms[name] = Kitchen(name)
            elif (m := DRINK.search(pred)) is not None:
                name = m.group("name")
                self.drinks[name] = Drink(name)
            elif (m := CONNECTED.search(pred)) is not None:
                pass
            else:
                skipped = True
            if not skipped:
                if pred not in self.parsed_predicates:
                    self.parsed_predicates.add(pred)

    def verify(self):
        logs = super().verify()

        return logs


class CoffeeInstance(judge.Instance):
    def verify(self, solution):
        v = CoffeeValidator(solution)
        return {
            "instance_summary": v.instance_summary(),
            "valid": len(solution) > 0 and v.is_valid(),
            "logs": "\n                 > ".join(v.coloured_logs()),
        }


def main():
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    print("Output path: ", OUTPUT_PATH)

    for instance_dir in sorted(
        [INSTANCES_PATH / p.name for p in INSTANCES_PATH.glob("*/")]
    ):
        instance = CoffeeInstance(
            instance_dir=instance_dir,
            assignment_path=judge.ASSIGNMENT_PATH,
            output_path=OUTPUT_PATH,
            is_single_agent=judge.SINGLE_AGENT,
        )

        instance.test()
        print(instance.results_str())


if __name__ == "__main__":
    main()
