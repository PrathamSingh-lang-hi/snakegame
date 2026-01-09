from flask import Flask, render_template, jsonify
import subprocess
import sys
import os
import threading
import time


app = Flask(__name__)

# Global process and lock for managing the pygame script
game_process = None
process_lock = threading.Lock()
# keep a short ring buffer of logs for debugging
game_logs = []
logs_lock = threading.Lock()

def _append_log(line: str):
    with logs_lock:
        game_logs.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {line}")
        # keep last 200 lines
        if len(game_logs) > 200:
            del game_logs[0]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_pygame', methods=['POST'])
def start_pygame():
    """Start `all.py` as a subprocess (opens local Pygame window)."""
    global game_process
    with process_lock:
        if game_process and game_process.poll() is None:
            return jsonify({"status": "running"})

        script_path = os.path.join(os.path.dirname(__file__), 'all.py')
        if not os.path.exists(script_path):
            return jsonify({"status": "error", "detail": f"script not found: {script_path}"}), 500

        # Launch using the current Python executable and capture output for debugging
        try:
            proc = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            game_process = proc

            # start threads to capture stdout/stderr
            def reader(stream, prefix):
                try:
                    for line in iter(stream.readline, ''):
                        if not line:
                            break
                        _append_log(f"{prefix}: {line.rstrip()}")
                except Exception as e:
                    _append_log(f"reader error: {e}")

            t_out = threading.Thread(target=reader, args=(proc.stdout, 'OUT'), daemon=True)
            t_err = threading.Thread(target=reader, args=(proc.stderr, 'ERR'), daemon=True)
            t_out.start()
            t_err.start()

            _append_log('Started all.py with pid ' + str(proc.pid))
            return jsonify({"status": "started", "pid": proc.pid})
        except Exception as e:
            _append_log('Failed to start: ' + str(e))
            return jsonify({"status": "error", "detail": str(e)}), 500


@app.route('/stop_pygame', methods=['POST'])
def stop_pygame():
    """Stop the running `all.py` process if any."""
    global game_process
    with process_lock:
        if not game_process or game_process.poll() is not None:
            return jsonify({"status": "not_running"})

        try:
            pid = game_process.pid
            game_process.terminate()
            try:
                game_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                game_process.kill()
            _append_log(f'stopped process {pid}')
            return jsonify({"status": "stopped"})
        except Exception as e:
            _append_log('stop error: ' + str(e))
            return jsonify({"status": "error", "detail": str(e)}), 500


@app.route('/game_status')
def game_status():
    """Return whether the pygame script is running."""
    running = bool(game_process and game_process.poll() is None)
    return jsonify({"status": "running" if running else "stopped"})


@app.route('/game_logs')
def game_logs_endpoint():
    with logs_lock:
        return jsonify({"lines": list(game_logs)})


if __name__ == '__main__':
    # Disable the auto-reloader to keep subprocess management predictable
    app.run(debug=True, port=5000, use_reloader=False)
