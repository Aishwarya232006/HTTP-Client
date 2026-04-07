from flask import Flask, render_template_string, jsonify
import subprocess
import sys
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>HTTP Client Demo</title>
    <style>
        body {
            background: #1e1e1e;
            color: #d4d4d4;
            font-family: monospace;
            padding: 20px;
        }
        .phase {
            background: #2d2d2d;
            margin: 20px 0;
            padding: 20px;
            border-left: 3px solid #4caf50;
            border-radius: 5px;
        }
        button {
            background: #4caf50;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-family: monospace;
            margin: 5px;
        }
        pre {
            background: #1e1e1e;
            padding: 15px;
            overflow-x: auto;
            border-radius: 5px;
            white-space: pre-wrap;
        }
        h2 {
            color: #4caf50;
        }
        .error {
            color: #f44336;
        }
    </style>
</head>
<body>
    <h1>HTTP Client Project</h1>
    <p>Built from scratch using Python sockets</p>
    
    <div class="phase">
        <h2>Phase 1: GET Request</h2>
        <button onclick="runPhase(1)">Run Phase 1</button>
        <pre id="phase1"></pre>
    </div>
    
    <div class="phase">
        <h2>Phase 2: Response Parser</h2>
        <button onclick="runPhase(2)">Run Phase 2</button>
        <pre id="phase2"></pre>
    </div>
    
    <div class="phase">
        <h2>Phase 3: POST Request</h2>
        <button onclick="runPhase(3)">Run Phase 3</button>
        <pre id="phase3"></pre>
    </div>
    
    <div class="phase">
        <h2>Phase 4: HTTPS + Redirects</h2>
        <button onclick="runPhase(4)">Run Phase 4</button>
        <pre id="phase4"></pre>
    </div>

    <script>
        async function runPhase(phase) {
            const response = await fetch(`/run/${phase}`);
            const data = await response.json();
            document.getElementById(`phase${phase}`).textContent = data.output;
        }
    </script>
</body>
</html>
"""

files = {
    1: r"D:\Documents\GitHub\HTTP-Client\src\phase1_get.py",
    2: r"D:\Documents\GitHub\HTTP-Client\src\Phase2parse.py",
    3: r"D:\Documents\GitHub\HTTP-Client\Phase3post.py",
    4: r"D:\Documents\GitHub\HTTP-Client\Phase4redirectshttps.py"
}

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/run/<int:phase>')
def run_phase(phase):
    if phase not in files:
        return jsonify({'output': 'Invalid phase'})
    
    try:
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            [sys.executable, files[phase]], 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='replace',
            env=env
        )
        
        output = result.stdout + result.stderr
        
        if phase == 4:
            output = output.replace('\u2192', '->')
        
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'output': f'Error: {str(e)}'})

if __name__ == '__main__':
    print("\nOpen http://localhost:5000 in your browser\n")
    print("Make sure Flask is installed. If not, run: python -m pip install flask\n")
    app.run(debug=True, port=5000)