<?php
header('Content-Type: text/html; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'ping') {
    header('Content-Type: application/json');
    
    $endpoint = $_POST['url'] ?? '';
    $param = $_POST['opt'] ?? '';
    $param_value = $_POST['data'] ?? '';
    $using_config = ($param === '-K' && $param_value);
    
    if (!$using_config) {
        if (!$endpoint || !is_string($endpoint)) {
            echo json_encode(['success' => false, 'message' => 'Invalid URL']);
            exit;
        }

        $url_parts = parse_url($endpoint);
        if (!$url_parts || !isset($url_parts['scheme'])) {
            echo json_encode(['success' => false, 'message' => 'Invalid URL format']);
            exit;
        }

        $allowed_schemes = ['http', 'https'];
        if (!in_array($url_parts['scheme'], $allowed_schemes)) {
            echo json_encode(['success' => false, 'message' => 'Invalid protocol. Only http and https allowed!']);
            exit;
        }
    }

    $cmd_parts = $endpoint ? [escapeshellarg($endpoint)] : [];
    
    if ($param && $param_value && is_string($param) && is_string($param_value)) {
        if (!preg_match('/^-[A-Za-z]$/', $param)) {
            echo json_encode(['success' => false, 'message' => 'Invalid option']);
            exit;
        }

        if ($param === '-K') {
            $cmd_parts[] = '-K';
            $cmd_parts[] = escapeshellarg($param_value);
        }
        else if ($param === '-T') {
            $cmd_parts[] = '-T';
            $cmd_parts[] = escapeshellarg($param_value);
        }
        else if ($param === '-o' && in_array($param_value, ['GET', 'POST'])) {
            $unique_id = bin2hex(random_bytes(8));
            $file_path = $param_value . '_' . $unique_id;
            $cmd_parts[] = '-o';
            $cmd_parts[] = escapeshellarg($file_path);
            $saved_file = $file_path;
        }
        else if ($param === '-d' || in_array($param_value, ['GET', 'POST'])) {
            $cmd_parts[] = $param;
            $cmd_parts[] = escapeshellarg($param_value);
        }
    }

    $command = 'cd /tmp && timeout 5 curl --max-time 3 ' . implode(' ', $cmd_parts) . ' 2>&1';
    exec($command, $result, $exit_code);
    
    $response = [
        'success' => $exit_code === 0,
        'message' => $exit_code === 0 ? 'Endpoint is reachable' : 'Endpoint is unreachable',
        'output' => implode("\n", array_slice($result, 0, 10))
    ];
    
    if (isset($saved_file)) {
        $response['filename'] = $saved_file;
        $response['message'] .= ' - Saved to: ' . $saved_file;
    }
    
    echo json_encode($response);
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechCorp Network Monitor - Admin Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 2.8em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        .panel {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            margin-bottom: 30px;
        }
        .status-badge {
            display: inline-block;
            background: rgba(76, 175, 80, 0.3);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            border: 1px solid rgba(76, 175, 80, 0.5);
        }
        h2 {
            font-size: 1.8em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .tool-section {
            background: rgba(255, 255, 255, 0.05);
            padding: 25px;
            border-radius: 10px;
            margin-top: 25px;
        }
        .tool-section h3 {
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        .tool-description {
            opacity: 0.85;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        label {
            font-weight: 500;
            margin-bottom: 5px;
            opacity: 0.9;
        }
        input {
            padding: 12px 15px;
            border-radius: 8px;
            border: none;
            background: rgba(255, 255, 255, 0.95);
            color: #333;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
        }
        input:focus {
            outline: 2px solid #667eea;
            background: white;
        }
        button {
            padding: 14px 20px;
            border-radius: 8px;
            border: none;
            background: #4CAF50;
            color: white;
            cursor: pointer;
            font-weight: 600;
            font-size: 1em;
            transition: all 0.3s ease;
        }
        button:hover {
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
        }
        .output {
            background: rgba(0, 0, 0, 0.4);
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            border-left: 4px solid #4CAF50;
        }
        .info-box {
            background: rgba(33, 150, 243, 0.15);
            border-left: 4px solid #2196F3;
            padding: 15px 20px;
            margin-top: 25px;
            border-radius: 5px;
            line-height: 1.6;
        }
        .info-box strong {
            display: block;
            margin-bottom: 8px;
            font-size: 1.05em;
        }
        code {
            background: rgba(0, 0, 0, 0.3);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 Admin Dashboard</h1>
            <p>TechCorp Network Monitoring System</p>
            <div style="margin-top: 15px;">
                <span class="status-badge">✓ Authenticated</span>
            </div>
        </div>

        <div class="panel">
            <h2>Network Diagnostics</h2>
            
            <div class="tool-section">
                <h3>🌐 Endpoint Health Check</h3>
                <p class="tool-description">
                    Test connectivity to HTTP/HTTPS endpoints. This tool uses curl to verify if services are responding correctly.
                </p>
                
                <form id="pingForm">
                    <div>
                        <label>Target URL</label>
                        <input type="text" name="url" placeholder="https://example.com" required>
                    </div>
                    <div>
                        <label>Additional Options (optional)</label>
                        <input type="text" name="opt" placeholder="curl option (e.g., -X, -d, -K)">
                    </div>
                    <div>
                        <label>Option Data (optional)</label>
                        <input type="text" name="data" placeholder="Value for the option above">
                    </div>
                    <button type="submit">Run Health Check</button>
                </form>
                
                <div id="output" class="output" style="display:none;"></div>

                <div class="info-box">
                    <strong>ℹ️ Supported Features:</strong>
                    <p>• HTTP/HTTPS protocol support<br>
                    • Custom curl options for advanced diagnostics<br>
                    • Output file storage with unique naming<br>
                    • Automatic timeout protection (5s)</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('pingForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            formData.append('action', 'ping');
            
            const output = document.getElementById('output');
            output.style.display = 'block';
            output.textContent = 'Loading...';
            
            try {
                const response = await fetch('', {
                    method: 'POST',
                    body: new URLSearchParams(formData)
                });
                const result = await response.json();
                output.textContent = `Status: ${result.success ? '✅ Success' : '❌ Failed'}\n` +
                                    `Message: ${result.message}\n\n` +
                                    `Output:\n${result.output || 'No output'}`;
            } catch (error) {
                output.textContent = 'Error: ' + error.message;
            }
        });
    </script>
</body>
</html>
