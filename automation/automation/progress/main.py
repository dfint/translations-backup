import json
from operator import itemgetter
from pathlib import Path
from pprint import pprint
from typing import Any, Tuple

import requests
import typer
from babel.messages.pofile import read_po
from langcodes import Language
from loguru import logger


def translated_lines(path: Path | str) -> Tuple[int, int]:
    entries: int = 0
    translated_entries: int = 0

    with open(path, "r", encoding="utf-8") as file:
        catalog = read_po(file)
        for message in catalog:
            if message.id:
                entries += 1
                if message.string:
                    translated_entries += 1

    return entries, translated_entries


def resource_stat(path: Path) -> Tuple[dict[str, int], int]:
    path = Path(path)
    output: dict[str, int] = {}
    total_lines: int = 0

    for file in sorted(filter(Path.is_file, path.glob("*.po"))):
        language = Language.get(file.stem).display_name()
        total_lines, translated = translated_lines(file)
        output[language] = translated
        logger.debug(f"{language}: {translated}")

    return output, total_lines


def prepare_chart_data(data: dict[str, dict[str, float]], labels: list[str], max_lines: int) -> dict[str, Any]:
    datasets = [dict(label=resource, data=[lines[label] for label in labels]) for resource, lines in data.items()]

    return dict(
        type="horizontalBar",
        data={"labels": labels, "datasets": datasets},
        options={
            "scales": {
                "yAxes": [{"stacked": True}],
                "xAxes": [
                    {
                        "stacked": True,
                        "ticks": {
                            "beginAtZero": True,
                            "max": max_lines,
                            "stepSize": 10000,
                        },
                    }
                ],
            },
        },
    )


def get_chart(chart_data: dict[str, Any], file_format: str = "png") -> bytes:
    url = "https://quickchart.io/chart"
    payload = dict(
        width=600,
        height=600,
        backgroundColor="rgb(255, 255, 255)",
        format=file_format,
        chart=chart_data,
    )

    headers = {"Content-type": "application/json"}
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    return response.content


def prepare_dataset(path: Path):
    dataset: dict[str, dict[str, float]] = {}
    total_lines: int = 0
    languages: set[str] = set()

    for resource_directory in sorted(filter(Path.is_dir, path.glob("*"))):
        logger.info(f"processing directory: {resource_directory}")
        resource_stats, resource_total_lines = resource_stat(resource_directory)
        dataset[resource_directory.name] = resource_stats
        logger.info(f"{resource_total_lines=}")
        total_lines += resource_total_lines
        languages.update(resource_stats.keys())

    return dataset, languages, total_lines


app = typer.Typer()


@app.command()
def generate_chart(source_dir: Path, output: Path):
    logger.info(f"source_dir: {source_dir.resolve().absolute()}")
    logger.info(f"output: {output.resolve().absolute()}")
    assert source_dir.exists()
    output.parent.mkdir(exist_ok=True, parents=True)

    dataset, languages, total_lines = prepare_dataset(source_dir)
    languages = sorted(languages)
    logger.info(f"resources={list(dataset.keys())}")
    logger.info(f"{languages=}")
    logger.info(f"{total_lines=}")
    assert total_lines, "Empty result"
    chart_data = prepare_chart_data(dataset, languages, total_lines)
    chart = get_chart(chart_data, file_format=output.suffix[1:])

    with open(output, "wb") as result_file:
        result_file.write(chart)
