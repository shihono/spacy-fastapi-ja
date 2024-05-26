import json

# load docker stats output
mem_usage_list = []
with open("stats.txt") as f:
    for line in f:
        data = json.loads(line.strip())
        if data["Name"] == "spacy_fastapi":
            # "171MiB / 1GiB"
            mem_usage = data["MemUsage"].split("/")[0].strip()[:-3]
            mem_usage_list.append(mem_usage)

with open("stats_memory.txt", "w")as f:
    f.writelines("\n".join(mem_usage_list))

