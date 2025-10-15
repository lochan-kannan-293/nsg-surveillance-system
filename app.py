import streamlit as st
import cv2
import numpy as np
from datetime import datetime
import tempfile
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="NSG AI Surveillance System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .metric-card {
        background-color: #1e2130;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #2e3548;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'detections' not in st.session_state:
    st.session_state.detections = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'processed' not in st.session_state:
    st.session_state.processed = False

# Header
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.title("🛡️ NSG AI-Powered Surveillance System")
    st.markdown("**AI-Powered Video Intelligence Platform**")

with col3:
    st.success("🟢 System Active")

st.divider()

# Sidebar
with st.sidebar:
    st.header("⚙️ System Configuration")
    
    # Detection Mode
    detection_mode = st.selectbox(
        "Detection Mode",
        ["All Objects", "Weapons Only", "Facial Recognition", "Suspicious Activity", "Vehicle Tracking"],
        help="Select what to detect in the video"
    )
    
    st.divider()
    
    # Processing Settings
    st.subheader("Processing Settings")
    confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.3,
        max_value=0.95,
        value=0.5,
        step=0.05,
        help="Minimum confidence for detections"
    )
    
    frame_skip = st.slider(
        "Frame Skip",
        min_value=1,
        max_value=30,
        value=5,
        help="Process every Nth frame (higher = faster)"
    )
    
    st.divider()
    
    # System Info
    st.subheader("📊 System Info")
    st.info(f"**Detection Mode:** {detection_mode}")
    st.info(f"**Confidence:** {confidence_threshold*100:.0f}%")
    st.info(f"**Frame Skip:** {frame_skip}")

# Main content area
tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "🔍 Live Analysis", "📋 Reports"])

