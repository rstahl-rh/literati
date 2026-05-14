#!/usr/bin/env python3
"""
Extract code from LaTeX documents.

Finds subsections named "Filename" and "Output" within sections,
and creates files with the content from Output subsections.
"""

import sys
import re
from pathlib import Path


def parse_latex_document(content):
    """
    Parse LaTeX document and extract filename/output pairs.

    Returns a list of (filename, output_content) tuples.
    """
    files = []

    # Split by sections to process each independently
    # Match both \section and \section*
    section_pattern = r'\\section\*?\{[^}]*\}'
    sections = re.split(section_pattern, content)

    for section in sections:
        if not section.strip():
            continue

        # Find Filename subsection
        filename_match = re.search(
            r'\\subsection\*?\{Filename\}\s*\n\s*([^\s\\]+)',
            section
        )

        if not filename_match:
            continue

        filename = filename_match.group(1).strip()

        # Find Output subsection and extract verbatim content
        output_match = re.search(
            r'\\subsection\*?\{Output\}\s*\n\s*\\begin\{verbatim\}(.*?)\\end\{verbatim\}',
            section,
            re.DOTALL
        )

        if output_match:
            output_content = output_match.group(1)
            # Remove leading/trailing whitespace but preserve internal formatting
            output_content = output_content.strip('\n')
            files.append((filename, output_content))

    return files


def main():
    if len(sys.argv) != 2:
        print("Usage: extract_literate.py <latex-file>", file=sys.stderr)
        sys.exit(1)

    latex_file = Path(sys.argv[1])

    if not latex_file.exists():
        print(f"Error: File '{latex_file}' not found", file=sys.stderr)
        sys.exit(1)

    # Read the LaTeX document
    content = latex_file.read_text()

    # Parse and extract files
    files = parse_latex_document(content)

    if not files:
        print("No files found to extract", file=sys.stderr)
        sys.exit(0)

    # Create the extracted files
    for filename, output_content in files:
        output_path = Path(filename)
        output_path.write_text(output_content)
        print(f"Created: {filename}")


if __name__ == "__main__":
    main()


#
# Generated with Claude Sonnet 4.5 on 2026-05-14
#
