import os
import requests
from datetime import datetime

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

    for value in props.values():
        if value.get("type") == "title":
            title_array = value.get("title", [])
            if title_array:
                title = title_array[0]["plain_text"]

    if "Deadline" not in props:
        continue

    deadline = props["Deadline"].get("date")

    if not deadline:
        continue

    start = deadline["start"][:10].replace("-", "")

    ics += f"""
BEGIN:VEVENT
SUMMARY:{title}
DTSTART;VALUE=DATE:{start}
DTEND;VALUE=DATE:{start}
END:VEVENT
"""

ics += """
END:VCALENDAR
"""

with open("calendar.ics", "w", encoding="utf-8") as f:
    f.write(ics)