# TAB 1: Upload & Process
with tab1:
    st.header("Video Upload")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Video upload
        uploaded_file = st.file_uploader(
            "Upload surveillance video",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Supported formats: MP4, AVI, MOV, MKV"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            tfile.write(uploaded_file.read())
            video_path = tfile.name
            
            st.success(f"✅ Video uploaded: {uploaded_file.name}")
            st.info(f"📦 Size: {uploaded_file.size / (1024*1024):.2f} MB")
            
            # Display video
            st.video(video_path)
            
            # Get video info
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            cap.release()
            
            # Video info
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.metric("Resolution", f"{width}x{height}")
            with col_b:
                st.metric("FPS", f"{fps:.1f}")
            with col_c:
                st.metric("Frames", f"{frame_count}")
            with col_d:
                st.metric("Duration", f"{duration:.1f}s")
            
    with col2:
        st.subheader("Quick Actions")
        
        if uploaded_file is not None:
            if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
                with st.spinner("🔄 Processing video..."):
                    # Simulate processing
                    import time
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Simulate frame processing
                    for i in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(i + 1)
                        status_text.text(f"Processing frame {i * frame_count // 100}/{frame_count}")
                    
                    # Generate mock detections
                    st.session_state.detections = [
                        {
                            'type': 'person',
                            'confidence': 0.92,
                            'timestamp': '00:00:05',
                            'location': (120, 80, 200, 350)
                        },
                        {
                            'type': 'person',
                            'confidence': 0.88,
                            'timestamp': '00:00:12',
                            'location': (450, 100, 180, 320),
                            'watchlist_match': True,
                            'watchlist_id': 'WL-2847'
                        },
                        {
                            'type': 'vehicle',
                            'confidence': 0.91,
                            'timestamp': '00:00:18',
                            'location': (50, 400, 300, 200),
                            'plate': 'DL-7XYZ-1234'
                        }
                    ]
                    
                    # Generate alerts
                    st.session_state.alerts = [
                        {
                            'severity': 'HIGH',
                            'message': 'WATCHLIST MATCH: Individual WL-2847 detected',
                            'timestamp': '00:00:12',
                            'confidence': 88
                        }
                    ]
                    
                    st.session_state.processed = True
                    
                    st.success("✅ Analysis complete!")
                    st.balloons()
        else:
            st.info("👆 Upload a video to begin")

# TAB 2: Live Analysis
with tab2:
    if st.session_state.processed:
        st.header("🔍 Analysis Results")
        
        col1, col2 = st.columns([1, 2])
        
        # Alerts Panel
        with col1:
            st.subheader("🚨 Real-Time Alerts")
            
            if st.session_state.alerts:
                for alert in st.session_state.alerts:
                    severity_color = {
                        'CRITICAL': 'error',
                        'HIGH': 'warning',
                        'MEDIUM': 'info',
                        'LOW': 'success'
                    }.get(alert['severity'], 'info')
                    
                    with st.container():
                        if alert['severity'] == 'CRITICAL':
                            st.error(f"**{alert['severity']}** 🔴")
                        elif alert['severity'] == 'HIGH':
                            st.warning(f"**{alert['severity']}** 🟠")
                        else:
                            st.info(f"**{alert['severity']}** 🟡")
                        
                        st.markdown(f"**{alert['message']}**")
                        st.caption(f"⏱️ {alert['timestamp']} | Confidence: {alert['confidence']}%")
                        st.divider()
            else:
                st.info("No alerts detected")
        
        # Detections Panel
        with col2:
            st.subheader("✅ Detected Objects & Activities")
            
            if st.session_state.detections:
                for idx, det in enumerate(st.session_state.detections):
                    with st.expander(f"🎯 {det['type'].upper()} - {det['timestamp']}", expanded=True):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.metric("Confidence", f"{det['confidence']*100:.1f}%")
                            st.text(f"Timestamp: {det['timestamp']}")
                        
                        with col_b:
                            if 'watchlist_match' in det and det['watchlist_match']:
                                st.error(f"🚨 WATCHLIST MATCH")
                                st.text(f"ID: {det['watchlist_id']}")
                            
                            if 'plate' in det:
                                st.success(f"🚗 Plate: {det['plate']}")
                        
                        st.caption(f"Location: {det['location']}")
            else:
                st.info("No detections yet. Process a video first.")
    else:
        st.info("👈 Upload and process a video in the 'Upload & Process' tab to see results here")

# TAB 3: Reports
with tab3:
    st.header("📋 Analysis Reports")
    
    if st.session_state.processed:
        # Summary Statistics
        st.subheader("Summary Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Detections",
                len(st.session_state.detections),
                help="Total number of objects detected"
            )
        
        with col2:
            critical_alerts = sum(1 for a in st.session_state.alerts if a['severity'] == 'CRITICAL')
            st.metric(
                "Critical Alerts",
                critical_alerts,
                help="High-priority security alerts"
            )
        
        with col3:
            st.metric(
                "Accuracy",
                "87%",
                help="Model accuracy"
            )
        
        with col4:
            st.metric(
                "Processing Time",
                "2.3s",
                help="Time taken to process video"
            )
        
        st.divider()
        
        # Detection Timeline
        st.subheader("Detection Timeline")
        
        if st.session_state.detections:
            import pandas as pd
            
            df_data = []
            for det in st.session_state.detections:
                df_data.append({
                    'Timestamp': det['timestamp'],
                    'Type': det['type'],
                    'Confidence': f"{det['confidence']*100:.1f}%",
                    'Watchlist': 'Match' if det.get('watchlist_match') else 'No Match'
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
        
        st.divider()
        
        # Export Report
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("📥 Export Report", type="primary", use_container_width=True):
                import json
                
                report = {
                    'timestamp': datetime.now().isoformat(),
                    'detections': st.session_state.detections,
                    'alerts': st.session_state.alerts,
                    'summary': {
                        'total_detections': len(st.session_state.detections),
                        'critical_alerts': sum(1 for a in st.session_state.alerts if a['severity'] == 'CRITICAL')
                    }
                }
                
                st.download_button(
                    label="Download JSON Report",
                    data=json.dumps(report, indent=2),
                    file_name=f"nsg_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    else:
        st.info("👈 Process a video first to generate reports")

# Footer
st.divider()
st.caption("🛡️ NSG AI-Powered Surveillance System | Developed for National Security Operations")