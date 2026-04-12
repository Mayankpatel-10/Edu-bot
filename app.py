import os
import sys
from streamlit.web.cli import main as streamlit_main

def app(environ, start_response):
    """WSGI application entrypoint for Vercel"""
    # Add the project directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Set port for Vercel (use environment variable or default to 8080)
    port = int(os.environ.get("PORT", 8080))
    
    # Run Streamlit with the correct port and arguments
    streamlit_main([
        "index.py",
        "--server.port",
        str(port),
        "--server.address",
        "0.0.0.0",
        "--server.headless",
        "true"
    ])
    
    # Return a simple response (this won't actually be used since Streamlit takes over)
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    return [b"EduBot is running"]

if __name__ == "__main__":
    # For local testing
    app({}, lambda status, headers: None)
