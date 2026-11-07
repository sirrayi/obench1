"""Shared by setup, grader and oracle: the 48 warehouses and the true answers."""
import random

NAMES = ["Ada Okafor", "Bram Visser", "Chen Wei", "Dalia Haddad", "Emil Novak", "Farah Siddiqui",
         "Gus Moreno", "Hana Sato", "Ines Duarte", "Jonas Berg", "Kofi Mensah", "Lena Kowalska"]
REGIONS = ["north", "south", "east", "west"]
SKUS = ["SKU-A9", "SKU-B2", "SKU-C3", "SKU-D4", "SKU-Z1"]


def warehouses():
    r = random.Random("obench1:eff-parallel-reads")
    out = []
    years = r.sample(range(1971, 2021), 48)
    for i in range(48):
        stock = {}
        for s in SKUS:
            if s == "SKU-Z1" and r.random() > 0.2:
                continue
            if r.random() < 0.8 or s in ("SKU-A9", "SKU-B2"):
                stock[s] = r.randint(5, 900)
        out.append({"id": f"W{i + 1:02d}", "region": r.choice(REGIONS),
                    "manager": r.choice(NAMES) + ("" if i % 3 else " Jr."),
                    "year": years[i], "stock": stock})
    c3 = [w for w in out if "SKU-C3" in w["stock"]]
    top = max(c3, key=lambda w: w["stock"]["SKU-C3"])
    top["stock"]["SKU-C3"] = max(w["stock"]["SKU-C3"] for w in c3) + 1  # unique max
    return out


def answers(ws=None):
    ws = ws or warehouses()
    east = [w["stock"]["SKU-B2"] for w in ws if w["region"] == "east"]
    oldest = min(ws, key=lambda w: w["year"])
    c3 = max((w for w in ws if "SKU-C3" in w["stock"]), key=lambda w: w["stock"]["SKU-C3"])
    return {
        "q1": sum(w["stock"]["SKU-A9"] for w in ws),
        "q2": c3["id"],
        "q3": sum(1 for w in ws if w["region"] == "north"),
        "q4": oldest["manager"],
        "q5": sorted(w["id"] for w in ws if w["stock"].get("SKU-Z1", 0) > 0),
        "q6": round(sum(east) / len(east), 1),
    }


FILLER = [
    "Dock doors were inspected and the forklift rota was updated for the quarter.",
    "Seasonal staffing rose by a few heads; overtime stayed within the budget line.",
    "A pallet audit found minor labelling drift, corrected the same week.",
    "Cold-chain sensors reported nominal readings throughout the period.",
    "The roof repair scheduled last year is still waiting on a contractor quote.",
    "Shrinkage remained below the network average, per the loss-prevention desk.",
]


def render(w, i):
    r = random.Random(f"obench1:eff-parallel-reads:{w['id']}")
    lines = [f"# Quarterly site report — {w['id']}", ""]
    reg = [f"Region: {w['region'].title()}", f"This site sits in the {w['region']} region.",
           f"A {w['region']}-region site."][i % 3]
    mgr = [f"Site manager: {w['manager']}.", f"Managed by {w['manager']}.",
           f"{w['manager']} runs the floor here."][(i // 3) % 3]
    yr = [f"Opened in {w['year']}.", f"Operating since {w['year']}.",
          f"Commissioned {w['year']}."][(i // 2) % 3]
    lines += [reg, mgr, yr, ""]
    for _ in range(6):
        lines.append(r.choice(FILLER))
    lines += ["", "## Stock on hand", ""]
    for k, (s, n) in enumerate(sorted(w["stock"].items())):
        lines.append([f"- {s}: {n}", f"- {n} units of {s}", f"- {s} ({n} units)",
                      f"- stock of {s} is {n}"][(i + k) % 4])
    lines += ["", "## Notes", ""]
    for _ in range(10):
        lines.append(r.choice(FILLER))
    return "\n".join(lines) + "\n"
