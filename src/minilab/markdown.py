import re


_ATX_HEADER_PATTERN = re.compile(r"^\s{0,3}(#{1,6})[ \t]+(.+?)\s*$")
_SETEXT_UNDERLINE_PATTERN = re.compile(r"^\s{0,3}(=+|-+)\s*$")
_FENCE_PATTERN = re.compile(r"^\s{0,3}([`~]{3,}).*$")


def extract_headers(markdown: str) -> list[str]:
    """Extract header text from a Markdown document.

    Supports ATX headers (`# Heading`) and Setext headers (`Heading\n===`).
    Headers inside fenced code blocks are ignored.
    """

    headers: list[str] = []
    lines = markdown.splitlines()

    in_fence = False
    fence_char = ""
    fence_length = 0

    index = 0
    while index < len(lines):
        line = lines[index]

        fence_match = _FENCE_PATTERN.match(line)
        if fence_match:
            marker = fence_match.group(1)
            marker_char = marker[0]
            marker_length = len(marker)

            if not in_fence:
                in_fence = True
                fence_char = marker_char
                fence_length = marker_length
                index += 1
                continue

            if marker_char == fence_char and marker_length >= fence_length:
                in_fence = False
                fence_char = ""
                fence_length = 0
                index += 1
                continue

        if in_fence:
            index += 1
            continue

        atx_match = _ATX_HEADER_PATTERN.match(line)
        if atx_match:
            text = atx_match.group(2)
            text = re.sub(r"\s+#+\s*$", "", text).strip()
            if text:
                headers.append(text)
            index += 1
            continue

        if index + 1 < len(lines):
            underline_match = _SETEXT_UNDERLINE_PATTERN.match(lines[index + 1])
            if underline_match and line.strip():
                headers.append(line.strip())
                index += 2
                continue

        index += 1

    return headers
