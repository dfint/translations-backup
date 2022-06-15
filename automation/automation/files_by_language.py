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
        "ru": {
            "hardcoded": "dwarf-fortress.hardcoded/ru.po",
            "raw-objects": "dwarf-fortress.raw-objects/ru.po",
            ...
        }
    }
    """

    for directory in translations_directory.glob("*"):
        resource_name = directory.name.partition(".")[2]
        for file in directory.glob("*.po"):
            language = file.stem
            result[language][resource_name] = str(PurePosixPath(directory.name) / file.name)
    
    assert result, "Empty result"
    
    print(json.dumps(result, indent=4, sort_keys=True))