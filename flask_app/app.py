import os
import sqlite3
from flask import Flask, request, jsonify
import requests
from datetime import datetime
This module provides Flask-JWT-Extended integration, including functions for creating and verifying JSON Web Tokens (JWT) for user authentication and authorization. The `JWTManager` class is used to initialize the JWT extension, while `jwt_required`, `create_access_token`, and `get_jwt_identity` are utility functions for managing JWT-based authentication in Flask routes.

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

# Flask App Initialization
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Replace with a real secret key
jwt = JWTManager(app)

# Configurations
DATABASE = "fastpost.db"
MAAM_RATE_CURRENT = 0.17  # Current VAT rate
MAAM_RATE_FUTURE = 0.18  # Future VAT rate starting 01/01/2025
VAT_CHANGE_DATE = datetime(2025, 1, 1)

# Database Setup
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS packages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            status TEXT,
            timestamp DATETIME,
            location TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            status TEXT,
            assigned_to TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

# Endpoints

# User Login
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    if username != "admin" or password != "password":
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# Add Package
@app.route('/add_package', methods=['POST'])
@jwt_required()
def add_package():
    data = request.json
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO packages (description, status, timestamp, location)
            VALUES (?, ?, ?, ?)
        ''', (data['description'], "in warehouse", datetime.now(), data['location']))
        conn.commit()
        conn.close()
        return jsonify({"message": "Package added successfully"})
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# Monitor Packages
@app.route('/monitor_packages', methods=['GET'])
@jwt_required()
def monitor_packages():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM packages')
        packages = cursor.fetchall()
        alerts = []
        for package in packages:
            package_id, description, status, timestamp, location = package
            time_in_warehouse = (datetime.now() - datetime.fromisoformat(timestamp)).total_seconds() / 3600
            if time_in_warehouse > 72:
                alerts.append({"package_id": package_id, "message": "Package exceeded 72 hours!"})
            elif time_in_warehouse > 60:
                alerts.append({"package_id": package_id, "message": "Package nearing 72-hour limit!"})
        conn.close()
        return jsonify({"alerts": alerts})
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# Update Package Status
@app.route('/update_package_status/<int:package_id>', methods=['POST'])
@jwt_required()
def update_package_status(package_id):
    data = request.json
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE packages
            SET status = ?
            WHERE id = ?
        ''', (data['status'], package_id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Package status updated successfully", "package_id": package_id})
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# Calculate VAT
@app.route('/calculate_vat', methods=['POST'])
@jwt_required()
def calculate_vat():
    data = request.json
    amount = data['amount']
    current_date = datetime.now()
    vat_rate = MAAM_RATE_FUTURE if current_date >= VAT_CHANGE_DATE else MAAM_RATE_CURRENT
    vat_amount = amount * vat_rate
    total = amount + vat_amount
    return jsonify({"amount": amount, "vat_rate": vat_rate, "vat_amount": vat_amount, "total": total})

# Optimize Route
@app.route('/optimize_route', methods=['POST'])
@jwt_required()
def optimize_route():
    data = request.json
    origin = data['origin']
    destinations = data['destinations']
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    optimized_route = []
    try:
        for destination in destinations:
            url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
            response = requests.get(url)
            response.raise_for_status()
            route_info = response.json()['routes'][0]['legs'][0]
            optimized_route.append({
                "destination": destination,
                "distance": route_info['distance']['text'],
                "duration": route_info['duration']['text']
            })
        return jsonify({"optimized_route": optimized_route})
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Run the App
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000)