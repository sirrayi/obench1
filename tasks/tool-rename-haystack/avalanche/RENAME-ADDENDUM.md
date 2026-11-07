# Rename addendum (agreed in review)

While we're in there: `load_account`'s keyword `include_deleted` becomes `with_deleted`.

- Every call site passes `with_deleted` (that includes partials and keyword dicts).
- `load_account` doesn't accept `include_deleted` at all.
- The deprecated `fetch_user` wrapper keeps accepting `include_deleted` and passes it on as `with_deleted`.
- docs/API.md shows the new keyword.
