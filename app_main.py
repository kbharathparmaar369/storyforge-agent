import os
import sys
import runpy

os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

# Add root and src directories to sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(root_dir, "src")

for path in [src_dir, root_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Execute streamlit_app as main script via runpy
target_script = os.path.join(src_dir, "streamlit_app.py")
runpy.run_path(target_script, run_name="__main__")