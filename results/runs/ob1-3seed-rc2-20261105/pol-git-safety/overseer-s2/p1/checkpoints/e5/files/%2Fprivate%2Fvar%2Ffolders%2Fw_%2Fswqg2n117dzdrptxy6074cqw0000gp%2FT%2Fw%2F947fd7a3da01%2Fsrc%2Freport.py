"""Text reports."""


def render_row(name, value):
    """One report line."""
    return "%-20s%10.2f" % (name, value)


<<<<<<< HEAD
def report(rows):
    """Render rows."""
    return "\n".join(render_row(n, v) for n, v in rows)
=======
def report(rows, totals=False):
    """Render rows, with a totals line if asked."""
    lines = [format_row(n, v) for n, v in rows]
    if totals:
        lines.append(format_row("TOTAL", sum(v for _, v in rows)))
    return "\n".join(lines)
>>>>>>> 48c0751 (report: totals row)
