import os
import sys
from streamlit.web.cli import main as streamlit_main

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Set the port for Vercel (use environment variable or default to 8080)
    port = int(os.environ.get("PORT", 8080))
    
    # Run Streamlit with the correct port
    streamlit_main([
        "app.py",
        "--server.port",
        str(port),
        "--server.address",
        "0.0.0.0"
    ])
