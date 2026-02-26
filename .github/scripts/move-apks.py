from pathlib import Path
import shutil

# Move to apk folder
REPO_DIR = Path(".")
apk_dir = REPO_DIR / "apk"

if apk_dir.exists():
    shutil.rmtree(apk_dir)
apk_dir.mkdir(parents=True, exist_ok=True)

for apk in (Path.home() / "apk-artifacts").glob("**/*.apk"):
    apk_name = apk.name.replace("-release-unsigned.apk", ".apk").replace("-release.apk", ".apk").replace("-debug.apk", ".apk")
    shutil.move(apk, apk_dir / apk_name)
