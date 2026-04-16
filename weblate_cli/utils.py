import json

def units_to_kv(units):
    result = {}

    for u in units:
        key = u.get("context") or u.get("source")

        if isinstance(key, list):
            key = json.dumps(key)

        key = key or "UNKNOWN_KEY"

        value = u.get("target")

        if isinstance(value, list):
            value = " | ".join(value)

        result[key] = value

    return result