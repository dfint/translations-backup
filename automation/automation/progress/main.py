import asyncio
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import httpx
import typer
from babel.messages.pofile import read_po
from langcodes import Language
from loguru import logger
from scour.scour import scourString as scour_string


async def translated_lines(language_name: str, path: Path) -> tuple[str, int, int]:
    entries: int = 0
    translated_entries: int = 0

    with path.open(encoding="utf-8") as file:
        catalog = await asyncio.to_thread(read_po, fileobj=file)
        for message in catalog:
            if message.id:
                entries += 1
                if message.string:
                    translated_entries += 1

    logger.debug(f"{language_name}: {translated_entries}")
    return language_name, entries, translated_entries


def file_to_language(file: Path):
    return Language.get(file.stem).display_name()


async def resource_stat(path: Path) -> tuple[Path, dict[str, int], int]:
    logger.info(f"processing directory: {path}")

    path = Path(path)
    output: dict[str, int] = {}
    total_lines: int = 0

    files = sorted(filter(Path.is_file, path.glob("*.po")))
    coroutines = [translated_lines(file_to_language(file), file) for file in files]
    results = await asyncio.gather(*coroutines)
    for language, total_lines, translated in results:
        output[language] = translated

    return path, output, total_lines


def prepare_chart_data(data: dict[str, dict[str, float]], labels: list[str], max_lines: int) -> dict[str, Any]:
    datasets = [
        dict(
            label=resource,
            data=[lines[label] for label in labels],
        )
        for resource, lines in data.items()
    ]

    return dict(
        type="horizontalBar",
        data=dict(labels=labels, datasets=datasets),
        options=dict(
            scales=dict(
                yAxes=[dict(stacked=True)],
                xAxes=[
                    dict(
                        stacked=True,
                        ticks=dict(
                            beginAtZero=True,
                            max=max_lines,
                            stepSize=10000,
                        ),
                    )
                ],
            ),
        ),
    )


async def get_chart(chart_data: dict[str, Any], file_format: str = "png") -> bytes:
    url = "https://quickchart.io/chart"
    payload = dict(
        width=600,
        height=600,
        backgroundColor="rgb(255, 255, 255)",
        format=file_format,
        chart=chart_data,
    )

    headers = {"Content-type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()

    return response.content


async def prepare_dataset(path: Path):
    dataset: dict[str, dict[str, float]] = {}
    total_lines: int = 0
    languages: set[str] = set()

    directory_list = sorted(filter(Path.is_dir, path.glob("*")))
    coroutines = [resource_stat(resource_directory) for resource_directory in directory_list]
    results = await asyncio.gather(*coroutines)
    for resource_directory, resource_stats, resource_total_lines in results:
        dataset[resource_directory.name] = resource_stats
        logger.info(f"{resource_total_lines=}")
        total_lines += resource_total_lines
        languages.update(resource_stats.keys())

    return dataset, languages, total_lines


def minify_svg(data: bytes) -> bytes:
    return scour_string(data.decode("utf-8"), options=SimpleNamespace(strip_ids=True)).encode("utf-8")


async def main(source_dir: Path, output: Path):
    logger.info(f"source_dir: {source_dir.resolve().absolute()}")
    logger.info(f"output: {output.resolve().absolute()}")
    assert source_dir.exists()
    output.parent.mkdir(exist_ok=True, parents=True)

    dataset, languages, total_lines = await prepare_dataset(source_dir)
    languages = sorted(languages)
    logger.info(f"resources={list(dataset.keys())}")
    logger.info(f"{languages=}")
    logger.info(f"{total_lines=}")
    assert total_lines, "Empty result"

    chart_data = prepare_chart_data(dataset, languages, total_lines)
    file_format = output.suffix[1:]
    chart = await get_chart(chart_data, file_format=file_format)

    if file_format == "svg":
        chart = minify_svg(chart)

    output.write_bytes(chart)
    logger.info(f"{output.name} chart file is saved")


app = typer.Typer()


@app.command()
def generate_chart(source_dir: Path, output: Path):
    asyncio.run(main(source_dir, output))
