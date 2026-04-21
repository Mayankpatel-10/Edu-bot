import os
import sys

def app(environ, start_response):
    """WSGI application entrypoint for Vercel"""
    # Add the project directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Import Streamlit components
    from streamlit.web.cli import main as streamlit_main
    
    # Set port for Vercel (use environment variable or default to 8080)
    port = int(os.environ.get("PORT", 8080))
    
    # Run Streamlit with the correct port and arguments
    try:
        streamlit_main([
            "index.py",
            "--server.port",
            str(port),
            "--server.address",
            "0.0.0.0",
            "--server.headless",
            "true"
        ])
    except SystemExit:
        pass  # Streamlit calls sys.exit(), which is expected
    
    # Return a simple response (this won't actually be used since Streamlit takes over)
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    return [b"<html><body><h1>EduBot is running</h1><p>Please access via Streamlit interface</p></body></html>"]

if __name__ == "__main__":
    # For local testing
    app({}, lambda status, headers: None)
