#!/usr/bin/env python3
"""
Simple Flask app for testing Docker container
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "Simple Flask app is running"})

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "SchedulesApp Backend - Simple Version"})

if __name__ == '__main__':
    print("Starting simple Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)
