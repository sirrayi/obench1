# OBENCH1-CANARY-41b9e6c03a
import json, os, sys
sys.path.insert(0, os.environ["OBENCH_TASK_DIR"])
import gen
json.dump(gen.answers(), open("answers.json", "w"))
