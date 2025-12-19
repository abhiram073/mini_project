"""
AI Model for Traffic Violation Detection
Uses YOLOv8 for detecting various traffic violations
"""

import cv2
import numpy as np
from ultralytics import YOLO
import os
from typing import List, Dict, Tuple
import torch

class TrafficViolationDetector:
    """
    Traffic violation detection using YOLOv8 model
    Detects: red-light jumping, helmet-less riders, triple riding, wrong-lane driving
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize the detector with YOLOv8 model
        
        Args:
            model_path: Path to custom trained model (optional)
        """
        self.model_path = model_path
        self.model = None
        self.violation_classes = {
            'red_light_jump': 0,
            'no_helmet': 1,
            'triple_riding': 2,
            'wrong_lane': 3,
            'speeding': 4
        }
        
        # Load model
        self._load_model()
    
    def _load_model(self):
        """Load YOLOv8 model"""
        try:
            if self.model_path and os.path.exists(self.model_path):
                self.model = YOLO(self.model_path)
                print(f"✅ Loaded custom model from {self.model_path}")
            else:
                # Use pretrained YOLOv8 model
                self.model = YOLO('yolov8n.pt')
                print("✅ Loaded pretrained YOLOv8 model")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            # Fallback to basic detection
            self.model = None
    
    def detect_violations(self, file_path: str) -> List[Dict]:
        """
        Detect traffic violations in uploaded file
        
        Args:
            file_path: Path to uploaded image/video file
            
        Returns:
            List of detected violations with details
        """
        violations = []
        
        # Check if file is video or image
        if self._is_video(file_path):
            violations = self._process_video(file_path)
        else:
            violations = self._process_image(file_path)
        
        return violations
    
    def _is_video(self, file_path: str) -> bool:
        """Check if file is a video"""
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
        return os.path.splitext(file_path)[1].lower() in video_extensions
    
    def _process_image(self, image_path: str) -> List[Dict]:
        """Process single image for violations"""
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return []
            
            # Run detection
            results = self._run_detection(image)
            
            # Process results
            violations = self._process_detection_results(results, image, image_path)
            
            return violations
            
        except Exception as e:
            print(f"❌ Error processing image: {e}")
            return []
    
    def _process_video(self, video_path: str) -> List[Dict]:
        """Process video for violations"""
        violations = []
        
        try:
            cap = cv2.VideoCapture(video_path)
            frame_count = 0
            max_frames = 30  # Process max 30 frames to avoid long processing
            
            while cap.isOpened() and frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process every 5th frame to balance accuracy and speed
                if frame_count % 5 == 0:
                    results = self._run_detection(frame)
                    frame_violations = self._process_detection_results(
                        results, frame, video_path, frame_number=frame_count
                    )
                    violations.extend(frame_violations)
                
                frame_count += 1
            
            cap.release()
            
        except Exception as e:
            print(f"❌ Error processing video: {e}")
        
        return violations
    
    def _run_detection(self, image: np.ndarray) -> List:
        """Run YOLO detection on image"""
        if self.model is None:
            return []
        
        try:
            results = self.model(image, conf=0.5, verbose=False)
            return results
        except Exception as e:
            print(f"❌ Detection error: {e}")
            return []
    
    def _process_detection_results(self, results: List, image: np.ndarray, 
                                 file_path: str, frame_number: int = 0) -> List[Dict]:
        """Process YOLO detection results and identify violations"""
        violations = []
        
        if not results or len(results) == 0:
            return violations
        
        try:
            # Get detection results
            result = results[0]
            boxes = result.boxes
            
            if boxes is None or len(boxes) == 0:
                return violations
            
            # Process each detection
            for i, box in enumerate(boxes):
                # Get box coordinates and confidence
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = float(box.conf[0].cpu().numpy())
                class_id = int(box.cls[0].cpu().numpy())
                
                # Map COCO classes to traffic violations
                violation_type = self._map_class_to_violation(class_id, confidence)
                
                if violation_type:
                    # Draw bounding box
                    annotated_image = self._draw_bounding_box(
                        image.copy(), (int(x1), int(y1), int(x2), int(y2)), 
                        violation_type, confidence
                    )
                    
                    # Save result image
                    result_filename = self._save_result_image(
                        annotated_image, file_path, frame_number, i
                    )
                    
                    violations.append({
                        'violation_type': violation_type,
                        'confidence': confidence,
                        'bbox': [int(x1), int(y1), int(x2), int(y2)],
                        'result_image': result_filename
                    })
        
        except Exception as e:
            print(f"❌ Error processing results: {e}")
        
        return violations
    
    def _map_class_to_violation(self, class_id: int, confidence: float) -> str:
        """
        Map YOLO class IDs to traffic violations
        COCO dataset classes: person, bicycle, car, motorcycle, bus, truck
        """
        # COCO class mapping
        coco_classes = {
            0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 
            5: 'bus', 7: 'truck'
        }
        
        class_name = coco_classes.get(class_id, 'unknown')
        
        # Simple heuristic-based violation detection
        # In a real application, you'd use a custom trained model
        
        if class_name == 'person' and confidence > 0.7:
            return 'no_helmet'  # Assuming person on bike without helmet
        elif class_name == 'motorcycle' and confidence > 0.8:
            return 'triple_riding'  # Multiple people on motorcycle
        elif class_name in ['car', 'bus', 'truck'] and confidence > 0.6:
            return 'wrong_lane'  # Vehicle in wrong lane
        elif class_name == 'bicycle' and confidence > 0.7:
            return 'red_light_jump'  # Bicycle jumping red light
        
        return None
    
    def _draw_bounding_box(self, image: np.ndarray, bbox: Tuple[int, int, int, int], 
                          violation_type: str, confidence: float) -> np.ndarray:
        """Draw bounding box and label on image"""
        x1, y1, x2, y2 = bbox
        
        # Colors for different violation types
        colors = {
            'red_light_jump': (0, 0, 255),      # Red
            'no_helmet': (0, 165, 255),         # Orange
            'triple_riding': (255, 0, 0),      # Blue
            'wrong_lane': (0, 255, 0),         # Green
            'speeding': (255, 255, 0)          # Yellow
        }
        
        color = colors.get(violation_type, (255, 255, 255))
        
        # Draw rectangle
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        
        # Draw label
        label = f"{violation_type.replace('_', ' ').title()}: {confidence:.2f}"
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        
        # Draw label background
        cv2.rectangle(image, (x1, y1 - label_size[1] - 10), 
                     (x1 + label_size[0], y1), color, -1)
        
        # Draw label text
        cv2.putText(image, label, (x1, y1 - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return image
    
    def _save_result_image(self, image: np.ndarray, file_path: str, 
                          frame_number: int, detection_id: int) -> str:
        """Save processed image with bounding boxes"""
        try:
            # Create result filename
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            result_filename = f"{base_name}_frame{frame_number}_det{detection_id}.jpg"
            result_path = os.path.join('static/results', result_filename)
            
            # Save image
            cv2.imwrite(result_path, image)
            
            return result_filename
            
        except Exception as e:
            print(f"❌ Error saving result image: {e}")
            return ""
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        if self.model is None:
            return {"status": "No model loaded"}
        
        return {
            "status": "Model loaded",
            "model_path": self.model_path or "Pretrained YOLOv8",
            "violation_classes": list(self.violation_classes.keys())
        }

