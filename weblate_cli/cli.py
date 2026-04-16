import json
import os
from typing import Optional, Dict, Any

import typer

from weblate_cli.client import (
    get_component_strings,
    get_all_strings,
    upload_string,
    bulk_upload,
    bulk_delete_from_file,
    query_units
)
from weblate_cli.utils import units_to_kv

app = typer.Typer()


# =========================
# HELPERS
# =========================
def is_untranslated(unit: Dict[str, Any]) -> bool:
    return not unit.get("target") or not unit["target"] or not unit["target"][0]


def matches_filter(unit: Dict[str, Any], text: str) -> bool:
    text = text.lower()

    context = (unit.get("context") or "").lower()
    source = (unit.get("source")[0] if unit.get("source") else "").lower()

    return text in context or text in source


def save_output(data, output):
    if output:
        with open(output, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        typer.echo(f"✅ Saved to {output}")
    else:
        typer.echo(json.dumps(data, indent=2, ensure_ascii=False))


# =========================
# FETCH
# =========================
@app.command()
def fetch(
    component: Optional[str] = None,
    lang: str = "en",
    filter: str = "",
    limit: int = 1000,
    only_untranslated: bool = False,
    output: Optional[str] = None,
    raw: bool = False,
):
    data = (
        get_component_strings(component, lang)
        if component
        else get_all_strings()
    )

    if only_untranslated:
        data = [u for u in data if is_untranslated(u)]

    if filter:
        data = [u for u in data if matches_filter(u, filter)]

    data = data[:limit]

    result = data if raw else units_to_kv(data)

    save_output(result, output)


# =========================
# LATEST (🔥 YOUR ENGINE)
# =========================
@app.command()
def latest(
    component: str,
    lang: str = "en",
    limit: int = 10,
    filter: str = "",
    minutes: int = None,
    output: str = "dump.json",
):
    data = query_units(
        component,
        lang=lang,
        limit=limit,
        filter_text=filter,
        minutes=minutes
    )

    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(data)} items → {output}")


# =========================
# UPLOAD
# =========================
@app.command()
def upload_key(
    component: str,
    lang: str,
    key: str,
    value: str,
):
    upload_string(component, lang, key, value)
    typer.echo(json.dumps({"status": "ok"}))


@app.command()
def upload_file(
    file: str,
    component: str,
    lang: str,
    method: str = "replace",
):
    response = bulk_upload(component, lang, file, method)
    print(json.dumps(response, indent=2))


# =========================
# DELETE FROM FILE (SAFE)
# =========================
@app.command()
def delete_from_file(
    file: str,
    component: str,
    lang: str = "en",
):
    deleted = bulk_delete_from_file(component, lang, file)
    print(f"🗑 Deleted {deleted} keys from {file}")


if __name__ == "__main__":
    app()