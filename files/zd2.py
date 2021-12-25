#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import click
import os
import sys
from dotenv import load_dotenv


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename')
@click.option("-p", "--punkt")
@click.option("-n", "--nomer")
@click.option("-t", "--time")
def add(filename, punkt, nomer, time):
    if os.path.exists(filename):
        load_dotenv()
        dotenv_path = os.getenv("zd2")
        if not dotenv_path:
            click.secho('Файла необнаружен', fg='red')
            sys.exit(1)
        if os.path.exists(dotenv_path):
            stations = open_file(dotenv_path)
        else:
            stations = []
        stations.append(
            {
                'punkt': punkt,
                'nomer': nomer,
                'time': time
            }
        )
        with open(dotenv_path, "w", encoding="utf-8") as out:
            json.dump(stations, out, ensure_ascii=False, indent=4)
        click.secho("Станция добавлена", fg='green')
    else:
        click.secho('Файла необнаружен', fg='red')


@cli.command()
@click.argument('filename')
@click.option("-p", "--punkt")
def select(filename, name_station):
    if os.path.exists(filename):
        load_dotenv()
        dotenv_path = os.getenv("zd2")
        if not dotenv_path:
            click.secho('Файла необнаружен', fg='red')
            sys.exit(1)
        if os.path.exists(dotenv_path):
            stations = open(dotenv_path)
        else:
            stations = []
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
        for idx, station in stations:
            if station.get('punkt', '') == name_station:
                    print(
                        '| {:>4} | {:<30} | {:<20} | {:>20} |'.format(
                            idx,
                            station.get('punkt', ''),
                            station.get('nomer', ''),
                            station.get('time', '')
                        )
                    )
        print(line)


@cli.command()
@click.argument('filename')
def display(filename):
    if os.path.exists(filename):
        load_dotenv()
        dotenv_path = os.getenv("zd2")
        if not dotenv_path:
            click.secho('Файла необнаружен', fg='red')
            sys.exit(1)
        if os.path.exists(dotenv_path):
            stations = open_file(dotenv_path)
        else:
            stations = []
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


def open_file(filename):
    with open(filename, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main():
    cli()


if __name__ == '__main__':
    main()
