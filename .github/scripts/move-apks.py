import shutil
import sys
from pathlib import Path

# Target directory is the first argument, or current dir
TARGET_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
apk_dir = TARGET_DIR / "apk"
apk_dir.mkdir(parents=True, exist_ok=True)

# Move APKs from common artifact location to the repo branch folder
for apk in (Path.home() / "apk-artifacts").glob("**/*.apk"):
    # Clear suffix -release, -release-unsigned, -debug
    apk_name = apk.name.replace("-release-unsigned.apk", ".apk").replace("-release.apk", ".apk").replace("-debug.apk", ".apk")
    
    # Special normalization for Mangago if needed, but the above should handle it
    print(f"Moving {apk} to {apk_dir / apk_name}")
    shutil.move(apk, apk_dir / apk_name)
