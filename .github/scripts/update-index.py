import json
from pathlib import Path

# Root directory of the repo
REPO_DIR = Path(".")

# Exact official metadata fields
extension_metadata = {
    "eu.kanade.tachiyomi.extension.en.mangago": {
        "name": "Tachiyomi: Mangago",
        "pkg": "eu.kanade.tachiyomi.extension.en.mangago",
        "lang": "en",
        "code": 30,
        "version": "1.4.30",
        "nsfw": 1,
        "hasIcon": 0,
        "hasBanner": 0,
        "sources": [
            {
                "name": "Mangago",
                "id": "2470059397662084186",
                "baseUrl": "https://www.mangago.me"
            }
        ]
    }
}

index_min_data = []

# Generate exactly one entry per extension
for pkg_name, meta in extension_metadata.items():
    data = meta.copy()
    data["apk"] = f"tachiyomi-{meta['lang']}.{meta['sources'][0]['name'].lower()}-v{meta['version']}.apk"
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

fingerprint_file = REPO_DIR / "fingerprint.txt"
if fingerprint_file.exists():
    with fingerprint_file.open("r", encoding="utf-8") as f:
        repo_data["meta"]["signingKeyFingerprint"] = f.readline().strip()
else:
    # Fallback to hardcoded fingerprint if file is missing in CI
    repo_data["meta"]["signingKeyFingerprint"] = "9fdf4569e651ebe179308070e1f59574d01513274d11ed3c3999e7339e0aa191"

with (REPO_DIR / "repo.json").open("w", encoding="utf-8") as f:
    json.dump(repo_data, f, indent=2)

print(f"Updated index.json/min with {len(index_min_data)} entries (official format) and created repo.json.")
