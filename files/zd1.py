#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path
import sys


def add_stations(stations, punkt, nomer, time):
    stations.append(
        {
            "punkt": punkt,
            "nomer": nomer,
            "time": time
        }
    )

    return stations


def display_stations(stations):
    if stations:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 20
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                "No",
                "Город прибытия",
                "Номер поезда",
                "Время отправления"
            )
        )
        print(line)

        for idx, station in enumerate(stations, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>20} |'.format(
                    idx,
                    station.get('punkt', ''),
                    station.get('nomer', ''),
                    station.get('time', '')
                )
            )
            print(line)

    else:
        print("Список маршрутов пуст.")


def select_stations(stations, name_station):
    result = []
    for station in stations:
        if station.get('punkt', '') == name_station:
            result.append(station)
    return result


def save_stations(file_name, staff):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_stations(file_name):
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-d",
        "--data",
        action="store",
        required=False,
        help="The data file name"
    )

    parser = argparse.ArgumentParser("stations")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new station"
    )
    add.add_argument(
        "-p",
        "--punkt",
        action="store",
        required=True,
        help="The punkt name"
    )
    add.add_argument(
        "-n",
        "--nomer",
        action="store",
        help="The nomer of station"
    )
    add.add_argument(
        "-t",
        "--time",
        action="store",
        type=int,
        required=True,
        help="The time otpravlenia"
    )

    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all stations"
    )

    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the stations"
    )
    select.add_argument(
        "-n",
        "--name_station",
        action="store",
        type=int,
        required=True,
        help="The required name_station"
    )

    args = parser.parse_args(command_line)

    data_file = args.data
    if not data_file:
        data_file = os.environ.get("zd1")
    if not data_file:
        print("The data file name is absent", file=sys.stderr)
        sys.exit(1)

    is_dirty = False
    if os.path.exists(data_file):
        stations = load_stations(data_file)
    else:
        stations = []

    # Добавить работника.
    if args.command == "add":
        stations = add_stations(stations, args.punkt, args.nomer, args.time)
        is_dirty = True

    elif args.command == "display":
        display_stations(stations)

    elif args.command == "select":
        selected = select_stations(stations, args.name_station)
        display_stations(selected)

    if is_dirty:
        save_stations(data_file, stations)


if __name__ == "__main__":
    main()
