import json
from pathlib import Path
from collections import OrderedDict

# Root directory of the repo
REPO_DIR = Path(".")

# Fetch fingerprint from file generated during CI
FINGERPRINT_FILE = REPO_DIR / "fingerprint.txt"
if FINGERPRINT_FILE.exists():
    with FINGERPRINT_FILE.open("r", encoding="utf-8") as f:
        fingerprint = f.read().strip()
else:
    fingerprint = "0000000000000000000000000000000000000000000000000000000000000000"

# Exact official metadata fields for Mangago (Version 41)
extension_metadata = {
    "eu.kanade.tachiyomi.extension.en.mangago": {
        "name": "Tachiyomi: Mangago",
        "pkg": "eu.kanade.tachiyomi.extension.en.mangago",
        "apk": "tachiyomi-en.mangago-v1.4.41.apk",
        "lang": "en",
        "code": 41,
        "version": "1.4.41",
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

print(f"Generated v41 metadata with confirmed fingerprint: {fingerprint}")
