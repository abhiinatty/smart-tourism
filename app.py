from flask import Flask, render_template_string, jsonify, request
import threading
import time
import random

app = Flask(__name__)

# Simulated blockchain-based digital tourist IDs
tourist_ids = {
    'TID001': {
        'name': 'Alice Johnson',
        'kyc': {'passport': 'X1234567'},
        'itinerary': 'Shillong, Cherrapunji',
        'emergency_contacts': ['+911234567890'],
        'score': 85,
        'valid_until': '2025-10-05'
    },
    'TID002': {
        'name': 'Bob Smith',
        'kyc': {'aadhaar': '1234-5678-9012'},
        'itinerary': 'Kaziranga, Guwahati',
        'emergency_contacts': ['+919876543210'],
        'score': 92,
        'valid_until': '2025-10-03'
    }
}

# Simulated tourist locations and status
tourists = {
    'TID001': {'lat': 25.5788, 'lon': 91.8933, 'status': 'safe', 'last_active': time.time()},
    'TID002': {'lat': 26.5775, 'lon': 93.1711, 'status': 'safe', 'last_active': time.time()}
}

# Simulated alerts and incidents
alerts = []

# Danger zones (geo-fencing)
danger_zones = [
    {'name': 'Restricted Forest', 'lat_min': 26.0, 'lat_max': 26.6, 'lon_min': 92.5, 'lon_max': 93.5}
]

def check_danger_zone(lat, lon):
    for zone in danger_zones:
        if zone['lat_min'] <= lat <= zone['lat_max'] and zone['lon_min'] <= lon <= zone['lon_max']:
            return zone['name']
    return None

def monitor_tourists():
    """Simulate real-time monitoring and anomaly detection."""
    while True:
        for tid, data in tourists.items():
            # Simulate movement
            data['lat'] += random.uniform(-0.01, 0.01)
            data['lon'] += random.uniform(-0.01, 0.01)
            data['last_active'] = time.time()

            # Geo-fencing check
            zone = check_danger_zone(data['lat'], data['lon'])
            if zone:
                data['status'] = 'incident'
                alert = {
                    'tourist': tourist_ids[tid]['name'],
                    'incident': f'Entered danger zone: {zone}',
                    'location': (data['lat'], data['lon']),
                    'time': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                alerts.append(alert)
                print(f"ALERT: {alert}")
            else:
                data['status'] = 'safe'

            # AI anomaly detection (simulated)
            if random.random() < 0.05:  # 5% chance of anomaly
                data['status'] = 'anomaly'
                alert = {
                    'tourist': tourist_ids[tid]['name'],
                    'incident': 'Sudden inactivity detected',
                    'location': (data['lat'], data['lon']),
                    'time': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                alerts.append(alert)
                print(f"ALERT: {alert}")

        time.sleep(10)

threading.Thread(target=monitor_tourists, daemon=True).start()

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Tourist Safety Dashboard</title>
    <style>
        body { font-family: Arial; background: #f4f4f4; margin: 20px; }
        .container { max-width: 900px; margin: auto; }
        .card { background: white; padding: 15px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px #ccc; }
        .safe { color: green; }
        .incident, .anomaly { color: red; }
        .alert { background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 6px; margin-bottom: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Smart Tourist Safety Monitoring Dashboard</h1>
        <h2>Tourist Digital IDs</h2>
        {% for tid, info in tourist_ids.items() %}
            <div class="card">
                <strong>{{ info.name }}</strong> ({{ tid }})<br>
                KYC: {{ info.kyc }}<br>
                Itinerary: {{ info.itinerary }}<br>
                Emergency Contacts: {{ info.emergency_contacts }}<br>
                Safety Score: {{ info.score }}<br>
                Valid Until: {{ info.valid_until }}
            </div>
        {% endfor %}
        <h2>Live Tourist Status</h2>
        {% for tid, data in tourists.items() %}
            <div class="card">
                <strong>{{ tourist_ids[tid].name }}</strong> ({{ tid }})<br>
                Location: ({{ "%.4f"|format(data.lat) }}, {{ "%.4f"|format(data.lon) }})<br>
                Status: <span class="{{ data.status }}">{{ data.status.upper() }}</span><br>
                Last Active: {{ data.last_active | int }}
            </div>
        {% endfor %}
        <h2>Recent Alerts</h2>
        {% for alert in alerts[-5:] %}
            <div class="alert">
                <strong>{{ alert.tourist }}</strong>: {{ alert.incident }}<br>
                Location: {{ alert.location }}<br>
                Time: {{ alert.time }}
            </div>
        {% endfor %}
        <button onclick="location.reload()">Refresh</button>
    </div>
    <script>
        setTimeout(() => location.reload(), 15000);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML, tourist_ids=tourist_ids, tourists=tourists, alerts=alerts)

@app.route('/api/tourists')
def api_tourists():
    return jsonify(tourists)

@app.route('/api/alerts')
def api_alerts():
    return jsonify(alerts[-10:])

@app.route('/api/digital_ids')
def api_digital_ids():
    return jsonify(tourist_ids)

@app.route('/simulate_panic/<tid>', methods=['POST'])
def simulate_panic(tid):
    if tid in tourists:
        tourists[tid]['status'] = 'panic'
        alert = {
            'tourist': tourist_ids[tid]['name'],
            'incident': 'Panic button pressed!',
            'location': (tourists[tid]['lat'], tourists[tid]['lon']),
            'time': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        alerts.append(alert)
        return jsonify({'status': 'Panic simulated', 'alert': alert})
    return jsonify({'error': 'Tourist not found'}), 404

# ...existing code...
if __name__ == '__main__':
    print("Starting Smart Tourist Safety Prototype...")
    print("Monitoring started. Visit http://127.0.0.1:5000/ in your browser.")
    app.run(debug=True, host='0.0.0.0', port=5000)
# ...existing code...