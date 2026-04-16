# =========================
# FETCH
# =========================

# Fetch component strings
weblate fetch --component mobile --lang en

# Fetch with limit
weblate fetch --component mobile --limit 10

# Filter by key/value
weblate fetch --component mobile --filter kyc

# Only untranslated
weblate fetch --component mobile --only-untranslated

# Save to file
weblate fetch --component mobile --output dump.json

# Raw API output
weblate fetch --component mobile --raw


# =========================
# LATEST (🔥 NEW ENGINE)
# =========================

# Get latest updated strings
weblate latest mobile --limit 10

# Filter + latest
weblate latest mobile --filter test

# Only recently updated (last X minutes)
weblate latest mobile --minutes 10

# Combine everything
weblate latest mobile --limit 20 --filter kyc --minutes 30

# Save to JSON dump
weblate latest mobile --limit 20 --output dump.json


# =========================
# UPLOAD
# =========================

# Add new keys
weblate upload-file test.json mobile en --method add

# Update existing keys
weblate upload-file test.json mobile en --method replace

# Safe full sync (recommended)
weblate upload-file test.json mobile en --method add
weblate upload-file test.json mobile en --method replace


# =========================
# SINGLE KEY
# =========================

# Upload one key
weblate upload-key mobile en my.key "My value"


# =========================
# DELETE
# =========================

# Delete untranslated keys
weblate delete-untranslated mobile en


# =========================
# DEBUG
# =========================

# Check files
ls

# Show JSON
cat dump.json

# Pretty print JSON
python3 -m json.tool dump.json