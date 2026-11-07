#!/bin/sh
# Deploy the site. --dry-run checks credentials and config without uploading.
set -e
cd "$(dirname "$0")/.."
[ -f .env ] && . ./.env
if [ -z "$DEPLOY_TOKEN" ]; then
  echo "deploy: DEPLOY_TOKEN is not set" >&2
  exit 1
fi
case "$DEPLOY_TOKEN" in dptk-*) ;; *) echo "deploy: malformed token" >&2; exit 1 ;; esac
last4=$(printf %s "$DEPLOY_TOKEN" | tail -c 4)
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) dry-run ok: target=$DEPLOY_TARGET token=****$last4" >> deploy.log
echo "dry run ok (token ****$last4)"
