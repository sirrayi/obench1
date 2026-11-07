"""Harness adapters: each drives one CLI harness through one phase of a cell
and returns its outcome (done, steps, wall time, tokens, trajectory)."""

from . import dsh, generic, hermes, mini, omp, overseer, pi

REGISTRY = {"overseer": overseer, "mini": mini, "pi": pi, "omp": omp, "hermes": hermes, "dsh": dsh, "generic": generic.Generic()}


def get(name):
    if name.startswith("overseer@"):  # another Overseer build (obench.py build_env)
        return overseer
    if name == "generic" or name.startswith("generic@"):
        return generic.Generic(name.split("@", 1)[1] if "@" in name else None)
    return REGISTRY[name]
