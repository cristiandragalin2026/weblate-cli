import os
import requests


def get_headers():
    token = os.getenv("WEBLATE_TOKEN")

    if not token:
        raise RuntimeError("Missing WEBLATE_TOKEN")

    # 🔥 HARD CLEAN (fixes 401)
    token = (
        token.strip()
        .replace("\n", "")
        .replace("\r", "")
        .replace('"', "")
        .replace("'", "")
    )

    return {
        "Authorization": f"Token {token}",
    }


def get(url, params=None):
    response = requests.get(url, headers=get_headers(), params=params)

    if response.status_code == 401:
        raise RuntimeError("Unauthorized (401). Check your WEBLATE_TOKEN.")

    response.raise_for_status()
    return response.json()


def post(url, json=None, files=None, data=None):
    headers = get_headers()  # ✅ FIX

    if files:
        # 🚨 CRITICAL: let requests set Content-Type automatically
        headers.pop("Content-Type", None)

        response = requests.post(
            url,
            headers=headers,
            files=files,
            data=data,  # ✅ include form data
        )
    else:
        response = requests.post(
            url,
            headers=headers,
            json=json,
        )

    if response.status_code == 401:
        raise RuntimeError("Unauthorized (401). Check your WEBLATE_TOKEN.")

    response.raise_for_status()
    return response.json()


def delete(url):
    response = requests.delete(url, headers=get_headers())

    if response.status_code == 401:
        raise RuntimeError("Unauthorized (401). Check your WEBLATE_TOKEN.")

    response.raise_for_status()
    return response.status_code