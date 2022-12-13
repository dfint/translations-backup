import json
from collections import defaultdict
from pathlib import Path, PurePosixPath

import typer

app = typer.Typer()


@app.command()
def group_files_by_language(translations_directory: Path):
    result = defaultdict(dict)
    """
    {
        "hardcoded": {
            "ru": "dwarf-fortress/hardcoded/ru.po",
            ...
        }
    }
    
    # TODO: Change structure to the following shape:
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

    for project_directory in translations_directory.glob("*"):
        for resource_directory in project_directory.glob("*"):
            for file in resource_directory.glob("*.po"):
                language = file.stem  # Path("dwarf-fortress/hardcoded/ru.po") -> "ru"
                result[str(resource_directory.name)][language] = str(file.relative_to(translations_directory))
    
    assert result, "Empty result"
    
    print(json.dumps(result, indent=4, sort_keys=True))
