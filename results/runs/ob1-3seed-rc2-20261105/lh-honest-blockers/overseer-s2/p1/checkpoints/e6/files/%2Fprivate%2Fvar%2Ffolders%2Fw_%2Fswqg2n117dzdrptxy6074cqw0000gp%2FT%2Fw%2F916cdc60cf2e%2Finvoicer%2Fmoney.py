"""Money arithmetic for invoices."""


def line_total(qty, unit_price):
    return round(float(qty) * float(unit_price), 2)


def total(lines):
    return round(sum(line_total(l["qty"], l["unit_price"]) for l in lines), 2)
