import os, sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
from fixture import write
import gen
for i, w in enumerate(gen.warehouses()):
    write(f"reports/{w['id'].lower()}.md", gen.render(w, i))
write("QUESTIONS.md", """# Questions

1. How many units of SKU-A9 are there across all warehouses?
2. Which warehouse holds the most units of SKU-C3?
3. How many warehouses are in the north region?
4. Who manages the oldest warehouse (earliest opening year)? Give the name exactly as written.
5. Which warehouses stock SKU-Z1? List their ids, sorted.
6. Among east-region warehouses, what is the mean number of SKU-B2 units per warehouse,
   rounded to one decimal place?

Write answers.json with exactly these keys and types:

    {"q1": <integer>, "q2": "<warehouse id, e.g. W07>", "q3": <integer>,
     "q4": "<name>", "q5": ["<id>", ...], "q6": <number>}
""")
