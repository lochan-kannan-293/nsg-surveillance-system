import cv2
import numpy as np
from datetime import datetime
import os

class VideoProcessor:
    """
    Basic video processing class for NSG Surveillance System
    Handles video loading, frame extraction, and basic operations
    """
    
    def __init__(self):
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv']
        print("✓ VideoProcessor initialized")
    
    def get_video_info(self, video_path):
        """Extract video metadata"""
        print(f"\n{'='*60}")
        print(f"Analyzing video: {video_path}")
        print(f"{'='*60}")
        
        # Open video file
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print("✗ Error: Cannot open video file")
            return None
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0
        
        cap.release()
        
        info = {
            'fps': fps,
            'frame_count': frame_count,
            'width': width,
            'height': height,
            'duration': duration,
            'resolution': f"{width}x{height}"
        }
        
        # Print info
        print(f"\nVideo Properties:")
        print(f"  Resolution: {info['resolution']}")
        print(f"  FPS: {info['fps']:.2f}")
        print(f"  Total Frames: {info['frame_count']}")
        print(f"  Duration: {info['duration']:.2f} seconds")
        print(f"{'='*60}\n")
        
        return info
    
    def extract_frame(self, video_path, frame_number):
        """Extract a specific frame from video"""
        cap = cv2.VideoCapture(video_path)
        
        # Set frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            print(f"✓ Extracted frame {frame_number}")
            return frame
        else:
            print(f"✗ Failed to extract frame {frame_number}")
            return None
    
    def process_video(self, video_path, frame_skip=30):
        """
        Process video frame by frame
        frame_skip: process every Nth frame (30 = 1 frame per second at 30fps)
        """
        print(f"\n{'='*60}")
        print(f"Starting video processing...")
        print(f"{'='*60}\n")
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print("✗ Error: Cannot open video")
            return
        
        frame_count = 0
        processed_count = 0
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            frame_count += 1
            
            # Skip frames for faster processing
            if frame_count % frame_skip != 0:
                continue
            
            processed_count += 1
            
            # Process frame here (we'll add detection later)
            # For now, just display progress
            timestamp = frame_count / cap.get(cv2.CAP_PROP_FPS)
            print(f"Processing frame {frame_count} | Time: {timestamp:.2f}s", end='\r')
            
            # Show the frame (press 'q' to quit)
            cv2.imshow('NSG Surveillance - Processing', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n\n✓ Processing stopped by user")
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n\n{'='*60}")
        print(f"Processing Complete!")
        print(f"  Total frames: {frame_count}")
        print(f"  Processed frames: {processed_count}")
        print(f"{'='*60}\n")
    
    def save_frame(self, frame, output_path):
        """Save a frame as image"""
        success = cv2.imwrite(output_path, frame)
        if success:
            print(f"✓ Frame saved to: {output_path}")
        else:
            print(f"✗ Failed to save frame")
        return success


# Test the processor
if __name__ == "__main__":
    processor = VideoProcessor()
    
    # Test with webcam (use 0 for default webcam)
    # OR replace with path to your video file
    video_source = 0  # Change to 'data/test_video.mp4' if you have a video file
    
    print("Press 'q' to stop the video")
    
    # Get video info (skip for webcam)
    if isinstance(video_source, str):
        info = processor.get_video_info(video_source)
    
    # Process video
    processor.process_video(video_source, frame_skip=10)