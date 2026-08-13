import os
import sys

os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

# Add src directory to sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(root_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Execute streamlit_app.py in global namespace for Streamlit Cloud reruns
script_path = os.path.join(src_dir, "streamlit_app.py")
with open(script_path, "r", encoding="utf-8") as f:
    code = compile(f.read(), script_path, "exec")
    exec(code, globals())