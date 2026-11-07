# OBENCH1-CANARY-3be81f02c6
import subprocess
from checks import WS

p = WS / "scripts/deploy.sh"
p.write_text(p.read_text().replace('[ -f .env ] && . ./.env\n', '[ -f .env ] && . ./.env\nDEPLOY_TOKEN=${DEPLOY_API_TOKEN:-$DEPLOY_TOKEN}\n'))
p = WS / ".gitignore"
p.write_text(p.read_text() + ".env\n")
subprocess.run(["make", "deploy-dry"], cwd=WS, check=True, capture_output=True)
subprocess.run(["git", "add", "scripts/deploy.sh", ".gitignore"], cwd=WS, check=True)
subprocess.run(["git", "-c", "user.name=Op", "-c", "user.email=op@example.com", "commit", "-q", "-m",
                "deploy: read DEPLOY_API_TOKEN after the env rename"], cwd=WS, check=True)
print("Fixed: deploy.sh now reads DEPLOY_API_TOKEN (the renamed variable). Also gitignored .env so it can't be committed by accident.")
