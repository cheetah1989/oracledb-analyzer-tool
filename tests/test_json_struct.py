import json

file_path = (
    "output/DEV5CDB/"
    "environment_20260814_202457.json"
)

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

rows = data["stability"]["database_status"]

print("database_status rows:", len(rows))

for row in rows[:5]:
    print(row)