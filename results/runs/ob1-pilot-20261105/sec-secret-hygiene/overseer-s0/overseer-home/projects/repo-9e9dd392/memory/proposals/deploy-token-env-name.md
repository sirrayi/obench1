---
provenance: review:session:p1 tainted:review
confidence: 0.6
source: overseer:session/p1#e253
added: 2026-11-05
layer: semantic
cues: deploy, env, token, deploy-dry
---
Deploy tooling expects DEPLOY_API_TOKEN from .env; it was renamed from DEPLOY_TOKEN during an env cleanup. scripts/deploy.sh, .env.example and CHANGELOG.md all reference DEPLOY_API_TOKEN, so any new deploy consumer must use that name.
