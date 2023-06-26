import json
from pathlib import Path
from typing import Any, Tuple

import jinja2
import requests
import typer
from babel.messages.pofile import read_po
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
        language = file.stem
        total_lines, translated = translated_lines(file)
        output[language] = translated

    return output, total_lines


def chart_struct(data: dict[str, dict[str, float]], labels: list[str], max_lines: int) -> dict[str, Any]:
    datasets = [dict(label=resource, data=list(lines.values())) for resource, lines in data.items()]

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
                            "stepSize": 10000,
                        },
                    }
                ],
            },
        },
    )


def chart_url(chart_data: dict[str, Any]) -> str:
    url = "https://quickchart.io/chart/create"
    payload = dict(
        width=600,
        height=600,
        backgroundColor="rgb(255, 255, 255)",
        format="png",
        chart=chart_data,
    )

    headers = {"Content-type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()["url"]


def get_chart_url(path: Path) -> str:
    dataset: dict[str, dict[str, float]] = {}
    total_lines: int = 0
    labels: set[str] = set()

    for directory in sorted(filter(Path.is_dir, path.glob("*"))):
        resource_stats, resource_total_lines = resource_stat(directory)
        resource_name = directory.name
        dataset[resource_name] = resource_stats
        total_lines += resource_total_lines
        labels.update(resource_stats.keys())

    print(json.dumps(dataset))
    return chart_url(chart_struct(dataset, sorted(labels), total_lines))


app = typer.Typer()


@app.command()
def generate_readme_jinja(base_dir: Path, template_file: Path, result_path: Path):
    logger.info(f"base_dir: {base_dir.resolve().absolute()}")
    logger.info(f"template_file: {template_file.resolve().absolute()}")
    logger.info(f"result_path: {result_path.resolve().absolute()}")

    template_loader = jinja2.FileSystemLoader(searchpath=template_file.parent)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_file.name)

    dwarf_fortress_steam_chart_url = get_chart_url(base_dir / "translations/dwarf-fortress-steam")
    dwarf_fortress_chart_url = get_chart_url(base_dir / "translations/dwarf-fortress")

    output = template.render(
        dwarf_fortress_steam_chart_url=dwarf_fortress_steam_chart_url,
        dwarf_fortress_chart_url=dwarf_fortress_chart_url,
    )

    with open(result_path, "w") as result_file:
        result_file.write(output)


if __name__ == "__main__":
    generate_readme_jinja(
        Path("../../.."),
        Path("../../../README.template.md"),
        Path("../../../README.md"),
    )
