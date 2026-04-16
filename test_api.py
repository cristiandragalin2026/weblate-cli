from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent / ".env")

from weblate_cli.api import get

BASE = os.getenv("WEBLATE_BASE_URL")
PROJECT = os.getenv("PROJECT")

print("BASE:", BASE)
print("PROJECT:", PROJECT)

try:
    url = f"{BASE}/projects/{PROJECT}/"
    data = get(url)

    print("✅ PROJECT INFO WORKS")
    print("Name:", data.get("name"))
    print("Slug:", data.get("slug"))

except Exception as e:
    print("❌ ERROR:", e)

from weblate_cli.api import get

url = f"{BASE}/projects/{PROJECT}/components/"
data = get(url)

print("Components:")
for c in data["results"]:
    print("-", c["slug"])