import json
from pathlib import Path

# Root directory of the repo
REPO_DIR = Path(".")

index_min_data = []

extension_metadata = {
    "eu.kanade.tachiyomi.extension.en.mangago": {
        "name": "Mangago",
        "pkg": "eu.kanade.tachiyomi.extension.en.mangago",
        "lang": "en",
        "code": 23,
        "version": "1.4.23",
        "nsfw": 1,
        "hasIcon": True,
        "sources": [
            {
                "name": "Mangago",
                "lang": "en",
                "id": 8101438258276709849,
                "baseUrl": "https://www.mangago.me"
            }
        ]
    }
}

# Find any APK in the root
for apk in REPO_DIR.glob("*.apk"):
    pkg_name = "eu.kanade.tachiyomi.extension.en.mangago"
    if pkg_name in extension_metadata:
        data = extension_metadata[pkg_name].copy()
        # Flat paths
        data["apk"] = apk.name
        data["icon"] = f"{pkg_name}.png"
        index_min_data.append(data)

index_min_data.sort(key=lambda x: x["pkg"])

with (REPO_DIR / "index.min.json").open("w", encoding="utf-8") as f:
    json.dump(index_min_data, f, ensure_ascii=False, separators=(",", ":"))

print(f"Updated index.min.json with {len(index_min_data)} entries.")
