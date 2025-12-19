"""
Traffic Violation Detection Flask Application
Main application file for AI-powered traffic violation detection
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import os
import sqlite3
from datetime import datetime
import json
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from models.violation_model import TrafficViolationDetector
from database import init_db, save_violation, get_violations, get_violation_stats

app = Flask(__name__)
app.config['SECRET_KEY'] = 'traffic_violation_detection_2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'static/results'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'mkv'}

# Initialize AI model
detector = TrafficViolationDetector()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    """Home page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and process for violations"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        
        # Save uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Process file for violations
            results = detector.detect_violations(file_path)
            
            # Save results to database
            for result in results:
                save_violation(
                    filename=filename,
                    violation_type=result['violation_type'],
                    confidence=result['confidence'],
                    timestamp=datetime.now(),
                    result_image=result.get('result_image', '')
                )
            
            return jsonify({
                'success': True,
                'results': results,
                'filename': filename
            })
            
        except Exception as e:
            return jsonify({'error': f'Processing failed: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/results/<filename>')
def show_results(filename):
    """Display detection results for a specific file"""
    violations = get_violations(filename=filename)
    return render_template('results.html', violations=violations, filename=filename)

@app.route('/reports')
def reports():
    """Display all violation reports"""
    violations = get_violations()
    stats = get_violation_stats()
    return render_template('reports.html', violations=violations, stats=stats)

@app.route('/dashboard')
def dashboard():
    """Dashboard with violation statistics"""
    stats = get_violation_stats()
    return render_template('dashboard.html', stats=stats)

@app.route('/api/violations')
def api_violations():
    """REST API endpoint to get violation data"""
    violations = get_violations()
    return jsonify(violations)

@app.route('/api/stats')
def api_stats():
    """REST API endpoint to get violation statistics"""
    stats = get_violation_stats()
    return jsonify(stats)

@app.route('/static/results/<filename>')
def serve_result(filename):
    """Serve processed result images"""
    return send_file(os.path.join(app.config['RESULTS_FOLDER'], filename))

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Initialize database
    init_db()
    
    print("🚦 Traffic Violation Detection App Starting...")
    print("📁 Upload folder:", app.config['UPLOAD_FOLDER'])
    print("📊 Results folder:", app.config['RESULTS_FOLDER'])
    print("🌐 Access the app at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

