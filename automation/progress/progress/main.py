from pathlib import Path
import re
import os
import json
from typing import Any, Tuple
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


def dir_stat(path: Path) -> Tuple[dict[str, float], int]:
    output: dict[str, float] = {}
    total_lines: int = 0
    
    for root in path.glob("*"):
        for file in root.glob("*.po"):
            file_name = file.name
            translated = translated_lines(file)
            output[file_name] = translated[1]
            total_lines = translated[0]

    return (output, total_lines)


def parse_project_section(path: Path) -> str:
    dataset: dict[str, dict[str, float]] = {}
    total_lines: int = 0
    labels: list[str] = []
    for root in path.glob("*"):
        for path in root.glob("*"):
            stat = dir_stat(path)
            dataset[path.name] = stat[0]
            total_lines += stat[1]
            labels = list(stat[0].keys())

    return chart_struct(dataset, labels, total_lines)


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


def get_chart_url(data: dict[str, Any]) -> str:
    url = "https://quickchart.io/chart/create"
    payload = dict(
        width=600,
        height=600,
        backgroundColor="rgb(255, 255, 255)",
        format="png",
        chart=data,
    )

    headers = {"Content-type": "application/json"}
    response = post(url, data=json.dumps(payload), headers=headers)
    return response.json()["url"]


def generate_readme(base_dir):
    base_dir = Path(base_dir)
    steam = parse_project_section(base_dir / "translations/dwarf-fortress-steam")
    print(steam)
    steam_chart_url = get_chart_url(steam)
    print(steam_chart_url)
    old = parse_project_section(base_dir / "translations/dwarf-fortress")
    print(old)
    old_chart_url = get_chart_url(old)
    print(old_chart_url)


if __name__ == "__main__":
    generate_readme("../../")
