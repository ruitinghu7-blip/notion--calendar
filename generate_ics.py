import os
import requests
from datetime import datetime, timedelta

TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["DATABASE_ID"]

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

response = requests.post(url, headers=headers)

data = response.json()

ics = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Notion Calendar//EN
"""

for page in data.get("results", []):

    props = page.get("properties", {})

    title = "Untitled"

    # Assignment Name
    if "Assignment Name" in props:
        title_prop = props["Assignment Name"]

        if title_prop["type"] == "title":
            title_array = title_prop.get("title", [])

            if title_array:
                title = title_array[0]["plain_text"]

    # Deadline
    if "Deadline" not in props:
        continue

    deadline = props["Deadline"].get("date")

    if not deadline:
        continue

    start_raw = deadline.get("start")

    if not start_raw:
        continue

    start = start_raw[:10].replace("-", "")

    end_raw = deadline.get("end")

    if end_raw:
        end_date = datetime.strptime(end_raw[:10], "%Y-%m-%d")
    else:
        end_date = datetime.strptime(start_raw[:10], "%Y-%m-%d") + timedelta(days=1)

    end = end_date.strftime("%Y%m%d")

    ics += f"""
BEGIN:VEVENT
SUMMARY:{title}
DTSTART;VALUE=DATE:{start}
DTEND;VALUE=DATE:{end}
END:VEVENT
"""

ics += """
END:VCALENDAR
"""

with open("calendar.ics", "w", encoding="utf-8") as f:
    f.write(ics)