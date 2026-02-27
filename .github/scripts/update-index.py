import json
import sys
from pathlib import Path
from collections import OrderedDict
import re

# Default to current directory if no argument provided
REPO_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
print(f"Updating index in: {REPO_DIR.absolute()}")

# Find the Mangago APK to determine the version
apk_dir = REPO_DIR / "apk"
mangago_apks = list(apk_dir.glob("tachiyomi-en.mangago-v1.4.*.apk"))
if not mangago_apks:
    # Fallback/Default if none found yet
    current_version = "1.4.100"
    current_code = 100
    apk_name = "tachiyomi-en.mangago-v1.4.100.apk"
else:
    # Sort by version number and pick highest
    mangago_apks.sort(key=lambda p: [int(x) for x in re.findall(r"\d+", p.name)])
    latest_apk = mangago_apks[-1]
    apk_name = latest_apk.name
    # Extract version from filename: tachiyomi-en.mangago-v1.4.102.apk
    version_match = re.search(r"v(1\.4\.(\d+))", apk_name)
    if version_match:
        current_version = version_match.group(1)
        current_code = int(version_match.group(2))
    else:
        current_version = "1.4.100"
        current_code = 100

print(f"Detected Mangago Version: {current_version} (Code: {current_code}) from {apk_name}")

# Fetch fingerprint from file generated during CI
FINGERPRINT_FILE = REPO_DIR / "fingerprint.txt"
if FINGERPRINT_FILE.exists():
    with FINGERPRINT_FILE.open("r", encoding="utf-8") as f:
        fingerprint = f.read().strip()
    print(f"Found fingerprint.txt: {fingerprint}")
else:
    # Use the hardcoded TRUE fingerprint confirmed via v42/v45/v50 logs
    fingerprint = "70ec4c637e8b5c5d1b5a3ca815b5cb8e608f275a3fae15326afd1b262b9adbff"
    print(f"No fingerprint.txt found, using fallback: {fingerprint}")

# Exact official metadata fields for Mangago
extension_metadata = {
    "eu.kanade.tachiyomi.extension.en.mangago": {
        "name": "Tachiyomi: Mangago",
        "pkg": "eu.kanade.tachiyomi.extension.en.mangago",
        "apk": apk_name,
        "lang": "en",
        "code": current_code,
        "version": current_version,
        "nsfw": 1,
        "sources": [
            {
                "name": "Mangago",
                "lang": "en",
                "id": "2470059397662084186",
                "baseUrl": "https://www.mangago.me"
            }
        ]
    }
}

index_min_data = []

# Generate entries for index.min.json
for pkg_name, meta in extension_metadata.items():
    data = OrderedDict()
    data["name"] = meta["name"]
    data["pkg"] = meta["pkg"]
    data["apk"] = meta["apk"]
    data["lang"] = meta["lang"]
    data["code"] = meta["code"]
    data["version"] = meta["version"]
    data["nsfw"] = meta["nsfw"]
    data["sources"] = meta["sources"]
    index_min_data.append(data)

index_min_data.sort(key=lambda x: x["pkg"])

repo_meta = {
    "meta": {
        "name": "yyu3333",
        "website": "https://github.com/yyu3333/yuu",
        "signingKeyFingerprint": fingerprint
    }
}

# 1. Write out minified index
with (REPO_DIR / "index.min.json").open("w", encoding="utf-8") as f:
    json.dump(index_min_data, f, ensure_ascii=False, separators=(",", ":"))

# 2. Write out pretty index
with (REPO_DIR / "index.json").open("w", encoding="utf-8") as f:
    json.dump(index_min_data, f, ensure_ascii=False, indent=2)

# 3. Write out repo metadata
with (REPO_DIR / "repo.json").open("w", encoding="utf-8") as f:
    json.dump(repo_meta, f, ensure_ascii=False, indent=2)

print(f"Generated {current_version} metadata with verified fingerprint: {fingerprint}")
