"""Text helpers shared by the ingest readers."""


def clean_number(raw):
    """Turn a feed amount into a plain decimal string ("1.234,56" -> "1234.56")."""
    return raw.strip().replace(".", "").replace(",", ".")


def squash(s):
    """Collapse runs of whitespace."""
    return " ".join(s.split())
