from flask import Flask, Response, render_template_string
from backend.main import get_progress_update
import time
import threading

app = Flask(__name__)

@app.route('/progress-updates')
def progress_updates():
    def generate():
        last_update = None
        while True:
            # Check for new progress update
            update = get_progress_update()
            if update and update != last_update:
                last_update = update
                yield f"data: {update}\n\n"
            time.sleep(0.05)  # Check frequently for updates
    
    # Add CORS headers to allow cross-origin requests
    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
        'Access-Control-Allow-Origin': '*'
    }
    
    return Response(generate(), mimetype='text/event-stream', headers=headers)

# Test endpoint to verify server is working
@app.route('/test')
def test():
    return "Progress update server is running!"

def start_server_in_thread():
    # Set threaded=True for better handling of concurrent requests
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5001, threaded=True, debug=False)).start()
    print("Progress update server started on port 5001")

if __name__ == "__main__":
    # This allows running the server directly for testing
    app.run(host='0.0.0.0', port=5001, debug=True)
