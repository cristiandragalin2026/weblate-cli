import os
from datetime import datetime, timedelta
from .api import get, post, delete


# =========================
# CONFIG
# =========================
def get_config():
    base = os.getenv("WEBLATE_BASE_URL")
    project = os.getenv("PROJECT")

    if not base or not project:
        raise RuntimeError("Missing WEBLATE_BASE_URL or PROJECT")

    return base, project


# =========================
# PAGINATION HELPER
# =========================
def fetch_all(url, params=None):
    results = []
    page = 1

    while True:
        current_params = dict(params or {})
        current_params["page"] = page

        data = get(url, params=current_params)
        results.extend(data.get("results", []))

        if not data.get("next"):
            break

        page += 1

    return results


# =========================
# FETCH STRINGS
# =========================
def get_component_strings(component, lang="en"):
    BASE_URL, PROJECT = get_config()
    url = f"{BASE_URL}/translations/{PROJECT}/{component}/{lang}/units/"

    return fetch_all(url, {"page_size": 1000})


def get_all_strings():
    BASE_URL, PROJECT = get_config()
    url = f"{BASE_URL}/units/"

    return fetch_all(url, {
        "project": PROJECT,
        "page_size": 1000
    })


# =========================
# QUERY ENGINE (🔥 CORE)
# =========================
def query_units(
    component,
    lang="en",
    limit=None,
    filter_text=None,
    minutes=None,
):
    BASE_URL, PROJECT = get_config()

    url = f"{BASE_URL}/translations/{PROJECT}/{component}/{lang}/units/"

    data = fetch_all(url, {"page_size": 100})

    # --- filter ---
    if filter_text:
        f = filter_text.lower()
        data = [
            u for u in data
            if f in (u.get("context") or "").lower()
            or any(f in s.lower() for s in u.get("source", []))
        ]

    # --- time filter ---
    if minutes:
        cutoff = datetime.now().astimezone() - timedelta(minutes=minutes)

        def parse_iso(dt):
            return datetime.fromisoformat(dt)

        data = [
            u for u in data
            if u.get("last_updated") and parse_iso(u["last_updated"]) > cutoff
        ]

    # --- sort ---
    data.sort(
        key=lambda u: u.get("last_updated", ""),
        reverse=True
    )

    # --- limit ---
    if limit:
        data = data[:limit]

    return data


def get_latest_strings(component, lang="en", limit=10, minutes=None):
    return query_units(component, lang, limit=limit, minutes=minutes)


# =========================
# UPLOAD
# =========================
def upload_string(component, lang, key, value):
    BASE_URL, PROJECT = get_config()

    url = f"{BASE_URL}/translations/{PROJECT}/{component}/{lang}/units/"

    return post(url, json={
        "key": key,
        "value": value
    })


def bulk_upload(component, lang, file_path, method="replace"):
    BASE_URL, PROJECT = get_config()

    url = f"{BASE_URL}/translations/{PROJECT}/{component}/{lang}/file/"

    with open(file_path, "rb") as f:
        return post(
            url,
            files={"file": f},
            data={
                "method": method,
                "conflicts": "replace-translated",
            }
        )


# =========================
# SAFE DELETE FROM FILE
# =========================
def bulk_delete_from_file(component, lang, file_path):
    import json

    BASE_URL, PROJECT = get_config()

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 🔥 HANDLE BOTH FORMATS
    if isinstance(data, dict):
        keys_to_delete = set(data.keys())

    elif isinstance(data, list):
        keys_to_delete = {
            item.get("context")
            for item in data
            if item.get("context")
        }

    else:
        raise ValueError("Unsupported JSON format")

    units = get_component_strings(component, lang)

    count = 0
    for u in units:
        if (u.get("context") or "") in keys_to_delete:
            delete(f"{BASE_URL}/units/{u['id']}/")
            count += 1

    return count