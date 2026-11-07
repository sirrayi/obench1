"""A minimal CLI 'harness' for the generic arm's wiring check: one chat call, prints the reply."""
import json, os, sys, urllib.request, uuid
instr = open(sys.argv[1]).read()
req = urllib.request.Request(os.environ["OPENAI_BASE_URL"] + "/chat/completions", method="POST",
    data=json.dumps({"model": sys.argv[2], "messages": [{"role": "user", "content": instr}]}).encode(),
    headers={"content-type": "application/json", "authorization": "Bearer " + os.environ.get("OPENAI_API_KEY", ""),
             "user-agent": "tiny-harness/0.1", "x-opencode-session": uuid.uuid4().hex})
print(json.load(urllib.request.urlopen(req))["choices"][0]["message"]["content"])
