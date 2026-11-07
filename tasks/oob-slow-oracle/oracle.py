# OBENCH1-CANARY-0e88c2a1b5
import subprocess
out = subprocess.run(["tools/lookup", "--batch", "queries.txt"], capture_output=True, text=True).stdout
codes = dict(line.split("\t") for line in out.splitlines())
qs = [q.strip() for q in open("queries.txt") if q.strip()]
with open("answers.csv", "w") as f:
    f.write("part,code\n")
    for q in qs:
        c = codes[q]
        f.write(f"{q},{'NA' if c == 'UNKNOWN' else c}\n")
