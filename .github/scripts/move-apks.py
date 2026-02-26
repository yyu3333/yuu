from pathlib import Path
import shutil

# Move to root
REPO_DIR = Path(".")

for apk in (Path.home() / "apk-artifacts").glob("**/*.apk"):
    apk_name = apk.name.replace("-release.apk", ".apk").replace("-debug.apk", ".apk")
    shutil.move(apk, REPO_DIR / apk_name)
