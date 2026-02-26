from pathlib import Path
import shutil

# Move to apk folder
REPO_DIR = Path(".")
(REPO_DIR / "apk").mkdir(parents=True, exist_ok=True)

for apk in (Path.home() / "apk-artifacts").glob("**/*.apk"):
    apk_name = apk.name.replace("-release.apk", ".apk").replace("-debug.apk", ".apk")
    shutil.move(apk, REPO_DIR / "apk" / apk_name)
