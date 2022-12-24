import json
import os
import re
from pathlib import Path
from typing import Any, Tuple

import jinja2
from loguru import logger
from requests import post


def translated_lines(path: str) -> Tuple[int, int, float]:
    entries: int = 0
    translated_entries: int = 0
    with open(path, "r", encoding="utf-8") as file:
        for match in re.finditer(
            r'^msgid\s"(.+)"\nmsgstr\s"(.*)"\n', file.read(), re.RegexFlag.MULTILINE
        ):
            entries += 1
            if match.group(1) != match.group(2) and match.group(2) != "":
                translated_entries += 1
    return (
        entries,
        translated_entries,
        (translated_entries / entries) if entries > 0 else 0,
    )


def dir_stat(path: str) -> Tuple[dict[str, float], int]:
    output: dict[str, float] = {}
    total_lines: int = 0
    for root, _dirs, files in os.walk(path):
        for file in files:
            file_name, _file_extension = os.path.splitext(file)
            translated = translated_lines(root + "/" + file)
            output[file_name] = translated[1]
            total_lines = translated[0]
    return (output, total_lines)


def pretty_section_name(path: str) -> str:
    *_, name = os.path.split(path)
    return name


def get_chart_url(path: str) -> str:
    dataset: dict[str, dict[str, float]] = {}
    total_lines: int = 0
    labels: list[str] = []
    for root, dirs, _files in os.walk(path):
        for dir in dirs:
            path = root + "/" + dir
            stat = dir_stat(path)
            dataset[dir] = stat[0]
            total_lines += stat[1]
            labels = list(stat[0].keys())

    chart = chart_url(chart_struct(dataset, labels, total_lines))

    return chart


def project_section(path: str) -> str:
    output: str = "\n### " + pretty_section_name(path) + "\n\n"
    chart = get_chart_url(path)
    output += "![Chart](" + chart + ")\n"
    return output


def chart_struct(
    data: dict[str, dict[str, float]], labels: list[str], max_lines: int
) -> dict[str, Any]:
    datasets: list[Any] = []
    for resourse, lines in data.items():
        # values = [round(elem * 100, 2) for elem in list(lines.values())]
        datasets.append(dict(label=resourse, data=list(lines.values())))
    return dict(
        type="horizontalBar",
        data={"labels": [elem.upper() for elem in labels], "datasets": datasets},
        options={
            "scales": {
                "yAxes": [{"stacked": True}],
                "xAxes": [
                    {
                        "stacked": True,
                        "ticks": {
                            "beginAtZero": True,
                            "max": max_lines,
                            "stepSize": 7500,
                        },
                    }
                ],
            },
        },
    )


def chart_url(data: dict[str, Any]) -> str:
    url = "https://quickchart.io/chart/create"
    payload = dict(
        width=600,
        height=600,
        backgroundColor="rgb(255, 255, 255)",
        format="png",
        chart=data,
    )
    print(json.dumps(payload))

    headers = {"Content-type": "application/json"}
    response = post(url, data=json.dumps(payload), headers=headers)
    return response.json()["url"]


def generate_readme(base_dir: Path):
    file = open("README.md", "w")
    file.write(
        "# Translations Backup\n\n[![Pull translations from transifex](https://github.com/dfint/translations-backup/actions/workflows/pull-translations.yml/badge.svg)](https://github.com/dfint/translations-backup/actions/workflows/pull-translations.yml)\n\nAutomatically pulls translations from transifex site. If there are any changes then it commits them to the repository.\n\n"
    )
    file.write("## Progress\n")
    file.write(project_section(base_dir / "translations/dwarf-fortress-steam"))
    file.write(project_section(base_dir / "translations/dwarf-fortress"))
    file.close()


def generate_readme_jinja(base_dir: Path, template_file: Path, result_path: Path):
    logger.info(f"base_dir: {base_dir.resolve().absolute()}")
    logger.info(f"template_file: {template_file.resolve().absolute()}")
    logger.info(f"result_path: {result_path.resolve().absolute()}")

    template_loader = jinja2.FileSystemLoader(searchpath=template_file.parent)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_file.name)
    dwarf_fortress_steam = get_chart_url(base_dir / "translations/dwarf-fortress-steam")
    dwarf_fortress = get_chart_url(base_dir / "translations/dwarf-fortress")
    output = template.render(
        dwarf_fortress_steam_chart_url=dwarf_fortress_steam,
        dwarf_fortress_chart_url=dwarf_fortress,
    )
    with open(result_path, "w") as result_file:
        result_file.write(output)


def main():
    generate_readme(Path("../.."))


if __name__ == "__main__":
    generate_readme_jinja(
        Path("../../.."),
        Path("../../../README.template.md"),
        Path("../../../README.md"),
    )
