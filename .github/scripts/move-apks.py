from pathlib import Path
import shutil
import sys

# Default to current directory if no argument provided
REPO_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
apk_dir = REPO_DIR / "apk"

if apk_dir.exists():
    shutil.rmtree(apk_dir)
apk_dir.mkdir(parents=True, exist_ok=True)

# Dynamically find Mangago version from build.gradle
# In CI, REPO_DIR is 'repo' branch, and 'master' is sibling
build_gradle = REPO_DIR.parent / "master" / "src" / "en" / "mangago" / "build.gradle"
version_code = 43
print(f"Checking for build.gradle at: {build_gradle.absolute()}")
if build_gradle.exists():
    print("Found build.gradle")
    with build_gradle.open("r", encoding="utf-8") as f:
        for line in f:
            if "extVersionCode =" in line:
                version_code = int(line.split("=")[1].strip())
                break
else:
    print("build.gradle NOT found at sibling path")
    # Local dev path fallback
    build_gradle = REPO_DIR / "src" / "en" / "mangago" / "build.gradle"
    print(f"Checking fallback path: {build_gradle.absolute()}")
    if build_gradle.exists():
        print("Found build.gradle at fallback path")
        with build_gradle.open("r", encoding="utf-8") as f:
            for line in f:
                if "extVersionCode =" in line:
                    version_code = int(line.split("=")[1].strip())
                    break
    else:
        print("CRITICAL: build.gradle NOT found anywhere")

print(f"Moving APKs for Mangago Version Code: {version_code}")

apk_artifacts = Path.home() / "apk-artifacts"
if not apk_artifacts.exists():
    # Fallback for local testing
    apk_artifacts = REPO_DIR.parent / "apk-artifacts"

for apk in apk_artifacts.glob("**/*.apk"):
    # Align naming with build.gradle
    if "mangago" in apk.name.lower():
        apk_name = f"tachiyomi-en.mangago-v1.4.{version_code}.apk"
    else:
        apk_name = apk.name.replace("-release-unsigned.apk", ".apk").replace("-release.apk", ".apk").replace("-debug.apk", ".apk")
    print(f"Moving {apk.name} -> apk/{apk_name}")
    shutil.move(str(apk), str(apk_dir / apk_name))
