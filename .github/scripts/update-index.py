import json
from pathlib import Path

# Root directory of the repo
REPO_DIR = Path(".")

index_min_data = []

# Exact official metadata fields (no icon, no prefix in apk)
extension_metadata = {
    "eu.kanade.tachiyomi.extension.en.mangago": {
        "name": "Tachiyomi: Mangago",
        "pkg": "eu.kanade.tachiyomi.extension.en.mangago",
        "lang": "en",
        "code": 23,
        "version": "1.4.23",
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

# Find any APK in the root or apk folder
# The index points to the filename without prefix, assuming standard app behavior
for apk in REPO_DIR.glob("**/*.apk"):
    pkg_name = "eu.kanade.tachiyomi.extension.en.mangago"
    if pkg_name in extension_metadata:
        data = extension_metadata[pkg_name].copy()
        # Flat filename as in official repo
        data["apk"] = apk.name
        index_min_data.append(data)

index_min_data.sort(key=lambda x: x["pkg"])

with (REPO_DIR / "index.min.json").open("w", encoding="utf-8") as f:
    json.dump(index_min_data, f, ensure_ascii=False, separators=(",", ":"))

with (REPO_DIR / "index.json").open("w", encoding="utf-8") as f:
    json.dump(index_min_data, f, indent=2)

repo_data = {
    "meta": {
        "name": "yyu3333",
        "website": "https://github.com/yyu3333/yuu",
    }
}

with (REPO_DIR / "repo.json").open("w", encoding="utf-8") as f:
    json.dump(repo_data, f, indent=2)

print(f"Updated index.json/min with {len(index_min_data)} entries (official format) and created repo.json.")
