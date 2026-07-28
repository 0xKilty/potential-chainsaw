#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import os

from tree_sitter import Language, Parser
import tree_sitter_cpp


CPP = Language(tree_sitter_cpp.language())

EXTENSIONS = {".c", ".cpp", ".h", ".hpp"}


def parse_file(path: Path):
    """Parse one file and return a list of (file, line, column, literal)."""

    parser = Parser()
    parser.language = CPP

    try:
        source = path.read_bytes()
    except Exception:
        return []

    tree = parser.parse(source)

    results = []

    cursor = tree.walk()

    while True:
        node = cursor.node

        if node.type == "string_literal":
            line, column = node.start_point

            literal = source[node.start_byte:node.end_byte].decode(
                "utf-8",
                errors="replace",
            )

            results.append(
                (
                    str(path),
                    line + 1,
                    column + 1,
                    literal,
                )
            )

        if cursor.goto_first_child():
            continue

        while not cursor.goto_next_sibling():
            if not cursor.goto_parent():
                return results


def main():
    files = [
        p
        for p in Path(".").rglob("*")
        if p.suffix in EXTENSIONS
    ]

    workers = os.cpu_count() or 4

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(parse_file, f) for f in files]

        for future in as_completed(futures):
            for filename, line, column, literal in future.result():
                print(f"{filename}:{line}:{column}: {literal}")


if __name__ == "__main__":
    main()
