from minilab.markdown import extract_headers


def test_extracts_atx_headers_in_order() -> None:
    markdown = """\
# Title
Some intro text.

## Section
### Subsection ###
"""

    assert extract_headers(markdown) == ["Title", "Section", "Subsection"]


def test_extracts_setext_headers() -> None:
    markdown = """\
Main Title
==========

Sub Title
---------
"""

    assert extract_headers(markdown) == ["Main Title", "Sub Title"]


def test_ignores_headers_inside_fenced_code_blocks() -> None:
    markdown = """\
```python
# not a header
```

# real header
"""

    assert extract_headers(markdown) == ["real header"]
