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
                "id": "2470059397662084186",
                "baseUrl": "https://www.mangago.me"
            }
        ]
    }
}

# Find any APK in the apk folder
for apk in (REPO_DIR / "apk").glob("*.apk"):
    pkg_name = "eu.kanade.tachiyomi.extension.en.mangago"
    if pkg_name in extension_metadata:
        data = extension_metadata[pkg_name].copy()
        # Relative paths
        data["apk"] = f"apk/{apk.name}"
        data["icon"] = f"icon/{pkg_name}.png"
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

print(f"Updated index.json/min with {len(index_min_data)} entries and created repo.json.")
