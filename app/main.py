from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Home route - shows a nice HTML page
@app.route('/')
def home():
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Flask App</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #0f172a;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 50px 60px;
            text-align: center;
            box-shadow: 0 25px 50px rgba(0,0,0,0.4);
        }
        .status-dot {
            width: 12px; height: 12px;
            background: #22c55e;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            animation: blink 1.5s infinite;
        }
        @keyframes blink {
            0%, 100% { opacity: 1; } 50% { opacity: 0.3; }
        }
        h1 { font-size: 2.5rem; margin-bottom: 10px; color: #38bdf8; }
        p  { color: #94a3b8; margin-bottom: 30px; }
        .badge {
            background: #0f172a;
            border: 1px solid #22c55e;
            color: #22c55e;
            padding: 6px 16px;
            border-radius: 999px;
            font-size: 0.85rem;
            margin-bottom: 30px;
            display: inline-block;
        }
        .routes { text-align: left; margin-top: 20px; }
        .route-item {
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 12px 20px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .method {
            background: #38bdf8;
            color: #0f172a;
            font-weight: bold;
            font-size: 0.75rem;
            padding: 3px 8px;
            border-radius: 4px;
        }
        .path { color: #e2e8f0; font-family: monospace; }
        .desc { color: #64748b; font-size: 0.85rem; margin-left: auto; }
    </style>
</head>
<body>
    <div class="card">
        <div class="badge"><span class="status-dot"></span>Server is Running</div>
        <h1>🚀 My Flask App</h1>
        <p>A simple REST API built with Python & Flask</p>

        <div class="routes">
            <div class="route-item">
                <span class="method">GET</span>
                <span class="path">/</span>
                <span class="desc">Home Page</span>
            </div>
            <div class="route-item">
                <span class="method">GET</span>
                <span class="path">/health</span>
                <span class="desc">Health Check</span>
            </div>
            <div class="route-item">
                <span class="method">GET</span>
                <span class="path">/hello/&lt;name&gt;</span>
                <span class="desc">Say Hello</span>
            </div>
        </div>
    </div>
</body>
</html>
    '''
    return render_template_string(html)

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "App is up and running!"
    }), 200

# A sample route
@app.route('/hello/<name>')
def hello(name):
    return jsonify({
        "message": f"Hello, {name}!"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
