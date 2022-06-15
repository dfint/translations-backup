from collections import defaultdict
import typer
import json
from pathlib import Path, PurePosixPath


app = typer.Typer()


@app.command()
def group_files_by_language(translations_directory: Path):
    result = defaultdict(dict)
    """
    {
        "ru": {
            "hardcoded": "dwarf-fortress.hardcoded/ru.po",
            "raw-objects": "dwarf-fortress.hardcoded/ru.po",
            ...
        }
    }
    """

    for directory in translations_directory.glob("*"):
        resource_name = directory.name.partition(".")[2]
        for file in directory.glob("*.po"):
            language = file.stem
            result[language][resource_name] = str(PurePosixPath(directory.name) / file.name)
    
    print(json.dumps(result, indent=4, sort_keys=True))
