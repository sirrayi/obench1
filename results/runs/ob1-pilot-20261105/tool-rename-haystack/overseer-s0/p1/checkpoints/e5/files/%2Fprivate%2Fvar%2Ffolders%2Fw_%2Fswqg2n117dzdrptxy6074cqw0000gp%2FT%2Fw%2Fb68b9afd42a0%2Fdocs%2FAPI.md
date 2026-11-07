# harbor API

### accounts.fetch_user(user_id, *, include_deleted=False)

The account for `user_id` as a dict (`id`, `name`, `tier`, `deleted`), or `None` if the account was deleted and
`include_deleted` is false. Raises `ValueError` for ids that aren't positive integers.

### accounts.fetch_user_count()

How many accounts exist.

### accounts.account_tiers()

The tiers, cheapest first.

### integrations.github.GitHubClient.fetch_user(login)

A GitHub user by login. Unrelated to harbor accounts.

### rpc.routes.resolve(name)

The callable behind a route name.
