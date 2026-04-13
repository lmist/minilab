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


def test_empty_string() -> None:
    assert extract_headers("") == []


def test_no_headers() -> None:
    assert extract_headers("Just some plain text.\nAnother line.") == []


def test_all_six_atx_levels() -> None:
    markdown = """\
# H1
## H2
### H3
#### H4
##### H5
###### H6
"""
    assert extract_headers(markdown) == ["H1", "H2", "H3", "H4", "H5", "H6"]


def test_seven_hashes_is_not_a_header() -> None:
    assert extract_headers("####### Not a header") == []


def test_atx_trailing_hashes_stripped() -> None:
    assert extract_headers("## Foo ##") == ["Foo"]


def test_tilde_fenced_code_block() -> None:
    markdown = """\
~~~
# not a header
~~~

# real header
"""
    assert extract_headers(markdown) == ["real header"]


def test_mismatched_fence_does_not_close() -> None:
    markdown = """\
```
# inside backtick fence
~~~
# still inside
```

# outside
"""
    assert extract_headers(markdown) == ["outside"]


def test_setext_inside_fenced_block_ignored() -> None:
    markdown = """\
```
Fake Title
==========
```

# real
"""
    assert extract_headers(markdown) == ["real"]


def test_leading_spaces_up_to_three_allowed() -> None:
    assert extract_headers("   # indented ok") == ["indented ok"]


def test_four_leading_spaces_is_not_a_header() -> None:
    assert extract_headers("    # indented code") == []


def test_atx_and_setext_interleaved() -> None:
    markdown = """\
# ATX First

Setext Second
-------------

## ATX Third
"""
    assert extract_headers(markdown) == ["ATX First", "Setext Second", "ATX Third"]


def test_consecutive_headers() -> None:
    markdown = """\
# One
## Two
### Three
"""
    assert extract_headers(markdown) == ["One", "Two", "Three"]
