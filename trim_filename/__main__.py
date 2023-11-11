from pathlib import Path
from typing import Annotated

import typer


def trim_string(s: str, bytes: int):
    while True:
        try:
            return s.encode("utf-8")[:bytes].decode("utf-8")
        except UnicodeDecodeError:
            bytes -= 1


def trim_filename(file: Path, bytes: int):
    if len(file.name.encode("utf-8")) <= bytes:
        return

    suffix = "".join(file.suffixes)
    stem = file.name.removesuffix(suffix)
    suffix_bytes = len(suffix.encode("utf-8"))
    stem_trimed = trim_string(s=stem, bytes=bytes - suffix_bytes)
    file_trimed = file.with_name(stem_trimed + suffix)

    if typer.confirm(f"Rename {file} to {file_trimed}"):
        file.rename(file_trimed)


def main(target: Annotated[Path, typer.Argument(exists=True)], bytes: int = 255):
    if target.is_dir():
        for path in target.glob("**/*"):
            if not path.is_dir():
                trim_filename(file=path, bytes=bytes)
    else:
        trim_filename(file=target, bytes=bytes)


def cli():
    typer.run(main)


if __name__ == "__main__":
    cli()
