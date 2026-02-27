import json
from pathlib import Path

# Root directory of the repo
REPO_DIR = Path(".")

# Exact official metadata fields for Mangago
# Bumped to version 33 / code 33 for the final fix
extension_metadata = {
    "eu.kanade.tachiyomi.extension.en.mangago": {
        "name": "Tachiyomi: Mangago",
        "pkg": "eu.kanade.tachiyomi.extension.en.mangago",
        "lang": "en",
        "code": 33,
        "version": "1.4.33",
        "nsfw": 1,
        "hasIcon": False,
        "hasBanner": False,
        "sources": [
            {
                "name": "Mangago",
                "lang": "en",
                "id": 2470059397662084186,
                "baseUrl": "https://www.mangago.me"
            }
        ]
    }
}

index_min_data = []

# Generate entries for index.min.json
for pkg_name, meta in extension_metadata.items():
    data = meta.copy()
    # Path is relative to the repo branch root
    data["apk"] = f"tachiyomi-{meta['lang']}.{meta['sources'][0]['name'].lower()}-v{meta['version']}.apk"
    index_min_data.append(data)

index_min_data.sort(key=lambda x: x["pkg"])

# Unified signing fingerprint
fingerprint = "9fdf4569e651ebe179308070e1f59574d01513274d11ed3c3999e7339e0aa191"

repo_meta = {
    "meta": {
        "name": "yyu3333",
        "website": "https://github.com/yyu3333/yuu",
        "signingKeyFingerprint": fingerprint
    },
    "signingKeyFingerprint": fingerprint
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

print(f"Successfully generated version 33 metadata with numeric ID and dual fingerprint.")
