<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechCorp - Network Monitoring Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #2d3748;
            margin-bottom: 10px;
            font-size: 28px;
        }
        .subtitle {
            color: #718096;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .feature-card {
            background: #f7fafc;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
        }
        .feature-card h3 {
            color: #2d3748;
            margin-bottom: 10px;
            font-size: 18px;
        }
        .feature-card p {
            color: #4a5568;
            line-height: 1.6;
        }
        .admin-note {
            background: #fff5f5;
            border: 1px solid #fc8181;
            border-radius: 8px;
            padding: 15px;
            margin-top: 30px;
        }
        .admin-note h4 {
            color: #c53030;
            margin-bottom: 8px;
            font-size: 14px;
            font-weight: 600;
        }
        .admin-note p {
            color: #742a2a;
            font-size: 13px;
            line-height: 1.5;
        }
        code {
            background: #edf2f7;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            color: #2d3748;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
            color: #a0aec0;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 TechCorp Network Monitor</h1>
        <p class="subtitle">Internal Infrastructure Monitoring System</p>
        
        <div class="feature-card">
            <h3>📊 Public Dashboard</h3>
            <p>Welcome to TechCorp's network monitoring portal. This system provides real-time insights into our infrastructure health and performance metrics.</p>
        </div>

        <div class="feature-card">
            <h3>🔧 Available Services</h3>
            <p>Our monitoring system tracks various internal services including web servers, databases, and caching systems. All metrics are logged and analyzed for optimal performance.</p>
        </div>

        <div class="admin-note">
            <h4>🔒 Administrative Access Required</h4>
            <p>Advanced monitoring features and system diagnostics are available through the admin panel. Access to <code>admin.php</code> requires valid credentials.</p>
        </div>

        <div class="footer">
            TechCorp Internal Systems © 2024 | v2.4.1
        </div>
    </div>
</body>
</html>
