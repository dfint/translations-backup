import json
from collections import defaultdict
from pathlib import Path, PurePosixPath

import typer

app = typer.Typer()


@app.command()
def group_files_by_language(translations_directory: Path, result_directory: Path):
    """
    # metadata.json structure:
    {
        "hardcoded": {
            "ru": "dwarf-fortress/hardcoded/ru.po",
            ...
        }
    }
    
    # metadata-v2.json structure:
    {
        "dwarf-fortress": {
            "hardcoded": {
                "ru": "dwarf-fortress/hardcoded/ru.po",
                ...
            },
            ...
        },
        ...
    }
    """
    metadata = defaultdict(dict)
    metadata_v2 = defaultdict(lambda: defaultdict(dict))

    for project_directory in translations_directory.glob("*"):
        for resource_directory in project_directory.glob("*"):
            for file in resource_directory.glob("*.po"):
                project = project_directory.name
                language = file.stem  # Path("dwarf-fortress/hardcoded/ru.po") -> "ru"
                resource = resource_directory.name
                metadata[resource][language] = str(file.relative_to(translations_directory))
                metadata_v2[project][resource][language] = str(file.relative_to(translations_directory))
    
    assert metadata, "Empty result"

    with open(result_directory / "metadata.json", "wt") as file:
        json.dump(metadata, file, indent=4, sort_keys=True)

    with open(result_directory / "metadata-v2.json", "wt") as file:
        json.dump(metadata_v2, file, indent=4, sort_keys=True)
