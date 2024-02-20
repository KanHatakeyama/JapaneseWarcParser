"""
junk_lineを消す
"""

from .junk_lines import junk_texts

junk_lines = junk_texts.split("\n")


def remove_junk_lines(lines):
    new_lines = []
    for line in lines:
        if line in junk_lines:
            continue
        new_lines.append(line)

    return new_lines
