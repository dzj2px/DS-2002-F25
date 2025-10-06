import csv, json, os
from pathlib import Path
import pandas as pd

out = Path(".")

rows = [
    [1001, "CS",      3,    "Yes", "10.5"],
    [1002, "Math",    3.7,  "No",  "14.0"],
    [1003, "Stats",   2,    "No",  "9.5"],
    [1004, "Econ",    3.25, "Yes", "12.0"],
    [1005, "History", 4,    "No",  "7.0"],
]
with open(out / "raw_survey_data.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["student_id","major","GPA","is_cs_major","credits_taken"])
    w.writerows(rows)

courses = [
    {
        "course_id": "DS2002",
        "section": "001",
        "title": "Data Science Systems",
        "level": 200,
        "instructors": [
            {"name": "Austin Rivera", "role": "Primary"},
            {"name": "Heywood Williams-Tracy", "role": "TA"},
        ],
    },
    {
        "course_id": "PHYS1655",
        "section": "001",
        "title": "Python for Scientists",
        "level": 100,
        "instructors": [
            {"name": "Craig Group", "role": "Primary"}
        ],
    },
    {
        "course_id": "CS3100",
        "section": "001",
        "title": "Data Structures and Algorithms 2",
        "level": 300,
        "instructors": [
            {"name": "Mark Floryan", "role": "Primary"}
        ],
    },
    {
        "course_id": "CS3140",
        "section": "001",
        "title": "Software Development Essentials",
        "level": 300,
        "instructors": [
            {"name": "Nhat Nguyen", "role": "Primary"}
        ],
    },
    {
        "course_id": "EVSC1600",
        "section": "001",
        "title": "Water on Earth",
        "level": 100,
        "instructors": [
            {"name": "Frederick Cheng", "role": "Primary"}
        ],
    },
]
with open(out / "raw_course_catalog.json", "w") as f:
    json.dump(courses, f, indent=2)

df = pd.read_csv(out / "raw_survey_data.csv")

df["is_cs_major"] = df["is_cs_major"].replace({"Yes": True, "No": False})

df = df.astype({"GPA":"float64", "credits_taken":"float64"})

df.to_csv(out / "clean_survey_data.csv", index=False)

with open(out / "raw_course_catalog.json") as f:
    data = json.load(f)

flat = pd.json_normalize(
    data,
    record_path=["instructors"],
    meta=["course_id", "section", "title", "level"],
    errors="ignore"
)
flat = flat.rename(columns={"name":"instructor_name", "role":"instructor_role"})

flat.to_csv(out / "clean_course_catalog.csv", index=False)

print("done")
