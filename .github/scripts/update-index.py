import json
from pathlib import Path
from collections import OrderedDict

# Root directory of the repo
REPO_DIR = Path(".")

# Exact official metadata fields for Mangago (Version 35)
# Using the ACTUAL EXTRACTED FINGERPRINT from v34 to ensure trust
# Fingerprint: 52608b9ec513f9073c9b3ccff4651e75b71900380f6fb1533b03e2e1145cd1f4
extension_metadata = {
    "eu.kanade.tachiyomi.extension.en.mangago": {
        "name": "Tachiyomi: Mangago",
        "pkg": "eu.kanade.tachiyomi.extension.en.mangago",
        "apk": "tachiyomi-en.mangago-v1.4.35.apk",
        "lang": "en",
        "code": 35,
        "version": "1.4.35",
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
    # Use OrderedDict for stable, official field ordering
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

# The actual certificate fingerprint from the CI-built APK
fingerprint = "52608b9ec513f9073c9b3ccff4651e75b71900380f6fb1533b03e2e1145cd1f4"

repo_meta = {
    "meta": {
        "name": "yyu3333",
        "website": "https://github.com/yyu3333/yuu",
        "signingKeyFingerprint": fingerprint
    }
}

# 1. Write out minified index (Tachiyomi standard)
with (REPO_DIR / "index.min.json").open("w", encoding="utf-8") as f:
    json.dump(index_min_data, f, ensure_ascii=False, separators=(",", ":"))

# 2. Write out pretty index (For debugging)
with (REPO_DIR / "index.json").open("w", encoding="utf-8") as f:
    json.dump(index_min_data, f, ensure_ascii=False, indent=2)

# 3. Write out repo metadata (Compatible with Tachimanga/Suwayomi)
with (REPO_DIR / "repo.json").open("w", encoding="utf-8") as f:
    json.dump(repo_meta, f, ensure_ascii=False, indent=2)

print(f"Successfully generated version 35 metadata with extracted fingerprint.")
