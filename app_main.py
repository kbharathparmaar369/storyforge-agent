import os
import sys

os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

root_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(root_dir, "src")

for path in [src_dir, root_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

script_path = os.path.join(src_dir, "streamlit_app.py")
with open(script_path, "r", encoding="utf-8") as f:
    exec(compile(f.read(), script_path, "exec"), globals())