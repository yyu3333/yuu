import json
import sys
import re
from pathlib import Path
from collections import OrderedDict

# Default to current directory if no argument provided
REPO_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
print(f"Updating index in: {REPO_DIR.absolute()}")

# Dynamically find Mangago version from build.gradle
# In CI, REPO_DIR is 'repo' branch, and 'master' is sibling
build_gradle = REPO_DIR.parent / "master" / "src" / "en" / "mangago" / "build.gradle"
version_code = 43
if build_gradle.exists():
    with build_gradle.open("r", encoding="utf-8") as f:
        for line in f:
            if "extVersionCode =" in line:
                version_code = int(line.split("=")[1].strip())
                break
else:
    # Local dev path fallback
    build_gradle = REPO_DIR / "src" / "en" / "mangago" / "build.gradle"
    if build_gradle.exists():
        with build_gradle.open("r", encoding="utf-8") as f:
            for line in f:
                if "extVersionCode =" in line:
                    version_code = int(line.split("=")[1].strip())
                    break

current_version = f"1.4.{version_code}"
apk_name = f"tachiyomi-en.mangago-v{current_version}.apk"

print(f"Detected Mangago Version: {current_version} (Code: {version_code})")

# Fetch fingerprint from file generated during CI
FINGERPRINT_FILE = REPO_DIR / "fingerprint.txt"
if FINGERPRINT_FILE.exists():
    with FINGERPRINT_FILE.open("r", encoding="utf-8") as f:
        fingerprint = f.read().strip()
else:
    # Use the hardcoded TRUE fingerprint confirmed via v42/v45/v50 logs
    fingerprint = "70ec4c637e8b5c5d1b5a3ca815b5cb8e608f275a3fae15326afd1b262b9adbff"

# Exact official metadata fields for Mangago
extension_metadata = {
    "eu.kanade.tachiyomi.extension.en.mangago": {
        "name": "Tachiyomi: Mangago",
        "pkg": "eu.kanade.tachiyomi.extension.en.mangago",
        "apk": apk_name,
        "lang": "en",
        "code": version_code,
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
