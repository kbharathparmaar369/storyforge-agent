import os
import sys
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Run the streamlit app
exec(open("src/streamlit_app.py").read())