#  Traffic Violation Detection System

An AI-powered web application for detecting traffic violations using YOLOv8 and Flask.

##  Features

- **AI-Powered Detection**: Uses YOLOv8 for detecting various traffic violations
- **Multiple Violation Types**: Red-light jumping, helmet violations, triple riding, wrong-lane driving
- **File Upload Support**: Images and videos (PNG, JPG, MP4, AVI, MOV, MKV)
- **Real-time Processing**: Live detection with confidence scores
- **Database Storage**: SQLite database for storing violation records
- **Analytics Dashboard**: Statistics and violation trends
- **REST API**: JSON endpoints for integration
- **Responsive UI**: Modern Bootstrap 5 interface with dark blue theme

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Navigate to your project folder**
   ```bash
   cd "C:\Users\Anusha Manneti\OneDrive\Desktop\bhanu"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   # Method 1: Double-click START.bat
   # Method 2: Run python start_website.py
   python start_website.py
   ```

4. **Access the application**
   Open your browser and go to: `http://localhost:8000`

## 📁 Project Structure

```
traffic_violation_app/
├── main.py                 # Flask application entry point
├── database.py             # Database operations
├── models/
│   └── violation_model.py  # AI model integration
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── results.html
│   ├── reports.html
│   └── dashboard.html
├── static/                 # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── uploads/               # Uploaded files (auto-created)
├── static/results/        # Processed images (auto-created)
├── requirements.txt
└── README.md
```

## 🎮 Usage

### 1. Upload Files
- Go to the home page
- Click "Choose File" or drag & drop
- Select image or video file
- Click "Upload and Analyze"

### 2. View Results
- Detection results appear immediately
- View detailed results with bounding boxes
- Check confidence scores

### 3. Browse Reports
- Navigate to "Reports" page
- View all detected violations
- Filter by violation type

### 4. Analytics Dashboard
- Go to "Dashboard" for statistics
- View violation trends
- Monitor system status

##  Configuration

### Model Configuration
Edit `models/violation_model.py` to:
- Use custom trained models
- Adjust confidence thresholds
- Add new violation types

### Database Configuration
The app uses SQLite by default. To use a different database:
1. Modify `database.py`
2. Update connection settings
3. Run database migrations

### File Upload Limits
Default limit: 100MB
To change: Modify `MAX_CONTENT_LENGTH` in `main.py`

## 🛠️ API Endpoints

### REST API
- `GET /api/violations` - Get all violations
- `GET /api/stats` - Get violation statistics
- `POST /upload` - Upload file for processing

### Example API Usage
```bash
# Get all violations
curl http://localhost:5000/api/violations

# Get statistics
curl http://localhost:5000/api/stats
```

##  Customization

### UI Theme
Edit `static/css/style.css` to customize:
- Colors and fonts
- Layout and spacing
- Animation effects

### Detection Rules
Modify `models/violation_model.py`:
- Add new violation types
- Adjust detection logic
- Change confidence thresholds

##  Troubleshooting

### Common Issues

1. **Model Loading Error**
   ```
   Solution: Ensure ultralytics is installed correctly
   pip install ultralytics
   ```

2. **File Upload Fails**
   ```
   Check file size (max 100MB)
   Verify file format is supported
   ```

3. **Database Error**
   ```
   Delete traffic_violations.db and restart
   The database will be recreated automatically
   ```

4. **Permission Errors**
   ```
   Ensure write permissions for uploads/ and static/results/
   ```

### Performance Tips

- Use smaller video files for faster processing
- Process videos in chunks for large files
- Consider GPU acceleration for better performance

##  System Requirements

### Minimum Requirements
- Python 3.8+
- 4GB RAM
- 2GB free disk space

### Recommended
- Python 3.9+
- 8GB RAM
- GPU with CUDA support (for faster processing)
- 10GB free disk space

## Security Notes

- File uploads are validated for type and size
- SQLite database is local-only
- No external API calls (unless configured)
- File paths are sanitized

##  Performance

### Processing Times
- Images: 1-3 seconds
- Videos (30s): 10-30 seconds
- Large files: May take longer

### Optimization
- Use GPU for faster processing
- Optimize video resolution
- Batch process multiple files

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

##  License

This project is open source. Feel free to use and modify as needed.

##  Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in the console
3. Ensure all dependencies are installed
4. Verify file permissions

##  Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
1. Use a production WSGI server (Gunicorn)
2. Set up reverse proxy (Nginx)
3. Configure environment variables
4. Set up SSL certificates

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

---

**Happy Detecting! 🚦✨**

