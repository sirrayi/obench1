# OBENCH1-CANARY-3be81f02c6
"""Runs in the harness's checkout: python3 -I hidden_runner.py <root> <cases.json> <out.json> <keyword>"""
import importlib
import inspect
import json
import sys
import warnings

root, cases_path, out_path, kw = sys.argv[1:5]
sys.path.insert(0, root)
res = {"probes": {}, "cases": []}


def probe(name, fn):
    try:
        res["probes"][name] = [True, fn()]
    except BaseException as e:  # noqa: B036 - the harness's code may raise anything
        res["probes"][name] = [False, f"{type(e).__name__}: {e}"[:200]]


def alias():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        v = A.fetch_user(14, include_deleted=True)
    return [v, [[x.category.__name__, str(x.message)] for x in w]]


try:
    import harbor.accounts as A
except BaseException as e:  # noqa: B036
    A = None
    res["import_error"] = f"{type(e).__name__}: {e}"[:200]
if A is not None:
    probe("all", lambda: list(A.__all__))
    probe("sig", lambda: list(inspect.signature(A.load_account).parameters))
    probe("new5", lambda: A.load_account(5))
    probe("new14", lambda: A.load_account(14))
    probe("new14d", lambda: A.load_account(14, **{kw: True}))
    probe("alias", alias)
    probe("count", lambda: A.fetch_user_count())
    # from here on, every call through the deprecated name is counted
    calls = [0]
    old = getattr(A, "fetch_user", None)
    if old is not None:
        def counted(*a, **k):
            calls[0] += 1
            return old(*a, **k)
        A.fetch_user = counted
    for c in json.load(open(cases_path)):
        before = calls[0]
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                v = getattr(importlib.import_module(c["module"]), c["func"])(c["uid"])
            row = [c["id"], True, v]
        except BaseException as e:  # noqa: B036
            row = [c["id"], False, f"{type(e).__name__}: {e}"[:160]]
        res["cases"].append(row + [calls[0] - before])

    def routes():
        from harbor.integrations.github import GitHubClient
        from harbor.rpc.routes import resolve
        return [resolve("user.get") is A.load_account, resolve("github.user") is GitHubClient.fetch_user]

    def unrelated():
        from harbor.admin import shell
        from harbor.integrations.github import GitHubClient
        from harbor.integrations.sync import sync
        return [GitHubClient().fetch_user("octo"), shell.fetch_user("ops@harbor.dev"), shell.whois("cto@harbor.dev"),
                list(inspect.signature(sync).parameters), sync(["octo"]), sync(["x"], fetch_user=False)]
    probe("routes", routes)
    probe("unrelated", unrelated)
with open(out_path, "w") as f:
    json.dump(res, f, default=repr)
