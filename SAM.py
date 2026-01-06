import tkinter as tk
import requests
import logging
from logging.handlers import RotatingFileHandler
from tkinter import simpledialog, messagebox, scrolledtext, filedialog
from PIL import Image, ImageTk, ImageDraw
import threading
import speech_recognition as sr
import pygame
import os
import datetime
import webbrowser
import psutil
import wikipedia
import pyautogui
import time
import sys
import subprocess
import platform
import urllib.parse
import re
import pyttsx3  # Add pyttsx3 for offline TTS
import smtplib
from email.mime.text import MIMEText
import random  # Add random for conversational enhancements
# Modern UI: Requires 'pip install customtkinter'
import customtkinter as ctk
import queue
import glob
import json
import shutil
import math
from typing import Optional, Dict, List
from features.web_automation import YouTubeAutomation, BrowserController, SystemLauncher, WhatsAppAutomation
try:
    from serpapi import GoogleSearch  # Optional dependency
except Exception:
    GoogleSearch = None

# System Tray Support
try:
    from features.system_tray import TrayManager, HotkeyManager, MiniFloatingWindow
    from config.settings import TRAY_CONFIG
    TRAY_AVAILABLE = True
except ImportError as e:
    TRAY_AVAILABLE = False
    TRAY_CONFIG = {"enabled": False}
    print(f"[INFO] System tray not available: {e}. Install with: pip install pystray pynput")

# Camera and AI Vision imports
try:
    import cv2
    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False
    print("[INFO] OpenCV not available. Install with: pip install opencv-python")

try:
    import base64
    import io
    from PIL import Image
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    print("[INFO] Vision processing not available")

# 3D Model Viewer imports
try:
    import numpy as np
    THREE_D_AVAILABLE = True
except ImportError:
    THREE_D_AVAILABLE = False
    print("[INFO] NumPy not available. Install with: pip install numpy")

try:
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("[INFO] Matplotlib not available. Install with: pip install matplotlib")

# 3D File Format Support
try:
    import trimesh
    TRIMESH_AVAILABLE = True
except ImportError:
    TRIMESH_AVAILABLE = False
    print("[INFO] Trimesh not available. Install with: pip install trimesh")

try:
    from stl import mesh as stl_mesh
    STL_AVAILABLE = True
except ImportError:
    STL_AVAILABLE = False
    print("[INFO] Numpy-STL not available. Install with: pip install numpy-stl")

# OCR (Optical Character Recognition) for screen analysis
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("[INFO] pytesseract not available. Install with: pip install pytesseract")

# --- API Keys ---
SERPAPI_KEY = "c386502a9f4115666d1120c7dcdcc33cc0bae6204cdbdf40fe9538029bbb8abd"
MISTRAL_API_KEY = "xRG7cM2rfijNOIIfQbMFWVF0ZAjCjCjW"
# Add Google Vision API key for image analysis
GOOGLE_VISION_API_KEY = ""  # You'll need to add your Google Vision API key here

CITY_NAME = "hyderabad"
LANGUAGES = {
    "English":     {"code": "en", "sr_code": "en-US", "tts_voice": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"},
    "Hindi":       {"code": "hi", "sr_code": "hi-IN", "tts_voice": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_HI-IN_HEMANT_11.0"},
    "Telugu":      {"code": "te", "sr_code": "te-IN", "tts_voice": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_TE-IN_CHAITANYA_11.0"},
}

# Modern AI-inspired themes with futuristic design
THEMES = {
    "copilot_dark": {
        "bg": "#0a0a0a", "fg": "#ffffff", "entrybg": "#1a1a1a", "textfg": "#ffffff",
        "sysfg": "#00d4ff", "btnbg": "#1a1a1a", "btnfg": "#ffffff", "btnactive": "#2a2a2a",
        "subfg": "#cccccc", "scrolledbg": "#0a0a0a", "inputfg": "#ffffff",
        "accent": "#00d4ff", "success": "#00ff88", "warning": "#ffaa00", "error": "#ff4444",
        "accent_hover": "#00b3cc", "success_hover": "#00cc6a", "error_hover": "#cc3333",
        "btnbg_hover": "#2a2a2a", "sidebar": "#1a1a1a", "card": "#1a1a1a", "hover": "#2a2a2a",
        "user_bubble": "#00d4ff", "assistant_bubble": "#1a1a1a", "system_bubble": "#2a2a2a",
        "chat_bg": "#0a0a0a", "input_border": "#2a2a2a", "typing_indicator": "#00d4ff",
        "gradient_start": "#00d4ff", "gradient_end": "#0099cc", "glow": "#00ffff",
        "panel_bg": "#0f0f0f", "progress_bg": "#1a1a1a", "progress_fill": "#00d4ff",
        "network_bg": "#0f0f0f", "temporal_bg": "#0f0f0f", "visual_bg": "#0f0f0f",
        "ai_gradient": "linear-gradient(135deg, #00d4ff 0%, #0099cc 50%, #0066aa 100%)",
        "neon_glow": "#00ffff", "matrix_green": "#00ff41", "cyber_blue": "#0080ff",
        "hologram": "#0a0a0a", "glass": "#1a1a1a",
        "shadow": "#00d4ff", "border_glow": "#00d4ff"
    },
    "copilot_light": {
        "bg": "#f8fafc", "fg": "#1a202c", "entrybg": "#ffffff", "textfg": "#1a202c",
        "sysfg": "#0078d4", "btnbg": "#ffffff", "btnfg": "#1a202c", "btnactive": "#f1f5f9",
        "subfg": "#64748b", "scrolledbg": "#f8fafc", "inputfg": "#1a202c",
        "accent": "#0078d4", "success": "#059669", "warning": "#d97706", "error": "#dc2626",
        "accent_hover": "#005a9e", "success_hover": "#047857", "error_hover": "#b91c1c",
        "btnbg_hover": "#f1f5f9", "sidebar": "#ffffff", "card": "#ffffff", "hover": "#f1f5f9",
        "user_bubble": "#0078d4", "assistant_bubble": "#ffffff", "system_bubble": "#f1f5f9",
        "chat_bg": "#f8fafc", "input_border": "#e2e8f0", "typing_indicator": "#0078d4",
        "gradient_start": "#0078d4", "gradient_end": "#005a9e", "glow": "#0078d4",
        "panel_bg": "#ffffff", "progress_bg": "#f1f5f9", "progress_fill": "#0078d4",
        "network_bg": "#ffffff", "temporal_bg": "#ffffff", "visual_bg": "#ffffff",
        "ai_gradient": "linear-gradient(135deg, #0078d4 0%, #005a9e 50%, #004080 100%)",
        "neon_glow": "#0078d4", "matrix_green": "#059669", "cyber_blue": "#0078d4",
        "hologram": "#f8fafc", "glass": "#ffffff",
        "shadow": "#0078d4", "border_glow": "#0078d4"
    },
    "copilot_blue": {
        "bg": "#001122", "fg": "#ffffff", "entrybg": "#002244", "textfg": "#ffffff",
        "sysfg": "#00d4ff", "btnbg": "#002244", "btnfg": "#ffffff", "btnactive": "#003366",
        "subfg": "#cccccc", "scrolledbg": "#001122", "inputfg": "#ffffff",
        "accent": "#00d4ff", "success": "#00ff88", "warning": "#ffaa00", "error": "#ff4444",
        "accent_hover": "#00b3cc", "success_hover": "#00cc6a", "error_hover": "#cc3333",
        "btnbg_hover": "#003366", "sidebar": "#002244", "card": "#002244", "hover": "#003366",
        "user_bubble": "#00d4ff", "assistant_bubble": "#002244", "system_bubble": "#003366",
        "chat_bg": "#001122", "input_border": "#003366", "typing_indicator": "#00d4ff",
        "gradient_start": "#00d4ff", "gradient_end": "#0099cc", "glow": "#00ffff",
        "panel_bg": "#001a33", "progress_bg": "#002244", "progress_fill": "#00d4ff",
        "network_bg": "#001a33", "temporal_bg": "#001a33", "visual_bg": "#001a33",
        "ai_gradient": "linear-gradient(135deg, #00d4ff 0%, #0099cc 50%, #0066aa 100%)",
        "neon_glow": "#00ffff", "matrix_green": "#00ff41", "cyber_blue": "#0080ff",
        "hologram": "#001122", "glass": "#002244",
        "shadow": "#00d4ff", "border_glow": "#00d4ff"
    },
    "ai_neon": {
        "bg": "#0a0a0a", "fg": "#ffffff", "entrybg": "#1a1a1a", "textfg": "#ffffff",
        "sysfg": "#00ff41", "btnbg": "#1a1a1a", "btnfg": "#ffffff", "btnactive": "#2a2a2a",
        "subfg": "#cccccc", "scrolledbg": "#0a0a0a", "inputfg": "#ffffff",
        "accent": "#00ff41", "success": "#00ff88", "warning": "#ffaa00", "error": "#ff4444",
        "accent_hover": "#00cc33", "success_hover": "#00cc6a", "error_hover": "#cc3333",
        "btnbg_hover": "#2a2a2a", "sidebar": "#1a1a1a", "card": "#1a1a1a", "hover": "#2a2a2a",
        "user_bubble": "#00ff41", "assistant_bubble": "#1a1a1a", "system_bubble": "#2a2a2a",
        "chat_bg": "#0a0a0a", "input_border": "#2a2a2a", "typing_indicator": "#00ff41",
        "gradient_start": "#00ff41", "gradient_end": "#00cc33", "glow": "#00ff41",
        "panel_bg": "#0f0f0f", "progress_bg": "#1a1a1a", "progress_fill": "#00ff41",
        "network_bg": "#0f0f0f", "temporal_bg": "#0f0f0f", "visual_bg": "#0f0f0f",
        "ai_gradient": "linear-gradient(135deg, #00ff41 0%, #00cc33 50%, #009926 100%)",
        "neon_glow": "#00ff41", "matrix_green": "#00ff41", "cyber_blue": "#00ff41",
        "hologram": "#0a0a0a", "glass": "#1a1a1a",
        "shadow": "#00ff41", "border_glow": "#00ff41"
    }
    ,
    "pro_slate": {
        "bg": "#0f1115", "fg": "#e5e7eb", "entrybg": "#111317", "textfg": "#e5e7eb",
        "sysfg": "#64748b", "btnbg": "#111317", "btnfg": "#e5e7eb", "btnactive": "#1a1f29",
        "subfg": "#9ca3af", "scrolledbg": "#0f1115", "inputfg": "#e5e7eb",
        "accent": "#4f46e5", "success": "#22c55e", "warning": "#f59e0b", "error": "#ef4444",
        "accent_hover": "#4338ca", "success_hover": "#16a34a", "error_hover": "#dc2626",
        "btnbg_hover": "#1a1f29", "sidebar": "#0e1014", "card": "#12141a", "hover": "#1a1f29",
        "user_bubble": "#4f46e5", "assistant_bubble": "#12141a", "system_bubble": "#1a1f29",
        "chat_bg": "#0f1115", "input_border": "#1a1f29", "typing_indicator": "#4f46e5",
        "gradient_start": "#1f2937", "gradient_end": "#0f172a", "glow": "#3b82f6",
        "panel_bg": "#0f1115", "progress_bg": "#111317", "progress_fill": "#4f46e5",
        "network_bg": "#0f1115", "temporal_bg": "#0f1115", "visual_bg": "#0f1115",
        "ai_gradient": "linear-gradient(135deg, #1f2937 0%, #0f172a 50%, #0b1220 100%)",
        "neon_glow": "#3b82f6", "matrix_green": "#22c55e", "cyber_blue": "#3b82f6",
        "hologram": "#0f1115", "glass": "#0e1014",
        "shadow": "#1f2937", "border_glow": "#4f46e5"
    },
    # Ultra Modern - Sleek glassmorphism theme with purple/violet accents
    "ultra_modern": {
        "bg": "#09090b", "fg": "#fafafa", "entrybg": "#18181b", "textfg": "#fafafa",
        "sysfg": "#a1a1aa", "btnbg": "#27272a", "btnfg": "#fafafa", "btnactive": "#3f3f46",
        "subfg": "#71717a", "scrolledbg": "#09090b", "inputfg": "#fafafa",
        "accent": "#8b5cf6", "success": "#10b981", "warning": "#f59e0b", "error": "#ef4444",
        "accent_hover": "#7c3aed", "success_hover": "#059669", "error_hover": "#dc2626",
        "btnbg_hover": "#3f3f46", "sidebar": "#0c0c0e", "card": "#18181b", "hover": "#27272a",
        "user_bubble": "#7c3aed", "assistant_bubble": "#18181b", "system_bubble": "#27272a",
        "chat_bg": "#09090b", "input_border": "#3f3f46", "typing_indicator": "#8b5cf6",
        "gradient_start": "#8b5cf6", "gradient_end": "#6366f1", "glow": "#a78bfa",
        "panel_bg": "#0c0c0e", "progress_bg": "#18181b", "progress_fill": "#8b5cf6",
        "network_bg": "#0c0c0e", "temporal_bg": "#0c0c0e", "visual_bg": "#0c0c0e",
        "ai_gradient": "linear-gradient(135deg, #8b5cf6 0%, #6366f1 50%, #4f46e5 100%)",
        "neon_glow": "#a78bfa", "matrix_green": "#10b981", "cyber_blue": "#6366f1",
        "hologram": "#09090b", "glass": "#18181b",
        "shadow": "#8b5cf6", "border_glow": "#8b5cf6",
        # Modern additions
        "glass_bg": "rgba(24, 24, 27, 0.8)", "glass_border": "#3f3f46",
        "send_gradient_start": "#8b5cf6", "send_gradient_end": "#ec4899",
        "avatar_glow": "#a78bfa", "header_accent": "#c4b5fd"
    },
    # Core System - Bhavesh Pandey futuristic style with particle orb
    "core_system": {
        "bg": "#0a0a0a", "fg": "#ffffff", "entrybg": "#0d1117", "textfg": "#ffffff",
        "sysfg": "#0ea5e9", "btnbg": "#0d1117", "btnfg": "#ffffff", "btnactive": "#1a2332",
        "subfg": "#9ca3af", "scrolledbg": "#0a0a0a", "inputfg": "#ffffff",
        "accent": "#0ea5e9", "success": "#22c55e", "warning": "#f97316", "error": "#dc2626",
        "accent_hover": "#0284c7", "success_hover": "#16a34a", "error_hover": "#b91c1c",
        "btnbg_hover": "#1a2332", "sidebar": "#0d1117", "card": "#0d1117", "hover": "#1a2332",
        "user_bubble": "#0ea5e9", "assistant_bubble": "#1a1f2e", "system_bubble": "#0d1117",
        "chat_bg": "#0a0a0a", "input_border": "#1e3a5f", "typing_indicator": "#0ea5e9",
        "gradient_start": "#0ea5e9", "gradient_end": "#0284c7", "glow": "#0ea5e9",
        "panel_bg": "#0d1117", "progress_bg": "#1a2332", "progress_fill": "#0ea5e9",
        "progress_orange": "#f97316", "progress_cyan": "#06b6d4",
        "network_bg": "#0d1117", "temporal_bg": "#0d1117", "visual_bg": "#0d1117",
        "ai_gradient": "linear-gradient(135deg, #0ea5e9 0%, #0284c7 50%, #0369a1 100%)",
        "neon_glow": "#0ea5e9", "matrix_green": "#22c55e", "cyber_blue": "#0ea5e9",
        "hologram": "#0a0a0a", "glass": "#0d1117",
        "shadow": "#0ea5e9", "border_glow": "#1e3a5f",
        "orb_particle": "#d4a574", "orb_particle_bright": "#fbbf24",
        "end_button": "#dc2626", "end_button_hover": "#b91c1c",
        "nav_active": "#0ea5e9", "nav_inactive": "#4b5563",
        "glass_border": "#1e3a5f", "header_accent": "#0ea5e9"
    }
}


class AnimatedSystemPanel(ctk.CTkFrame):
    """Enhanced system panel with futuristic design matching the video style."""
    
    def __init__(self, parent, theme="copilot_dark", **kwargs):
        colors = THEMES.get(theme, THEMES["copilot_dark"])
        super().__init__(parent, fg_color=colors["panel_bg"], corner_radius=12, **kwargs)
        
        self.theme = theme
        self.colors = colors
        self.animation_running = False
        
        # Create main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Title with futuristic styling
        title_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            title_frame,
            text="SYSTEM STATUS",
            font=("Consolas", 12, "bold"),
            text_color=colors["accent"]
        ).pack(anchor="w")
        
        # System metrics with enhanced styling
        self.create_system_metrics(main_container)
        
        # Environment section
        self.create_environment_section(main_container)
        
        # Start animations
        self.start_animations()
    
    def create_system_metrics(self, parent):
        """Create system metrics with futuristic progress bars."""
        metrics_frame = ctk.CTkFrame(parent, fg_color="transparent")
        metrics_frame.pack(fill="x", pady=(0, 15))
        
        # CPU Utilization
        cpu_frame = ctk.CTkFrame(metrics_frame, fg_color="transparent")
        cpu_frame.pack(fill="x", pady=3)
        
        ctk.CTkLabel(
            cpu_frame,
            text="CPU UTILIZATION",
            font=("Consolas", 9),
            text_color=self.colors["subfg"]
        ).pack(anchor="w")
        
        self.cpu_label = ctk.CTkLabel(
            cpu_frame,
            text="0%",
            font=("Consolas", 10, "bold"),
            text_color=self.colors["accent"]
        )
        self.cpu_label.pack(side="right")
        
        self.cpu_bar = ctk.CTkProgressBar(
            cpu_frame, 
            progress_color=self.colors["progress_fill"],
            fg_color=self.colors["progress_bg"],
            height=6
        )
        self.cpu_bar.pack(fill="x", pady=(2, 0))
        self.cpu_bar.set(0)
        
        # Memory Allocation
        mem_frame = ctk.CTkFrame(metrics_frame, fg_color="transparent")
        mem_frame.pack(fill="x", pady=3)
        
        ctk.CTkLabel(
            mem_frame,
            text="MEMORY ALLOCATION",
            font=("Consolas", 9),
            text_color=self.colors["subfg"]
        ).pack(anchor="w")
        
        self.memory_label = ctk.CTkLabel(
            mem_frame,
            text="0.0 / 0.0 GB",
            font=("Consolas", 10, "bold"),
            text_color=self.colors["accent"]
        )
        self.memory_label.pack(side="right")
        
        self.memory_bar = ctk.CTkProgressBar(
            mem_frame, 
            progress_color=self.colors["progress_fill"],
            fg_color=self.colors["progress_bg"],
            height=6
        )
        self.memory_bar.pack(fill="x", pady=(2, 0))
        self.memory_bar.set(0)
        
        # Storage Remaining
        storage_frame = ctk.CTkFrame(metrics_frame, fg_color="transparent")
        storage_frame.pack(fill="x", pady=3)
        
        ctk.CTkLabel(
            storage_frame,
            text="STORAGE REMAINING",
            font=("Consolas", 9),
            text_color=self.colors["subfg"]
        ).pack(anchor="w")
        
        self.storage_label = ctk.CTkLabel(
            storage_frame,
            text="0 / 0 GB",
            font=("Consolas", 10, "bold"),
            text_color=self.colors["accent"]
        )
        self.storage_label.pack(side="right")
        
        self.storage_bar = ctk.CTkProgressBar(
            storage_frame, 
            progress_color=self.colors["progress_fill"],
            fg_color=self.colors["progress_bg"],
            height=6
        )
        self.storage_bar.pack(fill="x", pady=(2, 0))
        self.storage_bar.set(0)
        
        # GPU Temperature
        gpu_frame = ctk.CTkFrame(metrics_frame, fg_color="transparent")
        gpu_frame.pack(fill="x", pady=3)
        
        ctk.CTkLabel(
            gpu_frame,
            text="GPU TEMPERATURE",
            font=("Consolas", 9),
            text_color=self.colors["subfg"]
        ).pack(anchor="w")
        
        self.gpu_label = ctk.CTkLabel(
            gpu_frame,
            text="0°C",
            font=("Consolas", 10, "bold"),
            text_color=self.colors["accent"]
        )
        self.gpu_label.pack(side="right")
        
        self.gpu_bar = ctk.CTkProgressBar(
            gpu_frame, 
            progress_color=self.colors["progress_fill"],
            fg_color=self.colors["progress_bg"],
            height=6
        )
        self.gpu_bar.pack(fill="x", pady=(2, 0))
        self.gpu_bar.set(0)
        
        # Battery
        battery_frame = ctk.CTkFrame(metrics_frame, fg_color="transparent")
        battery_frame.pack(fill="x", pady=3)
        
        ctk.CTkLabel(
            battery_frame,
            text="BATTERY",
            font=("Consolas", 9),
            text_color=self.colors["subfg"]
        ).pack(anchor="w")
        
        self.battery_label = ctk.CTkLabel(
            battery_frame,
            text="0%",
            font=("Consolas", 10, "bold"),
            text_color=self.colors["accent"]
        )
        self.battery_label.pack(side="right")
        
        self.battery_bar = ctk.CTkProgressBar(
            battery_frame, 
            progress_color=self.colors["progress_fill"],
            fg_color=self.colors["progress_bg"],
            height=6
        )
        self.battery_bar.pack(fill="x", pady=(2, 0))
        self.battery_bar.set(0)
    
    def create_environment_section(self, parent):
        """Create environment section with location and temperature."""
        env_frame = ctk.CTkFrame(parent, fg_color="transparent")
        env_frame.pack(fill="x")
        
        ctk.CTkLabel(
            env_frame,
            text="ENVIRONMENT",
            font=("Consolas", 9),
            text_color=self.colors["subfg"]
        ).pack(anchor="w")
        
        # Location and temperature
        env_info_frame = ctk.CTkFrame(env_frame, fg_color="transparent")
        env_info_frame.pack(fill="x", pady=(5, 0))
        
        self.location_label = ctk.CTkLabel(
            env_info_frame,
            text="NOIDA CITY",
            font=("Consolas", 10, "bold"),
            text_color=self.colors["accent"]
        )
        self.location_label.pack(side="left")
        
        self.temp_label = ctk.CTkLabel(
            env_info_frame,
            text="34°C",
            font=("Consolas", 10, "bold"),
            text_color=self.colors["accent"]
        )
        self.temp_label.pack(side="right")
    
    def start_animations(self):
        """Start the system monitoring animations."""
        self.animation_running = True
        self.update_system_info()
        self.update_time()
    
    def update_system_info(self):
        """Update system information with real-time data for futuristic panel."""
        if not self.animation_running:
            return
        
        try:
            # CPU usage (non-blocking)
            cpu_percent = psutil.cpu_percent(interval=None)
            if hasattr(self, 'cpu_label') and self.cpu_label:
                self.cpu_label.configure(text=f"{cpu_percent:.0f}%")
            if hasattr(self, 'cpu_bar') and self.cpu_bar:
                self.animate_progress_bar(self.cpu_bar, cpu_percent / 100)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_gb = memory.used / (1024**3)
            memory_total_gb = memory.total / (1024**3)
            if hasattr(self, 'memory_label') and self.memory_label:
                self.memory_label.configure(text=f"{memory_gb:.1f} / {memory_total_gb:.0f} GB")
            if hasattr(self, 'memory_bar') and self.memory_bar:
                self.animate_progress_bar(self.memory_bar, memory_percent / 100)
            
            # Storage usage
            try:
                disk = psutil.disk_usage('/')
                disk_used_gb = disk.used / (1024**3)
                disk_total_gb = disk.total / (1024**3)
                disk_percent = (disk.used / disk.total) * 100
                if hasattr(self, 'storage_label') and self.storage_label:
                    self.storage_label.configure(text=f"{disk_used_gb:.0f} / {disk_total_gb:.0f} GB")
                if hasattr(self, 'storage_bar') and self.storage_bar:
                    self.animate_progress_bar(self.storage_bar, disk_percent / 100)
            except:
                if hasattr(self, 'storage_label') and self.storage_label:
                    self.storage_label.configure(text="N/A")
                if hasattr(self, 'storage_bar') and self.storage_bar:
                    self.storage_bar.set(0)
            
            # GPU Temperature (simulated for now)
            try:
                gpu_temp = 60  # Default value
                if hasattr(self, 'gpu_label') and self.gpu_label:
                    self.gpu_label.configure(text=f"{gpu_temp}°C")
                if hasattr(self, 'gpu_bar') and self.gpu_bar:
                    self.animate_progress_bar(self.gpu_bar, gpu_temp / 100)
            except:
                if hasattr(self, 'gpu_label') and self.gpu_label:
                    self.gpu_label.configure(text="N/A")
                if hasattr(self, 'gpu_bar') and self.gpu_bar:
                    self.gpu_bar.set(0)
            
            # Battery status
            try:
                battery = psutil.sensors_battery()
                if battery and hasattr(self, 'battery_label') and self.battery_label:
                    battery_percent = battery.percent
                    self.battery_label.configure(text=f"{battery_percent:.0f}%")
                    if hasattr(self, 'battery_bar') and self.battery_bar:
                        self.animate_progress_bar(self.battery_bar, battery_percent / 100)
                else:
                    if hasattr(self, 'battery_label') and self.battery_label:
                        self.battery_label.configure(text="N/A")
                    if hasattr(self, 'battery_bar') and self.battery_bar:
                        self.battery_bar.set(0)
            except:
                if hasattr(self, 'battery_label') and self.battery_label:
                    self.battery_label.configure(text="N/A")
                if hasattr(self, 'battery_bar') and self.battery_bar:
                    self.battery_bar.set(0)
            
        except Exception as e:
            print(f"Error updating system info: {e}")
        
        # Schedule next update with longer interval to reduce CPU usage
        if self.animation_running:
            self.after(3000, self.update_system_info)
    
    def update_time(self):
        """Update time display with smooth transitions."""
        if not self.animation_running:
            return
            
        try:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            
            time_text = f"🕐 {current_time}\n📅 {current_date}"
            
            if hasattr(self, 'time_label') and self.time_label:
                self.time_label.configure(text=time_text)
        except Exception as e:
            print(f"Error updating time: {e}")
        
        # Schedule next update
        if self.animation_running:
            self.after(1000, self.update_time)
    
    def animate_progress_bar(self, bar, target_value):
        """Animate progress bar to target value smoothly."""
        current_value = bar.get()
        step = (target_value - current_value) * 0.3  # Smooth interpolation
        
        if abs(target_value - current_value) > 0.01:
            new_value = current_value + step
            bar.set(new_value)
            self.after(50, lambda: self.animate_progress_bar(bar, target_value))
        else:
            bar.set(target_value)
    
    def stop_animations(self):
        """Stop all animations."""
        self.animation_running = False

class EnhancedChatBubble(ctk.CTkFrame):
    """Modern AI chat bubble with Core System design."""
    
    def __init__(self, parent, message, sender="user", timestamp=None, **kwargs):
        # Try to get core_system theme, fallback to copilot_dark
        colors = THEMES.get("core_system", THEMES.get("copilot_dark", THEMES["copilot_dark"]))
        
        # Determine bubble styling based on sender
        if sender.lower() == "user":
            fg_color = colors["user_bubble"]  # Teal/cyan
            text_color = "#ffffff"
            anchor = "e"
            padx = (40, 8)  # Push to right
            sender_name = "YOU"
            sender_color = colors.get("progress_cyan", "#06b6d4")
        elif sender.lower() in ["assistant", "jarvis", "sam"]:
            fg_color = colors["assistant_bubble"]  # Dark slate
            text_color = colors["fg"]
            anchor = "w"
            padx = (8, 40)  # Push to left
            sender_name = "SAM"
            sender_color = colors["accent"]
        else:  # system
            fg_color = colors["system_bubble"]
            text_color = colors["subfg"]
            anchor = "center"
            padx = (20, 20)
            sender_name = "SYSTEM"
            sender_color = colors["subfg"]
        
        # Create container frame (for label + bubble)
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        # Sender label above bubble
        label_frame = ctk.CTkFrame(self, fg_color="transparent")
        label_frame.pack(fill="x", pady=(0, 2))
        
        sender_label = ctk.CTkLabel(
            label_frame,
            text=sender_name,
            font=("Consolas", 9, "bold"),
            text_color=sender_color
        )
        if anchor == "e":
            sender_label.pack(side="right", padx=4)
        elif anchor == "w":
            sender_label.pack(side="left", padx=4)
        else:
            sender_label.pack(anchor="center")
        
        # The actual bubble
        bubble = ctk.CTkFrame(
            self,
            fg_color=fg_color,
            corner_radius=12,
            border_width=1,
            border_color=colors.get("border_glow", colors["input_border"])
        )
        
        if anchor == "e":
            bubble.pack(fill="x", padx=padx, anchor="e")
        elif anchor == "w":
            bubble.pack(fill="x", padx=padx, anchor="w")
        else:
            bubble.pack(fill="x", padx=padx)
        
        # Message container
        msg_frame = ctk.CTkFrame(bubble, fg_color="transparent")
        msg_frame.pack(fill="both", expand=True, padx=12, pady=8)
        
        # Message text
        message_parts = self._parse_message(message, colors)
        
        for part in message_parts:
            if part["type"] == "code":
                code_frame = ctk.CTkFrame(
                    msg_frame, 
                    fg_color=colors["card"], 
                    corner_radius=8,
                    border_width=1,
                    border_color=colors["input_border"]
                )
                code_frame.pack(fill="x", pady=4)
                
                code_label = ctk.CTkLabel(
                    code_frame,
                    text=part["content"],
                    font=("Consolas", 10),
                    text_color=colors["accent"],
                    wraplength=250,
                    justify="left"
                )
                code_label.pack(padx=10, pady=6)
            else:
                text_label = ctk.CTkLabel(
                    msg_frame,
                    text=part["content"],
                    text_color=text_color,
                    font=("Segoe UI", 11),
                    wraplength=250,
                    justify="left"
                )
                text_label.pack(anchor="w" if anchor == "w" else "e", fill="x", pady=1)
        
        # Timestamp at bottom
        if timestamp:
            time_label = ctk.CTkLabel(
                msg_frame,
                text=timestamp,
                font=("Consolas", 8),
                text_color=colors["subfg"]
            )
            if anchor == "e":
                time_label.pack(anchor="e", pady=(4, 0))
            else:
                time_label.pack(anchor="w", pady=(4, 0))
        
        # Pack the whole bubble frame
        self.pack(fill="x", pady=4)
        
        # Store for animation
        self.bubble = bubble
        self.original_fg_color = fg_color
        self.animate_entrance()

    
    def _parse_message(self, message, colors):
        """Parse message for code blocks and special formatting."""
        parts = []
        
        # Simple code block detection (text between backticks)
        import re
        code_pattern = r'`([^`]+)`'
        
        last_end = 0
        for match in re.finditer(code_pattern, message):
            # Add text before code
            if match.start() > last_end:
                parts.append({
                    "type": "text",
                    "content": message[last_end:match.start()]
                })
            
            # Add code block
            parts.append({
                "type": "code",
                "content": match.group(1)
            })
            
            last_end = match.end()
        
        # Add remaining text
        if last_end < len(message):
            parts.append({
                "type": "text",
                "content": message[last_end:]
            })
        
        # If no code blocks found, return as single text part
        if not parts:
            parts.append({
                "type": "text",
                "content": message
            })
        
        return parts
    
    def animate_entrance(self):
        """Animate the bubble entrance."""
        if not hasattr(self, 'bubble'):
            return
        
        # Simple fade-in effect
        def fade_in(step=0):
            if step < 5 and hasattr(self, 'bubble'):
                try:
                    self.bubble.configure(fg_color=self.original_fg_color)
                except:
                    pass
        
        # Start animation
        self.after(50, lambda: fade_in(1))

class VoiceVisualizer(ctk.CTkFrame):
    """Voice activity visualizer with animated bars."""
    
    def __init__(self, parent, theme="copilot_dark", **kwargs):
        colors = THEMES.get(theme, THEMES["copilot_dark"])
        super().__init__(parent, fg_color=colors["card"], corner_radius=8, **kwargs)
        
        self.theme = theme
        self.colors = colors
        self.bars = []
        self.animation_running = False
        
        # Create canvas for visualization
        self.canvas = tk.Canvas(self, bg=colors["card"], highlightthickness=0, height=60)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create animated bars
        self.create_bars()
    
    def create_bars(self):
        """Create the voice visualization bars."""
        bar_width = 4
        bar_spacing = 6
        num_bars = 15
        
        for i in range(num_bars):
            x = 20 + i * (bar_width + bar_spacing)
            bar = self.canvas.create_rectangle(
                x, 50, x + bar_width, 50,
                fill=self.colors["accent"],
                outline=self.colors["accent"]
            )
            self.bars.append({"id": bar, "height": 0, "target": 0})
    
    def start_animation(self):
        """Start the voice visualization animation."""
        self.animation_running = True
        self.animate_bars()
    
    def stop_animation(self):
        """Stop the voice visualization animation."""
        self.animation_running = False
        # Reset all bars
        for bar in self.bars:
            self.canvas.coords(bar["id"], 
                             self.canvas.coords(bar["id"])[0], 50,
                             self.canvas.coords(bar["id"])[2], 50)


class PlannerStepPanel(ctk.CTkFrame):
    """Compact step-by-step execution panel shown above the chat area.
    Modular component that can be reused or replaced independently.

    Usage:
      panel = PlannerStepPanel(parent, theme="copilot_dark")
      panel.set_steps(["open youtube", "play music"])  # initializes rows
      panel.update_step(1, status="running")
      panel.update_step(1, status="success", message="YouTube opened", elapsed=0.8)
    """

    def __init__(self, parent, theme="copilot_dark", **kwargs):
        self.theme = theme
        self.colors = THEMES.get(theme, THEMES["copilot_dark"])
        super().__init__(parent, fg_color=self.colors["card"], corner_radius=10, **kwargs)
        self.rows = []
        self.header = ctk.CTkLabel(
            self, text="Planner", font=("Segoe UI", 12, "bold"), text_color=self.colors["accent"]
        )
        self.header.pack(anchor="w", padx=12, pady=(10, 6))
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="x", padx=10, pady=(0, 10))
        self.pack_forget()  # hidden by default

    def set_steps(self, steps):
        # Clear previous rows
        for r in self.rows:
            try:
                r["frame"].destroy()
            except Exception:
                pass
        self.rows = []
        # Build rows
        for i, step in enumerate(steps, 1):
            row = ctk.CTkFrame(self.container, fg_color="transparent")
            row.pack(fill="x", pady=4)
            icon = ctk.CTkLabel(row, text="⏳", font=("Segoe UI", 12))
            icon.pack(side="left", padx=(2, 8))
            title = ctk.CTkLabel(row, text=f"Step {i}: {step}", font=("Segoe UI", 11), text_color=self.colors["fg"]) 
            title.pack(side="left")
            status = ctk.CTkLabel(row, text="pending", font=("Segoe UI", 10), text_color=self.colors["subfg"]) 
            status.pack(side="right")
            self.rows.append({"frame": row, "icon": icon, "title": title, "status": status})
        # Show panel
        self.pack(fill="x", padx=20, pady=(6, 0))

    def update_step(self, index, status, message=None, elapsed=None):
        # index is 1-based
        if not (1 <= index <= len(self.rows)):
            return
        row = self.rows[index - 1]
        colors = self.colors
        # Map status to icon and color
        mapping = {
            "pending": ("⏳", colors["subfg"]),
            "running": ("▶️", colors["accent"]),
            "success": ("✅", colors["success"]),
            "error": ("❌", colors["error"]),
        }
        icon_text, status_color = mapping.get(status, ("⏳", colors["subfg"]))
        try:
            row["icon"].configure(text=icon_text, text_color=status_color)
            status_text = status
            if elapsed is not None:
                status_text += f" · {elapsed:.2f}s"
            row["status"].configure(text=status_text, text_color=status_color)
            if message:
                # Append a small subtext line for details
                details = ctk.CTkLabel(row["frame"], text=f"{message}", font=("Segoe UI", 10), text_color=colors["subfg"]) 
                details.pack(fill="x", padx=(28, 0))
        except Exception:
            pass

    def hide(self):
        try:
            self.pack_forget()
        except Exception:
            pass


class ToastManager:
    """Lightweight toast notifications manager.
    Creates small temporary windows in the bottom-right corner of the screen.
    Modular and replaceable without touching core assistant logic.
    """

    def __init__(self, root, theme="copilot_dark"):
        self.root = root
        self.theme = theme
        self.colors = THEMES.get(theme, THEMES["copilot_dark"])
        self.toasts = []

    def show(self, text, kind="info", duration_ms=2200):
        # Compute stacking position relative to root window
        try:
            x = self.root.winfo_rootx() + self.root.winfo_width() - 320
            y = self.root.winfo_rooty() + self.root.winfo_height() - 80 - (len(self.toasts) * 70)
        except Exception:
            x, y = 100, 100
        win = ctk.CTkToplevel(self.root)
        win.overrideredirect(True)
        win.geometry(f"300x60+{int(x)}+{int(y)}")
        win.configure(fg_color=self.colors["card"])

        # Icon/color based on kind
        icon_map = {
            "info": ("ℹ️", self.colors["accent"]),
            "success": ("✅", self.colors["success"]),
            "warning": ("⚠️", self.colors["warning"]),
            "error": ("❌", self.colors["error"]),
        }
        icon_text, icon_color = icon_map.get(kind, ("ℹ️", self.colors["accent"]))

        ctk.CTkLabel(win, text=icon_text, font=("Segoe UI", 14), text_color=icon_color).pack(side="left", padx=(10, 8), pady=10)
        ctk.CTkLabel(win, text=text, wraplength=240, font=("Segoe UI", 11), text_color=self.colors["fg"]).pack(side="left", padx=(0, 10), pady=10)

        self.toasts.append(win)

        def _close():
            try:
                if win in self.toasts:
                    self.toasts.remove(win)
                win.destroy()
            except Exception:
                pass

        win.after(duration_ms, _close)
    
    def animate_bars(self):
        """Animate the voice visualization bars."""
        if not self.animation_running:
            return
        
        import random
        
        for bar in self.bars:
            # Randomly update target heights
            if random.random() < 0.3:
                bar["target"] = random.randint(5, 50)
            
            # Smoothly animate to target
            current_height = bar["height"]
            target_height = bar["target"]
            
            if abs(current_height - target_height) > 1:
                bar["height"] += (target_height - current_height) * 0.3
            else:
                bar["height"] = target_height
            
            # Update bar position
            coords = self.canvas.coords(bar["id"])
            self.canvas.coords(bar["id"], 
                             coords[0], 50 - bar["height"],
                             coords[2], 50)
        
        self.after(50, self.animate_bars)

class EnhancedTypingIndicator(ctk.CTkFrame):
    """Enhanced typing indicator with smooth animations."""
    
    def __init__(self, parent, **kwargs):
        colors = THEMES.get("copilot_dark", THEMES["copilot_dark"])
        super().__init__(parent, fg_color=colors["assistant_bubble"], corner_radius=16, **kwargs)
        
        self.dots = []
        self.animation_running = False
        
        # Create dots with modern styling
        for i in range(3):
            dot = ctk.CTkLabel(
                self, 
                text="●", 
                text_color=colors["typing_indicator"],
                font=("Segoe UI", 18)
            )
            dot.pack(side="left", padx=4)
            self.dots.append({"widget": dot, "phase": i * 0.3})
        
        self.pack(fill="x", padx=(20, 100), pady=6)
        self.start_animation()
    
    def start_animation(self):
        """Start the typing indicator animation."""
        self.animation_running = True
        self.animate()
    
    def stop_animation(self):
        """Stop the typing indicator animation."""
        self.animation_running = False
    
    def animate(self):
        """Animate the typing indicator dots."""
        if not self.animation_running:
            return
        
        import math
        
        for i, dot in enumerate(self.dots):
            # Create wave effect
            phase = dot["phase"]
            intensity = (math.sin(phase) + 1) / 2  # 0 to 1
            
            # Interpolate between colors
            colors = THEMES.get("copilot_dark", THEMES["copilot_dark"])
            base_color = colors["typing_indicator"]
            bright_color = "#ffffff"
            
            # Calculate current color
            r1, g1, b1 = int(base_color[1:3], 16), int(base_color[3:5], 16), int(base_color[5:7], 16)
            r2, g2, b2 = int(bright_color[1:3], 16), int(bright_color[3:5], 16), int(bright_color[5:7], 16)
            
            r = int(r1 + (r2 - r1) * intensity)
            g = int(g1 + (g2 - g1) * intensity)
            b = int(b1 + (b2 - b1) * intensity)
            
            current_color = f"#{r:02x}{g:02x}{b:02x}"
            dot["widget"].configure(text_color=current_color)
            
            # Update phase
            dot["phase"] += 0.2
        
        self.after(100, self.animate)

class ModernButton(ctk.CTkButton):
    """Enhanced modern button with hover effects and animations."""
    
    def __init__(self, parent, text, command, theme="copilot_dark", icon=None, **kwargs):
        # Get theme colors
        colors = THEMES.get(theme, THEMES["copilot_dark"])
        
        # Set default styling
        default_kwargs = {
            'fg_color': colors["accent"],
            'hover_color': colors["hover"],
            'text_color': "#ffffff",
            'font': ("Segoe UI", 12, "bold"),
            'corner_radius': 10,
            'height': 40,
            'border_width': 2,
            'border_color': colors["accent"]
        }
        
        # Add icon if provided
        if icon:
            text = f"{icon} {text}"
        
        # Update with any provided kwargs
        default_kwargs.update(kwargs)
        
        super().__init__(parent, text=text, command=command, **default_kwargs)
        self.theme = theme
        self.original_fg_color = default_kwargs['fg_color']
        
        # Bind hover events for enhanced effects
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event):
        """Enhanced hover effect."""
        colors = THEMES.get(self.theme, THEMES["copilot_dark"])
        self.configure(border_color=colors["glow"])
    
    def on_leave(self, event):
        """Reset hover effect."""
        self.configure(border_color=self.original_fg_color)
    
    def update_theme(self, new_theme):
        """Update button theme colors."""
        self.theme = new_theme
        colors = THEMES.get(new_theme, THEMES["copilot_dark"])
        
        self.configure(
            fg_color=colors["accent"],
            hover_color=colors["hover"],
            text_color="#ffffff",
            border_color=colors["accent"]
        )
        self.original_fg_color = colors["accent"]


class CoreSystemOrb(ctk.CTkFrame):
    """Animated particle orb visualization for Core System UI with realistic AI speaking animation."""
    
    def __init__(self, parent, theme="core_system", size=300, **kwargs):
        colors = THEMES.get(theme, THEMES["core_system"])
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.theme = theme
        self.colors = colors
        self.size = size
        self.particles = []
        self.animation_running = False
        self.voice_active = False
        self.pulse_phase = 0
        self.global_time = 0
        self.intensity = 0.0  # Smooth transition for voice activation
        
        # Create canvas for particle rendering
        self.canvas = tk.Canvas(
            self,
            width=size,
            height=size,
            bg=colors["bg"],
            highlightthickness=0
        )
        self.canvas.pack(expand=True)
        
        # Initialize particles
        self.create_particles()
        
    def create_particles(self):
        """Create particle system for the orb."""
        import random
        
        center_x = self.size // 2
        center_y = self.size // 2
        radius = self.size // 2 - 20
        
        # Create multiple layers of particles
        num_particles = 500  # More particles for denser effect
        
        for i in range(num_particles):
            # Random position within sphere
            angle = random.uniform(0, 2 * math.pi)
            r = random.uniform(0, radius) * random.uniform(0.3, 1.0)  # Denser in center
            
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            
            # Particle properties
            particle_size = random.uniform(1, 4)
            speed = random.uniform(0.3, 1.2)
            phase = random.uniform(0, 2 * math.pi)
            orbit_speed = random.uniform(0.01, 0.03)  # For orbital movement
            
            # Color variation (golden/amber tones with more variety)
            colors_list = ["#d4a574", "#e8b886", "#fbbf24", "#f59e0b", "#c8956c", "#fcd34d", "#f97316"]
            color = random.choice(colors_list)
            
            # Distance from center for scaling effects
            dist_from_center = r / radius
            
            particle = {
                "x": x,
                "y": y,
                "base_x": x,
                "base_y": y,
                "original_x": x,
                "original_y": y,
                "size": particle_size,
                "base_size": particle_size,
                "speed": speed,
                "phase": phase,
                "orbit_speed": orbit_speed,
                "color": color,
                "dist_from_center": dist_from_center,
                "layer": random.choice(["inner", "middle", "outer"]),
                "id": None
            }
            
            # Draw particle
            particle["id"] = self.canvas.create_oval(
                x - particle_size, y - particle_size,
                x + particle_size, y + particle_size,
                fill=color,
                outline=""
            )
            
            self.particles.append(particle)
    
    def start_animation(self):
        """Start the particle animation."""
        self.animation_running = True
        self.animate()
    
    def stop_animation(self):
        """Stop the particle animation."""
        self.animation_running = False
    
    def set_voice_active(self, active):
        """Set voice activity state for enhanced animation."""
        self.voice_active = active
    
    def animate(self):
        """Animate particles with realistic AI speaking effect."""
        if not self.animation_running:
            return
        
        import random
        
        # Update global time
        self.global_time += 0.05
        self.pulse_phase += 0.15 if self.voice_active else 0.03
        
        # Smooth intensity transition
        target_intensity = 1.0 if self.voice_active else 0.0
        self.intensity += (target_intensity - self.intensity) * 0.1
        
        center_x = self.size // 2
        center_y = self.size // 2
        
        # Pulsate scale when speaking (breathing effect)
        pulse_scale = 1.0 + (math.sin(self.pulse_phase) * 0.15 * self.intensity)
        secondary_pulse = 1.0 + (math.sin(self.pulse_phase * 1.7) * 0.08 * self.intensity)
        
        for particle in self.particles:
            # Update phase
            speed_multiplier = 1.0 + (self.intensity * 2.0)  # Faster when speaking
            particle["phase"] += particle["speed"] * 0.1 * speed_multiplier
            
            # Calculate base position relative to center
            dx = particle["original_x"] - center_x
            dy = particle["original_y"] - center_y
            
            # Apply pulsating scale
            layer_pulse = pulse_scale if particle["layer"] != "inner" else secondary_pulse
            scaled_dx = dx * layer_pulse
            scaled_dy = dy * layer_pulse
            
            # Orbital rotation when speaking
            if self.intensity > 0.1:
                orbit_angle = self.global_time * particle["orbit_speed"] * 20 * self.intensity
                cos_a = math.cos(orbit_angle)
                sin_a = math.sin(orbit_angle)
                rotated_dx = scaled_dx * cos_a - scaled_dy * sin_a
                rotated_dy = scaled_dx * sin_a + scaled_dy * cos_a
                scaled_dx = rotated_dx
                scaled_dy = rotated_dy
            
            # Wave movement (more dynamic when speaking)
            wave_amplitude = 2.0 + (8.0 * self.intensity)
            wave_freq = 1.0 + (0.5 * self.intensity)
            offset_x = math.sin(particle["phase"] * wave_freq) * wave_amplitude
            offset_y = math.cos(particle["phase"] * 0.7 * wave_freq) * wave_amplitude
            
            # Spiral effect when speaking
            if self.intensity > 0.1:
                spiral = math.sin(self.global_time * 3 + particle["dist_from_center"] * 10)
                offset_x += spiral * 3 * self.intensity
                offset_y += math.cos(self.global_time * 2.5 + particle["phase"]) * 3 * self.intensity
            
            new_x = center_x + scaled_dx + offset_x
            new_y = center_y + scaled_dy + offset_y
            
            # Dynamic particle size when speaking
            size_pulse = 1.0 + (math.sin(self.pulse_phase * 2 + particle["phase"]) * 0.4 * self.intensity)
            size = particle["base_size"] * size_pulse
            
            # Update particle position
            try:
                self.canvas.coords(
                    particle["id"],
                    new_x - size, new_y - size,
                    new_x + size, new_y + size
                )
            except Exception:
                pass
            
            # Dynamic color changes when speaking
            if self.intensity > 0.3:
                if random.random() < 0.15 * self.intensity:
                    # Bright flashing colors when speaking
                    bright_colors = ["#fbbf24", "#fcd34d", "#fef3c7", "#fff7ed", "#ffedd5", "#fed7aa"]
                    try:
                        self.canvas.itemconfig(particle["id"], fill=random.choice(bright_colors))
                    except Exception:
                        pass
            elif random.random() < 0.03:
                # Occasionally restore original color
                try:
                    self.canvas.itemconfig(particle["id"], fill=particle["color"])
                except Exception:
                    pass
        
        # Schedule next frame (faster when speaking)
        frame_delay = 25 if self.voice_active else 40
        self.after(frame_delay, self.animate)


class NaturalLanguageNavigator:

    """Modular natural language system navigator.
    Interprets high-level navigation requests and executes OS-level actions.
    """

    def __init__(self, assistant):
        self.assistant = assistant
        self.os_name = platform.system().lower()

    def _open_path(self, path):
        try:
            if self.os_name.startswith('win'):
                try:
                    os.startfile(path)
                except Exception:
                    subprocess.Popen(['explorer', path])
            elif self.os_name == 'darwin':
                subprocess.Popen(['open', path])
            else:
                subprocess.Popen(['xdg-open', path])
            return f"📂 Opening {path}"
        except Exception as e:
            return f"❌ Unable to open {path}: {e}"

    def _open_settings(self, section=None):
        try:
            if self.os_name.startswith('win'):
                uri_map = {
                    None: 'ms-settings:',
                    'display': 'ms-settings:display',
                    'sound': 'ms-settings:sound',
                    'wifi': 'ms-settings:network-wifi',
                    'bluetooth': 'ms-settings:bluetooth',
                    'network': 'ms-settings:network',
                    'battery': 'ms-settings:battery',
                    'storage': 'ms-settings:storagesense',
                }
                uri = uri_map.get(section, 'ms-settings:')
                try:
                    os.startfile(uri)
                except Exception:
                    os.system(f"start {uri}")
                return f"⚙️ Opening Settings{(' → ' + section) if section else ''}"
            elif self.os_name == 'darwin':
                # macOS: Use URL schemes for instant deep links when available
                pane_map = {
                    'display': 'x-apple.systempreferences:com.apple.preference.displays',
                    'sound': 'x-apple.systempreferences:com.apple.preference.sound',
                    'wifi': 'x-apple.systempreferences:com.apple.preference.network',
                    'bluetooth': 'x-apple.systempreferences:com.apple.preference.bluetooth',
                    'network': 'x-apple.systempreferences:com.apple.preference.network',
                    'battery': 'x-apple.systempreferences:com.apple.preference.battery',
                    'keyboard': 'x-apple.systempreferences:com.apple.preference.keyboard',
                    'trackpad': 'x-apple.systempreferences:com.apple.preference.trackpad',
                    'mouse': 'x-apple.systempreferences:com.apple.preference.mouse',
                    'privacy': 'x-apple.systempreferences:com.apple.preference.security',
                }
                try:
                    if section and section in pane_map:
                        subprocess.run(['open', pane_map[section]], check=False)
                    else:
                        subprocess.run(['open', '-a', 'System Settings'], check=False)
                    # Bring to foreground quickly
                    subprocess.run(['osascript', '-e', 'tell application "System Settings" to activate'], check=False)
                except Exception:
                    subprocess.Popen(['open', '/System/Applications/System Settings.app'])
                return f"⚙️ Opening System Settings{(' → ' + section) if section else ''}"
            else:
                # Linux: try gnome-control-center
                subprocess.Popen(['gnome-control-center'])
                return "⚙️ Opening System Settings"
        except Exception as e:
            return f"❌ Unable to open Settings: {e}"

    def _known_folder_path(self, name):
        home = os.path.expanduser('~')
        mapping = {
            'downloads': os.path.join(home, 'Downloads'),
            'documents': os.path.join(home, 'Documents'),
            'pictures': os.path.join(home, 'Pictures'),
            'photos': os.path.join(home, 'Pictures'),
            'music': os.path.join(home, 'Music'),
            'videos': os.path.join(home, 'Videos'),
            'desktop': os.path.join(home, 'Desktop'),
        }
        return mapping.get(name)

    def _press(self, *keys):
        try:
            pyautogui.hotkey(*keys)
            return True
        except Exception:
            return False

    def handle(self, text):
        """Parse text and execute navigation actions. Returns a status string."""
        cmd = text.lower().strip()

        m = re.search(r"\bopen\s+(?:the\s+)?(file|document)\s+(.+)\b", cmd)
        if m:
            name = m.group(2).strip()
            try:
                return self.assistant.open_file_human_like(name, kind='file')
            except Exception as e:
                return f"❌ Unable to open file '{name}': {e}"

        m = re.search(r"\bfind\s+(.+?)\s+and\s+open\b", cmd)
        if m:
            name = m.group(1).strip()
            try:
                return self.assistant.open_file_human_like(name, kind='file')
            except Exception as e:
                return f"❌ Unable to open file '{name}': {e}"

        m = re.search(r"\bopen\s+(.+)\b", cmd)
        if m:
            raw = m.group(1).strip()
            if any(ext for ext in [".", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".png", ".jpg", ".jpeg", ".gif", ".txt"] if ext in raw):
                try:
                    return self.assistant.open_file_human_like(raw, kind='file')
                except Exception as e:
                    return f"❌ Unable to open '{raw}': {e}"

        m = re.search(r"\bopen\s+folder\s+(.+)\b", cmd)
        if m:
            name = m.group(1).strip()
            try:
                return self.assistant.open_file_human_like(name, kind='folder')
            except Exception as e:
                return f"❌ Unable to open folder '{name}': {e}"

        # Open known folders: "go to downloads", "open documents"
        m = re.search(r"\b(go to|open|show)\s+(downloads|documents|pictures|photos|music|videos|desktop)\b", cmd)
        if m:
            folder = m.group(2)
            path = self._known_folder_path(folder)
            if path and os.path.exists(path):
                return self._open_path(path)
            else:
                return f"❌ I couldn't find your {folder} folder."

        # Show desktop / minimize all
        if re.search(r"\b(show\s+desktop|minimize\s+all\s+windows)\b", cmd):
            ok = self._press('win', 'd') if self.os_name.startswith('win') else self._press('command', 'f3')
            return "🖥️ Showing desktop" if ok else "❌ Couldn't show desktop via shortcut"

        # Switch windows: next/previous
        m = re.search(r"\b(switch|cycle)\s+(window|app)(?:\s+(next|previous))?\b", cmd)
        if m:
            direction = m.group(3) or 'next'
            if self.os_name.startswith('win'):
                if direction == 'previous':
                    pyautogui.keyDown('alt'); pyautogui.press('tab'); pyautogui.keyUp('alt')
                else:
                    pyautogui.keyDown('alt'); pyautogui.press('tab'); pyautogui.keyUp('alt')
            else:
                self._press('alt', 'tab')
            return f"🪟 Switching {direction} window"

        # Maximize / minimize current window
        m = re.search(r"\b(maximize|minimize|restore)\s+(this\s+)?window\b", cmd)
        if m:
            action = m.group(1)
            if self.os_name.startswith('win'):
                if action == 'maximize':
                    ok = self._press('win', 'up')
                elif action == 'minimize':
                    ok = self._press('win', 'down')
                else:
                    ok = self._press('win', 'down')
            else:
                ok = self._press('command', 'm') if action == 'minimize' else self._press('command', 'ctrl', 'f')
            return f"🪟 {action.title()} window" if ok else f"❌ Couldn't {action} window"

        # Close current window/app
        if re.search(r"\b(close\s+(this\s+)?(window|app|tab))\b", cmd):
            if self.os_name.startswith('win'):
                ok = self._press('alt', 'f4')
            elif 'tab' in cmd:
                ok = self._press('command', 'w')
            else:
                ok = self._press('command', 'q')
            return "❌ Couldn't close" if not ok else "✅ Closed"

        # Navigate back/forward
        if re.search(r"\b(go\s+back|previous\s+page)\b", cmd):
            ok = self._press('alt', 'left') if self.os_name.startswith('win') else self._press('command', 'left')
            return "⬅️ Going back" if ok else "❌ Couldn't go back"
        if re.search(r"\b(go\s+forward|next\s+page)\b", cmd):
            ok = self._press('alt', 'right') if self.os_name.startswith('win') else self._press('command', 'right')
            return "➡️ Going forward" if ok else "❌ Couldn't go forward"

        # Scroll up/down
        m = re.search(r"\bscroll\s+(up|down)(?:\s+by\s+(\d+))?\b", cmd)
        if m:
            direction = m.group(1)
            amount = int(m.group(2)) if m.group(2) else 1000
            try:
                pyautogui.scroll(amount if direction == 'up' else -amount)
                return f"🖱️ Scrolling {direction}"
            except Exception as e:
                return f"❌ Couldn't scroll: {e}"

        # Open settings sections
        m = re.search(r"\b(open|show)\s+(settings|system\s+settings)(?:\s+(for|about)\s+(display|sound|wifi|bluetooth|network|battery|storage))?\b", cmd)
        if m:
            section = m.group(4) if m.group(4) else None
            return self._open_settings(section)

        # Open application or website (delegate to existing logic)
        if re.search(r"\bopen\s+.+", cmd):
            try:
                return self.assistant.intelligent_open_command(cmd)
            except Exception:
                return self.assistant.handle_file_operations(cmd)

        # If we reach here, try AI-backed intent interpretation
        try:
            intent = self._interpret_with_ai(cmd)
            if intent and isinstance(intent, dict):
                action = intent.get('action')
                target = intent.get('target')
                if action == 'open_folder' and target:
                    path = self._known_folder_path(target)
                    if path and os.path.exists(path):
                        return self._open_path(path)
                if action == 'open_settings':
                    return self._open_settings(target)
                if action == 'switch_window':
                    pyautogui.keyDown('alt'); pyautogui.press('tab'); pyautogui.keyUp('alt')
                    return "🪟 Switching window"
                if action == 'show_desktop':
                    self._press('win','d')
                    return "🖥️ Showing desktop"
                if action == 'open_app' and target:
                    return self.assistant.intelligent_open_command(f"open {target}")
        except Exception as e:
            if hasattr(self.assistant, 'logger'):
                self.assistant.logger.debug(f"AI intent parse failed: {e}")

        return "🧭 I can help you navigate your system. Try: 'show desktop', 'go to downloads', 'switch window', 'open settings for wifi', or 'scroll down'."

    def _interpret_with_ai(self, text):
        """Use the assistant's AI to extract intent in a structured way."""
        if not hasattr(self.assistant, 'mistral_chat'):
            return None
        prompt = (
            "You are a command interpreter. Extract a simple intent from the user's request for system navigation. "
            "Respond ONLY in JSON with keys: action, target. Examples: "
            "'go to downloads' -> {\"action\": \"open_folder\", \"target\": \"downloads\"}. "
            "'open settings for wifi' -> {\"action\": \"open_settings\", \"target\": \"wifi\"}. "
            "'show desktop' -> {\"action\": \"show_desktop\"}. "
            f"User: {text}"
        )
        raw = self.assistant.mistral_chat(prompt)
        try:
            # Try to find JSON in response
            m = re.search(r"\{[\s\S]*\}", raw)
            if m:
                return json.loads(m.group(0))
        except Exception:
            return None
        return None


class MultiIntentPlanner:
    """Parse and execute compound natural language commands in sequence.
    Splits text into steps, categorizes each, and routes to existing handlers.
    Falls back to AI planning when needed.
    """

    def __init__(self, assistant):
        self.assistant = assistant

    def _split_into_steps(self, text):
        # Split on common connectors: and, then, after that, next, commas, plus tolerant 'an'
        parts = re.split(r"\s*(?:,|\band\b|\ban\b|\bthen\b|\bafter that\b|\bnext\b)\s*", text, flags=re.IGNORECASE)
        # Filter out empty fragments
        return [p.strip() for p in parts if p and p.strip()]

    def _normalize_segment(self, segment):
        seg = segment.strip().lower()
        # Heuristics for media playback
        if re.search(r"\bplay\s+(a\s+)?song\b", seg) and 'youtube' not in seg and 'music' not in seg:
            return 'play music'
        # Normalize common YouTube play phrasings
        m = re.search(r"^play\s+(.+?)\s+(?:song\s+)?(?:on|in|from)\s+youtube$", seg)
        if m:
            return f"play {m.group(1)} on youtube"
        # Normalize 'play <q> youtube'
        m = re.search(r"^play\s+(.+?)\s+youtube$", seg)
        if m:
            return f"play {m.group(1)} on youtube"
        
        # Normalize 'open youtube/yt and/an play <q>' → single play command
        # This prevents opening homepage first which wastes time and focus
        m = re.search(r"^open\s+(?:youtube|yt)\s+(?:and|an)\s+play\s+(.+)$", seg)
        if m:
            return f"play {m.group(1)} on youtube"
            
        # Normalize 'search about X' -> 'search X'
        m = re.search(r"^search\s+about\s+(.+)$", seg)
        if m:
            return f"search {m.group(1)}"
        return segment

    def _execute_segment(self, segment):
        try:
            seg = self._normalize_segment(segment)
            category = self.assistant._categorize_command(seg)
            if category == 'navigation':
                return self.assistant._handle_navigation_command(seg)
            elif category == 'search':
                return self.assistant._handle_search_command(seg)
            elif category == 'media':
                return self.assistant._handle_media_command(seg)
            elif category == 'file':
                return self.assistant._handle_file_command(seg)
            elif category == 'system':
                return self.assistant._handle_system_command(seg)
            else:
                # Default to AI for complex or unknown segments
                try:
                    return self.assistant.mistral_chat(seg)
                except Exception:
                    return self.assistant._get_fallback_response(seg)
        except Exception as e:
            return f"❌ Error executing step '{segment}': {e}"

    def execute(self, text):
        # Pre-process: consolidate "open youtube/yt and play" into a single play command
        # This prevents splitting into [open youtube, play X]
        consolidated = re.sub(
            r"\bopen\s+(?:youtube|yt)\s+(?:and|an)\s+play\b", 
            "play", 
            text, 
            flags=re.IGNORECASE
        )
        # Also handle "open spotify/music and play" -> "play"
        consolidated = re.sub(
            r"\bopen\s+(?:spotify|music)\s+(?:and|an)\s+play\b", 
            "play", 
            consolidated, 
            flags=re.IGNORECASE
        )
        
        steps = self._split_into_steps(consolidated)
        if not steps:
            # Try AI planning if we couldn't split
            steps = self._interpret_with_ai(text)
        if not steps:
            return "🤖 I couldn't understand the sequence. Please try simpler steps, e.g., 'open youtube and play music and open google and search cats'."

        # Visualize steps if supported
        try:
            if getattr(self.assistant, 'planner_enabled', True) and hasattr(self.assistant, 'start_planner_visual'):
                self.assistant.start_planner_visual(steps)
        except Exception:
            pass

        # Stream step-by-step execution
        results = []
        for i, step in enumerate(steps, 1):
            msg = f"▶️ Step {i}: {step}"
            try:
                self.assistant.add_to_chat("SAM", msg, "system")
            except Exception:
                pass
            # Notify start
            start_ts = time.time()
            try:
                if hasattr(self.assistant, 'notify_step_start'):
                    self.assistant.notify_step_start(i, step)
            except Exception:
                pass

            result = self._execute_segment(step)
            elapsed = time.time() - start_ts
            # Determine success
            success = True
            try:
                if isinstance(result, str) and (result.startswith("❌") or "❌" in result.lower()):
                    success = False
            except Exception:
                success = True
            results.append(f"Step {i}: {result}")
            try:
                self.assistant.add_to_chat("SAM", result, "jarvis")
            except Exception:
                pass
            # Notify finish
            try:
                if hasattr(self.assistant, 'notify_step_finish'):
                    self.assistant.notify_step_finish(i, step, success=success, message=result, elapsed=elapsed)
            except Exception:
                pass

        summary = "\n".join(results)
        # End visualization
        try:
            if hasattr(self.assistant, 'end_planner_visual'):
                self.assistant.end_planner_visual()
        except Exception:
            pass
        return f"✅ Completed {len(steps)} step(s).\n{summary}"

    def _interpret_with_ai(self, text):
        if not hasattr(self.assistant, 'mistral_chat'):
            return None
        prompt = (
            "You are a planner. Break the user's request into a minimal list of executable steps. "
            "Return ONLY JSON: {\"steps\": [\"...\", \"...\"]}. Example: "
            "'open youtube and play a song and open google and search about cats' -> "
            "{\"steps\": [\"open youtube\", \"play music\", \"open google\", \"search cats\"]}. "
            f"User: {text}"
        )
        raw = self.assistant.mistral_chat(prompt)
        try:
            m = re.search(r"\{[\s\S]*\}", raw)
            if m:
                data = json.loads(m.group(0))
                steps = data.get('steps')
                if isinstance(steps, list):
                    return steps
        except Exception:
            return None
        return None


class SystemNavigationService:
    def __init__(self):
        self.bundle_cache = {
            'safari': 'com.apple.Safari',
            'chrome': 'com.google.Chrome',
            'terminal': 'com.apple.Terminal',
            'finder': 'com.apple.finder',
            'notes': 'com.apple.Notes',
            'system settings': 'com.apple.systempreferences',
        }
        self.pane_map = {
            'display': 'x-apple.systempreferences:com.apple.preference.displays',
            'sound': 'x-apple.systempreferences:com.apple.preference.sound',
            'wifi': 'x-apple.systempreferences:com.apple.preference.network',
            'network': 'x-apple.systempreferences:com.apple.preference.network',
            'bluetooth': 'x-apple.systempreferences:com.apple.preference.bluetooth',
            'battery': 'x-apple.systempreferences:com.apple.preference.battery',
            'keyboard': 'x-apple.systempreferences:com.apple.preference.keyboard',
            'trackpad': 'x-apple.systempreferences:com.apple.preference.trackpad',
            'mouse': 'x-apple.systempreferences:com.apple.preference.mouse',
            'privacy': 'x-apple.systempreferences:com.apple.preference.security',
        }

    def open_settings(self, section=None):
        try:
            if section and section in self.pane_map:
                subprocess.run(['open', self.pane_map[section]], check=False)
            else:
                subprocess.run(['open', '-a', 'System Settings'], check=False)
            subprocess.run(['osascript', '-e', 'tell application "System Settings" to activate'], check=False)
            return f"⚙️ Opening System Settings{(' → ' + section) if section else ''}"
        except Exception as e:
            try:
                subprocess.Popen(['open', '/System/Applications/System Settings.app'])
                return "⚙️ Opening System Settings"
            except Exception:
                return f"❌ Failed to open System Settings: {e}"

    def open_app(self, app_name):
        try:
            key = app_name.strip().lower()
            bid = self.bundle_cache.get(key)
            if bid:
                subprocess.run(['open', '-b', bid], check=False)
            else:
                subprocess.run(['open', '-a', app_name], check=False)
            subprocess.run(['osascript', '-e', f'tell application "{app_name}" to activate'], check=False)
            return f"🚀 Opening {app_name}"
        except Exception as e:
            return f"❌ Failed to open {app_name}: {e}"

    def open_folder(self, name):
        try:
            n = name.strip()
            home = os.path.expanduser('~')
            known = {
                'downloads': os.path.join(home, 'Downloads'),
                'documents': os.path.join(home, 'Documents'),
                'desktop': os.path.join(home, 'Desktop'),
                'pictures': os.path.join(home, 'Pictures'),
                'music': os.path.join(home, 'Music'),
                'videos': os.path.join(home, 'Videos'),
            }
            path = known.get(n.lower())
            if not path:
                path = os.path.expanduser(n)
            if os.path.isdir(path):
                subprocess.run(['open', path], check=False)
                return f"📁 Opening '{os.path.basename(path)}'"
            return f"❌ Folder not found: {name}"
        except Exception as e:
            return f"❌ Failed to open folder '{name}': {e}"

class MemoryManager:
    def __init__(self, app):
        self.app = app
        self.data = {
            'identity': {'name': None, 'timezone': None, 'locale': None},
            'preferences': {'theme': None, 'language': None, 'voice': None, 'fast_mode': True, 'wakeword': None},
            'favorites': {'apps': [], 'folders': [], 'websites': []},
            'recents': {'commands': [], 'files': [], 'apps': []},
            'facts': []
        }

    def load(self, memory):
        if isinstance(memory, dict):
            for k in self.data:
                if k in memory and isinstance(memory[k], type(self.data[k])):
                    self.data[k] = memory[k]

    def save(self):
        return self.data

    def get_name(self):
        return self.data.get('identity', {}).get('name')

    def set_name(self, name):
        self.data.setdefault('identity', {})['name'] = name

    def set_pref(self, key, value):
        self.data.setdefault('preferences', {})[key] = value

    def get_pref(self, key):
        return self.data.get('preferences', {}).get(key)

    def add_recent_command(self, text):
        rec = self.data.setdefault('recents', {}).setdefault('commands', [])
        rec.append({'text': text, 'ts': datetime.datetime.now().isoformat()})
        if len(rec) > 50:
            self.data['recents']['commands'] = rec[-50:]

    def add_recent_file(self, path):
        rec = self.data.setdefault('recents', {}).setdefault('files', [])
        rec.append({'path': path, 'ts': datetime.datetime.now().isoformat()})
        if len(rec) > 50:
            self.data['recents']['files'] = rec[-50:]

    def add_recent_app(self, name):
        rec = self.data.setdefault('recents', {}).setdefault('apps', [])
        rec.append({'name': name, 'ts': datetime.datetime.now().isoformat()})
        if len(rec) > 50:
            self.data['recents']['apps'] = rec[-50:]

    def remember_fact(self, key, value, tags=None):
        facts = self.data.setdefault('facts', [])
        facts.append({'key': key, 'value': value, 'tags': tags or []})
class EnhancedJarvisGUI:
    """
    Enhanced GUI for SAM with Microsoft Copilot-inspired design.
    Features modern chat bubbles, improved voice interaction, and streamlined UI.
    """
    
    def __init__(self) -> None:
        """
        Initialize the ultra-efficient GUI with Copilot-style theming and features.
        """
        # Setup logging early so we can capture init issues
        self._setup_logging()
        self.theme = "core_system"  # Bhavesh Pandey futuristic Core System style
        self.sidebar_width = 200  # Slimmer sidebar for ChatGPT-style layout
        self.chat_font_size = 13
        self.conversation_history = []
        self.speaking = False
        self.listening = False
        self.hotword_detection = False
        
        # Profile settings
        self.profile_picture_path = None
        self.user_commands = {}
        self.hotwords = []
        self.username = "Default"
        
        # Performance monitoring for efficiency
        self.command_times = []
        self.response_times = []
        self.start_time = time.time()
        self.total_commands = 0
        self.avg_response_time = 0
        # Planner controls (modular)
        self.planner_enabled = True
        self.planning_strategy = "simple"  # simple | ai_assisted (extensible)
        # Automation strategy: direct (uses webbrowser.open - reliable) | simulate (mouse/keyboard - can have issues)
        self.automation_strategy = "direct"
        self.browser_controller = BrowserController()
        self.system_launcher = SystemLauncher()
        self.whatsapp_automation = WhatsAppAutomation()  # WhatsApp messaging automation
        self.fast_nav = SystemNavigationService()
        self.window_mgr = WindowManager()
        # Creator identity for origin questions
        self.creator_name = "DaivikReddy"

        # Initialize components
        self._initialize_ui_components()
        self._initialize_audio_components()

        try:
            self.voice_mgr = VoiceInputManager(self)
            self.hotword_engine = HotwordEngine(self)
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.warning(f"Voice manager init failed: {e}")

        # Initialize modular natural language navigator for system navigation
        try:
            self.navigator = NaturalLanguageNavigator(self)
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.warning(f"Failed to initialize navigator: {e}")
            self.navigator = None

        # Initialize multi-intent planner for compound commands
        try:
            self.multi_planner = MultiIntentPlanner(self)
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.warning(f"Failed to initialize multi-intent planner: {e}")
            self.multi_planner = None
        
        # Load user data
        self.load_user_commands()
        self.load_hotwords()

        # Show profile selection
        self.load_or_prompt_profile()
        try:
            self.memory_manager = MemoryManager(self)
            self.memory_manager.load(getattr(self, 'profile_memory', {}))
        except Exception:
            self.memory_manager = MemoryManager(self)
        
        # Initialize wake word detection (cross-platform)
        self.wake_word_detector = None
        self._init_wake_word_detection()

        # Initialize system tray and hotkeys
        self.always_on_top = False
        self.tray_manager = None
        self.hotkey_manager = None
        self.mini_window = None
        self._init_system_tray()

        
        # Show main UI
        self.show_main_ui()
        
        # Update Gmail status after UI is initialized
        self.update_gmail_status()

    def show_main_ui(self):
        """Display the main user interface."""
        self.setup_main_window()
        self.setup_menu()
        # Sidebar removed - now using 3-panel Core System layout
        self.setup_main_content()
        # Chat area is now part of setup_transcript_panel in setup_main_content
        self.setup_input_area()
        self.setup_status_bar()
        self.setup_speech_recognition()
        
        # Apply theme
        self.apply_theme_to_widgets()

        # Initialize ToastManager after root window exists
        try:
            self.toast = ToastManager(self.root, theme=self.theme)
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.warning(f"ToastManager init failed: {e}")
            self.toast = None
        
        # Start system tray and hotkeys
        self._start_tray_and_hotkeys()
        
        # Start system info updates
        self.update_system_info()
        
        # Add welcome message
        greet_name = None
        try:
            greet_name = self.memory_manager.get_name()
        except Exception:
            greet_name = None
        msg = f"Hello {greet_name}! I'm SAM, your AI assistant." if greet_name else "Hello! I'm SAM, your AI assistant."
        msg += " How can I help you today?"
        self.root.after(1000, lambda: self.add_to_chat("SAM", msg, "info"))
        
        # Check if should start minimized
        if TRAY_AVAILABLE and TRAY_CONFIG.get("start_minimized", False):
            self.root.after(100, self.minimize_to_tray)
        
        # Show the window
        self.root.mainloop()

    def _setup_logging(self):
        """Configure application logging to help diagnose UI/backend issues."""
        try:
            # Create logs directory if it doesn't exist
            os.makedirs("logs", exist_ok=True)
            self.logger = logging.getLogger("SAM_UI")
            self.logger.setLevel(logging.INFO)
            # Avoid duplicate handlers if re-instantiated
            if not self.logger.handlers:
                file_handler = RotatingFileHandler(
                    os.path.join("logs", "sam_ui.log"), maxBytes=1024 * 1024, backupCount=3
                )
                file_handler.setFormatter(logging.Formatter(
                    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
                ))
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
                self.logger.addHandler(file_handler)
                self.logger.addHandler(console_handler)
            self.logger.info("Logging initialized")
        except Exception as e:
            # Fallback to print if logging setup fails
            print(f"Logging setup error: {e}")

    def _initialize_ui_components(self):
        """Initialize UI-related components."""
        # Initialize conversation history
        self.conversation_history = []
        
        # Initialize theme
        self.theme = "copilot_dark"
        
        # Initialize sidebar width
        self.sidebar_width = 280
        
        # Initialize chat images list (prevents garbage collection)
        self.chat_images = []
    
    def _initialize_audio_components(self):
        """Initialize audio-related components."""
        # Initialize TTS engine
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 185)  # Faster JARVIS-like speech
            self.tts_engine.setProperty('volume', 0.8)
            self.tts_rate = 185
            self.tts_volume = 0.8
            if hasattr(self, 'logger'):
                self.logger.info("TTS engine initialized")
            # TTS queue and worker to ensure seamless, non-blocking speech
            self.tts_queue = queue.Queue()
            self._tts_worker_running = True
            def _tts_worker():
                while self._tts_worker_running:
                    try:
                        item = self.tts_queue.get()
                        if item is None:
                            break
                        text = self._prepare_text_for_speech(item)
                        if not text:
                            continue
                        self.speaking = True
                        # Activate orb animation when speaking
                        self._set_orb_voice_active(True)
                        self._apply_enhanced_tts_settings()
                        self.tts_engine.say(text)
                        self.tts_engine.runAndWait()
                    except Exception as e:
                        print(f"TTS worker error: {e}")
                        try:
                            self.tts_engine = pyttsx3.init()
                            self.update_tts_settings()
                        except Exception:
                            pass
                    finally:
                        self.speaking = False
                        # Deactivate orb animation when done speaking
                        self._set_orb_voice_active(False)
            try:
                self.tts_thread = threading.Thread(target=_tts_worker, daemon=True)
                self.tts_thread.start()
            except Exception:
                pass
        except Exception as e:
            print(f"TTS initialization error: {e}")
            if hasattr(self, 'logger'):
                self.logger.error(f"TTS initialization error: {e}")
            self.tts_engine = None
            self.tts_voice_id = None
            self.tts_rate = 185
            self.tts_volume = 0.8
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
            self.mic_available = True
            if hasattr(self, 'logger'):
                self.logger.info("Microphone available and initialized")
        except Exception as e:
            # Microphone not available or PyAudio missing
            self.microphone = None
            self.mic_available = False
            print(f"Microphone initialization error: {e}")
            if hasattr(self, 'logger'):
                self.logger.warning(f"Microphone initialization error: {e}")
        
        # Audio state
        self.speaking = False
        self.listening = False
        self.hotword_detection = False
        self.is_listening = False
        self.hotword_thread = None
        self.mic_available = True
        self.hotword_enabled = False  # Add missing attribute
        
        # Language settings
        self.language = "English"
        self.lang_code = LANGUAGES[self.language]["code"]
        self.sr_code = LANGUAGES[self.language]["sr_code"]
        self.current_tts_voice = LANGUAGES[self.language].get("tts_voice", None)
        
        # Gmail settings
        self.gmail_address = None
        self.gmail_app_password = None
        
        # Theme settings
        self.accent_color = "#0078d4"  # Default accent color

    def _init_wake_word_detection(self):
        """Initialize wake word detection using Picovoice Porcupine."""
        try:
            from features.wake_word import WakeWordDetector, PORCUPINE_AVAILABLE, PYAUDIO_AVAILABLE
            from config.settings import WAKE_WORD_CONFIG
            
            if not WAKE_WORD_CONFIG.get("enabled", False):
                if hasattr(self, 'logger'):
                    self.logger.info("Wake word detection disabled in settings")
                return
            
            if not PORCUPINE_AVAILABLE or not PYAUDIO_AVAILABLE:
                if hasattr(self, 'logger'):
                    self.logger.warning("Wake word detection unavailable - missing dependencies")
                return
            
            access_key = WAKE_WORD_CONFIG.get("access_key", "")
            if not access_key:
                if hasattr(self, 'logger'):
                    self.logger.warning("Wake word detection requires Picovoice access key. Get free key at https://console.picovoice.ai/")
                print("[INFO] Wake word detection requires Picovoice access key.")
                print("[INFO] Get your free access key at: https://console.picovoice.ai/")
                return
            
            keywords = WAKE_WORD_CONFIG.get("keywords", ["jarvis"])
            sensitivity = WAKE_WORD_CONFIG.get("sensitivity", 0.5)
            
            self.wake_word_detector = WakeWordDetector(
                access_key=access_key,
                keywords=keywords,
                sensitivities=[sensitivity] * len(keywords),
                on_wake_word=self._on_wake_word_detected
            )
            
            if self.wake_word_detector.start():
                if hasattr(self, 'logger'):
                    self.logger.info(f"Wake word detection started. Listening for: {keywords}")
                print(f"[INFO] Wake word detection active. Say '{keywords[0]}' to activate SAM.")
            else:
                self.wake_word_detector = None
                if hasattr(self, 'logger'):
                    self.logger.error("Failed to start wake word detection")
                    
        except ImportError as e:
            if hasattr(self, 'logger'):
                self.logger.warning(f"Wake word module not available: {e}")
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Wake word initialization error: {e}")
            print(f"[ERROR] Wake word initialization failed: {e}")

    def _on_wake_word_detected(self, keyword: str):
        """Callback when wake word is detected."""
        try:
            if hasattr(self, 'logger'):
                self.logger.info(f"Wake word detected: {keyword}")
            
            # Show toast notification if available
            if hasattr(self, 'toast') and self.toast:
                try:
                    self.root.after(0, lambda: self.toast.show(f"🎤 Wake word '{keyword}' detected!", "info"))
                except Exception:
                    pass
            
            # Trigger speech recognition
            self.root.after(0, self._start_listening_after_wake)
            
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error handling wake word: {e}")

    def _start_listening_after_wake(self):
        """Start listening for command after wake word."""
        try:
            # Provide audio feedback
            self.speak("Yes?")
            
            # Start speech recognition
            self.listening = True
            self.is_listening = True
            
            # Update UI if possible
            if hasattr(self, 'mic_button'):
                try:
                    colors = THEMES.get(self.theme, THEMES["copilot_dark"])
                    self.mic_button.configure(fg_color=colors["success"])
                except Exception:
                    pass
            
            # Listen for command in background thread
            threading.Thread(target=self._listen_for_command, daemon=True).start()
            
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error starting listen after wake: {e}")

    def stop_wake_word_detection(self):
        """Stop wake word detection - call on app exit."""
        if self.wake_word_detector:
            self.wake_word_detector.stop()
            self.wake_word_detector = None

    def toggle_wake_word(self):
        """Toggle Porcupine wake word detection on/off."""
        try:
            if self.wake_word_detector and self.wake_word_detector.is_running():
                # Stop wake word detection
                self.wake_word_detector.stop()
                self.wake_word_detector = None
                self.add_to_chat("System", "🎤 Wake word detection disabled.", "system")
                if hasattr(self, 'wake_word_btn'):
                    self.wake_word_btn.configure(
                        text="🎤 Wake Word: Off",
                        fg_color=THEMES[self.theme]["btnbg"]
                    )
            else:
                # Start wake word detection
                from config.settings import WAKE_WORD_CONFIG
                access_key = WAKE_WORD_CONFIG.get("access_key", "")
                
                if not access_key:
                    self.add_to_chat("System", "⚠️ Wake word requires Picovoice API key.\nGet free key at: https://console.picovoice.ai/\nAdd to config/settings.py → WAKE_WORD_CONFIG['access_key']", "warning")
                    return
                
                from features.wake_word import WakeWordDetector, PORCUPINE_AVAILABLE, PYAUDIO_AVAILABLE
                
                if not PORCUPINE_AVAILABLE or not PYAUDIO_AVAILABLE:
                    self.add_to_chat("System", "⚠️ Wake word dependencies not installed.\nRun: pip install pvporcupine pyaudio", "warning")
                    return
                
                keywords = WAKE_WORD_CONFIG.get("keywords", ["jarvis"])
                sensitivity = WAKE_WORD_CONFIG.get("sensitivity", 0.5)
                
                self.wake_word_detector = WakeWordDetector(
                    access_key=access_key,
                    keywords=keywords,
                    sensitivities=[sensitivity] * len(keywords),
                    on_wake_word=self._on_wake_word_detected
                )
                
                if self.wake_word_detector.start():
                    self.add_to_chat("System", f"🎤 Wake word detection enabled!\nSay '{keywords[0]}' to activate SAM.", "success")
                    if hasattr(self, 'wake_word_btn'):
                        self.wake_word_btn.configure(
                            text=f"🎤 Wake Word: On ({keywords[0]})",
                            fg_color=THEMES[self.theme]["success"]
                        )
                else:
                    self.wake_word_detector = None
                    self.add_to_chat("System", "❌ Failed to start wake word detection.", "error")
                    
        except Exception as e:
            print(f"Wake word toggle error: {e}")
            self.add_to_chat("System", f"❌ Wake word error: {str(e)}", "error")

    # ============================================================================
    # SYSTEM TRAY AND HOTKEY METHODS
    # ============================================================================
    
    def _init_system_tray(self):
        """Initialize system tray icon and global hotkeys."""
        if not TRAY_AVAILABLE or not TRAY_CONFIG.get("enabled", False):
            if hasattr(self, 'logger'):
                self.logger.info("System tray disabled or unavailable")
            return
        
        try:
            # Get theme colors for mini window
            theme_colors = THEMES.get(self.theme, THEMES["copilot_dark"])
            
            # Map theme colors to mini window expected keys
            mini_colors = {
                "bg": theme_colors.get("bg", "#1a1a2e"),
                "fg": theme_colors.get("fg", "#ffffff"),
                "accent": theme_colors.get("accent", "#7C3AED"),
                "input_bg": theme_colors.get("entrybg", theme_colors.get("input_bg", "#2d2d44")),
                "input_border": theme_colors.get("input_border", "#3d3d5c")
            }
            
            # Initialize mini floating window
            self.mini_window = MiniFloatingWindow(self, theme_colors=mini_colors)
            
            if hasattr(self, 'logger'):
                self.logger.info("System tray components initialized (will start after main window)")
                
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Failed to initialize system tray: {e}")
            print(f"[ERROR] System tray initialization failed: {e}")
    
    def _start_tray_and_hotkeys(self):
        """Start the tray icon and hotkey listener after main window is ready."""
        if not TRAY_AVAILABLE or not TRAY_CONFIG.get("enabled", False):
            return
        
        try:
            # Define callbacks for tray menu
            tray_callbacks = {
                'toggle_visibility': self.toggle_visibility,
                'toggle_always_on_top': self.toggle_always_on_top,
                'show_mini_mode': self.show_mini_mode,
                'toggle_listening': self.toggle_listening if hasattr(self, 'toggle_listening') else lambda: None,
                'mute': self.stop_speaking if hasattr(self, 'stop_speaking') else lambda: None,
                'show_settings': self.show_settings if hasattr(self, 'show_settings') else lambda: None,
                'exit': self.on_exit
            }
            
            # Initialize and start tray manager
            self.tray_manager = TrayManager(self, callbacks=tray_callbacks)
            if self.tray_manager.start():
                if hasattr(self, 'logger'):
                    self.logger.info("System tray icon started")
            
            # Initialize and start hotkey manager
            hotkey = TRAY_CONFIG.get("hotkey", "ctrl+shift+s")
            self.hotkey_manager = HotkeyManager(self, hotkey=hotkey)
            self.hotkey_manager.register('toggle_visibility', self.toggle_visibility)
            if self.hotkey_manager.start():
                if hasattr(self, 'logger'):
                    self.logger.info(f"Global hotkey registered: {hotkey}")
            
            # Show notification that SAM is ready
            if TRAY_CONFIG.get("show_notifications", True) and self.tray_manager:
                self.root.after(2000, lambda: self.tray_manager.notify("SAM Ready", "Press Ctrl+Shift+S to show/hide"))
                
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Failed to start tray/hotkeys: {e}")
    
    def minimize_to_tray(self):
        """Minimize the main window to system tray."""
        try:
            self.root.withdraw()  # Hide the window
            
            # Show notification
            if self.tray_manager and TRAY_CONFIG.get("show_notifications", True):
                self.tray_manager.notify("SAM Minimized", "Click tray icon or press Ctrl+Shift+S to restore")
            
            if hasattr(self, 'logger'):
                self.logger.info("Window minimized to tray")
                
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error minimizing to tray: {e}")
    
    def restore_from_tray(self):
        """Restore the main window from system tray."""
        try:
            self.root.deiconify()  # Show the window
            self.root.lift()  # Bring to front
            self.root.focus_force()  # Focus the window
            
            # Restore always-on-top state if enabled
            if self.always_on_top:
                self.root.attributes("-topmost", True)
            
            if hasattr(self, 'logger'):
                self.logger.info("Window restored from tray")
                
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error restoring from tray: {e}")
    
    def toggle_visibility(self):
        """Toggle main window visibility (for hotkey and tray menu)."""
        try:
            if self.root.state() == 'withdrawn' or not self.root.winfo_viewable():
                self.restore_from_tray()
            else:
                self.minimize_to_tray()
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error toggling visibility: {e}")
    
    def toggle_always_on_top(self):
        """Toggle always-on-top mode for the main window."""
        try:
            self.always_on_top = not self.always_on_top
            self.root.attributes("-topmost", self.always_on_top)
            
            status = "enabled" if self.always_on_top else "disabled"
            if hasattr(self, 'toast') and self.toast:
                self.toast.show(f"📌 Always on Top {status}", "info")
            
            if hasattr(self, 'logger'):
                self.logger.info(f"Always-on-top {status}")
                
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error toggling always-on-top: {e}")
    
    def show_mini_mode(self):
        """Show the mini floating window."""
        try:
            if self.mini_window:
                # Hide main window first
                self.minimize_to_tray()
                # Show mini window
                self.mini_window.show()
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error showing mini mode: {e}")
    
    def hide_mini_mode(self):
        """Hide the mini floating window."""
        try:
            if self.mini_window:
                self.mini_window.hide()
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error hiding mini mode: {e}")
    
    def _stop_tray_and_hotkeys(self):
        """Stop system tray and hotkey listeners."""
        try:
            if self.tray_manager:
                self.tray_manager.stop()
                self.tray_manager = None
            
            if self.hotkey_manager:
                self.hotkey_manager.stop()
                self.hotkey_manager = None
            
            if self.mini_window:
                self.mini_window.hide()
                self.mini_window = None
                
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error stopping tray/hotkeys: {e}")


    @staticmethod
    def prompt_for_profile():
        """
        Static method to prompt user for profile selection.
        Returns a tuple of (profile_name, profile_picture_path).
        """
        profile_window = ctk.CTkToplevel()
        profile_window.title("Welcome to SAM - Choose Your Profile")
        profile_window.geometry("400x300")
        profile_window.resizable(False, False)
        
        # Center the window
        profile_window.update_idletasks()
        x = (profile_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (profile_window.winfo_screenheight() // 2) - (300 // 2)
        profile_window.geometry(f"400x300+{x}+{y}")
        
        # Make it modal
        profile_window.transient()
        profile_window.grab_set()
        
        result = {"profile_name": "Default", "profile_picture_path": None}
        
        def on_select():
            result["profile_name"] = profile_var.get()
            profile_window.destroy()
        
        def on_dropdown_change(choice):
            # Update profile picture based on selection
            # For now, we'll use None for all profiles to avoid missing file errors
            result["profile_picture_path"] = None
        
        # Main frame
        main_frame = ctk.CTkFrame(profile_window, fg_color=THEMES["copilot_dark"]["bg"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Welcome to SAM", 
            font=("Segoe UI", 24, "bold"),
            text_color=THEMES["copilot_dark"]["fg"]
        )
        title_label.pack(pady=(20, 10))
        
        subtitle_label = ctk.CTkLabel(
            main_frame, 
            text="Choose your profile to get started", 
            font=("Segoe UI", 14),
            text_color=THEMES["copilot_dark"]["subfg"]
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Profile selection
        profile_var = ctk.StringVar(value="Default")
        profile_dropdown = ctk.CTkOptionMenu(
            main_frame,
            variable=profile_var,
            values=["Default", "Developer", "Student", "Professional"],
            command=on_dropdown_change,
            font=("Segoe UI", 14),
            fg_color=THEMES["copilot_dark"]["entrybg"],
            text_color=THEMES["copilot_dark"]["fg"],
            button_color=THEMES["copilot_dark"]["accent"],
            button_hover_color=THEMES["copilot_dark"]["hover"]
        )
        profile_dropdown.pack(pady=(0, 30))
        
        # Continue button
        continue_btn = ctk.CTkButton(
            main_frame,
            text="Continue",
            command=on_select,
            font=("Segoe UI", 14, "bold"),
            fg_color=THEMES["copilot_dark"]["accent"],
            hover_color=THEMES["copilot_dark"]["hover"],
            height=40
        )
        continue_btn.pack(pady=(0, 20))
        
        # Wait for window to close
        profile_window.wait_window()
        
        return result["profile_name"], result["profile_picture_path"]

    def setup_main_window(self) -> None:
        """
        Set up the main application window with Copilot-style appearance.
        """
        # Set CustomTkinter appearance based on theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("SAM - Your AI Assistant")
        
        # Set window properties
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        self.root.state('zoomed')
        
        # Configure colors based on theme
        colors = THEMES[self.theme]
        self.root.configure(fg_color=colors["bg"])
        
        # Set window icon
        try:
            self.root.iconbitmap("jarvis_icon.ico")
        except Exception:
            pass
        
        # Set close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        
        # Create main container
        self.container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_menu(self) -> None:
        """
        Set up the application menu bar with Copilot-style theming.
        """
        menubar = tk.Menu(self.root, bg=THEMES[self.theme]["sidebar"], fg=THEMES[self.theme]["fg"])
        
        # Theme menu
        theme_menu = tk.Menu(menubar, tearoff=0, bg=THEMES[self.theme]["sidebar"], fg=THEMES[self.theme]["fg"])
        theme_menu.add_command(label="🌙 Copilot Dark", command=lambda: self.change_theme("copilot_dark"))
        theme_menu.add_command(label="☀️ Copilot Light", command=lambda: self.change_theme("copilot_light"))
        theme_menu.add_command(label="🔵 Copilot Blue", command=lambda: self.change_theme("copilot_blue"))
        menubar.add_cascade(label="🎨 Themes", menu=theme_menu)
        
        # Language menu
        lang_menu = tk.Menu(menubar, tearoff=0, bg=THEMES[self.theme]["sidebar"], fg=THEMES[self.theme]["fg"])
        for lang in LANGUAGES.keys():
            lang_menu.add_command(label=f"🌐 {lang}", command=lambda l=lang: self.change_language(l))
        menubar.add_cascade(label="🌍 Language", menu=lang_menu)
        
        # Window menu (new)
        window_menu = tk.Menu(menubar, tearoff=0, bg=THEMES[self.theme]["sidebar"], fg=THEMES[self.theme]["fg"])
        window_menu.add_command(label="📌 Always on Top", command=self.toggle_always_on_top)
        window_menu.add_command(label="💬 Mini Mode", command=self.show_mini_mode)
        window_menu.add_separator()
        window_menu.add_command(label="⬇️ Minimize to Tray", command=self.minimize_to_tray)
        menubar.add_cascade(label="🪟 Window", menu=window_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=THEMES[self.theme]["sidebar"], fg=THEMES[self.theme]["fg"])
        help_menu.add_command(label="❓ Help", command=self.show_help)
        help_menu.add_command(label="ℹ️ About", command=self.show_about)
        help_menu.add_command(label="⚙️ Settings", command=self.show_settings)
        menubar.add_cascade(label="🔧 Help", menu=help_menu)
        
        self.root.config(menu=menubar)

    def start_new_chat(self):
        """Clear chat history and start a fresh conversation."""
        self.clear_chat()
        self.add_to_chat("SAM", "Starting a new chat session. How can I help you?", "assistant")

    def load_chat_sessions(self):
        """Load past chat sessions (placeholder)."""
        self.chat_sessions = {}
        # TODO: Implement actual session loading from file
        pass

    def delete_chat_session(self, session_id):
        """Delete a chat session."""
        if session_id in self.chat_sessions:
            del self.chat_sessions[session_id]
    def start_new_chat(self):
        """Start a new chat session."""
        try:
            # Save current session if not empty
            if self.conversation_history:
                self.save_current_chat_session()
            
            # Clear UI
            for widget in self.chat_scrollable_frame.winfo_children():
                widget.destroy()
            
            # Clear history
            self.conversation_history = []
            
            # Reset ID
            self.current_session_id = int(time.time())
            
            # Add welcome message
            greeting = f"Hello {self.username.split()[0]}! How can I help you today?"
            self.add_to_chat("SAM", greeting, "assistant")
            
            self.refresh_chat_history_ui()
            
        except Exception as e:
            print(f"Error starting new chat: {e}")

    def refresh_chat_history_ui(self):
        """Refresh the sidebar chat history list."""
        if not hasattr(self, 'chat_history_frame'):
            return
            
        # Clear existing
        for widget in self.chat_history_frame.winfo_children():
            widget.destroy()
            
        colors = THEMES[self.theme]
        
        # Determine current ID
        current_id = getattr(self, "current_session_id", 0)
        
        # Add buttons for each session
        for session in self.chat_sessions:
            s_id = session.get("id")
            s_preview = session.get("preview", "New Chat")
            
            # Truncate preview
            if len(s_preview) > 22:
                s_preview = s_preview[:20] + "..."
            
            btn = ctk.CTkButton(
                self.chat_history_frame,
                text=s_preview,
                font=("Segoe UI", 12),
                fg_color=colors["card"] if s_id != current_id else colors["accent"],
                text_color=colors["fg"] if s_id != current_id else "#ffffff",
                hover_color=colors["hover"],
                anchor="w",
                height=32,
                command=lambda sid=s_id: self.load_chat_session(sid)
            )
            btn.pack(fill="x", pady=2)

    def setup_sidebar(self) -> None:
        """
        Set up the sidebar with ChatGPT-style chat history and user account.
        """
        colors = THEMES[self.theme]
        
        # Main sidebar with rounded corners and subtle border
        self.sidebar = ctk.CTkFrame(
            self.container, 
            fg_color=colors["sidebar"], 
            width=self.sidebar_width, 
            corner_radius=16,
            border_width=1,
            border_color=colors.get("glass_border", colors["input_border"])
        )
        self.sidebar.pack(side="left", fill="y", padx=(0, 8), pady=0)
        self.sidebar.pack_propagate(False)
        
        # Resize handle
        self.sidebar_drag = ctk.CTkFrame(
            self.container, 
            fg_color=colors["input_border"], 
            width=3,
            corner_radius=2
        )
        self.sidebar_drag.pack(side="left", fill="y")
        self.sidebar_drag.bind('<B1-Motion>', self.resize_sidebar)
        
        # === TOP: New Chat Button ===
        new_chat_btn = ctk.CTkButton(
            self.sidebar,
            text="+ New Chat",
            font=("SF Pro Display", 13, "bold") if platform.system() == "Darwin" else ("Segoe UI", 13, "bold"),
            fg_color=colors["accent"],
            hover_color=colors["accent_hover"],
            height=40,
            corner_radius=10,
            command=self.start_new_chat
        )
        new_chat_btn.pack(fill="x", padx=12, pady=(16, 12))
        
        # === MIDDLE: Chat History List ===
        history_label = ctk.CTkLabel(
            self.sidebar,
            text="Chat History",
            font=("SF Pro Display", 11) if platform.system() == "Darwin" else ("Segoe UI", 11),
            text_color=colors["subfg"]
        )
        history_label.pack(anchor="w", padx=16, pady=(8, 4))
        
        # Scrollable chat history container
        self.chat_history_frame = ctk.CTkScrollableFrame(
            self.sidebar,
            fg_color="transparent",
            corner_radius=0
        )
        self.chat_history_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        # Initialize chat sessions storage
        self.chat_sessions = []
        self.current_session_id = 0
        self.load_chat_sessions()
        self.refresh_chat_history_ui()
        
        # === BOTTOM: User Account Section ===
        account_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color=colors["card"],
            corner_radius=12,
            border_width=1,
            border_color=colors.get("glass_border", colors["input_border"])
        )
        account_frame.pack(fill="x", padx=12, pady=(0, 12), side="bottom")
        
        account_inner = ctk.CTkFrame(account_frame, fg_color="transparent")
        account_inner.pack(fill="x", padx=12, pady=10)
        
        # User icon
        user_icon = ctk.CTkLabel(
            account_inner,
            text="👤",
            font=("Segoe UI", 20),
            text_color=colors["accent"]
        )
        user_icon.pack(side="left", padx=(0, 10))
        
        # Username
        self.account_name_label = ctk.CTkLabel(
            account_inner,
            text=getattr(self, 'username', 'User'),
            font=("SF Pro Display", 12, "bold") if platform.system() == "Darwin" else ("Segoe UI", 12, "bold"),
            text_color=colors["fg"]
        )
        self.account_name_label.pack(side="left", fill="x", expand=True, anchor="w")
        
        # Switch account button
        switch_btn = ctk.CTkButton(
            account_inner,
            text="⚙️",
            width=30,
            height=30,
            corner_radius=8,
            fg_color="transparent",
            hover_color=colors["hover"],
            command=self.switch_user_account
        )
        switch_btn.pack(side="right")
        
    def switch_user_account(self):
        """Switch user account dialog."""
        dialog = ctk.CTkInputDialog(text="Enter username:", title="Switch User")
        new_user = dialog.get_input()
        if new_user and new_user.strip():
            self.username = new_user.strip()
            self.account_name_label.configure(text=self.username)
            # Re-save profile with new name to create new file
            self.save_profile()
            self.add_to_chat("System", f"Switched to user: {self.username}", "system")
            # Clear sessions for new user (in real app, load user specific sessions)
            self.chat_sessions = [] 
            self.start_new_chat()

    def save_current_chat_session(self):
        """Save the current chat session to history."""
        if not self.conversation_history:
            return
            
        # Don't save empty "Hello!" sessions
        if len(self.conversation_history) <= 1:
            return

        session_data = {
            "id": getattr(self, "current_session_id", int(time.time())),
            "timestamp": datetime.datetime.now().isoformat(),
            "preview": self.conversation_history[1]["message"][:30] + "..." if len(self.conversation_history) > 1 else "New Chat",
            "messages": self.conversation_history
        }
        
        # Load existing or init new
        sessions = self.load_chat_sessions()
        
        # Update or add
        updated = False
        for i, s in enumerate(sessions):
            if s["id"] == session_data["id"]:
                sessions[i] = session_data
                updated = True
                break
        
        if not updated:
            sessions.insert(0, session_data)  # Add to top
            
        # Keep only last 20 sessions per user
        sessions = sessions[:20]
        
        try:
            with open(f"chat_history_{self.username}.json", "w", encoding="utf-8") as f:
                json.dump(sessions, f, indent=2, ensure_ascii=False)
            self.chat_sessions = sessions
            self.refresh_chat_history_ui()
        except Exception as e:
            print(f"Error saving chat history: {e}")

    def load_chat_sessions(self):
        """Load chat sessions from disk."""
        try:
            filename = f"chat_history_{self.username}.json"
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    self.chat_sessions = json.load(f)
            else:
                self.chat_sessions = []
            return self.chat_sessions
        except Exception:
            return []

    def load_chat_session(self, session_id):
        """Load a specific chat session."""
        try:
            # First save current if it's new/modified
            if self.conversation_history and self.current_session_id != session_id:
                self.save_current_chat_session()
            
            # Find session
            target_session = next((s for s in self.chat_sessions if s["id"] == session_id), None)
            
            if target_session:
                self.current_session_id = session_id
                self.conversation_history = target_session.get("messages", [])
                
                # Clear UI
                for widget in self.chat_scrollable_frame.winfo_children():
                    widget.destroy()
                
                # Rebuild UI
                for msg in self.conversation_history:
                    self.add_to_chat(
                        msg.get("sender", "SAM"), 
                        msg.get("message", ""), 
                        msg.get("type", "info")
                    )
                
                self.refresh_chat_history_ui()
                
        except Exception as e:
            print(f"Error loading session: {e}")

    def setup_avatar(self) -> None:
        """Set up the avatar with Copilot-style design."""
        try:
            self.avatar_frame.configure(width=120, height=120)
            self.avatar_frame.pack_propagate(False)
            
            # Always use the emoji fallback for now to avoid missing file errors
            self.avatar_label = tk.Label(
                self.avatar_frame, 
                text="🤖", 
                font=("Segoe UI", 48), 
                fg=THEMES[self.theme]["accent"], 
                bg=THEMES[self.theme]["sidebar"]
            )
            self.avatar_label.pack(expand=True)
            
        except Exception as e:
            print(f"Error in setup_avatar: {e}")
            # Final fallback
            self.avatar_label = tk.Label(
                self.avatar_frame, 
                text="🤖", 
                font=("Segoe UI", 48), 
                fg=THEMES[self.theme]["accent"], 
                bg=THEMES[self.theme]["sidebar"]
            )
            self.avatar_label.pack(expand=True)

    def setup_quick_actions(self) -> None:
        """
        Set up quick action buttons with Copilot-style design.
        """
        colors = THEMES[self.theme]
        
        actions_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(20, 10), padx=20)
        
        ctk.CTkLabel(
            actions_frame, 
            text="Quick Actions",
            font=("Segoe UI", 14, "bold"), 
            text_color=colors["fg"]
        ).pack(anchor="w")
        
        buttons_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        actions = [
            ("🌐", "Web", lambda: self.open_website("https://google.com")),
            ("🎵", "Music", self.play_music_folder),
            ("📝", "Notes", self.open_notepad),
            ("🧮", "Calc", self.open_calculator),
            ("🌤️", "Weather", lambda: self.process_command("weather")),
            ("📸", "Screen", self.quick_screenshot),
            ("🔍", "Analyze", self.quick_screen_analysis),  # Screen Analysis with OCR + AI
            ("📰", "News", lambda: self.process_command("news")),
            ("🛠️", "System", self.show_system_info_popup),
            ("🔤", "ASCII Art", self.ascii_art_generator),
            ("💻", "Code", lambda: self.process_command("generate fibonacci")),
            ("🎲", "3D Models", self.open_3d_model_viewer),
            ("📁", "Load 3D", self.load_custom_3d_model),
            ("🔎", "Find & Open", self.prompt_find_and_open)
        ]
        
        for i, (icon, text, command) in enumerate(actions):
            row, col = i // 2, i % 2
            btn_frame = ctk.CTkFrame(
                buttons_frame, 
                fg_color=colors["card"], 
                corner_radius=8
            )
            btn_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            btn = ctk.CTkButton(
                btn_frame, 
                text=f"{icon}\n{text}",
                font=("Segoe UI", 10), 
                fg_color=colors["card"], 
                text_color=colors["fg"],
                hover_color=colors["hover"], 
                command=command, 
                corner_radius=6
            )
            btn.pack(fill="both", expand=True)
        
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)

        # Navigator quick actions
        nav_label = ctk.CTkLabel(
            self.sidebar, 
            text="Navigator", 
            font=("Segoe UI", 14, "bold"), 
            text_color=colors["fg"]
        )
        nav_label.pack(anchor="w", padx=20, pady=(10, 0))

        nav_buttons = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_buttons.pack(fill="x", padx=20, pady=10)

        nav_actions = [
            ("🖥️", "Desktop", lambda: self.process_command("show desktop")),
            ("🔄", "Switch", lambda: self.process_command("switch window")),
            ("📥", "Downloads", lambda: self.process_command("go to downloads")),
            ("📶", "Wi‑Fi", lambda: self.process_command("open settings for wifi")),
            ("↘️", "Scroll", lambda: self.process_command("scroll down")),
            ("✨", "Multi‑Step", lambda: self.process_command("open youtube and play a song and open google and search cats")),
        ]
        for i, (icon, text, command) in enumerate(nav_actions):
            row, col = i // 2, i % 2
            btn_frame = ctk.CTkFrame(
                nav_buttons, fg_color=colors["card"], corner_radius=8
            )
            btn_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            btn = ctk.CTkButton(
                btn_frame,
                text=f"{icon}\n{text}",
                font=("Segoe UI", 10),
                fg_color=colors["card"],
                text_color=colors["fg"],
                hover_color=colors["hover"],
                command=command,
                corner_radius=6,
            )
            btn.pack(fill="both", expand=True)
        nav_buttons.columnconfigure(0, weight=1)
        nav_buttons.columnconfigure(1, weight=1)
        
        # Voice activation button
        hotword_btn = ctk.CTkButton(
            self.sidebar, 
            text="🎙️ Voice: Off", 
            font=("Segoe UI", 10),
            fg_color=colors["btnbg"], 
            text_color=colors["btnfg"],
            hover_color=colors["btnactive"], 
            command=self.toggle_hotword_detection, 
            corner_radius=8
        )
        hotword_btn.pack(fill="x", padx=20, pady=(0, 5))
        self.hotword_btn = hotword_btn
        self.update_hotword_btn_state()
        
        # Wake Word (Porcupine) toggle button
        wake_word_btn = ctk.CTkButton(
            self.sidebar, 
            text="🎤 Wake Word: Off", 
            font=("Segoe UI", 10),
            fg_color=colors["btnbg"], 
            text_color=colors["btnfg"],
            hover_color=colors["btnactive"], 
            command=self.toggle_wake_word, 
            corner_radius=8
        )
        wake_word_btn.pack(fill="x", padx=20, pady=(0, 10))
        self.wake_word_btn = wake_word_btn

    def setup_system_panel(self) -> None:
        """
        Set up the enhanced system status panel with animations.
        """
        colors = THEMES[self.theme]
        
        # Create enhanced system panel
        self.system_panel = AnimatedSystemPanel(
            self.sidebar, 
            theme=self.theme
        )
        self.system_panel.pack(fill="x", padx=20, pady=20)
        
        # Add title
        ctk.CTkLabel(
            self.system_panel, 
            text="🖥️ System Monitor",
            font=("Segoe UI", 14, "bold"), 
            text_color=colors["fg"]
        ).pack(pady=(10, 5))
        
        # Add weather info
        self.weather_label = ctk.CTkLabel(
            self.system_panel, 
            text="🌤️ Loading weather...",
            font=("Segoe UI", 10), 
            text_color=colors["subfg"]
        )
        self.weather_label.pack(pady=2)
        
        # Update weather periodically
        self.update_weather_display()

    def setup_main_content(self) -> None:
        """Set up the main content with Core System 3-panel layout."""
        colors = THEMES[self.theme]
        
        # Top navigation bar (Core System style)
        self.setup_core_system_navbar()
        
        # Main content area with 3 panels
        content_region = ctk.CTkFrame(self.container, fg_color=colors["bg"], corner_radius=0)
        content_region.pack(fill="both", expand=True)
        
        # Configure grid for 3-panel layout
        content_region.grid_columnconfigure(0, weight=0, minsize=280)  # Left panel
        content_region.grid_columnconfigure(1, weight=1)  # Center panel (flexible)
        content_region.grid_columnconfigure(2, weight=0, minsize=320)  # Right panel
        content_region.grid_rowconfigure(0, weight=1)
        
        # Store reference
        self.main_content_region = content_region
        
        # Left panel - Visual Input + System Metrics
        self.setup_left_panel(content_region)
        
        # Center panel - Core System Orb
        self.setup_core_system_center(content_region)
        
        # Right panel - Transcript/Chat
        self.setup_transcript_panel(content_region)
        
        # Footer with attribution
        self.setup_footer()
        
        self.welcome_gif_visible = False
        self.welcome_gif_shown_once = True
    
    def setup_core_system_navbar(self):
        """Set up the Core System style navigation bar (simplified - no tabs)."""
        colors = THEMES[self.theme]
        
        # Navigation bar
        navbar = ctk.CTkFrame(self.container, fg_color=colors["panel_bg"], height=48, corner_radius=0)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        # Left side - SAM branding and Online indicator
        nav_left = ctk.CTkFrame(navbar, fg_color="transparent")
        nav_left.pack(side="left", padx=20, pady=8)
        
        # SAM Logo/Title
        ctk.CTkLabel(
            nav_left,
            text="⚡ SAM",
            font=("Consolas", 14, "bold"),
            text_color=colors["accent"]
        ).pack(side="left")
        
        ctk.CTkLabel(
            nav_left,
            text="Smart AI Manager",
            font=("Consolas", 11),
            text_color=colors["subfg"]
        ).pack(side="left", padx=(12, 0))
        
        self.nav_tabs = {}  # Keep empty dict for compatibility
        
        # Online indicator
        online_frame = ctk.CTkFrame(nav_left, fg_color="transparent")
        online_frame.pack(side="left", padx=(30, 0))
        
        online_dot = ctk.CTkLabel(
            online_frame,
            text="●",
            font=("Segoe UI", 12),
            text_color=colors["success"]
        )
        online_dot.pack(side="left")
        
        ctk.CTkLabel(
            online_frame,
            text="ONLINE",
            font=("Consolas", 11),
            text_color=colors["success"]
        ).pack(side="left", padx=(4, 0))
        
        # Right side - Status indicators
        nav_right = ctk.CTkFrame(navbar, fg_color="transparent")
        nav_right.pack(side="right", padx=20, pady=8)
        
        # System Ready indicator
        ctk.CTkLabel(
            nav_right,
            text="◉ SYSTEM READY",
            font=("Consolas", 10),
            text_color=colors["subfg"]
        ).pack(side="right", padx=(10, 0))
        
        # Network indicator
        ctk.CTkLabel(
            nav_right,
            text="📶 NET",
            font=("Consolas", 10),
            text_color=colors["subfg"]
        ).pack(side="right")
    
    def switch_nav_tab(self, tab_name):
        """Switch active navigation tab."""
        colors = THEMES[self.theme]
        for name, btn in self.nav_tabs.items():
            if name == tab_name:
                btn.configure(fg_color=colors["accent"], text_color="#ffffff")
            else:
                btn.configure(fg_color="transparent", text_color=colors["subfg"])
    
    def setup_left_panel(self, parent):
        """Set up left panel with Visual Input, Chat History, and Change User."""
        colors = THEMES[self.theme]
        
        # Left panel container
        left_panel = ctk.CTkFrame(
            parent,
            fg_color=colors["panel_bg"],
            corner_radius=12,
            border_width=1,
            border_color=colors["border_glow"]
        )
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        
        # --- Visual Input Section ---
        visual_section = ctk.CTkFrame(left_panel, fg_color="transparent")
        visual_section.pack(fill="x", padx=12, pady=(12, 8))
        
        # Header with recording indicator
        visual_header = ctk.CTkFrame(visual_section, fg_color="transparent")
        visual_header.pack(fill="x")
        
        ctk.CTkLabel(
            visual_header,
            text="📹 VISUAL INPUT",
            font=("Consolas", 11, "bold"),
            text_color=colors["accent"]
        ).pack(side="left")
        
        self.recording_indicator = ctk.CTkLabel(
            visual_header,
            text="●",
            font=("Segoe UI", 14),
            text_color=colors.get("progress_orange", "#f97316")
        )
        self.recording_indicator.pack(side="right")
        
        # Camera feed container
        self.visual_input_frame = ctk.CTkFrame(
            visual_section,
            fg_color="#000000",
            height=140,
            corner_radius=8
        )
        self.visual_input_frame.pack(fill="x", pady=(8, 0))
        self.visual_input_frame.pack_propagate(False)
        
        # Camera feed label (placeholder)
        self.camera_feed_label = ctk.CTkLabel(
            self.visual_input_frame,
            text="📹 Camera Feed\n(Click to start)",
            font=("Consolas", 10),
            text_color=colors["subfg"]
        )
        self.camera_feed_label.pack(expand=True)
        self.camera_feed_label.bind("<Button-1>", lambda e: self.toggle_camera())
        
        # Initialize camera variables
        self.camera_active = False
        self.camera_capture = None
        self.camera_thread = None
        self.camera_running = False
        
        # --- Chat History Section ---
        history_section = ctk.CTkFrame(left_panel, fg_color="transparent")
        history_section.pack(fill="both", expand=True, padx=12, pady=(8, 8))
        
        # Header
        history_header = ctk.CTkFrame(history_section, fg_color="transparent")
        history_header.pack(fill="x")
        
        ctk.CTkLabel(
            history_header,
            text="💬 CHAT HISTORY",
            font=("Consolas", 11, "bold"),
            text_color=colors["accent"]
        ).pack(side="left")
        
        # New chat button
        new_chat_btn = ctk.CTkButton(
            history_header,
            text="+ New",
            width=50,
            height=24,
            corner_radius=6,
            fg_color=colors["accent"],
            hover_color=colors["hover"],
            font=("Consolas", 10),
            command=self.start_new_chat
        )
        new_chat_btn.pack(side="right")
        
        # Scrollable chat history list
        self.left_chat_history_frame = ctk.CTkScrollableFrame(
            history_section,
            fg_color="transparent",
            corner_radius=8
        )
        self.left_chat_history_frame.pack(fill="both", expand=True, pady=(8, 0))
        
        # Refresh chat history in left panel
        self.refresh_left_chat_history()
        
        # --- Change User Section (Bottom) ---
        user_section = ctk.CTkFrame(
            left_panel,
            fg_color=colors["card"],
            corner_radius=8
        )
        user_section.pack(fill="x", padx=12, pady=(0, 12))
        
        user_inner = ctk.CTkFrame(user_section, fg_color="transparent")
        user_inner.pack(fill="x", padx=10, pady=10)
        
        # User icon
        ctk.CTkLabel(
            user_inner,
            text="👤",
            font=("Segoe UI", 18),
            text_color=colors["accent"]
        ).pack(side="left", padx=(0, 8))
        
        # Current user name
        self.left_panel_user_label = ctk.CTkLabel(
            user_inner,
            text=getattr(self, 'username', 'User'),
            font=("Consolas", 12, "bold"),
            text_color=colors["fg"]
        )
        self.left_panel_user_label.pack(side="left", fill="x", expand=True, anchor="w")
        
        # Change user button
        change_user_btn = ctk.CTkButton(
            user_inner,
            text="Change",
            width=60,
            height=28,
            corner_radius=6,
            fg_color=colors["accent"],
            hover_color=colors["hover"],
            font=("Consolas", 10),
            command=self.change_user_from_left_panel
        )
        change_user_btn.pack(side="right")
        
        # Initialize dummy labels for compatibility with metrics updates
        self.cpu_percent_label = ctk.CTkLabel(left_panel, text="")
        self.ram_percent_label = ctk.CTkLabel(left_panel, text="")
        self.ram_usage_label = ctk.CTkLabel(left_panel, text="")
        self.online_status = ctk.CTkLabel(left_panel, text="")
        self.process_list_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        
        # Store reference to left panel
        self.left_panel = left_panel
    
    def refresh_left_chat_history(self):
        """Refresh the chat history list in the left panel."""
        colors = THEMES[self.theme]
        
        if not hasattr(self, 'left_chat_history_frame'):
            return
        
        # Clear existing items
        for widget in self.left_chat_history_frame.winfo_children():
            widget.destroy()
        
        # Get chat sessions
        sessions = getattr(self, 'chat_sessions', [])
        
        if not sessions:
            # Show placeholder
            ctk.CTkLabel(
                self.left_chat_history_frame,
                text="No chat history yet.\nStart a new conversation!",
                font=("Consolas", 10),
                text_color=colors["subfg"]
            ).pack(expand=True, pady=20)
            return
        
        # Display recent sessions (newest first, limit to 10)
        for i, session in enumerate(reversed(sessions[-10:])):
            session_frame = ctk.CTkFrame(
                self.left_chat_history_frame,
                fg_color=colors["card"] if i == 0 else "transparent",
                corner_radius=6,
                cursor="hand2"
            )
            session_frame.pack(fill="x", pady=2)
            
            # Session title (first message preview)
            title = session.get('title', 'New Chat')
            if len(title) > 25:
                title = title[:22] + "..."
            
            session_label = ctk.CTkLabel(
                session_frame,
                text=f"💬 {title}",
                font=("Consolas", 10),
                text_color=colors["fg"] if i == 0 else colors["subfg"],
                anchor="w"
            )
            session_label.pack(fill="x", padx=8, pady=6)
            
            # Bind click to load session
            session_idx = len(sessions) - 1 - i
            session_frame.bind("<Button-1>", lambda e, idx=session_idx: self.load_chat_session(idx))
            session_label.bind("<Button-1>", lambda e, idx=session_idx: self.load_chat_session(idx))
    
    def change_user_from_left_panel(self):
        """Change user from the left panel button."""
        colors = THEMES[self.theme]
        dialog = ctk.CTkInputDialog(text="Enter username:", title="Change User")
        new_user = dialog.get_input()
        if new_user and new_user.strip():
            self.username = new_user.strip()
            # Update left panel label
            if hasattr(self, 'left_panel_user_label'):
                self.left_panel_user_label.configure(text=self.username)
            # Update sidebar label if exists
            if hasattr(self, 'account_name_label'):
                self.account_name_label.configure(text=self.username)
            # Save profile
            self.save_profile()
            self.add_to_chat("System", f"Switched to user: {self.username}", "system")
            # Clear sessions for new user
            self.chat_sessions = []
            self.start_new_chat()
            self.refresh_left_chat_history()
    
    def setup_core_system_center(self, parent):
        """Set up center panel with Core System orb visualization."""
        colors = THEMES[self.theme]
        
        # Center panel container
        center_panel = ctk.CTkFrame(
            parent,
            fg_color=colors["bg"],
            corner_radius=0
        )
        center_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)
        
        # Configure grid
        center_panel.grid_rowconfigure(0, weight=0)  # Header
        center_panel.grid_rowconfigure(1, weight=1)  # Orb
        center_panel.grid_rowconfigure(2, weight=0)  # Controls
        center_panel.grid_columnconfigure(0, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(center_panel, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 0))
        
        ctk.CTkLabel(
            header_frame,
            text="⚡ CORE SYSTEM",
            font=("Consolas", 14, "bold"),
            text_color=colors["accent"]
        ).pack(side="left")
        
        self.freq_label = ctk.CTkLabel(
            header_frame,
            text="FREQ: 16-24KHZ",
            font=("Consolas", 10),
            text_color=colors["subfg"]
        )
        self.freq_label.pack(side="right")
        
        # Orb visualization container
        orb_container = ctk.CTkFrame(center_panel, fg_color="transparent")
        orb_container.grid(row=1, column=0, sticky="nsew")
        
        # Create the particle orb
        self.core_orb = CoreSystemOrb(
            orb_container,
            theme=self.theme,
            size=350
        )
        self.core_orb.pack(expand=True)
        self.core_orb.start_animation()
        
        # Control buttons
        controls_frame = ctk.CTkFrame(center_panel, fg_color="transparent")
        controls_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Center the buttons
        button_container = ctk.CTkFrame(controls_frame, fg_color="transparent")
        button_container.pack(expand=True)
        
        # Camera button
        self.ctrl_camera_btn = ctk.CTkButton(
            button_container,
            text="📹",
            width=50,
            height=50,
            corner_radius=25,
            fg_color=colors["card"],
            text_color=colors["fg"],
            hover_color=colors["hover"],
            font=("Segoe UI", 18),
            command=self.toggle_camera
        )
        self.ctrl_camera_btn.pack(side="left", padx=10)
        
        # END button (main control)
        self.end_btn = ctk.CTkButton(
            button_container,
            text="⏻ END",
            width=100,
            height=50,
            corner_radius=25,
            fg_color=colors.get("end_button", "#dc2626"),
            text_color="#ffffff",
            hover_color=colors.get("end_button_hover", "#b91c1c"),
            font=("Consolas", 14, "bold"),
            command=self.end_session
        )
        self.end_btn.pack(side="left", padx=10)
        
        # Microphone button
        self.ctrl_mic_btn = ctk.CTkButton(
            button_container,
            text="🎤",
            width=50,
            height=50,
            corner_radius=25,
            fg_color=colors["card"],
            text_color=colors["fg"],
            hover_color=colors["hover"],
            font=("Segoe UI", 18),
            command=self.toggle_voice_input
        )
        self.ctrl_mic_btn.pack(side="left", padx=10)
        
        # Screen share button
        self.ctrl_screen_btn = ctk.CTkButton(
            button_container,
            text="🖥️",
            width=50,
            height=50,
            corner_radius=25,
            fg_color=colors["card"],
            text_color=colors["fg"],
            hover_color=colors["hover"],
            font=("Segoe UI", 18),
            command=self.share_screen
        )
        self.ctrl_screen_btn.pack(side="left", padx=10)
        
        # Store reference
        self.center_panel = center_panel
    
    def setup_transcript_panel(self, parent):
        """Set up right panel with transcript/chat."""
        colors = THEMES[self.theme]
        
        # Right panel container
        right_panel = ctk.CTkFrame(
            parent,
            fg_color=colors["panel_bg"],
            corner_radius=12,
            border_width=1,
            border_color=colors["border_glow"]
        )
        right_panel.grid(row=0, column=2, sticky="nsew", padx=(5, 10), pady=10)
        
        # Configure grid
        right_panel.grid_rowconfigure(0, weight=0)  # Header
        right_panel.grid_rowconfigure(1, weight=1)  # Chat
        right_panel.grid_rowconfigure(2, weight=0)  # Input
        right_panel.grid_columnconfigure(0, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 8))
        
        ctk.CTkLabel(
            header_frame,
            text="📝 TRANSCRIPT",
            font=("Consolas", 11, "bold"),
            text_color=colors["accent"]
        ).pack(side="left")
        
        # Chat scrollable area - THIS IS THE MAIN CHAT FRAME
        self.chat_scrollable_frame = ctk.CTkScrollableFrame(
            right_panel,
            fg_color="transparent",
            corner_radius=0
        )
        self.chat_scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)
        
        # Store reference (used by other parts of the code)
        self.right_panel = right_panel
    
    def setup_footer(self):
        """Footer removed as per user request."""
        pass
    
    def end_session(self):
        """End the current session - stop listening and speaking."""
        if self.speaking:
            self.stop_speaking()
        if self.listening:
            self.stop_listening()
        self.add_to_chat("System", "Session ended.", "system")
    
    def share_screen(self):
        """Share screen functionality placeholder."""
        self.add_to_chat("System", "Screen sharing not yet implemented.", "system")
    
    def _set_orb_voice_active(self, active):
        """Thread-safe method to control orb voice animation state."""
        try:
            if hasattr(self, 'core_orb') and self.core_orb:
                # Use after() to safely update from main thread
                self.root.after(0, lambda: self.core_orb.set_voice_active(active))
        except Exception:
            pass



    def setup_top_appbar(self):
        colors = THEMES[self.theme]
        bar = ctk.CTkFrame(self.container, fg_color=colors["card"], height=48, corner_radius=0)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        left = ctk.CTkFrame(bar, fg_color="transparent")
        left.pack(side="left", padx=16, pady=8)
        menu_btn = ctk.CTkButton(left, text="☰", width=36, height=28, corner_radius=6,
                                 fg_color=colors["btnbg"], text_color=colors["fg"],
                                 hover_color=colors["btnbg_hover"], command=self.open_control_panel)
        menu_btn.pack(side="left")
        logo = ctk.CTkLabel(left, text="S", width=28, height=28,
                            font=("Segoe UI", 16, "bold"), text_color="#ffffff",
                            fg_color=colors["accent"])
        logo.pack(side="left", padx=(12, 8))
        title = ctk.CTkLabel(left, text="SAM", font=("Segoe UI", 14, "bold"), text_color=colors["fg"])
        title.pack(side="left")
        subtitle = ctk.CTkLabel(left, text="Smart AI Manager", font=("Segoe UI", 11), text_color=colors["subfg"])
        subtitle.pack(side="left", padx=(8, 0))
        right = ctk.CTkFrame(bar, fg_color="transparent")
        right.pack(side="right", padx=16)
        online = ctk.CTkLabel(right, text="● ONLINE", font=("Segoe UI", 11), text_color=colors["success"])
        online.pack(side="right")
    
    def setup_right_panel(self):
        """Set up the right panel with temporal and network information like in the video."""
        colors = THEMES[self.theme]
        
        # Right panel container
        self.right_panel = ctk.CTkFrame(
            self.container.winfo_children()[-1],
            fg_color=colors["temporal_bg"],
            width=280,
            corner_radius=0
        )
        self.right_panel.pack(side="right", fill="y")
        self.right_panel.pack_propagate(False)
        
        # Main container for right panel content
        right_container = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        right_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Temporal Synchronization Section
        temporal_frame = ctk.CTkFrame(right_container, fg_color="transparent")
        temporal_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            temporal_frame,
            text="TEMPORAL SYNCHRONIZATION",
            font=("Consolas", 12, "bold"),
            text_color=colors["accent"]
        ).pack(anchor="w")
        
        # Current time and date
        self.time_display = ctk.CTkLabel(
            temporal_frame,
            text="12:22:46",
            font=("Consolas", 16, "bold"),
            text_color=colors["fg"]
        )
        self.time_display.pack(anchor="w", pady=(5, 2))
        
        self.date_display = ctk.CTkLabel(
            temporal_frame,
            text="Wednesday, 26 July 2023",
            font=("Consolas", 10),
            text_color=colors["subfg"]
        )
        self.date_display.pack(anchor="w")
        
        # Network Interface Section
        network_frame = ctk.CTkFrame(right_container, fg_color="transparent")
        network_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            network_frame,
            text="NETWORK INTERFACE",
            font=("Consolas", 12, "bold"),
            text_color=colors["accent"]
        ).pack(anchor="w")
        
        # IP Address
        self.ip_label = ctk.CTkLabel(
            network_frame,
            text="IP ADDRESS: 192.168.1.3",
            font=("Consolas", 9),
            text_color=colors["subfg"]
        )
        self.ip_label.pack(anchor="w", pady=2)
        
        # SSID
        self.ssid_label = ctk.CTkLabel(
            network_frame,
            text="SSID: DELLEMC12",
            font=("Consolas", 9),
            text_color=colors["subfg"]
        )
        self.ssid_label.pack(anchor="w", pady=2)
        
        # Upload/Download speeds
        self.speed_label = ctk.CTkLabel(
            network_frame,
            text="1.1 Mbps / 61.7 Mbps",
            font=("Consolas", 9),
            text_color=colors["subfg"]
        )
        self.speed_label.pack(anchor="w", pady=2)
        
        # Visual Input Section
        visual_frame = ctk.CTkFrame(right_container, fg_color="transparent")
        visual_frame.pack(fill="x")
        
        ctk.CTkLabel(
            visual_frame,
            text="VISUAL INPUT",
            font=("Consolas", 12, "bold"),
            text_color=colors["accent"]
        ).pack(anchor="w")
        
        # Camera control frame
        camera_control_frame = ctk.CTkFrame(visual_frame, fg_color="transparent")
        camera_control_frame.pack(fill="x", pady=(5, 10))
        
        # Camera on/off button
        self.camera_btn = ctk.CTkButton(
            camera_control_frame,
            text="📹 Camera: OFF",
            font=("Consolas", 10),
            fg_color=colors["error"],
            text_color="#ffffff",
            hover_color="#ff6666",
            command=self.toggle_camera,
            corner_radius=6,
            height=30
        )
        self.camera_btn.pack(side="left", padx=(0, 10))
        
        # Camera status indicator
        self.camera_status = ctk.CTkLabel(
            camera_control_frame,
            text="🔴 Camera Disabled",
            font=("Consolas", 9),
            text_color=colors["error"]
        )
        self.camera_status.pack(side="left")
        
        # Visual input frame (camera feed)
        self.visual_input = ctk.CTkFrame(
            visual_frame,
            fg_color=colors["visual_bg"],
            height=120,
            corner_radius=8
        )
        self.visual_input.pack(fill="x", pady=(0, 5))
        
        # Camera feed label
        self.camera_feed_label = ctk.CTkLabel(
            self.visual_input,
            text="📹 Camera Feed\n(Click Camera: ON to start)",
            font=("Consolas", 10),
            text_color=colors["subfg"]
        )
        self.camera_feed_label.pack(expand=True)
        
        # Initialize camera variables
        self.camera_active = False
        self.camera_capture = None
        self.camera_thread = None
        self.camera_running = False
        
        # Start updating temporal and network info
        self.update_temporal_info()
        self.update_network_info()
        self.setup_notifications_card(right_container)

    def setup_notifications_card(self, parent):
        colors = THEMES[self.theme]
        card = ctk.CTkFrame(parent, fg_color=colors["card"], corner_radius=12)
        card.pack(fill="x", pady=(10,0))
        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.pack(fill="x", padx=12, pady=(10,6))
        ctk.CTkLabel(hdr, text="Notifications", font=("Segoe UI", 14, "bold"), text_color=colors["fg"]).pack(side="left")
        self.notif_badge = ctk.CTkLabel(hdr, text="0", width=26, height=22, fg_color=colors["accent"], text_color="#ffffff")
        self.notif_badge.pack(side="right")
        self.notif_list = ctk.CTkScrollableFrame(card, fg_color="transparent")
        self.notif_list.pack(fill="x", padx=12, pady=(0,10))
        btn = ctk.CTkButton(card, text="Mark All as Read", fg_color=colors["btnbg"], text_color=colors["fg"], hover_color=colors["btnbg_hover"], command=self._mark_all_notifs_read)
        btn.pack(fill="x", padx=12, pady=(0,10))
        self.notifications = []

    def add_notification(self, title, body):
        colors = THEMES[self.theme]
        self.notifications.append({"title": title, "body": body, "time": datetime.datetime.now().strftime("%I:%M %p")})
        for w in self.notif_list.winfo_children():
            w.destroy()
        for n in self.notifications[-6:]:
            row = ctk.CTkFrame(self.notif_list, fg_color=colors["glass"], corner_radius=8)
            row.pack(fill="x", pady=6)
            ctk.CTkLabel(row, text=n["title"], font=("Segoe UI", 12, "bold"), text_color=colors["fg"]).pack(anchor="w", padx=10, pady=(6,0))
            ctk.CTkLabel(row, text=n["body"], font=("Segoe UI", 11), text_color=colors["subfg"]).pack(anchor="w", padx=10)
            ctk.CTkLabel(row, text=n["time"], font=("Segoe UI", 10), text_color=colors["subfg"]).pack(anchor="w", padx=10, pady=(0,6))
        self.notif_badge.configure(text=str(len(self.notifications)))

    def _mark_all_notifs_read(self):
        self.notifications = []
        for w in self.notif_list.winfo_children():
            w.destroy()
        self.notif_badge.configure(text="0")

    def open_control_panel(self):
        colors = THEMES[self.theme]
        panel = ctk.CTkToplevel(self.root)
        panel.title("Control Panel")
        panel.geometry("340x540")
        panel.transient(self.root)
        panel.grab_set()
        container = ctk.CTkFrame(panel, fg_color=colors["card"])
        container.pack(fill="both", expand=True)
        ctk.CTkLabel(container, text="Control Panel", font=("Segoe UI", 16, "bold"), text_color=colors["fg"]).pack(anchor="w", padx=16, pady=(16,8))
        items = ["Settings", "Agent", "Background", "Custom Hotword", "Custom Command", "Help", "About", "Updates"]
        for it in items:
            row = ctk.CTkFrame(container, fg_color=colors["glass"], corner_radius=8)
            row.pack(fill="x", padx=16, pady=6)
            ctk.CTkLabel(row, text=it, font=("Segoe UI", 12), text_color=colors["fg"]).pack(anchor="w", padx=12, pady=10)
    
    def update_temporal_info(self):
        """Update temporal information display safely."""
        try:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
            
            if hasattr(self, 'time_display') and self.time_display:
                self.time_display.configure(text=current_time)
            if hasattr(self, 'date_display') and self.date_display:
                self.date_display.configure(text=current_date)
        except Exception as e:
            print(f"Error updating temporal info: {e}")
        
        # Schedule next update
        if hasattr(self, 'root') and self.root.winfo_exists():
            self.root.after(1000, self.update_temporal_info)
    
    def update_network_info(self):
        """Update network information display safely."""
        try:
            # Get local IP address
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            if hasattr(self, 'ip_label') and self.ip_label:
                self.ip_label.configure(text=f"IP ADDRESS: {local_ip}")
            
            # Simulate network speeds (in real implementation, you'd get actual network stats)
            import random
            upload_speed = random.uniform(0.5, 2.0)
            download_speed = random.uniform(20.0, 100.0)
            
            if hasattr(self, 'speed_label') and self.speed_label:
                self.speed_label.configure(text=f"{upload_speed:.1f} Mbps / {download_speed:.1f} Mbps")
                
        except Exception as e:
            print(f"Error updating network info: {e}")
        
        # Schedule next update with longer interval
        if hasattr(self, 'root') and self.root.winfo_exists():
            self.root.after(10000, self.update_network_info)  # Reduced frequency

    def toggle_camera(self):
        """Toggle camera on/off."""
        if not CAMERA_AVAILABLE:
            self.add_to_chat("System", "❌ Camera not available. Install OpenCV: pip install opencv-python", "error")
            return
        
        if self.camera_active:
            self.stop_camera()
        else:
            self.start_camera()
    
    def start_camera(self):
        """Start the camera feed with improved reliability."""
        try:
            print("Starting camera...")
            
            if not CAMERA_AVAILABLE:
                self.add_to_chat("System", "❌ OpenCV not available. Install with: pip install opencv-python", "error")
                return
            
            # Stop any existing camera
            if self.camera_active:
                print("Stopping existing camera...")
                self.stop_camera()
            
            # Initialize camera capture
            print("Initializing camera capture...")
            self.camera_capture = cv2.VideoCapture(0)
            
            if not self.camera_capture.isOpened():
                self.add_to_chat("System", "❌ Could not open camera. Check if camera is connected.", "error")
                return
            
            print("Camera opened successfully")
            
            # Set camera properties
            self.camera_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera_capture.set(cv2.CAP_PROP_FPS, 30)
            
            # Test camera by reading multiple frames
            print("Testing camera...")
            # Single quick test read to avoid blocking the UI
            ret, test_frame = self.camera_capture.read()
            if not (ret and test_frame is not None):
                self.add_to_chat("System", "❌ Camera test failed. Cannot read frames.", "error")
                self.camera_capture.release()
                return
            print("Camera test successful")
            
            # Update UI
            colors = THEMES[self.theme]
            self.camera_btn.configure(
                text="📹 Camera: ON",
                fg_color=colors["success"],
                hover_color=colors["matrix_green"]
            )
            self.camera_status.configure(
                text="🟢 Camera Active",
                text_color=colors["success"]
            )
            
            # Update camera feed label to show loading
            self.camera_feed_label.configure(
                text="📹 Starting camera...",
                image=None
            )
            
            # Set camera state
            self.camera_active = True
            self.camera_running = True
            
            print("Starting camera thread...")
            # Start camera thread
            self.camera_thread = threading.Thread(target=self.camera_feed_loop, daemon=True)
            self.camera_thread.start()
            
            if self.camera_thread.is_alive():
                print("Camera thread started successfully")
                self.add_to_chat("SAM", "📹 Camera activated! You can now ask me 'What is this?' to analyze what I see.", "info")
            else:
                print("Camera thread failed to start")
                self.add_to_chat("System", "❌ Camera thread failed to start.", "error")
                self.stop_camera()
            
        except Exception as e:
            print(f"Error starting camera: {e}")
            self.add_to_chat("System", f"❌ Error starting camera: {str(e)}", "error")
            import traceback
            traceback.print_exc()
            self.stop_camera()
    
    def stop_camera(self):
        """Stop the camera feed."""
        try:
            print("Stopping camera...")
            self.camera_running = False
            self.camera_active = False
            
            # Wait briefly for camera thread to finish without freezing UI
            if hasattr(self, 'camera_thread') and self.camera_thread and self.camera_thread.is_alive():
                self.camera_thread.join(timeout=0.25)
                print("Camera thread stopped")
            
            # Release camera
            if hasattr(self, 'camera_capture') and self.camera_capture:
                self.camera_capture.release()
                self.camera_capture = None
                print("Camera released")
            
            # Update UI
            colors = THEMES[self.theme]
            self.camera_btn.configure(
                text="📹 Camera: OFF",
                fg_color=colors["error"],
                hover_color="#ff6666"
            )
            self.camera_status.configure(
                text="🔴 Camera Disabled",
                text_color=colors["error"]
            )
            
            # Reset camera feed display
            if hasattr(self, 'camera_feed_label') and self.camera_feed_label:
                self.camera_feed_label.configure(
                    text="📹 Camera Feed\n(Click Camera: ON to start)",
                    image=None
                )
                if hasattr(self.camera_feed_label, 'image'):
                    delattr(self.camera_feed_label, 'image')
            
            self.add_to_chat("SAM", "📹 Camera deactivated.", "info")
            
        except Exception as e:
            self.add_to_chat("System", f"❌ Error stopping camera: {str(e)}", "error")
            import traceback
            traceback.print_exc()
    
    def camera_feed_loop(self):
        """Main camera feed loop with improved reliability."""
        print("Camera feed loop started")
        frame_count = 0
        consecutive_failures = 0
        max_failures = 10
        
        while self.camera_running and self.camera_active:
            try:
                if not self.camera_capture or not self.camera_capture.isOpened():
                    print("Camera capture not available")
                    break
                
                ret, frame = self.camera_capture.read()
                if ret and frame is not None:
                    consecutive_failures = 0  # Reset failure counter
                    
                    # Store current frame for analysis
                    self.current_frame = frame.copy()
                    
                    # Convert frame to PIL Image
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(frame_rgb)
                    
                    # Resize for display (larger for better visibility)
                    display_size = (280, 100)
                    pil_image_resized = pil_image.resize(display_size, Image.Resampling.LANCZOS)
                    
                    # Convert to PhotoImage
                    photo_image = ImageTk.PhotoImage(pil_image_resized)
                    
                    # Update UI in main thread
                    try:
                        self.root.after(0, lambda img=photo_image, count=frame_count: self.update_camera_display(img, count))
                        frame_count += 1
                    except Exception as ui_error:
                        print(f"UI update error: {ui_error}")
                        
                else:
                    consecutive_failures += 1
                    print(f"Failed to read frame from camera (attempt {consecutive_failures})")
                    if consecutive_failures >= max_failures:
                        print("Too many consecutive failures, stopping camera")
                        break
                        
                time.sleep(0.033)  # ~30 FPS
                
            except Exception as e:
                consecutive_failures += 1
                print(f"Camera feed error: {e}")
                import traceback
                traceback.print_exc()
                if consecutive_failures >= max_failures:
                    break
                time.sleep(0.1)  # Wait a bit before retrying
        
        print("Camera feed loop ended")
        # Cleanup
        if self.camera_capture:
            self.camera_capture.release()
    
    def update_camera_display(self, photo_image, frame_count=0):
        """Update camera display in main thread with improved reliability."""
        try:
            if not hasattr(self, 'camera_feed_label') or not self.camera_feed_label:
                print("Camera feed label not available")
                return
            
            # Store reference to prevent garbage collection
            self.camera_feed_label.image = photo_image
            
            # Update the label configuration
            self.camera_feed_label.configure(
                image=photo_image,
                text="",
                compound="center"
            )
            
            # Avoid forcing full update which can stutter; idletasks is fine
            try:
                self.camera_feed_label.update_idletasks()
            except Exception:
                pass
            
            # Log successful updates every 30 frames
            if frame_count % 30 == 0:
                print(f"Camera display updated successfully (frame {frame_count})")
            
        except Exception as e:
            print(f"Error updating camera display: {e}")
            import traceback
            traceback.print_exc()
    
    def analyze_camera_image(self, query=""):
        """Analyze the current camera image using AI vision."""
        try:
            if not self.camera_active or not hasattr(self, 'current_frame'):
                return "❌ No camera feed available. Please activate the camera first."
            
            if not VISION_AVAILABLE:
                return "❌ Vision processing not available. Install required packages."
            
            # Convert frame to base64 for API
            _, buffer = cv2.imencode('.jpg', self.current_frame)
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # Try Google Vision API first
            if GOOGLE_VISION_API_KEY:
                result = self.analyze_with_google_vision(image_base64, query)
                if result:
                    return result
            
            # Fallback to Mistral AI with image description
            return self.analyze_with_mistral_vision(image_base64, query)
            
        except Exception as e:
            return f"❌ Error analyzing image: {str(e)}"
    
    def analyze_with_google_vision(self, image_base64, query=""):
        """Analyze image using Google Vision API."""
        try:
            url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_VISION_API_KEY}"
            
            # Prepare request
            request_data = {
                "requests": [
                    {
                        "image": {
                            "content": image_base64
                        },
                        "features": [
                            {
                                "type": "LABEL_DETECTION",
                                "maxResults": 10
                            },
                            {
                                "type": "TEXT_DETECTION",
                                "maxResults": 5
                            },
                            {
                                "type": "OBJECT_LOCALIZATION",
                                "maxResults": 5
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(url, json=request_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                analysis = self.parse_google_vision_response(data, query)
                return analysis
            else:
                return None  # Fallback to Mistral
                
        except Exception as e:
            print(f"Google Vision API error: {e}")
            return None
    
    def parse_google_vision_response(self, data, query=""):
        """Parse Google Vision API response."""
        try:
            if not data.get('responses') or not data['responses'][0]:
                return "🤖 I can see the image but couldn't analyze it properly."
            
            response = data['responses'][0]
            analysis_parts = []
            
            # Labels
            if 'labelAnnotations' in response:
                labels = [label['description'] for label in response['labelAnnotations'][:5]]
                analysis_parts.append(f"🔍 I can see: {', '.join(labels)}")
            
            # Objects
            if 'localizedObjectAnnotations' in response:
                objects = [obj['name'] for obj in response['localizedObjectAnnotations'][:3]]
                analysis_parts.append(f"📦 Objects detected: {', '.join(objects)}")
            
            # Text
            if 'textAnnotations' in response and len(response['textAnnotations']) > 1:
                text = response['textAnnotations'][0]['description'][:100]
                analysis_parts.append(f"📝 Text found: '{text}...'")
            
            if analysis_parts:
                result = " ".join(analysis_parts)
                if query:
                    result += f"\n\n🤔 Regarding your question '{query}': Based on what I can see, "
                    if any(word in result.lower() for word in query.lower().split()):
                        result += "the image appears to be related to your question."
                    else:
                        result += "the image doesn't seem directly related to your question."
                
                return result
            else:
                return "🤖 I can see the image but couldn't identify specific objects or text."
                
        except Exception as e:
            return f"❌ Error parsing vision response: {str(e)}"
    
    def analyze_with_mistral_vision(self, image_base64, query=""):
        """Analyze image using Mistral AI with image description."""
        try:
            # Create a simple description of the image for Mistral
            prompt = f"""
            I have an image from my camera. {f"The user is asking: '{query}'" if query else ""}
            
            Please describe what you think might be in this image and answer any questions the user has about it.
            Be helpful and descriptive, but also mention that this is an AI interpretation since I can't actually see the image.
            """
            
            response = self.mistral_chat(prompt)
            return f"🤖 {response}\n\n💡 Note: This is an AI interpretation since I can't directly analyze the image."
            
        except Exception as e:
            return f"❌ Error with AI analysis: {str(e)}"
    
    def get_camera_status(self):
        """Get detailed camera status for debugging."""
        status = {
            "camera_available": CAMERA_AVAILABLE,
            "camera_active": getattr(self, 'camera_active', False),
            "camera_running": getattr(self, 'camera_running', False),
            "camera_capture": getattr(self, 'camera_capture', None) is not None,
            "camera_thread": getattr(self, 'camera_thread', None) is not None,
            "camera_thread_alive": getattr(self, 'camera_thread', None) and getattr(self, 'camera_thread', None).is_alive() if hasattr(self, 'camera_thread') else False,
            "current_frame": hasattr(self, 'current_frame'),
            "camera_feed_label": hasattr(self, 'camera_feed_label')
        }
        
        if hasattr(self, 'camera_capture') and self.camera_capture:
            status["camera_opened"] = self.camera_capture.isOpened()
            if self.camera_capture.isOpened():
                ret, frame = self.camera_capture.read()
                status["can_read_frames"] = ret and frame is not None
                if ret and frame is not None:
                    status["frame_size"] = f"{frame.shape[1]}x{frame.shape[0]}"
        
        return status
    
    def test_camera_simple(self):
        """Simple camera test method."""
        try:
            if not CAMERA_AVAILABLE:
                return "❌ OpenCV not available"
            
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return "❌ Cannot open camera"
            
            ret, frame = cap.read()
            cap.release()
            
            if ret and frame is not None:
                return f"✅ Camera test successful - Frame size: {frame.shape[1]}x{frame.shape[0]}"
            else:
                return "❌ Cannot read frames from camera"
                
        except Exception as e:
            return f"❌ Camera test error: {str(e)}"

    def setup_chat_area(self) -> None:
        """
        Set up the chat area with modern sleek design and refined chat bubbles.
        """
        colors = THEMES[self.theme]
        
        # Modern chat header with rounded top corners
        chat_header = ctk.CTkFrame(
            self.center_panel, 
            fg_color=colors["card"], 
            height=64, 
            corner_radius=16,
            border_width=1,
            border_color=colors.get("glass_border", colors["input_border"])
        )
        chat_header.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 4))
        chat_header.pack_propagate(False)
        
        # Header content with better spacing
        header_left = ctk.CTkFrame(chat_header, fg_color="transparent")
        header_left.pack(side="left", fill="y", padx=24, pady=12)
        
        # Title with icon
        title_row = ctk.CTkFrame(header_left, fg_color="transparent")
        title_row.pack(anchor="w")
        
        ctk.CTkLabel(
            title_row,
            text="💬",
            font=("SF Pro Display", 18) if platform.system() == "Darwin" else ("Segoe UI", 18),
            text_color=colors["accent"]
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(
            title_row, 
            text="Chat with SAM",
            font=("SF Pro Display", 17, "bold") if platform.system() == "Darwin" else ("Segoe UI", 17, "bold"), 
            text_color=colors["fg"]
        ).pack(side="left")
        
        self.chat_status = ctk.CTkLabel(
            header_left, 
            text="● Ready to assist",
            font=("SF Pro Display", 12) if platform.system() == "Darwin" else ("Segoe UI", 12), 
            text_color=colors["success"]
        )
        self.chat_status.pack(anchor="w", pady=(4, 0))
        
        # Header right controls with modern pill buttons
        header_right = ctk.CTkFrame(chat_header, fg_color="transparent")
        header_right.pack(side="right", fill="y", padx=24, pady=12)
        
        # Clear button with modern styling
        clear_btn = ctk.CTkButton(
            header_right, 
            text="🗑️ Clear",
            font=("SF Pro Display", 11) if platform.system() == "Darwin" else ("Segoe UI", 11), 
            fg_color=colors["btnbg"], 
            text_color=colors["error"],
            hover_color=colors["hover"], 
            command=self.clear_chat, 
            corner_radius=20,  # Pill shape
            height=32,
            width=80
        )
        clear_btn.pack(side="right", padx=(8, 0))
        
        # Export button
        export_btn = ctk.CTkButton(
            header_right, 
            text="📥 Export",
            font=("SF Pro Display", 11) if platform.system() == "Darwin" else ("Segoe UI", 11), 
            fg_color=colors["btnbg"], 
            text_color=colors["subfg"],
            hover_color=colors["hover"], 
            command=self.export_chat, 
            corner_radius=20,
            height=32,
            width=80
        )
        export_btn.pack(side="right", padx=0)
        
        # Chat container with scrollable frame
        chat_container = ctk.CTkFrame(self.center_panel, fg_color=colors["chat_bg"])
        chat_container.grid(row=1, column=0, sticky="nsew")
        chat_container.grid_rowconfigure(0, weight=1)  # Allow content to expand
        chat_container.grid_columnconfigure(0, weight=1)
        
        # Create scrollable frame for chat bubbles - use grid for proper expansion
        self.chat_scrollable_frame = ctk.CTkScrollableFrame(
            chat_container,
            fg_color=colors["chat_bg"],
            corner_radius=0
        )
        self.chat_scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=16, pady=10)

        # Always-visible scrollbar for chat area + mouse wheel support
        try:
            canvas = getattr(self.chat_scrollable_frame, "_parent_canvas", None)
            if canvas:
                self.chat_scrollbar = ctk.CTkScrollbar(
                    chat_container,
                    command=canvas.yview,
                    fg_color=colors["card"],
                    button_color=colors["accent"],
                    button_hover_color=colors["accent_hover"],
                )
                self.chat_scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
                canvas.configure(yscrollcommand=self.chat_scrollbar.set)

                # Bind wheel events for consistent scrolling across platforms
                canvas.bind("<MouseWheel>", self._on_chat_wheel)
                canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
                canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        except Exception:
            pass

        # Planner step panel (hidden by default, shown when multi-intent runs)
        try:
            self.planner_panel = PlannerStepPanel(chat_container, theme=self.theme)
            # Initially hide; will be shown via start_planner_visual
            self.planner_panel.hide()
        except Exception:
            self.planner_panel = None

    def setup_input_area(self) -> None:
        """
        Set up the modern AI input area with unified island design.
        """
        colors = THEMES[self.theme]
        
        # Main input container - placed in right transcript panel
        input_container = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        input_container.grid(row=2, column=0, sticky="ew", padx=8, pady=(4, 12))
        
        # Voice visualizer (hidden by default)
        self.voice_visualizer = VoiceVisualizer(
            input_container,
            theme=self.theme
        )
        self.voice_visualizer.pack(fill="x", pady=(0, 8))
        self.voice_visualizer.pack_forget()
        
        # Unified Input Bar (The Island)
        self.input_frame = ctk.CTkFrame(
            input_container, 
            fg_color=colors["card"], 
            corner_radius=20,
            border_width=1,
            border_color=colors.get("glass_border", colors["input_border"]),
            height=44
        )
        self.input_frame.pack(fill="x", anchor="center")
        
        # Inner packing for the island
        # Left: Attach (+)
        self.attach_btn = ctk.CTkButton(
            self.input_frame,
            text="+",
            width=36,
            height=36,
            corner_radius=18,
            fg_color="transparent",
            text_color=colors["subfg"],
            hover_color=colors["hover"],
            font=("Segoe UI", 20),
            command=self.open_file_browser
        )
        self.attach_btn.pack(side="left", padx=(8, 4), pady=4)
        
        # Center: Text Input
        self.input_entry = ctk.CTkTextbox(
            self.input_frame,
            font=("SF Pro Display", 14) if platform.system() == "Darwin" else ("Segoe UI", 14), 
            fg_color="transparent",
            text_color=colors["fg"], 
            border_width=0,
            height=40,
            wrap="word",
            activate_scrollbars=False
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=8, pady=6)
        
        # Bind keys
        self.input_entry.bind("<KeyPress>", self.on_input_key_press)
        
        # Right: Mic & Send
        
        # Mic Button
        self.voice_btn = ctk.CTkButton(
            self.input_frame, 
            text="🎤",
            font=("Segoe UI", 16),
            width=36,
            height=36,
            corner_radius=18,
            fg_color="transparent",
            text_color=colors["subfg"],  # Default color
            hover_color=colors["hover"],
            command=self.toggle_voice_input
        )
        self.voice_btn.pack(side="right", padx=(2, 4), pady=4)
        
        # Initialize placeholder text attribute to avoid errors
        self.placeholder_text = ""
        
        # Send Button 
        self.send_btn = ctk.CTkButton(
            self.input_frame, 
            text="➤",
            font=("Segoe UI", 14),
            width=36,
            height=36,
            corner_radius=18,
            fg_color=colors["accent"],
            text_color="#ffffff",
            hover_color=colors["accent_hover"],
            command=self.process_input
        )
        self.send_btn.pack(side="right", padx=(4, 8), pady=4)
        


    
    def open_file_browser(self):
        """Open file browser to attach files."""
        from tkinter import filedialog
        file_path = filedialog.askopenfilename()
        if file_path:
            self.input_entry.insert("end", f" [Attached: {os.path.basename(file_path)}] ")
            self.add_to_chat("System", f"File attached: {file_path}", "system")

    def process_input(self):
        """Process the user input from the text box."""
        self.on_user_input()

    def on_input_key_press(self, event):
        """Handle key presses in the text input."""
        if event.keysym == "Return" and not event.state & 0x1:  # Return without Shift
            self.on_user_input()
            return "break"  # Prevent default behavior
    
    def _quick_suggestion(self, suggestion):
        """Handle quick suggestion clicks."""
        suggestion_map = {
            "🌤️ Weather": "weather",
            "🧮 Calculate": "calculate 2 + 2",
            "🔍 Search": "search python programming",
            "💻 System": "system info",
            "🧭 Navigate": "show desktop",
            "✨ Multi‑step": "open youtube and play a song and open google and search cats",
        }
        
        if suggestion in suggestion_map:
            self.input_entry.delete("1.0", tk.END)
            self.input_entry.insert("1.0", suggestion_map[suggestion])
            self.on_user_input()

        # Add a tip hint below input suggesting multi‑step commands

    def show_placeholder(self) -> None:
        """Show placeholder text in the input entry if empty."""
        current_text = self.input_entry.get("1.0", tk.END).strip()
        if not current_text or current_text == self.placeholder_text:
            self.input_entry.delete("1.0", tk.END)
            self.input_entry.insert("1.0", self.placeholder_text)
            self.input_entry.configure(text_color=THEMES[self.theme]["subfg"])

    def hide_placeholder(self) -> None:
        """Hide the placeholder text from the input entry if present."""
        current_text = self.input_entry.get("1.0", tk.END).strip()
        if current_text == self.placeholder_text:
            self.input_entry.delete("1.0", tk.END)
            self.input_entry.configure(text_color=THEMES[self.theme]["inputfg"])

    def on_input_focus_in(self, event: object) -> None:
        """Event handler for input entry focus in; hides placeholder."""
        self.hide_placeholder()

    def on_input_focus_out(self, event: object) -> None:
        """Event handler for input entry focus out; shows placeholder."""
        self.show_placeholder()

    # ===== Planner visualization callbacks (modular, easy to replace) =====
    def start_planner_visual(self, steps):
        """Show the planner panel with provided steps and a toast notification."""
        try:
            if getattr(self, 'planner_panel', None) is not None:
                self.planner_panel.set_steps(steps)
            if getattr(self, 'toast', None):
                self.toast.show(f"Planning {len(steps)} step(s)", kind="info")
        except Exception:
            pass

    def notify_step_start(self, index, step):
        try:
            if getattr(self, 'planner_panel', None) is not None:
                self.planner_panel.update_step(index, status="running")
            if getattr(self, 'toast', None):
                self.toast.show(f"Step {index} started: {step}", kind="info", duration_ms=1600)
        except Exception:
            pass

    def notify_step_finish(self, index, step, success=True, message=None, elapsed=None):
        try:
            if getattr(self, 'planner_panel', None) is not None:
                self.planner_panel.update_step(index, status=("success" if success else "error"), message=message, elapsed=elapsed)
            if getattr(self, 'toast', None):
                self.toast.show(
                    f"Step {index} {'✓' if success else '✗'} · {elapsed:.2f}s",
                    kind=("success" if success else "error"),
                    duration_ms=2200,
                )
        except Exception:
            pass

    def end_planner_visual(self):
        try:
            if getattr(self, 'toast', None):
                self.toast.show("Planner finished", kind="success", duration_ms=1800)
        except Exception:
            pass

    def setup_status_bar(self) -> None:
        """
        Set up the status bar with Copilot-style design.
        """
        colors = THEMES[self.theme]
        
        self.status_bar = ctk.CTkFrame(
            self.root, 
            fg_color=colors["card"], 
            height=30, 
            corner_radius=0
        )
        self.status_bar.pack(side="bottom", fill="x")
        self.status_bar.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.status_bar, 
            text="Ready",
            font=("Segoe UI", 10), 
            text_color=colors["subfg"], 
            anchor="w"
        )
        self.status_label.pack(side="left", padx=20, pady=5)
        
        self.connection_status = ctk.CTkLabel(
            self.status_bar, 
            text="🟢 AI Ready",
            font=("Segoe UI", 10), 
            text_color=colors["success"]
        )
        self.connection_status.pack(side="right", padx=20, pady=5)
        
        # Gmail status indicator
        self.gmail_status = ctk.CTkLabel(
            self.status_bar, 
            text="📧 Gmail: Not Configured",
            font=("Segoe UI", 10), 
            text_color=colors["warning"]
        )
        self.gmail_status.pack(side="right", padx=10, pady=5)

    def setup_speech_recognition(self) -> None:
        """
        Set up the speech recognition engine and microphone.
        """
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
            self.mic_available = True
            self.connection_status.configure(text="🟢 Mic Ready")
        except Exception:
            self.mic_available = False
            self.connection_status.configure(text="🔴 No Mic", text_color=THEMES[self.theme]["error"])

    def change_theme(self, new_theme):
        """Change the application theme safely without freezing."""
        if new_theme not in THEMES:
            return
        
        try:
            self.theme = new_theme
            colors = THEMES[self.theme]
            
            # Update CustomTkinter appearance mode
            if new_theme == "copilot_light":
                ctk.set_appearance_mode("light")
            else:
                ctk.set_appearance_mode("dark")
            
            # Update all UI components with new theme (without animation overlay)
            self.apply_theme_to_widgets()

            # Create/update background gradient layer
            try:
                self._create_background_gradient()
            except Exception:
                pass
            
            # Update status
            if hasattr(self, 'status_label'):
                self.status_label.configure(text=f"🎨 Theme changed to {new_theme.title()}")
            
            # Save profile
            self.save_profile()
            
        except Exception as e:
            print(f"Error changing theme: {e}")
            # Fallback to safe theme
            self.theme = "copilot_dark"
            self.apply_theme_to_widgets()

    def apply_theme_to_widgets(self):
        """Apply the current theme to all UI widgets efficiently."""
        colors = THEMES[self.theme]
        
        try:
            # Update main window
            if hasattr(self, 'root'):
                self.root.configure(fg_color=colors["bg"])
                try:
                    # Redraw background gradient to match theme
                    self._draw_background_gradient(colors["gradient_start"], colors["gradient_end"]) 
                except Exception:
                    pass
            
            # Update main content area
            if hasattr(self, 'main_frame'):
                self.main_frame.configure(fg_color=colors["bg"])
            
            if hasattr(self, 'center_panel'):
                self.center_panel.configure(fg_color=colors["bg"])
            
            # Update right panel
            if hasattr(self, 'right_panel'):
                self.right_panel.configure(fg_color=colors["temporal_bg"])
            
            # Update sidebar
            if hasattr(self, 'sidebar'):
                self.sidebar.configure(fg_color=colors["sidebar"])
            
            # Update system panel
            if hasattr(self, 'system_panel'):
                self.system_panel.theme = self.theme
                self.system_panel.colors = colors
                self.system_panel.configure(fg_color=colors["panel_bg"])
            
            # Update chat area
            if hasattr(self, 'chat_scrollable_frame'):
                self.chat_scrollable_frame.configure(fg_color=colors["chat_bg"])
            
            # Update input area
            if hasattr(self, 'input_entry'):
                self.input_entry.configure(
                    fg_color=colors["entrybg"],
                    text_color=colors["inputfg"],
                    border_color=colors["input_border"]
                )
            
            # Update voice visualizer
            if hasattr(self, 'voice_visualizer'):
                self.voice_visualizer.theme = self.theme
                self.voice_visualizer.colors = colors
                self.voice_visualizer.configure(fg_color=colors["card"])
            
            # Update buttons
            if hasattr(self, 'send_button'):
                self.send_button.configure(
                    fg_color=colors["accent"],
                    hover_color=colors["hover"]
                )
            
            if hasattr(self, 'voice_button'):
                self.voice_button.configure(
                    fg_color=colors["accent"],
                    hover_color=colors["hover"]
                )
            
            # Update status bar
            if hasattr(self, 'status_bar'):
                self.status_bar.configure(fg_color=colors["card"])
            
            if hasattr(self, 'status_label'):
                self.status_label.configure(text_color=colors["subfg"])
            
            # Update temporal and network displays
            if hasattr(self, 'time_display'):
                self.time_display.configure(text_color=colors["fg"])
            
            if hasattr(self, 'date_display'):
                self.date_display.configure(text_color=colors["subfg"])
            
            if hasattr(self, 'ip_label'):
                self.ip_label.configure(text_color=colors["subfg"])
            
            if hasattr(self, 'ssid_label'):
                self.ssid_label.configure(text_color=colors["subfg"])
            
            if hasattr(self, 'speed_label'):
                self.speed_label.configure(text_color=colors["subfg"])
            
            if hasattr(self, 'visual_input'):
                self.visual_input.configure(fg_color=colors["visual_bg"])
            
            # Update sidebar theme components
            self.update_sidebar_theme(colors)
            
        except Exception as e:
            print(f"Theme update error: {e}")
            # Continue without crashing

    # ===== Gradient Background Helpers =====
    def _hex_to_rgb(self, hex_color):
        h = hex_color.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def _create_background_gradient(self):
        colors = THEMES[self.theme]
        self._draw_background_gradient(colors["gradient_start"], colors["gradient_end"]) 
        def _on_resize(event):
            try:
                self._draw_background_gradient(colors["gradient_start"], colors["gradient_end"]) 
            except Exception:
                pass
        self.root.bind("<Configure>", _on_resize)

    def _draw_background_gradient(self, start_hex, end_hex):
        try:
            w = max(1, self.root.winfo_width())
            h = max(1, self.root.winfo_height())
            start = self._hex_to_rgb(start_hex)
            end = self._hex_to_rgb(end_hex)
            img = Image.new('RGB', (w, h), start_hex)
            draw = ImageDraw.Draw(img)
            for y in range(h):
                t = y / float(max(h - 1, 1))
                r = int(start[0] + (end[0] - start[0]) * t)
                g = int(start[1] + (end[1] - start[1]) * t)
                b = int(start[2] + (end[2] - start[2]) * t)
                draw.line([(0, y), (w, y)], fill=(r, g, b))
            self.bg_gradient_image = ImageTk.PhotoImage(img)
            if not hasattr(self, 'bg_gradient_label'):
                self.bg_gradient_label = tk.Label(self.root, image=self.bg_gradient_image, borderwidth=0)
                self.bg_gradient_label.place(x=0, y=0, relwidth=1, relheight=1)
                # Send to back
                self.bg_gradient_label.lower()
            else:
                self.bg_gradient_label.configure(image=self.bg_gradient_image)
        except Exception:
            pass
    
    def update_sidebar_theme(self, colors):
        """Update sidebar components with new theme colors safely."""
        try:
            # Update title labels
            if hasattr(self, 'title_label'):
                self.title_label.configure(text_color=colors["accent"])
            
            if hasattr(self, 'subtitle_label'):
                self.subtitle_label.configure(text_color=colors["subfg"])
            
            # Update status indicator
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(fg_color=colors["success"])
            
            # Update hotword button
            if hasattr(self, 'hotword_btn'):
                self.hotword_btn.configure(
                    fg_color=colors["btnbg"],
                    text_color=colors["btnfg"],
                    hover_color=colors["btnactive"]
                )
            
            # Update weather label
            if hasattr(self, 'weather_label'):
                self.weather_label.configure(text_color=colors["subfg"])
                
        except Exception as e:
            print(f"Sidebar theme update error: {e}")
            # Continue without crashing
    
    def update_menu_theme(self, colors):
        """Update menu colors with new theme safely."""
        try:
            # Menu updates are handled automatically by CustomTkinter
            pass
        except Exception:
            pass

    def change_language(self, new_language):
        """Change language with enhanced voice support for Hindi and Telugu."""
        self.language = new_language
        self.lang_code = LANGUAGES[self.language]["code"]
        self.sr_code = LANGUAGES[self.language]["sr_code"]
        self.current_tts_voice = LANGUAGES[self.language].get("tts_voice", None)
        
        # Update status and chat
        self.status_label.configure(text=f"Language changed to {self.language}")
        
        # Language-specific welcome messages
        welcome_messages = {
            "English": "Language switched to English. How can I help you today?",
            "Hindi": "भाषा हिंदी में बदल गई है। मैं आपकी कैसे मदद कर सकता हूं?",
            "Telugu": "భాష తెలుగులో మార్చబడింది. నేను మీకు ఎలా సహాయం చేయగలను?"
        }
        
        welcome_msg = welcome_messages.get(self.language, f"Language switched to {self.language}")
        self.add_to_chat("System", welcome_msg, "system")
        
        # Update TTS voice to match new language
        self.update_tts_settings()
        
        # Speak the welcome message in the new language
        threading.Thread(target=self.speak_text, args=(welcome_msg,), daemon=True).start()

    def add_to_chat(self, sender, message, msg_type="info"):
        """Add a message to the chat using modern chat bubbles."""
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        # Create chat bubble
        bubble = EnhancedChatBubble(
            self.chat_scrollable_frame,
            message=message,
            sender=sender,
            timestamp=timestamp
        )
        
        # Schedule scroll to bottom after widget is rendered
        self.root.after(50, self._scroll_to_bottom)
        
        # Store in conversation history
        self.conversation_history.append({
            "timestamp": timestamp,
            "sender": sender,
            "message": message,
            "type": msg_type
        })
        
        # Save profile (debounced)
        try:
            if hasattr(self, "_save_profile_after_id") and self._save_profile_after_id:
                self.root.after_cancel(self._save_profile_after_id)
        except Exception:
            pass
        try:
            # debounce writes to avoid frequent disk I/O stutter
            self._save_profile_after_id = self.root.after(800, self.save_profile)
        except Exception:
            # fallback in rare headless cases
            self.save_profile()
        
        # Show toast notification for errors
        if msg_type == "error":
            ModernPopup(self.root, "Error", message)

    def _on_chat_wheel(self, event):
        try:
            canvas = getattr(self.chat_scrollable_frame, "_parent_canvas", None)
            if not canvas:
                return
            delta = event.delta
            # Normalize delta across platforms
            step = -1 if delta > 0 else 1
            canvas.yview_scroll(step, "units")
        except Exception:
            pass

    def _maybe_scroll_to_bottom(self):
        """Legacy method - redirects to _scroll_to_bottom."""
        self._scroll_to_bottom()

    def _scroll_to_bottom(self):
        """Force scroll chat to bottom to show latest message."""
        try:
            canvas = getattr(self.chat_scrollable_frame, "_parent_canvas", None)
            if not canvas:
                return
            # Force update to ensure new widgets are rendered
            self.chat_scrollable_frame.update_idletasks()
            # Scroll to absolute bottom
            canvas.yview_moveto(1.0)
        except Exception as e:
            print(f"Scroll error: {e}")

    def on_user_input(self):
        """Handle user input from text entry or send button."""
        try:
            user_input = self.input_entry.get("1.0", tk.END).strip()
            if user_input == self.placeholder_text or not user_input:
                return
            if hasattr(self, 'logger'):
                self.logger.info(f"User input received: {user_input}")
            
            # Clear input immediately for better UX
            self.input_entry.delete("1.0", tk.END)
            self.show_placeholder()
            
            # Add user message to chat
            self.add_to_chat("User", user_input, "user")
            
            # Update status immediately
            current_lang = getattr(self, 'language', 'English')
            status_messages = {
                "English": "Processing your request...",
                "Hindi": "आपका अनुरोध संसाधित किया जा रहा है...",
                "Telugu": "మీ అభ్యర్థనను ప్రాసెస్ చేస్తున్నాను..."
            }
            status_msg = status_messages.get(current_lang, "Processing your request...")
            self.update_status(status_msg)
            
            # Process command with priority for common commands
            if self._is_quick_command(user_input):
                self._process_quick_command(user_input)
            else:
                # Show typing indicator for AI responses
                self.show_typing_indicator()
                # Process command in background thread with enhanced error handling
                try:
                    threading.Thread(target=self.process_command, args=(user_input,), daemon=True).start()
                except Exception as e:
                    print(f"Error starting command thread: {e}")
                    if hasattr(self, 'logger'):
                        self.logger.error(f"Error starting command thread: {e}")
                    error_messages = {
                        "English": "Sorry, I encountered an error processing your request. Please try again.",
                        "Hindi": "क्षमा करें, आपके अनुरोध को संसाधित करने में त्रुटि आई। कृपया पुनः प्रयास करें।",
                        "Telugu": "క్షమించండి, మీ అభ్యర్థనను ప్రాసెస్ చేయడంలో లోపం ఉంది. దయచేసి మళ్లీ ప్రయత్నించండి."
                    }
                    error_msg = error_messages.get(current_lang, "Sorry, I encountered an error processing your request. Please try again.")
                    self.add_to_chat("System", error_msg, "error")
        except Exception as e:
            print(f"Error in on_user_input: {e}")
            if hasattr(self, 'logger'):
                self.logger.exception(f"Error in on_user_input: {e}")
            self.add_to_chat("System", f"Error processing input: {e}", "error")
    
    def _is_quick_command(self, command):
        """Check if command can be processed quickly without AI"""
        command_lower = command.lower()
        
        # Email commands should NOT be quick commands - they need full processing
        if any(email_cmd in command_lower for email_cmd in ['send gmail', 'send email', 'gmail', 'email']):
            return False
            
        quick_commands = [
            'help', 'clear', 'weather', 'time', 'date', 'system', 'screenshot',
            'music', 'notes', 'calc', 'web', 'news', 'ascii', 'hello', 'hi',
            'thanks', 'thank you', 'bye', 'goodbye', 'what can you do', 'who are you',
            'open', 'play', 'generate', 'code', '3d', 'model', 'viewer',
            'analyze screen', 'what\'s on my screen', 'read screen', 'screen analysis'  # Screen analysis
        ]
        return any(cmd in command_lower for cmd in quick_commands)
    
    def _process_quick_command(self, command):
        """Process quick commands with intelligent task execution"""
        command_lower = command.lower()
        try:
            if 'help' in command_lower:
                response = self.get_help_text()
            elif 'clear' in command_lower:
                self.clear_chat()
                return
            elif 'weather' in command_lower:
                response = self.get_weather_info()
            elif 'time' in command_lower:
                response = f"🕐 Current time: {datetime.datetime.now().strftime('%H:%M:%S')}"
            elif 'date' in command_lower:
                response = f"📅 Today's date: {datetime.datetime.now().strftime('%B %d, %Y')}"
            elif 'system' in command_lower:
                response = self.get_detailed_system_info()
            elif any(phrase in command_lower for phrase in ['analyze screen', 'what\'s on my screen', 'read screen', 'screen analysis', 'what is on my screen']):
                response = self.analyze_screen()
            elif 'screenshot' in command_lower:
                response = self.take_screenshot()
            elif 'music' in command_lower:
                response = self.handle_music_command()
            elif 'notes' in command_lower:
                response = self.intelligent_open_application("notepad", "Notepad")
            elif (
                (re.search(r"\bcalc(ulator)?\b", command_lower) and any(x in command_lower for x in ['open', 'launch', 'start']))
                or command_lower.strip() in ['calc', 'calculator']
            ):
                response = self.intelligent_open_application("calculator", "Calculator")
            elif 'web' in command_lower:
                response = self.intelligent_open_application("browser", "Web Browser")
            elif 'news' in command_lower:
                response = self.get_latest_news()
            elif 'ascii' in command_lower:
                response = self.ascii_art_generator()
            elif 'generate' in command_lower or 'code' in command_lower:
                # Extract the code generation prompt
                if 'generate' in command_lower:
                    prompt = command_lower.split('generate', 1)[1].strip()
                elif 'code' in command_lower:
                    prompt = command_lower.split('code', 1)[1].strip()
                else:
                    prompt = ""
                
                if prompt:
                    response = self.generate_code(prompt)
                else:
                    response = "🤖 Please specify what code you want me to generate. Try:\n• 'generate fibonacci'\n• 'generate factorial'\n• 'generate calculator'\n• 'generate palindrome'"
            elif '3d' in command_lower or 'model' in command_lower or 'viewer' in command_lower:
                if 'load' in command_lower or 'open' in command_lower or 'file' in command_lower:
                    response = self.load_custom_3d_model()
                else:
                    response = self.open_3d_model_viewer()
            elif any(greeting in command_lower for greeting in ['hello', 'hi', 'hey']):
                response = "👋 Hello! How can I help you today?"
            elif any(thanks in command_lower for thanks in ['thanks', 'thank you']):
                response = "😊 You're welcome! Is there anything else I can help with?"
            elif any(bye in command_lower for bye in ['bye', 'goodbye']):
                response = "👋 Goodbye! Feel free to come back anytime."
            elif 'what can you do' in command_lower or 'who are you' in command_lower:
                response = "🤖 I'm SAM, your AI assistant! I can help with calculations, web searches, system info, weather, music, and much more. Just ask!"
            elif 'open' in command_lower:
                # Intelligent application opening with search-first approach
                response = self.intelligent_open_command(command_lower)
            else:
                # Try intelligent task execution for unknown commands
                response = self.intelligent_task_execution(command_lower)
            
            self.root.after(0, lambda: self.display_response(response))
            
        except Exception as e:
            print(f"Error in _process_quick_command: {e}")
            response = "🤖 I encountered an error processing your command. Please try again."
            self.root.after(0, lambda: self.display_response(response))

    def intelligent_open_command(self, command_lower):
        """Fast application opening with direct routes for settings, apps, and folders."""
        try:
            # Extract the target from "open [target]" command
            if 'open' in command_lower:
                target = command_lower.replace('open', '').strip()
                
                tl = target.lower().strip()
                if 'settings' in tl:
                    sec = None
                    msec = re.search(r'settings\s+(?:for|about)\s+(\w+)', tl)
                    if msec:
                        sec = msec.group(1)
                    return self.fast_nav.open_settings(sec)

                if tl.startswith('file '):
                    q = tl.replace('file', '').strip()
                    return self.open_file_human_like(q, kind='file')

                if tl.startswith('folder '):
                    q = tl.replace('folder', '').strip()
                    return self.open_file_human_like(q, kind='folder')

                m_with = re.search(r"(file|document)\s+(.+?)\s+with\s+([\w\s]+)$", tl)
                if m_with:
                    q = m_with.group(2).strip()
                    app = m_with.group(3).strip()
                    return self.open_file_human_like(q, kind='file', open_with=app)
                if any(ext in tl for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.png', '.jpg', '.jpeg', '.gif', '.txt']):
                    q = target.strip()
                    return self.open_file_human_like(q, kind='file')

                return self._execute_intelligent_open(target)

                # If command also includes a YouTube play clause, trigger playback shortly after open
                try:
                    m = re.search(r"play\s+(.+?)\s+(?:on|in|from)\s+youtube\b", command_lower)
                    if m:
                        query = m.group(1).strip()
                        self.root.after(1600, lambda: self.add_to_chat("SAM", self._play_on_youtube_direct(query), "system"))
                except Exception:
                    pass
                
                return f"✅ Opening '{target}'"
            
            return "❓ Please specify what you want to open. Try: 'open recycle bin', 'open notepad', etc."
            
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def _execute_intelligent_open(self, target):
        """Execute opening with fast paths and direct actions."""
        try:
            target_lower = target.lower()
            typo_map = {
                'youtbue': 'youtube',
                'youtbe': 'youtube',
                'youtueb': 'youtube',
                'yooutube': 'youtube',
            }
            for wrong, right in typo_map.items():
                if wrong in target_lower:
                    target_lower = target_lower.replace(wrong, right)
                    target = target.replace(wrong, right)
            if 'youtube' in target_lower:
                m = re.search(r'youtube.*\bplay\s+(.+)$', target_lower)
                if m:
                    q = m.group(1).strip()
                    self.add_to_chat("SAM", self._play_on_youtube_direct(q), "system")
                    return f"📺 Playing '{q}' on YouTube"
                yt = YouTubeAutomation(strategy=getattr(self, 'automation_strategy', 'direct'))
                result = yt.open_youtube()
                self.add_to_chat("SAM", result, "system")
                return result
            
            if any(app in target_lower for app in ['recycle', 'bin', 'trash']):
                subprocess.Popen(['explorer.exe', 'shell:RecycleBinFolder'])
                self.add_to_chat("SAM", f"🗑️ Opening Recycle Bin...", "system")
                return "🗑️ Recycle Bin opened successfully!"
                
            elif any(app in target_lower for app in ['notepad', 'note', 'text']):
                subprocess.Popen(['notepad.exe'])
                self.add_to_chat("SAM", f"📝 Opening Notepad...", "system")
                return "📝 Notepad opened successfully!"
                
            elif any(app in target_lower for app in ['calc', 'calculator', 'calc']):
                subprocess.Popen(['calc.exe'])
                self.add_to_chat("SAM", f"🧮 Opening Calculator...", "system")
                return "🧮 Calculator opened successfully!"
                
            elif any(app in target_lower for app in ['paint', 'draw']):
                subprocess.Popen(['mspaint.exe'])
                self.add_to_chat("SAM", f"🎨 Opening Paint...", "system")
                return "🎨 Paint opened successfully!"
                
            elif platform.system().lower() == 'darwin' and any(app in target_lower for app in ['safari','chrome','terminal','finder','notes']):
                app = 'safari' if 'safari' in target_lower else ('chrome' if 'chrome' in target_lower else ('terminal' if 'terminal' in target_lower else ('finder' if 'finder' in target_lower else 'notes')))
                res = self.fast_nav.open_app(app)
                try:
                    if hasattr(self, 'memory_manager'):
                        self.memory_manager.add_recent_app(app)
                except Exception:
                    pass
                return res

            elif any(app in target_lower for app in ['explorer']):
                subprocess.Popen(['explorer.exe'])
                self.add_to_chat("SAM", f"📁 Opening File Explorer...", "system")
                return "📁 File Explorer opened successfully!"
                
            elif any(app in target_lower for app in ['task', 'manager']):
                subprocess.Popen(['taskmgr.exe'])
                self.add_to_chat("SAM", f"⚙️ Opening Task Manager...", "system")
                return "⚙️ Task Manager opened successfully!"
                
            elif any(app in target_lower for app in ['control', 'panel']):
                subprocess.Popen(['control.exe'])
                self.add_to_chat("SAM", f"⚙️ Opening Control Panel...", "system")
                return "⚙️ Control Panel opened successfully!"
                
            elif any(app in target_lower for app in ['cmd', 'command', 'prompt']):
                subprocess.Popen(['cmd.exe'])
                self.add_to_chat("SAM", f"💻 Opening Command Prompt...", "system")
                return "💻 Command Prompt opened successfully!"
                
            elif any(app in target_lower for app in ['powershell']):
                subprocess.Popen(['powershell.exe'])
                self.add_to_chat("SAM", f"💻 Opening PowerShell...", "system")
                return "💻 PowerShell opened successfully!"
                
            elif any(app in target_lower for app in ['wordpad']):
                subprocess.Popen(['wordpad.exe'])
                self.add_to_chat("SAM", f"📄 Opening WordPad...", "system")
                return "📄 WordPad opened successfully!"
            
            # Web applications
            elif any(app in target_lower for app in ['google', 'search']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://www.google.com")
                    self.add_to_chat("SAM", f"🌐 Opening Google...", "system")
                    return "🌐 Google opened successfully!"
                else:
                    self.open_website("https://www.google.com")
                    self.add_to_chat("SAM", f"🌐 Opening Google...", "system")
                    return "🌐 Google opened successfully!"
                
            elif any(app in target_lower for app in ['youtube', 'yt']):
                yt = YouTubeAutomation(strategy=getattr(self, 'automation_strategy', 'direct'))
                result = yt.open_youtube()
                self.add_to_chat("SAM", result, "system")
                return result
                
            elif any(app in target_lower for app in ['facebook', 'fb']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://www.facebook.com")
                else:
                    self.open_website("https://www.facebook.com")
                self.add_to_chat("SAM", f"📘 Opening Facebook...", "system")
                return "📘 Facebook opened successfully!"
                
            elif any(app in target_lower for app in ['twitter', 'x']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://twitter.com")
                else:
                    self.open_website("https://twitter.com")
                self.add_to_chat("SAM", f"🐦 Opening Twitter/X...", "system")
                return "🐦 Twitter/X opened successfully!"
                
            elif any(app in target_lower for app in ['instagram', 'ig']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://www.instagram.com")
                else:
                    self.open_website("https://www.instagram.com")
                self.add_to_chat("SAM", f"📷 Opening Instagram...", "system")
                return "📷 Instagram opened successfully!"
                
            elif any(app in target_lower for app in ['github', 'git']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://github.com")
                else:
                    self.open_website("https://github.com")
                self.add_to_chat("SAM", f"💻 Opening GitHub...", "system")
                return "💻 GitHub opened successfully!"
                
            elif any(app in target_lower for app in ['stackoverflow', 'stack']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://stackoverflow.com")
                else:
                    self.open_website("https://stackoverflow.com")
                self.add_to_chat("SAM", f"🔧 Opening Stack Overflow...", "system")
                return "🔧 Stack Overflow opened successfully!"
                
            elif any(app in target_lower for app in ['reddit']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://www.reddit.com")
                else:
                    self.open_website("https://www.reddit.com")
                self.add_to_chat("SAM", f"🤖 Opening Reddit...", "system")
                return "🤖 Reddit opened successfully!"
                
            elif any(app in target_lower for app in ['wikipedia', 'wiki']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://www.wikipedia.org")
                else:
                    self.open_website("https://www.wikipedia.org")
                self.add_to_chat("SAM", f"📚 Opening Wikipedia...", "system")
                return "📚 Wikipedia opened successfully!"
                
            elif any(app in target_lower for app in ['amazon']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://www.amazon.com")
                else:
                    self.open_website("https://www.amazon.com")
                self.add_to_chat("SAM", f"🛒 Opening Amazon...", "system")
                return "🛒 Amazon opened successfully!"
                
            elif any(app in target_lower for app in ['netflix']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://www.netflix.com")
                else:
                    self.open_website("https://www.netflix.com")
                self.add_to_chat("SAM", f"🎬 Opening Netflix...", "system")
                return "🎬 Netflix opened successfully!"
                
            elif any(app in target_lower for app in ['spotify']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://open.spotify.com")
                else:
                    self.open_website("https://open.spotify.com")
                self.add_to_chat("SAM", f"🎵 Opening Spotify...", "system")
                return "🎵 Spotify opened successfully!"
                
            elif any(app in target_lower for app in ['discord']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://discord.com")
                else:
                    self.open_website("https://discord.com")
                self.add_to_chat("SAM", f"💬 Opening Discord...", "system")
                return "💬 Discord opened successfully!"
                
            elif any(app in target_lower for app in ['whatsapp', 'wa']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://web.whatsapp.com")
                else:
                    self.open_website("https://web.whatsapp.com")
                self.add_to_chat("SAM", f"💬 Opening WhatsApp Web...", "system")
                return "💬 WhatsApp Web opened successfully!"
                
            elif any(app in target_lower for app in ['gmail', 'mail']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://mail.google.com")
                else:
                    self.open_website("https://mail.google.com")
                self.add_to_chat("SAM", f"📧 Opening Gmail...", "system")
                return "📧 Gmail opened successfully!"
                
            elif any(app in target_lower for app in ['drive', 'google drive']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://drive.google.com")
                else:
                    self.open_website("https://drive.google.com")
                self.add_to_chat("SAM", f"☁️ Opening Google Drive...", "system")
                return "☁️ Google Drive opened successfully!"
                
            elif any(app in target_lower for app in ['maps', 'google maps']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://maps.google.com")
                else:
                    self.open_website("https://maps.google.com")
                self.add_to_chat("SAM", f"🗺️ Opening Google Maps...", "system")
                return "🗺️ Google Maps opened successfully!"
                
            elif any(app in target_lower for app in ['translate', 'google translate']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://translate.google.com")
                else:
                    self.open_website("https://translate.google.com")
                self.add_to_chat("SAM", f"🌍 Opening Google Translate...", "system")
                return "🌍 Google Translate opened successfully!"
                
            elif any(app in target_lower for app in ['calendar', 'google calendar']):
                if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                    self.browser_controller.open_url_via_typing("https://calendar.google.com")
                else:
                    self.open_website("https://calendar.google.com")
                self.add_to_chat("SAM", f"📅 Opening Google Calendar...", "system")
                return "📅 Google Calendar opened successfully!"
            
            else:
                if 'folder' in target_lower:
                    q = target_lower.replace('folder', '').strip()
                    if platform.system().lower() == 'darwin':
                        res = self.fast_nav.open_folder(q)
                        try:
                            if hasattr(self, 'memory_manager'):
                                self.memory_manager.add_recent_file(q)
                        except Exception:
                            pass
                        return res
                    res = self.open_file_human_like(q, kind='folder')
                    try:
                        if hasattr(self, 'memory_manager'):
                            self.memory_manager.add_recent_file(q)
                    except Exception:
                        pass
                    return res
                q = target.strip()
                if any(ext in q.lower() for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.png', '.jpg', '.jpeg', '.gif', '.txt']):
                    return self.open_file_human_like(q, kind='file')
                if not target.startswith('http'):
                    domain = target.split()[0]
                    if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'system_launcher'):
                        ok = self.system_launcher.search_and_open(domain)
                        if ok:
                            self.add_to_chat("SAM", f"🚀 Opening {domain} via search", "system")
                            return f"🚀 {domain} opened via search."
                    if domain.lower() == 'youtube':
                        self.open_website("https://www.youtube.com")
                        return "📺 YouTube opened."
                    target = f"https://www.{domain}.com"
                self.open_website(target)
                self.add_to_chat("SAM", f"🌐 Opening {target}...", "system")
                return f"🌐 {target} opened successfully!"
                
        except Exception as e:
            return f"❌ Error opening {target}: {str(e)}"

    def intelligent_open_application(self, app_type, app_name):
        """Intelligent application opening with search simulation."""
        try:
            # Show searching animation first
            self.add_to_chat("SAM", f"🔍 Searching for {app_name}...", "system")
            
            # Simulate search delay for better UX
            self.root.after(1000, lambda: self._execute_app_open(app_type, app_name))
            
            return f"🔍 Searching for {app_name}... Please wait."
            
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def _execute_app_open(self, app_type, app_name):
        """Execute the application opening after search simulation."""
        try:
            if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'system_launcher'):
                ok = self.system_launcher.search_and_open(app_name)
                if ok:
                    self.add_to_chat("SAM", f"🚀 Opening {app_name} via search", "system")
                    return f"🚀 {app_name} opened via search."
            if app_type == "notepad":
                subprocess.Popen(['notepad.exe'])
                self.add_to_chat("SAM", f"📝 Opening {app_name}...", "system")
                return f"📝 {app_name} opened successfully!"
            elif app_type == "calculator":
                subprocess.Popen(['calc.exe'])
                self.add_to_chat("SAM", f"🧮 Opening {app_name}...", "system")
                return f"🧮 {app_name} opened successfully!"
            elif app_type == "browser":
                self.open_website("https://www.google.com")
                self.add_to_chat("SAM", f"🌐 Opening {app_name}...", "system")
                return f"🌐 {app_name} opened successfully!"
                
        except Exception as e:
            return f"❌ Error opening {app_name}: {str(e)}"

    def intelligent_task_execution(self, command):
        """Intelligent task execution for unknown commands."""
        try:
            # Try to understand the command and provide helpful response
            command_lower = command.lower()
            
            # Check for common patterns
            if any(word in command_lower for word in ['play', 'music', 'song']):
                return "🎵 I can help you play music! Try:\n• 'play music' - Opens your music folder\n• 'play [song] in youtube' - Searches YouTube\n• 'open spotify' - Opens Spotify"
                
            elif any(word in command_lower for word in ['search', 'find', 'look']):
                return "🔍 I can help you search! Try:\n• 'search [query]' - Google search\n• 'google [query]' - Google search\n• 'image [query]' - Image search\n• 'news [query]' - News search"
                
            elif any(word in command_lower for word in ['calculate', 'math', 'compute']):
                return "🧮 I can help with calculations! Try:\n• 'calculate 2 + 2'\n• 'what is 15 * 7'\n• 'solve 3x + 5 = 20'"
                
            elif any(word in command_lower for word in ['weather', 'temperature', 'forecast']):
                return "🌤️ I can help with weather! Try:\n• 'weather' - Current weather\n• 'weather forecast' - Extended forecast"
                
            elif any(word in command_lower for word in ['system', 'computer', 'pc', 'laptop']):
                return "🖥️ I can help with system info! Try:\n• 'system' - Detailed system info\n• 'system info' - System status\n• 'cpu usage' - CPU information"
                
            elif any(word in command_lower for word in ['screenshot', 'screen', 'capture']):
                return "📸 I can help with screenshots! Try:\n• 'screenshot' - Take a screenshot\n• 'screen capture' - Capture screen"
                
            elif any(word in command_lower for word in ['news', 'latest', 'current']):
                return "📰 I can help with news! Try:\n• 'news' - Latest news\n• 'latest news' - Current events"
                
            elif any(word in command_lower for word in ['code', 'program', 'generate']):
                return "💻 I can help with code! Try:\n• 'generate fibonacci' - Generate Fibonacci code\n• 'generate calculator' - Generate calculator code\n• 'generate factorial' - Generate factorial code"
                
            else:
                # Fallback to AI processing
                return "🤖 I'm not sure about that command. Let me process it with AI..."
                
        except Exception as e:
            return f"❌ Error: {str(e)}"



    def process_command(self, command):
        """Ultra-efficient command processing inspired by modern AI assistants."""
        start_time = time.time()
        try:
            command_lower = command.lower().strip()
            try:
                if hasattr(self, 'memory_manager'):
                    self.memory_manager.add_recent_command(command)
            except Exception:
                pass
            if hasattr(self, 'logger'):
                self.logger.info(f"Processing command: {command_lower}")

            # Origin/creator questions handled explicitly
            origin_patterns = [
                r"who\s+made\s+(you|sam)",
                r"who\s+created\s+(you|sam)",
                r"who\s+invented\s+(you|sam)",
                r"your\s+creator",
                r"who\s+is\s+your\s+creator",
                r"who\s+developed\s+(you|sam)",
            ]
            if any(re.search(p, command_lower) for p in origin_patterns):
                response = f"👨‍💻 I was created and built by {self.creator_name}."
                self._track_performance(start_time, "ai")
                self.root.after(0, lambda: self.display_response(response))
                return response
            
            mname = re.search(r"\bmy\s+name\s+is\s+([\w\s]+)$", command_lower)
            if mname:
                name = mname.group(1).strip().title()
                if hasattr(self, 'memory_manager'):
                    self.memory_manager.set_name(name)
                self.username = name
                try:
                    self.save_profile()
                except Exception:
                    pass
                response = f"👌 Got it, {name}. I’ll remember your name."
                self._track_performance(start_time, "ai")
                self.root.after(0, lambda: self.display_response(response))
                return response

            # ⚡ Ultra-fast quick command detection
            if self._is_quick_command(command_lower):
                response = self._process_quick_command(command_lower)
                self._track_performance(start_time, "quick")
                return response
            
            # 🎯 Intelligent command categorization for faster routing
            command_type = self._categorize_command(command_lower)
            if hasattr(self, 'logger'):
                self.logger.info(f"Categorized command as: {command_type}")
            
            # Show minimal typing indicator for AI processing
            self.show_typing_indicator()
            
            try:
                # Route to specialized handlers for maximum efficiency
                if command_type == "user_defined":
                    response = self.user_commands[command]
                elif command_type == "vision":
                    response = self._handle_vision_command(command)
                elif command_type == "system":
                    response = self._handle_system_command(command)
                elif command_type == "search":
                    response = self._handle_search_command(command)
                elif command_type == "calculation":
                    response = self._handle_calculation_command(command)
                elif command_type == "file":
                    response = self._handle_file_command(command)
                elif command_type == "navigation":
                    response = self._handle_navigation_command(command)
                elif command_type == "multi_intent":
                    response = self._handle_multi_intent_command(command)
                elif command_type == "media":
                    response = self._handle_media_command(command)
                elif command_type == "email":
                    response = self._handle_email_command(command)
                elif command_type == "whatsapp":
                    response = self._handle_whatsapp_command(command)
                elif command_type == "3d_model":
                    response = self._handle_3d_model_command(command)
                else:
                    # Use AI for complex queries with enhanced error handling
                    try:
                        response = self.mistral_chat(command)
                        if not response or response.strip() == "":
                            response = "🤖 I'm not sure how to respond to that. Could you try rephrasing your question or ask me something else?"
                    except Exception as ai_error:
                        print(f"AI processing error: {ai_error}")
                        if hasattr(self, 'logger'):
                            self.logger.error(f"AI processing error: {ai_error}")
                        response = self._get_fallback_response(command)
                self._track_performance(start_time, command_type)
                self.root.after(0, lambda: self.display_response(response))
                
            except Exception as e:
                self.hide_typing_indicator()
                error_msg = f"❌ Error processing command: {str(e)}"
                if hasattr(self, 'logger'):
                    self.logger.exception(error_msg)
                self.root.after(0, lambda: self.display_response(error_msg, "error"))
            
        except Exception as e:
            print(f"Error in process_command: {e}")
            if hasattr(self, 'logger'):
                self.logger.exception(f"Error in process_command: {e}")
            error_msg = "🤖 I'm having some technical difficulties right now. I can still help with system tasks, calculations, and basic information. Try using the quick action buttons or ask about system info!"
            self.root.after(0, lambda: self.display_response(error_msg, "error"))
    
    def _track_performance(self, start_time, command_type):
        """Track command performance for efficiency monitoring."""
        try:
            response_time = time.time() - start_time
            self.response_times.append(response_time)
            self.total_commands += 1
            
            # Keep only last 100 measurements for efficiency
            if len(self.response_times) > 100:
                self.response_times = self.response_times[-100:]
            
            # Calculate average response time
            if self.response_times:
                self.avg_response_time = sum(self.response_times) / len(self.response_times)
            
            # Log performance for optimization
            if response_time > 2.0:  # Log slow responses
                print(f"⚠️ Slow response ({response_time:.2f}s) for {command_type} command")
            elif response_time < 0.5:  # Log fast responses
                print(f"⚡ Fast response ({response_time:.2f}s) for {command_type} command")
                
        except Exception as e:
            print(f"Performance tracking error: {e}")
    
    def get_performance_stats(self):
        """Get performance statistics for efficiency monitoring."""
        try:
            uptime = time.time() - self.start_time
            commands_per_minute = (self.total_commands / uptime) * 60 if uptime > 0 else 0
            
            return {
                "total_commands": self.total_commands,
                "avg_response_time": f"{self.avg_response_time:.2f}s",
                "uptime": f"{uptime/3600:.1f}h",
                "commands_per_minute": f"{commands_per_minute:.1f}",
                "efficiency_score": f"{min(100, max(0, 100 - (self.avg_response_time * 20))):.0f}%"
            }
        except Exception as e:
            print(f"Error getting performance stats: {e}")
            return {"error": "Unable to get performance stats"}
    
    def _categorize_command(self, command):
        """Ultra-fast command categorization for efficient routing."""
        command_lower = command.lower()

        # Compound multi-intent connectors
        if re.search(r"\b(and|then|after that|next)\b", command_lower) or "," in command_lower:
            return "multi_intent"

        # Media priority: if both 'play' and 'youtube' are present, treat as media
        if ('play' in command_lower) and ('youtube' in command_lower):
            return "media"
        
        # Camera/vision commands
        if any(word in command_lower for word in ['what is this', 'what do you see', 'analyze', 'camera', 'vision', 'see']):
            return "vision"
        
        # 3D model commands
        if any(word in command_lower for word in ['3d', 'model', 'viewer', 'cube', 'sphere', 'cylinder', 'pyramid', 'load', 'stl', 'obj', 'ply']):
            return "3d_model"
        
        # User-defined commands
        if command in self.user_commands:
            return "user_defined"
            
        # System commands
        system_keywords = [
            'system', 'cpu', 'memory', 'battery', 'screenshot', 'open', 'close', 'kill',
            'volume', 'mute', 'unmute', 'brightness', 'display', 'screen', 'extend', 'duplicate',
            'second screen', 'pc screen', 'shutdown', 'restart', 'sleep', 'hibernate', 'lock', 'power'
        ]
        if any(keyword in command_lower for keyword in system_keywords):
            return "system"
        
        # Search commands
        search_keywords = ['search', 'google', 'find', 'look up', 'wikipedia', 'news']
        if any(keyword in command_lower for keyword in search_keywords):
            return "search"

        # Navigation commands (system navigation & window/folder actions)
        navigation_keywords = [
            'desktop','window','tab','switch','minimize','maximize','restore',
            'scroll','back','forward','settings','wifi','bluetooth','display','sound','network',
            'battery','storage','downloads','documents','pictures','photos','music','videos'
        ]
        if any(keyword in command_lower for keyword in navigation_keywords) or re.search(r"\bgo to\b", command_lower):
            return "navigation"
        
        # Calculation commands
        calc_keywords = ['calculate', 'compute', 'math', '+', '-', '*', '/', '=']
        if any(keyword in command_lower for keyword in calc_keywords):
            return "calculation"
        
        # File operations
        file_keywords = ['file', 'folder', 'directory', 'create', 'delete', 'move', 'copy']
        if any(keyword in command_lower for keyword in file_keywords):
            return "file"
        
        # Media commands
        media_keywords = ['play', 'music', 'video', 'song', 'volume']
        if any(keyword in command_lower for keyword in media_keywords):
            return "media"
        
        # WhatsApp commands (check before email to catch "send whatsapp" before "send")
        if 'whatsapp' in command_lower or ('wa' in command_lower.split() and any(w in command_lower for w in ['send', 'message', 'msg'])):
            return "whatsapp"
        
        # Email commands (exclude whatsapp to prevent conflict)
        email_keywords = ['email', 'gmail', 'mail']
        if any(keyword in command_lower for keyword in email_keywords) and 'whatsapp' not in command_lower:
            return "email"
        
        # Default to AI processing
        return "ai"
    
    def _handle_system_command(self, command):
        """Handle system-related commands with instant responses."""
        cmd = command.lower().strip()

        # Volume controls
        import re
        if re.search(r"\b(mute(\s+volume)?)\b", cmd):
            result = self._mute_system_volume(True)
            return f"🔈 Muted system volume. {result}"
        if re.search(r"\b(unmute(\s+volume)?)\b", cmd):
            result = self._mute_system_volume(False)
            return f"🔊 Unmuted system volume. {result}"
        m = re.search(r"\b(set|change|adjust)\s+volume\s+to\s+(\d{1,3})%?\b", cmd)
        if m:
            percent = int(m.group(2))
            percent = max(0, min(100, percent))
            ok, msg = self._set_system_volume_percent(percent)
            if ok:
                return f"🔊 Volume set to {percent}%"
            else:
                return f"ℹ️ {msg}"
        m = re.search(r"\bvolume\s+(up|down)(?:\s+by\s+(\d{1,3}))?\b", cmd)
        if m:
            direction = m.group(1)
            amount = int(m.group(2)) if m.group(2) else 5
            ok, msg = self._adjust_system_volume(direction, amount)
            if ok:
                return f"🔊 Volume {direction} by {amount}%"
            else:
                return f"ℹ️ {msg}"

        # Brightness controls
        m = re.search(r"\b(set|change|adjust)\s+brightness\s+to\s+(\d{1,3})%?\b", cmd)
        if m:
            percent = int(m.group(2))
            percent = max(0, min(100, percent))
            ok, msg = self._set_brightness_percent(percent)
            if ok:
                return f"💡 Brightness set to {percent}%"
            else:
                return f"ℹ️ {msg}"
        m = re.search(r"\bbrightness\s+(up|down)(?:\s+by\s+(\d{1,3}))?\b", cmd)
        if m:
            direction = m.group(1)
            amount = int(m.group(2)) if m.group(2) else 10
            ok, msg = self._adjust_brightness(direction, amount)
            if ok:
                return f"💡 Brightness {direction} by {amount}%"
            else:
                return f"ℹ️ {msg}"

        # Display preferences (projector modes)
        if any(k in cmd for k in ["extend", "duplicate", "second screen", "pc screen"]):
            mode = None
            if "extend" in cmd:
                mode = "extend"
            elif "duplicate" in cmd or "clone" in cmd:
                mode = "duplicate"
            elif "second screen" in cmd or "external" in cmd:
                mode = "external"
            elif "pc screen" in cmd or "internal" in cmd:
                mode = "internal"
            if mode:
                ok, msg = self._switch_display_mode(mode)
                if ok:
                    human = {
                        'extend': 'Extend',
                        'duplicate': 'Duplicate',
                        'external': 'Second screen only',
                        'internal': 'PC screen only'
                    }[mode]
                    return f"🖥️ Switched display to: {human}"
                else:
                    return f"ℹ️ {msg}"

        # Power management
        if any(k in cmd for k in ["shutdown", "restart", "sleep", "hibernate", "lock"]):
            action = None
            if "shutdown" in cmd:
                action = "shutdown"
            elif "restart" in cmd or "reboot" in cmd:
                action = "restart"
            elif "sleep" in cmd:
                action = "sleep"
            elif "hibernate" in cmd:
                action = "hibernate"
            elif "lock" in cmd:
                action = "lock"
            ok, msg = self._perform_power_action(action)
            if ok:
                icons = {
                    'shutdown': '⏻',
                    'restart': '🔁',
                    'sleep': '🌙',
                    'hibernate': '❄️',
                    'lock': '🔒'
                }
                return f"{icons.get(action, '⚙️')} Executing {action}..."
            else:
                return f"ℹ️ {msg}"

        if 'cpu' in cmd:
            cpu_percent = psutil.cpu_percent(interval=None)
            return f"🖥️ CPU Usage: {cpu_percent:.1f}%"
        elif 'memory' in cmd:
            memory = psutil.virtual_memory()
            return f"💾 Memory: {memory.percent:.1f}% used ({memory.used//(1024**3):.1f}GB/{memory.total//(1024**3):.1f}GB)"
        elif 'battery' in cmd:
            battery = psutil.sensors_battery()
            if battery:
                return f"🔋 Battery: {battery.percent:.1f}% ({'Plugged in' if battery.power_plugged else 'On battery'})"
            else:
                return "🔋 Battery info not available"
        elif 'performance' in cmd or 'stats' in cmd or 'efficiency' in cmd:
            stats = self.get_performance_stats()
            return f"⚡ Performance Stats:\n" + \
                   f"• Commands: {stats['total_commands']}\n" + \
                   f"• Avg Response: {stats['avg_response_time']}\n" + \
                   f"• Efficiency: {stats['efficiency_score']}\n" + \
                   f"• Commands/min: {stats['commands_per_minute']}"
        else:
            return self.get_detailed_system_info()

    # ===== System control helpers (Cross-platform) =====
    def _get_volume_controller(self):
        """Legacy compatibility wrapper. Now uses platform_utils for cross-platform support."""
        # Return None to indicate we're using the new cross-platform methods
        return None, None

    def _set_system_volume_percent(self, percent: int):
        """Set system volume using cross-platform utilities."""
        try:
            from core.platform_utils import set_volume
            return set_volume(percent)
        except ImportError:
            return False, "Platform utilities not available."
        except Exception as e:
            return False, f"Failed to set volume: {e}"

    def _adjust_system_volume(self, direction: str, amount: int):
        """Adjust system volume up or down using cross-platform utilities."""
        try:
            from core.platform_utils import adjust_volume
            return adjust_volume(direction, amount)
        except ImportError:
            return False, "Platform utilities not available."
        except Exception as e:
            return False, f"Failed to adjust volume: {e}"

    def _mute_system_volume(self, mute: bool):
        """Mute or unmute system volume using cross-platform utilities."""
        try:
            from core.platform_utils import mute_volume
            success, msg = mute_volume(mute)
            return msg if not success else ""
        except ImportError:
            return "Platform utilities not available."
        except Exception as e:
            return f"Failed to {'mute' if mute else 'unmute'}: {e}"

    def _set_brightness_percent(self, percent: int):
        """Set screen brightness using cross-platform utilities."""
        try:
            from core.platform_utils import set_brightness
            return set_brightness(percent)
        except ImportError:
            return False, "Platform utilities not available."
        except Exception as e:
            return False, f"Failed to set brightness: {e}"

    def _get_current_brightness(self):
        """Get current brightness using cross-platform utilities."""
        try:
            from core.platform_utils import get_brightness
            return get_brightness()
        except ImportError:
            return None
        except Exception:
            return None

    def _adjust_brightness(self, direction: str, amount: int):
        """Adjust brightness up or down using cross-platform utilities."""
        try:
            from core.platform_utils import adjust_brightness
            return adjust_brightness(direction, amount)
        except ImportError:
            return False, "Platform utilities not available."
        except Exception as e:
            return False, f"Failed to adjust brightness: {e}"

    def _switch_display_mode(self, mode: str):
        """Switch display mode using cross-platform utilities."""
        try:
            from core.platform_utils import switch_display_mode
            return switch_display_mode(mode)
        except ImportError:
            return False, "Platform utilities not available."
        except Exception as e:
            return False, f"Failed to switch display: {e}"

    def _perform_power_action(self, action: str):
        """Perform power action using cross-platform utilities."""
        try:
            from core.platform_utils import power_action
            return power_action(action)
        except ImportError:
            return False, "Platform utilities not available."
        except Exception as e:
            return False, f"Failed to execute power action: {e}"

    
    def _handle_search_command(self, command):
        """Handle search commands with instant results."""
        if command.lower().startswith("google ") or command.lower().startswith("search "):
            query = command.split(" ", 1)[1]
            return self.google_search(query)
        elif command.lower().startswith("image ") or command.lower().startswith("images "):
            query = command.split(" ", 1)[1]
            return self.google_image_search(query)
        elif command.lower().startswith("news "):
            query = command.split(" ", 1)[1]
            return self.google_news_search(query)
        else:
            return "🔍 Please specify what you want to search for."

    def _handle_navigation_command(self, command):
        """Handle natural language system navigation via the modular navigator."""
        try:
            if not hasattr(self, 'navigator') or self.navigator is None:
                return "🧭 Navigation module isn't available right now."
            return self.navigator.handle(command)
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Navigation handling error: {e}")
            return f"❌ Error handling navigation command: {e}"

    def _handle_multi_intent_command(self, command):
        """Handle compound commands by planning and executing sequentially."""
        try:
            if not hasattr(self, 'multi_planner') or self.multi_planner is None:
                return "🧩 Multi-intent module isn't available right now."
            return self.multi_planner.execute(command)
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Multi-intent handling error: {e}")
            return f"❌ Error handling multi-intent command: {e}"
    
    def _handle_calculation_command(self, command):
        """Handle calculation commands instantly."""
        return self.handle_calculation(command)
    
    def _handle_file_command(self, command):
        """Handle file operations with intelligent opening."""
        if 'open' in command.lower():
            return self.intelligent_open_command(command)
        else:
            return self.handle_file_operations(command)
    
    def _handle_media_command(self, command):
        """Handle media commands efficiently."""
        cmd = command.lower().strip()

        # Play on YouTube: tolerate extra words and punctuation
        patterns = [
            r"play\s+(.+?)\s+(?:on|in|from)\s+youtube\b",
            r"play\s+(?:on|in|from)\s+youtube\s+(.+?)\b",
            r"play\s+(.+?)\s+youtube\b",
        ]
        for pat in patterns:
            m = re.search(pat, cmd, flags=re.IGNORECASE)
            if m:
                query = m.group(1).strip()
                return self._play_on_youtube_direct(query)

        # Generic "play <query>" defaults to YouTube search
        m = re.search(r"\bplay\s+(.+)$", cmd, flags=re.IGNORECASE)
        if m and 'music' not in cmd:
            query = m.group(1).strip()
            return self._play_on_youtube_direct(query)

        # Music folder/open local player
        if 'play' in cmd and 'music' in cmd:
            return self.handle_music_command()

        if 'screenshot' in cmd:
            return self.take_screenshot()

        return "🎵 Media command recognized. Please be more specific."

    def _play_on_youtube_direct(self, query: str):
        """Play a song on YouTube using human-like automation."""
        try:
            # Use human-like automation directly
            self.add_to_chat("SAM", f"🎵 Opening YouTube and searching for '{query}'...", "system")
            
            yt = YouTubeAutomation(strategy="simulate")
            
            # Run the automation in a thread to not block the UI
            def play_async():
                try:
                    result = yt.play_song(query)
                    self.root.after(0, lambda: self.add_to_chat("SAM", result, "system"))
                except Exception as e:
                    # Fallback to direct URL if simulation fails
                    import webbrowser, urllib.parse
                    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
                    webbrowser.open(url)
                    self.root.after(0, lambda: self.add_to_chat("SAM", f"🔎 Opened YouTube search for '{query}' (fallback)", "system"))
            
            import threading
            threading.Thread(target=play_async, daemon=True).start()
            
            return f"🎬 Playing '{query}' on YouTube..."
            
        except Exception as e:
            # Last resort: just open the search URL
            try:
                import webbrowser, urllib.parse
                webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}")
                return f"🔎 Opened YouTube search for '{query}'"
            except:
                return f"❌ Error: {e}"
    
    def _handle_vision_command(self, command):
        """Handle vision/camera commands with AI analysis."""
        try:
            # Extract the question from the command
            command_lower = command.lower()
            
            # Camera test command
            if 'camera test' in command_lower:
                return self.test_camera_simple()
            
            # Camera debug command
            if 'camera debug' in command_lower or 'camera status' in command_lower:
                status = self.get_camera_status()
                status_text = "📹 Camera Status:\n"
                for key, value in status.items():
                    status_text += f"• {key}: {value}\n"
                return status_text
            
            if 'what is this' in command_lower or 'what do you see' in command_lower:
                query = command.replace('what is this', '').replace('what do you see', '').strip()
                if not query:
                    query = "What is in this image?"
            elif 'analyze' in command_lower:
                query = command.replace('analyze', '').strip()
                if not query:
                    query = "Please analyze this image"
            else:
                query = command
            
            # Analyze the camera image
            response = self.analyze_camera_image(query)
            return response
            
        except Exception as e:
            return f"❌ Error processing vision command: {str(e)}"
    
    def _handle_email_command(self, command):
        """Handle email commands with pattern matching."""
        # Email patterns for efficient matching
        email_patterns = [
            r'^send email to ([^ ]+) subject (.+?) body (.+)$',
            r'^send gmail to ([^ ]+) subject (.+?) body (.+)$',
            r'^send gmail ([^ ]+) subject (.+?) body (.+)$',
            r'^send email ([^ ]+) subject (.+?) body (.+)$',
            r'^email ([^ ]+) (.+) \| (.+)$',
            r'^email ([^ ]+) \| (.+) \| (.+)$',
            r'^email ([^ ]+) \| (.+)$',
            r'^email ([^ ]+): (.+)$',
            r'^email to ([^ ]+): (.+)$',
            r'^send gmail ([^ ]+): (.+)$',
            r'^send email ([^ ]+): (.+)$',
            r'^gmail ([^ ]+): (.+)$',
            r'^gmail ([^ ]+) \| (.+)$',
            r'^gmail ([^ ]+) \| (.+) \| (.+)$',
        ]
        
        for i, pat in enumerate(email_patterns):
            m = re.match(pat, command.strip(), re.IGNORECASE)
            if m:
                # Patterns with subject and body (3 groups)
                if i in [0, 1, 2, 3, 4, 5, 12, 13]:
                    to, subject, body = m.group(1), m.group(2), m.group(3)
                # Patterns with only recipient and body (2 groups)
                elif i in [6, 7, 8, 9, 10, 11]:
                    to, body = m.group(1), m.group(2)
                    subject = "Message from SAM"
                else:
                    continue
                
                return self.send_gmail(to, subject, body)
        
        # Handle simple email commands
        if command.lower().strip() in ["send gmail", "send email", "gmail", "email"]:
            return "📧 To send an email, please provide the recipient and message. Try:\n\n" + \
                  "• 'Send gmail friend@example.com: Hello there!'\n" + \
                  "• 'Email boss@company.com subject Meeting body Please join the meeting'\n" + \
                  "• 'Gmail mom@gmail.com: I'll be home late'\n\n" + \
                  "First, make sure Gmail is configured in Settings → Gmail Settings."
        
        return "📧 Email command not recognized. Please try a different format."
    
    def _handle_whatsapp_command(self, command):
        """Handle WhatsApp messaging commands with human-like browser automation."""
        try:
            command_lower = command.lower().strip()
            
            # WhatsApp command patterns to match
            # Pattern: send whatsapp to [name] saying [message]
            # Pattern: whatsapp [name] [message]
            # Pattern: message [name] on whatsapp [message]
            # Pattern: send message to [name] on whatsapp [message]
            
            whatsapp_patterns = [
                # "send whatsapp to Mom saying Hello there"
                r'^send\s+(?:a\s+)?whatsapp\s+(?:message\s+)?to\s+(.+?)\s+(?:saying|message|msg|:)\s+(.+)$',
                # "whatsapp Mom Hello there"
                r'^whatsapp\s+(.+?)\s+(?:saying|message|msg|:)\s+(.+)$',
                # "whatsapp Mom: Hello there"
                r'^whatsapp\s+(.+?):\s+(.+)$',
                # "message Mom on whatsapp Hello there"
                r'^(?:send\s+)?message\s+(.+?)\s+(?:on|via|through)\s+whatsapp\s+(?:saying|message|msg|:)?\s*(.+)$',
                # "send message to Mom on whatsapp saying Hello"
                r'^send\s+(?:a\s+)?message\s+to\s+(.+?)\s+(?:on|via|through)\s+whatsapp\s+(?:saying|message|msg|:)?\s*(.+)$',
                # Simple: "whatsapp Mom Hello" (name then message, separated by space after name)
                r'^whatsapp\s+(\S+)\s+(.+)$',
                # "wa Mom Hello" (shorthand)
                r'^wa\s+(\S+)\s+(.+)$',
                # "send wa to Mom saying Hello"
                r'^send\s+wa\s+to\s+(.+?)\s+(?:saying|message|msg|:)\s+(.+)$',
            ]
            
            contact_name = None
            message = None
            
            for pattern in whatsapp_patterns:
                match = re.match(pattern, command_lower, re.IGNORECASE)
                if match:
                    contact_name = match.group(1).strip()
                    message = match.group(2).strip()
                    break
            
            # If we found a match, send the message
            if contact_name and message:
                # Show progress in chat
                self.add_to_chat("SAM", f"💬 Opening WhatsApp and sending message to {contact_name}...", "system")
                
                # Use the WhatsApp automation to send the message
                if hasattr(self, 'whatsapp_automation'):
                    result = self.whatsapp_automation.send_message(contact_name, message)
                    return result
                else:
                    return "❌ WhatsApp automation is not available. Please restart SAM."
            
            # Handle "just open whatsapp" commands
            if command_lower in ['open whatsapp', 'whatsapp', 'open wa', 'open whatsapp web']:
                if hasattr(self, 'whatsapp_automation'):
                    result = self.whatsapp_automation.open_whatsapp()
                    return result
                else:
                    # Fallback: try to open app directly
                    import subprocess
                    subprocess.run(["open", "-a", "WhatsApp"], check=False)
                    return "💬 WhatsApp app opened."
            
            # No pattern matched - show help
            return ("💬 To send a WhatsApp message, try:\n\n"
                    "• 'Send whatsapp to Mom saying Hello!'\n"
                    "• 'Whatsapp John: Meeting at 5pm'\n"
                    "• 'Message Sarah on whatsapp I'll be late'\n"
                    "• 'WA Dad Call me when free'\n\n"
                    "Note: WhatsApp desktop app must be installed and logged in.")
                    
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.exception(f"Error in _handle_whatsapp_command: {e}")
            return f"❌ Error processing WhatsApp command: {str(e)}"

    def display_response(self, response, msg_type="jarvis"):
        """Display SAM's response in the chat with typing indicator."""
        try:
            # Remove typing indicator if present
            if hasattr(self, 'typing_indicator'):
                self.typing_indicator.destroy()
                delattr(self, 'typing_indicator')
            
            # Enhance response to be more conversational and human-like
            enhanced_response = self._enhance_response_for_conversation(response)
            if hasattr(self, 'logger'):
                self.logger.info(f"Displaying response: {enhanced_response}")
            
            # Add response to chat
            self.add_to_chat("SAM", enhanced_response, msg_type)
            self.update_status("Ready")
            
            # Speak response if TTS is enabled and not already speaking
            if enhanced_response and not self.speaking:
                threading.Thread(target=self.speak_text, args=(enhanced_response,), daemon=True).start()
        except Exception as e:
            print(f"Error in display_response: {e}")
            if hasattr(self, 'logger'):
                self.logger.exception(f"Error in display_response: {e}")
    
    def _enhance_response_for_conversation(self, response):
        """Enhance response to be more conversational without losing content."""
        if not response:
            return response
        # Normalize for checks
        response_lower = response.lower()

        # Important: never replace the user's informative content.
        # Only prepend or append lightweight conversational phrases.

        # Greeting augmentation (keep original content intact)
        if any(word in response_lower for word in ['hello', 'hi', 'hey']):
            # If the response is a short standalone greeting, add an emoji
            if len(response.strip()) <= 40:
                return "👋 " + response
            # Otherwise, keep content as-is
            return response

        # Task completion tone
        if any(word in response_lower for word in ['opened', 'launched', 'started', 'completed']):
            return "✅ " + response

        # Error tone
        if any(word in response_lower for word in ['error', 'failed', 'could not', 'unable']):
            return "⚠️ " + response

        # Information tone
        if any(word in response_lower for word in ['temperature', 'weather', 'system', 'cpu', 'memory']):
            return "ℹ️ " + response

        # Calculation tone
        if any(word in response_lower for word in ['equals', 'result', 'calculation', '=']):
            return "🧮 " + response

        # Search tone
        if any(word in response_lower for word in ['search', 'found', 'results']):
            return "🔎 " + response

        # Occasionally add a friendly prefix but preserve content
        if random.random() < 0.2:
            prefixes = [
                "Sure! ",
                "Absolutely! ",
                "Here you go: ",
                "Happy to help: "
            ]
            return random.choice(prefixes) + response

        return response
    
    def show_typing_indicator(self):
        """Show typing indicator while processing response."""
        try:
            if not hasattr(self, 'typing_indicator'):
                self.typing_indicator = EnhancedTypingIndicator(self.chat_scrollable_frame)
                self.chat_scrollable_frame._parent_canvas.yview_moveto(1.0)
        except Exception as e:
            print(f"Error showing typing indicator: {e}")
    
    def hide_typing_indicator(self):
        """Hide typing indicator."""
        try:
            if hasattr(self, 'typing_indicator'):
                self.typing_indicator.destroy()
                delattr(self, 'typing_indicator')
        except Exception as e:
            print(f"Error hiding typing indicator: {e}")
    
    def update_status(self, message):
        """Update the status bar with a message."""
        try:
            if hasattr(self, 'status_label'):
                self.status_label.configure(text=message)
            print(f"Status: {message}")
        except Exception as e:
            print(f"Error updating status: {e}")
    
    def update_hotword_btn_state(self):
        """Update the hotword button state based on listening status."""
        try:
            # This method updates hotword button appearance
            # Currently a placeholder - can be expanded for hotword functionality
            pass
        except Exception as e:
            print(f"Error updating hotword button state: {e}")

    def generate_ai_response(self, query):
        query_lower = query.lower()
        # Volcano improvement
        if "volcano" in query_lower:
            try:
                summary = wikipedia.summary("Volcano", sentences=2)
                return f"🌋 Volcano: {summary}"
            except Exception:
                return "🌋 A volcano is a rupture in the crust of a planetary-mass object, such as Earth, that allows hot lava, volcanic ash, and gases to escape from a magma chamber below the surface."
        knowledge_responses = {
            "python": "🐍 Python is a high-level programming language known for its simplicity and readability. It's widely used in web development, data science, AI, and automation.",
            "artificial intelligence": "🧠 Artificial Intelligence (AI) is the simulation of human intelligence in machines. It includes machine learning, natural language processing, and computer vision.",
            "machine learning": "🤖 Machine Learning is a subset of AI that enables computers to learn and make decisions from data without being explicitly programmed.",
            "computer": "💻 A computer is an electronic device that processes data according to instructions. It consists of hardware (physical components) and software (programs).",
            "internet": "🌐 The Internet is a global network of interconnected computers that communicate using standardized protocols, enabling worldwide information sharing.",
            "programming": "   Programming is the process of creating instructions for computers using programming languages. It involves problem-solving and logical thinking.",
            "database": "🗄️ A database is an organized collection of structured information stored electronically, designed for efficient data storage and retrieval.",
            "algorithm": "🔢 An algorithm is a step-by-step procedure for solving a problem or completing a task. It's fundamental to computer programming and problem-solving.",
        }
        for topic, explanation in knowledge_responses.items():
            if topic in query_lower:
                return explanation
        if query_lower.startswith(("what is", "what are", "define", "explain")):
            topic = query_lower.replace("what is", "").replace("what are", "").replace("define", "").replace("explain", "").strip()
            return f"🤔 I'd be happy to help explain {topic}. Could you be more specific about what aspect you'd like to know about?"
        if query_lower.startswith(("how to", "how do", "how can")):
            return f"🛠️ That's a great 'how-to' question! What specific aspect of '{query}' would you like me to focus on first?"
        if query_lower.startswith(("why", "why is", "why do", "why does")):
            return f"🔍 That's an interesting 'why' question about '{query}'. The reasons often involve multiple factors including historical, technical, and practical considerations."
        if len(query.split()) > 10:
            return "📖 That's quite a detailed question! I understand you're asking about a complex topic. Let me provide what information I can based on my knowledge."
        if any(char in query for char in "?"):
            return f"🧐 I understand you're asking about '{query}'. This is an interesting question that I'd be happy to help with based on my available knowledge."
        return f"🤖 I received your message about '{query}'. I'm here to help with information, explanations, and assistance with various tasks. Could you provide more specific details about what you'd like to know?"

    def get_weather_info(self):
        try:
            import random
            temperatures = list(range(15, 35))
            conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Clear"]
            temp = random.choice(temperatures)
            condition = random.choice(conditions)
            humidity = random.randint(30, 80)
            return f"🌤️ Weather in {CITY_NAME.title()}:\nTemperature: {temp}°C\nCondition: {condition}\nHumidity: {humidity}%\n\n(Note: This is simulated data. For real weather, please check a weather website.)"
        except Exception as e:
            print(f"Error in get_weather_info: {e}")
            return f"Sorry, I couldn't fetch weather information right now. Error: {str(e)}"

    def get_detailed_system_info(self):
        try:
            cpu_percent = psutil.cpu_percent(interval=None)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_total = round(memory.total / (1024**3), 2)
            memory_used = round(memory.used / (1024**3), 2)
            disk = psutil.disk_usage('/')
            disk_percent = round((disk.used / disk.total) * 100, 1)
            disk_total = round(disk.total / (1024**3), 2)
            disk_used = round(disk.used / (1024**3), 2)
            try:
                battery = psutil.sensors_battery()
                if battery:
                    battery_percent = battery.percent
                    battery_plugged = "Yes" if battery.power_plugged else "No"
                    battery_info = f"Battery: {battery_percent}% (Plugged: {battery_plugged})"
                else:
                    battery_info = "Battery: Not available (Desktop system)"
            except:
                battery_info = "Battery: Information not available"
            response = f"""💻 System Information:
🔧 CPU:
   Usage: {cpu_percent}%
   Cores: {cpu_count}
   Frequency: {cpu_freq.current:.2f} MHz
🧠 Memory:
   Usage: {memory_percent}%
   Used: {memory_used} GB / {memory_total} GB
💾 Disk:
   Usage: {disk_percent}%
   Used: {disk_used} GB / {disk_total} GB
🔋 {battery_info}
🖥️ Platform: {platform.system()} {platform.release()}"""
            return response
        except Exception as e:
            print(f"Error in get_detailed_system_info: {e}")
            return f"Sorry, I couldn't gather system information. Error: {str(e)}"

    def handle_calculation(self, command):
        try:
            expression = re.sub(r'[a-zA-Z\s]+', '', command)
            expression = expression.replace('x', '*').replace('÷', '/')
            if not expression:
                numbers = re.findall(r'\d+\.?\d*', command)
                if len(numbers) >= 2:
                    num1, num2 = float(numbers[0]), float(numbers[1])
                    if 'add' in command or 'plus' in command or '+' in command:
                        result = num1 + num2
                        return f"🧮 {num1} + {num2} = {result}"
                    elif 'subtract' in command or 'minus' in command or '-' in command:
                        result = num1 - num2
                        return f"🧮 {num1} - {num2} = {result}"
                    elif 'multiply' in command or 'times' in command or '*' in command:
                        result = num1 * num2
                        return f"🧮 {num1} × {num2} = {result}"
                    elif 'divide' in command or '/' in command:
                        if num2 != 0:
                            result = num1 / num2
                            return f"🧮 {num1} ÷ {num2} = {result}"
                        else:
                            return "Cannot divide by zero!"
            if expression:
                allowed_chars = set('0123456789+-*/.() ')
                if all(c in allowed_chars for c in expression):
                    result = eval(expression)
                    return f"🧮 {expression} = {result}"
            return "🧮 I couldn't understand the mathematical expression. Please try something like '5 + 3' or 'calculate 10 times 7'."
        except Exception as e:
            print(f"Error in handle_calculation: {e}")
            return f"🧮 Error in calculation: {str(e)}"

    def handle_file_operations(self, command):
        command_lower = command.lower()
        try:
            import re
            # Open any website if a URL is detected
            url_match = re.search(r'(https?://[^\s]+)', command)
            if url_match:
                webbrowser.open(url_match.group(1))
                return f"🌐 Opening {url_match.group(1)} in your browser!"

            # If command contains .com, .org, .net, etc., treat as website
            domain_match = re.search(r'([a-zA-Z0-9.-]+\.(com|org|net|in|io|gov|edu))', command)
            if domain_match:
                url = domain_match.group(1)
                if not url.startswith('http'):
                    url = 'https://' + url
                webbrowser.open(url)
                return f"🌐 Opening {url} in your browser!"

            # Known apps
            if "youtube" in command_lower:
                yt = YouTubeAutomation(strategy=getattr(self, 'automation_strategy', 'direct'))
                return yt.open_youtube()
            if "notepad" in command_lower or "text editor" in command_lower:
                subprocess.Popen(['notepad.exe'])
                return "📝 Notepad opened successfully!"
            elif "calculator" in command_lower:
                subprocess.Popen(['calc.exe'])
                return "🧮 Calculator opened successfully!"
            elif "paint" in command_lower:
                subprocess.Popen(['mspaint.exe'])
                return "🎨 Paint opened successfully!"
            elif "file explorer" in command_lower or "explorer" in command_lower:
                subprocess.Popen(['explorer.exe'])
                return "📁 File Explorer opened successfully!"
            elif "control panel" in command_lower:
                subprocess.Popen(['control.exe'])
                return "⚙️ Control Panel opened successfully!"
            elif "task manager" in command_lower:
                subprocess.Popen(['taskmgr.exe'])
                return "📊 Task Manager opened successfully!"
            elif "browser" in command_lower or "chrome" in command_lower:
                webbrowser.open('https://www.google.com')
                return "🌐 Web browser opened successfully!"

            # Try to open any app by name (e.g., open whatsapp)
            match = re.search(r'open ([a-zA-Z0-9_\- ]+)', command_lower)
            if match:
                app_name = match.group(1).strip().replace(" ", "")
                exe_name = app_name + ".exe"
                exe_path = shutil.which(exe_name)
                if exe_path:
                    subprocess.Popen([exe_path])
                    return f"🚀 {app_name.title()} opened successfully!"
                return f"❌ Could not find or open '{app_name}'. Please make sure it is installed and added to PATH."

            return "I can open any website (just say 'open facebook.com') or try to open any app by name (e.g., 'open whatsapp')."
        except Exception as e:
            print(f"Error in handle_file_operations: {e}")
            return f"Sorry, I couldn't open that application or website. Error: {str(e)}"

    def open_file_human_like(self, query, open_with=None, scope=None, max_results=5, kind='file'):
        q = str(query).strip().strip('"').strip("'")
        self.add_to_chat("SAM", f"🔍 Searching for '{q}'", "system")
        sysname = platform.system().lower()
        if sysname == 'darwin':
            matches = self._spotlight_search(q, scope, max_results, kind)
            if not matches:
                return f"❌ No files found for '{q}'"
            choice = self._choose_best_match(matches)
            if not choice:
                return f"❌ No suitable match for '{q}'"
            ok = self._mac_reveal_and_open(choice, app=open_with)
            if ok:
                return f"📂 Opened '{os.path.basename(choice)}'"
            return f"❌ Failed to open '{os.path.basename(choice)}'"
        home = os.path.expanduser('~')
        search_roots = [p for p in [os.path.join(home, 'Downloads'), os.path.join(home, 'Documents'), os.path.join(home, 'Desktop'), os.path.join(home, 'Pictures'), os.path.join(home, 'Music'), os.path.join(home, 'Videos')] if os.path.isdir(p)]
        patterns = [f"**/{q}", f"**/*{q}*"]
        candidates = []
        for root in search_roots:
            for pat in patterns:
                try:
                    for p in glob.glob(os.path.join(root, pat), recursive=True):
                        if kind == 'folder' and os.path.isdir(p):
                            candidates.append(p)
                        elif kind != 'folder' and os.path.isfile(p):
                            candidates.append(p)
                except Exception:
                    pass
        if not candidates:
            return f"❌ No files found for '{q}'"
        candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        target = candidates[0]
        if sysname.startswith('win'):
            try:
                os.startfile(target)
                return f"📂 Opened '{os.path.basename(target)}'"
            except Exception as e:
                return f"❌ Failed to open '{target}': {e}"
        elif sysname == 'linux':
            try:
                subprocess.Popen(['xdg-open', target])
                return f"📂 Opened '{os.path.basename(target)}'"
            except Exception as e:
                return f"❌ Failed to open '{target}': {e}"
        else:
            try:
                subprocess.Popen(['open', target])
                return f"📂 Opened '{os.path.basename(target)}'"
            except Exception as e:
                return f"❌ Failed to open '{target}': {e}"

    def _spotlight_search(self, query, scope=None, limit=10, kind='file'):
        term = query.strip()
        cmd = ['mdfind', f'kMDItemFSName == "*{term}*"c']
        if scope and os.path.isdir(scope):
            cmd = ['mdfind', '-onlyin', scope, f'kMDItemFSName == "*{term}*"c']
        try:
            out = subprocess.check_output(cmd, text=True)
            lines = [l.strip() for l in out.splitlines() if l.strip()]
            if kind == 'folder':
                files = [p for p in lines if os.path.isdir(p)]
            else:
                files = [p for p in lines if os.path.isfile(p)]
            files = files[:limit]
            return files
        except Exception:
            return []

    def _choose_best_match(self, paths):
        try:
            return sorted(paths, key=lambda p: os.path.getmtime(p), reverse=True)[0]
        except Exception:
            return paths[0] if paths else None

    def _mac_reveal_and_open(self, path, app=None):
        try:
            script = f'tell application "Finder" to reveal POSIX file "{path}"'
            subprocess.check_call(['osascript', '-e', script])
            subprocess.check_call(['osascript', '-e', 'tell application "Finder" to activate'])
            if app:
                script2 = f'tell application "{app}" to open POSIX file "{path}"'
                subprocess.check_call(['osascript', '-e', script2])
                return True
            subprocess.check_call(['osascript', '-e', 'tell application "Finder" to open selection'])
            return True
        except Exception:
            try:
                subprocess.Popen(['open', path])
                return True
            except Exception:
                return False

    def handle_search_query(self, query):
        search_term = query.lower()
        # SerpAPI Google Search fallback
        if search_term.startswith("google ") or search_term.startswith("search "):
            q = query.split(" ", 1)[1]
            return self.google_search(q)
        # SerpAPI Image Search
        if search_term.startswith("image ") or search_term.startswith("images "):
            q = query.split(" ", 1)[1]
            return self.google_image_search(q)
        # SerpAPI News Search
        if search_term.startswith("news "):
            q = query.split(" ", 1)[1]
            return self.google_news_search(q)
        if "youtube" in search_term:
            import re  # Ensure re module is imported in this scope
            match = re.search(r'play (.+?) (?:song )?in youtube', search_term)
            if match:
                song = match.group(1)
                return self._play_on_youtube_direct(song)
            else:
                self.open_website("https://www.youtube.com")
                return "📺 YouTube opened."
        search_keywords = ["search", "find", "look up", "what is", "who is", "tell me about", "explain", "define"]
        for keyword in search_keywords:
            search_term = search_term.replace(keyword, "").strip()
        if not search_term:
            return "What would you like me to search for or explain?"
        topic_responses = {
            "india": "🇮🇳 India is a diverse country in South Asia, known for its rich culture, history, and technological advancement. It's the world's largest democracy and second-most populous country.",
            "technology": "💻 Technology encompasses the application of scientific knowledge for practical purposes. It includes computers, AI, robotics, and emerging fields like quantum computing.",
            "space": "🚀 Space exploration involves the discovery and exploration of celestial structures in outer space. Notable achievements include moon landings, Mars rovers, and the International Space Station.",
            "history": "📚 History is the study of past events, civilizations, and human development. It helps us understand how societies evolved and learn from past experiences.",
            "science": "🔬 Science is the systematic study of the natural world through observation and experimentation. Major branches include physics, chemistry, biology, and earth sciences.",
            "health": "🏥 Health encompasses physical, mental, and social well-being. It involves proper nutrition, exercise, medical care, and maintaining a balanced lifestyle.",
            "education": "🎓 Education is the process of acquiring knowledge, skills, and values. It plays a crucial role in personal development and societal progress.",
            "environment": "🌱 The environment includes all living and non-living components of Earth. Environmental conservation is crucial for sustainable development and future generations.",
        }
        for topic, info in topic_responses.items():
            if topic in search_term:
                return f"📚 About {topic.title()}:\n\n{info}\n\nWould you like to know more about any specific aspect of {topic}?"
        return f"🔍 You're searching for information about '{search_term}'. This is an interesting topic! If you want more details, please specify or ask for a Wikipedia summary: 'wikipedia {search_term}'."

    def search_wikipedia(self, query):
        try:
            if not query:
                return "Please specify what you'd like to search on Wikipedia."
            wikipedia.set_lang(self.lang_code)
            summary = wikipedia.summary(query, sentences=3)
            page = wikipedia.page(query)
            response = f"📖 Wikipedia Summary for '{query}':\n\n{summary}\n\n🔗 Full article: {page.url}"
            return response
        except Exception as e:
            print(f"Error in search_wikipedia: {e}")
            return f"Error searching Wikipedia: {str(e)}"

    def get_latest_news(self):
        try:
            sample_news = [
                "🌍 Global Climate Summit addresses environmental challenges",
                "💻 New AI breakthrough in natural language processing",
                "🚀 Space mission successfully reaches Mars orbit",
                "💡 Scientists develop renewable energy breakthrough",
                "🏥 Medical research shows promising results for new treatment",
                "📱 Technology companies announce new innovations",
                "🌱 Sustainable development projects gain momentum worldwide",
                "🔬 Research institutions collaborate on scientific advancement"
            ]
            import random
            selected_news = random.sample(sample_news, 5)
            response = "📰 Latest News Headlines:\n\n" + "\n\n".join(selected_news)
            response += "\n\n(Note: These are sample headlines. For real news, please visit a news website.)"
            return response
        except Exception as e:
            print(f"Error in get_latest_news: {e}")
            return f"Sorry, I couldn't fetch news at the moment. Error: {str(e)}"

    def take_screenshot(self):
        try:
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(screenshots_dir, filename)
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            return f"📸 Screenshot saved as '{filename}' in the screenshots folder!"
        except Exception as e:
            print(f"Error in take_screenshot: {e}")
            return f"Sorry, I couldn't take a screenshot. Error: {str(e)}"

    def analyze_screen(self, question: str = None):
        """
        Capture screen, extract text via OCR, and analyze with AI.
        
        Args:
            question: Optional specific question about the screen content
        """
        try:
            self.add_to_chat("SAM", "🔍 Capturing and analyzing your screen...", "system")
            
            # Step 1: Capture screenshot
            screenshot = pyautogui.screenshot()
            
            # Save for reference
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(screenshots_dir, f"analysis_{timestamp}.png")
            screenshot.save(filepath)
            
            # Step 2: Extract text via OCR
            ocr_text = ""
            if OCR_AVAILABLE:
                try:
                    ocr_text = pytesseract.image_to_string(screenshot)
                    ocr_text = ocr_text.strip()
                except Exception as e:
                    print(f"OCR Error: {e}")
                    ocr_text = "(OCR unavailable - Tesseract may not be installed)"
            else:
                ocr_text = "(OCR not available - install pytesseract and Tesseract)"
            
            # Step 3: Analyze with AI (Gemini Vision if available)
            ai_analysis = self._analyze_screenshot_with_ai(screenshot, question, ocr_text)
            
            # Build response
            response_parts = ["📸 **Screen Analysis Results**\n"]
            
            if ocr_text and ocr_text != "(OCR unavailable - Tesseract may not be installed)" and ocr_text != "(OCR not available - install pytesseract and Tesseract)":
                # Truncate OCR text if too long
                display_ocr = ocr_text[:500] + "..." if len(ocr_text) > 500 else ocr_text
                response_parts.append(f"📝 **Text Found on Screen:**\n```\n{display_ocr}\n```\n")
            
            if ai_analysis:
                response_parts.append(f"🤖 **AI Analysis:**\n{ai_analysis}")
            else:
                response_parts.append("💡 *For better analysis, configure your Gemini API key in settings.*")
            
            response_parts.append(f"\n\n📁 Screenshot saved: `{filepath}`")
            
            return "\n".join(response_parts)
            
        except Exception as e:
            print(f"Error in analyze_screen: {e}")
            return f"❌ Screen analysis failed: {str(e)}"
    
    def _analyze_screenshot_with_ai(self, screenshot, question: str = None, ocr_text: str = ""):
        """Send screenshot to Gemini Vision API for analysis."""
        try:
            from config.settings import API_KEYS
            api_key = API_KEYS.get("gemini")
            
            if not api_key:
                return None
            
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            # Build the prompt
            if question:
                prompt = f"Analyze this screenshot and answer: {question}"
            else:
                prompt = """Analyze this screenshot and provide:
1. A brief description of what's visible on screen
2. Key information or text content
3. Any notable elements (apps, windows, content type)

Be concise and helpful."""
            
            # Add OCR context if available
            if ocr_text and len(ocr_text) > 10:
                prompt += f"\n\nOCR extracted text for context:\n{ocr_text[:1000]}"
            
            # Convert PIL Image to bytes
            import io
            img_byte_arr = io.BytesIO()
            screenshot.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Use Gemini Vision model
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content([
                prompt,
                {"mime_type": "image/png", "data": img_byte_arr}
            ])
            
            return response.text
            
        except ImportError:
            print("[INFO] google-generativeai not installed")
            return None
        except Exception as e:
            print(f"AI analysis error: {e}")
            return None
    
    def quick_screen_analysis(self):
        """Quick action button handler for screen analysis."""
        result = self.analyze_screen()
        self.add_to_chat("SAM", result, "system")

    def handle_music_command(self):
        try:
            if sys.platform.startswith('win'):
                subprocess.Popen(['start', 'wmplayer'], shell=True)
                return "🎵 Windows Media Player opened! You can now play your music."
            else:
                return "🎵 Please open your preferred music application manually."
        except Exception as e:
            print(f"Error in handle_music_command: {e}")
            return f"Sorry, I couldn't open the music player. Error: {str(e)}"

    def get_random_joke(self):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything! 😄",
            "Why did the computer go to the doctor? Because it had a virus! 🤣",
            "Why don't programmers like nature? It has too many bugs! 😂",
            "What do you call a bear with no teeth? A gummy bear! 🐻",
            "Why did the math book look so sad? Because it was full of problems! 📚",
            "What did the ocean say to the beach? Nothing, it just waved! 🌊",
            "Why don't eggs tell jokes? They'd crack each other up! 🥚",
            "What do you call a sleeping bull? A bulldozer! 🐂"
        ]
        import random
        return random.choice(jokes)

    def get_help_text(self):
        return """🤖 SAM Help - Available Commands:
📍 General Commands:
• "Hello" - Greet SAM
• "What time is it?" - Get current time
• "What's the date?" - Get current date
• "Weather" - Get weather information
• "Tell me a joke" - Get a random joke
🖥️ System Commands:
• "System info" - View system information
• "Take screenshot" - Capture screen
• "Open [app]" - Launch applications (notepad, calculator, etc.)
 🧭 Navigation:
 • "Show desktop" / "Switch window" / "Go to downloads"
 • "Open settings for wifi" / "Scroll down"
 • "Open YouTube" or "Play [song] in YouTube"
🔍 Information & Search:
• "What is [topic]" - Get explanations
• "Search [query]" - Search for information
• "Wikipedia [topic]" - Search Wikipedia
• "News" - Get latest headlines
📧 Email Commands:
• "Send gmail [recipient]: [message]" - Send email with default subject
• "Send gmail [recipient] subject [subject] body [message]" - Send email
• "Email [recipient] | [subject] | [message]" - Send email
• "Email [recipient]: [message]" - Send email with default subject
• "Email [recipient] subject [subject] body [message]" - Send email
• "Gmail [recipient]: [message]" - Send email with default subject
🧮 Utilities:
• "Calculate [expression]" - Perform calculations
• "Play music" - Open music player
 💫 Multi‑step Commands (natural language):
 • "open youtube and play a song and open google and search cats"
 • "open settings for bluetooth, then show desktop, then switch window"
 • "go to downloads and open calculator"
💻 Code Generation:
• "Generate fibonacci" - Generate Fibonacci sequence code
• "Generate factorial" - Generate factorial calculation code
• "Generate calculator" - Generate simple calculator code
• "Generate palindrome" - Generate palindrome checker code
• "Generate prime" - Generate prime number checker code
• "Generate dictionary" - Generate dictionary operations code
• "Generate class student" - Generate Student class example
• "Generate web scraper" - Generate web scraping code
• "Generate json" - Generate JSON operations code
🗣️ Voice Commands:
• Click the microphone button to use voice input
• All text commands work with voice too
⚙️ Gmail Setup:
• Go to Settings → Gmail Settings to configure email
• Enable 2-factor authentication on your Google account
• Generate an App Password (Google Account → Security → App Passwords)
• Use your Gmail address and the generated app password
💡 Tips:
• Type naturally - I understand conversational language
• Use the voice button for hands-free interaction
• Try asking about technology, science, or general knowledge topics
Need help with something specific? Just ask!"""

    def toggle_voice_input(self):
        """Toggle voice input on/off with enhanced visual feedback."""
        if not hasattr(self, 'mic_available') or not self.mic_available:
            self.add_to_chat("System", "Microphone not available. Please check your audio settings.", "error")
            return
        
        if self.is_listening:
            self.stop_listening()
            # Update button appearance
            self.voice_btn.configure(
                text="🎤 Voice",
                fg_color=THEMES[self.theme]["success"]
            )
            # Hide voice visualizer
            if hasattr(self, 'voice_visualizer'):
                self.voice_visualizer.pack_forget()
        else:
            self.start_listening()
            # Update button appearance
            self.voice_btn.configure(
                text="🎤 Listening...",
                fg_color=THEMES[self.theme]["error"]
            )
            # Show voice visualizer
            if hasattr(self, 'voice_visualizer'):
                self.voice_visualizer.pack(fill="x", pady=(0, 10))
                self.voice_visualizer.start_animation()

    def start_listening(self):
        """Start listening for voice input with Copilot-style feedback."""
        self.is_listening = True
        self.update_hotword_btn_state()
        self.update_status("Listening...")
        self.add_to_chat("System", "🎤 Listening for voice input... Speak now!", "system")
        threading.Thread(target=self.voice_recognition_thread, daemon=True).start()

    def stop_listening(self):
        """Stop listening for voice input with enhanced feedback."""
        self.is_listening = False
        self.update_hotword_btn_state()
        self.update_status("Ready")
        
        # Stop voice visualizer
        if hasattr(self, 'voice_visualizer'):
            self.voice_visualizer.stop_animation()
            self.voice_visualizer.pack_forget()

    def voice_recognition_thread(self):
        try:
            text, err = self.voice_mgr.listen_once(timeout=5, phrase_time_limit=8)
            if text:
                self.root.after(0, lambda: self.process_voice_input(text))
            else:
                if err == 'mic_unavailable':
                    self.root.after(0, lambda: self.add_to_chat("System", "Microphone not available.", "error"))
                elif err == 'network_error':
                    self.root.after(0, lambda: self.add_to_chat("System", "Network error during transcription.", "error"))
                elif err == 'no_speech':
                    self.root.after(0, lambda: self.add_to_chat("System", "Could not understand audio. Please try again.", "warning"))
                else:
                    self.root.after(0, lambda: self.add_to_chat("System", "Voice recognition error.", "error"))
        except Exception:
            self.root.after(0, lambda: self.add_to_chat("System", "Voice recognition error.", "error"))
        finally:
            self.root.after(0, self.stop_listening)

    def process_voice_input(self, text):
        """Process voice input and add to text input for editing."""
        # Add to text input for editing
        self.input_entry.delete("1.0", tk.END)
        self.input_entry.insert("1.0", text)
        
        # Add to chat
        self.add_to_chat("User (Voice)", text, "user")
        
        # Process command
        self.process_command(text)

    def speak_text(self, text):
        """Convert text to speech using TTS engine - enhanced for human-like voice."""
        if not text:
            return
        try:
            # Enqueue text for the TTS worker to speak sequentially
            if hasattr(self, 'tts_queue') and self.tts_queue:
                self.tts_queue.put(text)
            else:
                # Fallback: speak synchronously
                if not hasattr(self, 'tts_engine') or self.tts_engine is None:
                    self.tts_engine = pyttsx3.init()
                    self.update_tts_settings()
                self._apply_enhanced_tts_settings()
                self.tts_engine.say(self._prepare_text_for_speech(text))
                self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
            try:
                self.tts_engine = pyttsx3.init()
                self.update_tts_settings()
            except Exception:
                pass
    
    def _prepare_text_for_speech(self, text):
        """Prepare text for more natural speech synthesis."""
        # Remove emojis and special characters
        clean_text = re.sub(r'[\U0001F300-\U0001FAFF]', '', text)
        clean_text = re.sub(r'\[.*?\]', '', clean_text)
        # Normalize whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text)
        
        # Limit text length for faster speech while maintaining natural flow
        if len(clean_text) > 300:
            # Try to break at sentence boundaries
            sentences = clean_text.split('.')
            if len(sentences) > 1:
                clean_text = '.'.join(sentences[:2]) + '...'
            else:
                clean_text = clean_text[:300] + "..."
        
        return clean_text.strip()

    def stop_speaking(self):
        try:
            if hasattr(self, 'tts_engine') and self.tts_engine:
                self.tts_engine.stop()
            if hasattr(self, 'tts_queue') and self.tts_queue:
                # Clear queued items
                while not self.tts_queue.empty():
                    try:
                        self.tts_queue.get_nowait()
                    except Exception:
                        break
        except Exception:
            pass
    
    def _apply_enhanced_tts_settings(self):
        """Apply enhanced TTS settings for more human-like speech with multi-language support."""
        try:
            if hasattr(self, 'tts_engine') and self.tts_engine:
                # Optimize speech rate for natural conversation (not too fast, not too slow)
                natural_rate = 140  # Slightly slower than default for more natural flow
                self.tts_engine.setProperty('rate', natural_rate)
                
                # Set volume to comfortable level
                self.tts_engine.setProperty('volume', 0.85)
                
                # Set language-specific voice
                self._set_language_voice()
                        
        except Exception as e:
            print(f"Error applying enhanced TTS settings: {e}")
    
    def _set_language_voice(self):
        """Set the appropriate voice for the current language (cross-platform)."""
        try:
            voices = self.tts_engine.getProperty('voices')
            if not voices:
                return
            
            # Get current language voice preference
            current_lang = self.language
            target_voice_id = LANGUAGES.get(current_lang, {}).get("tts_voice", None)
            
            # Try to find the target voice
            if target_voice_id:
                for voice in voices:
                    if target_voice_id in voice.id:
                        self.tts_engine.setProperty('voice', voice.id)
                        print(f"Set voice to: {voice.name} for {current_lang}")
                        return
            
            # Fallback: look for voices matching the language (platform-aware)
            # Windows voices
            windows_keywords = {
                "Hindi": ["hindi", "hi-in", "hemant", "kalpana"],
                "Telugu": ["telugu", "te-in", "chaitanya", "priya"],
                "English": ["english", "en-us", "david", "zira", "mark"]
            }
            
            # macOS voices (NSSpeechSynthesizer)
            macos_keywords = {
                "Hindi": ["hindi", "lekha"],
                "Telugu": ["telugu"],
                "English": ["samantha", "alex", "daniel", "karen", "moira", "tessa", "veena", "en-us", "en_us"]
            }
            
            # Choose keywords based on platform
            import platform as plat
            if plat.system() == "Darwin":
                lang_keywords = macos_keywords
            else:
                lang_keywords = windows_keywords
            
            target_keywords = lang_keywords.get(current_lang, [])
            for voice in voices:
                voice_name = voice.name.lower()
                voice_id = voice.id.lower()
                if any(keyword in voice_name or keyword in voice_id for keyword in target_keywords):
                    self.tts_engine.setProperty('voice', voice.id)
                    print(f"Set fallback voice to: {voice.name} for {current_lang}")
                    return
            
            # Final fallback: use first available voice
            self.tts_engine.setProperty('voice', voices[0].id)
            print(f"Using default voice: {voices[0].name}")
            
        except Exception as e:
            print(f"Error setting language voice: {e}")

    def stop_speech(self):
        """Stop speech playback."""
        try:
            self.speaking = False
            # Only try to stop pygame mixer if it's initialized
            try:
                pygame.mixer.music.stop()
            except:
                pass  # Ignore pygame mixer errors
            self.add_to_chat("System", "Speech stopped.", "system")
        except Exception as e:
            print(f"Error stopping speech: {e}")

    def update_system_info(self):
        """Update Core System UI with real-time system data."""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=None)
            if hasattr(self, 'cpu_percent_label'):
                self.cpu_percent_label.configure(text=f"{cpu_percent:.0f}%")
            
            # RAM usage
            memory = psutil.virtual_memory()
            ram_percent = memory.percent
            ram_gb = memory.used / (1024**3)
            if hasattr(self, 'ram_percent_label'):
                self.ram_percent_label.configure(text=f"{ram_percent:.0f}%")
            if hasattr(self, 'ram_usage_label'):
                self.ram_usage_label.configure(text=f"RAM USAGE    {ram_gb:.1f} GB")
            
            # Update top processes
            if hasattr(self, 'process_list_frame'):
                self.update_top_processes()
                
        except Exception as e:
            print(f"Error updating system info: {e}")
        
        # Schedule next update
        if hasattr(self, 'root') and self.root.winfo_exists():
            self.root.after(3000, self.update_system_info)
    
    def update_top_processes(self):
        """Update the top processes list."""
        try:
            colors = THEMES.get(self.theme, THEMES["core_system"])
            
            # Clear existing processes
            for widget in self.process_list_frame.winfo_children():
                widget.destroy()
            
            # Get top processes by CPU
            processes = []
            for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    if pinfo['cpu_percent'] is not None:
                        processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU and take top 5
            processes.sort(key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)
            top_processes = processes[:5]
            
            for proc in top_processes:
                name = proc.get('name', 'Unknown')[:20]
                cpu = proc.get('cpu_percent', 0) or 0
                mem = proc.get('memory_percent', 0) or 0
                
                row = ctk.CTkFrame(self.process_list_frame, fg_color="transparent")
                row.pack(fill="x", pady=2)
                
                ctk.CTkLabel(
                    row,
                    text=name,
                    font=("Consolas", 9),
                    text_color=colors["fg"],
                    anchor="w",
                    width=120
                ).pack(side="left")
                
                ctk.CTkLabel(
                    row,
                    text=f"{mem:.1f}%",
                    font=("Consolas", 9),
                    text_color=colors.get("progress_cyan", "#06b6d4"),
                    width=40
                ).pack(side="right")
                
                ctk.CTkLabel(
                    row,
                    text=f"{cpu:.1f}%",
                    font=("Consolas", 9),
                    text_color=colors.get("progress_orange", "#f97316"),
                    width=40
                ).pack(side="right")
                
        except Exception as e:
            print(f"Error updating processes: {e}")
    
    def update_weather_display(self):
        """Update weather display in the system panel."""
        try:
            weather_info = self.get_weather_info()
            # Extract just the temperature and condition for the sidebar
            lines = weather_info.split('\n')
            temp_line = next((line for line in lines if 'Temperature:' in line), '')
            condition_line = next((line for line in lines if 'Condition:' in line), '')
            
            if temp_line and condition_line:
                temp = temp_line.split(':')[1].strip()
                condition = condition_line.split(':')[1].strip()
                weather_text = f"🌤️ {temp} | {condition}"
            else:
                weather_text = "🌤️ Weather data unavailable"
            
            if hasattr(self, 'weather_label'):
                self.weather_label.configure(text=weather_text)
        except Exception as e:
            print(f"Error updating weather display: {e}")
            if hasattr(self, 'weather_label'):
                self.weather_label.configure(text="🌤️ Weather unavailable")
        
        # Schedule next update
        if hasattr(self, 'root'):
            self.root.after(300000, self.update_weather_display)  # Update every 5 minutes

    def update_status(self, message):
        """Update the status bar with a message."""
        try:
            if hasattr(self, 'status_label'):
                self.status_label.configure(text=message)
            print(f"Status: {message}")
        except Exception as e:
            print(f"Error updating status: {e}")
    
    def update_gmail_status(self):
        """Update the Gmail status indicator in the status bar."""
        try:
            if hasattr(self, 'gmail_status') and self.gmail_status:
                try:
                    if self.gmail_address and self.gmail_app_password:
                        self.gmail_status.configure(
                            text="📧 Gmail: Configured",
                            text_color=THEMES[self.theme]["success"]
                        )
                    else:
                        self.gmail_status.configure(
                            text="📧 Gmail: Not Configured",
                            text_color=THEMES[self.theme]["warning"]
                        )
                except tk.TclError:
                    # Widget might have been destroyed
                    pass
        except Exception as e:
            print(f"Error updating Gmail status: {e}")

    def clear_chat(self):
        """Clear the chat area."""
        # Clear all widgets in the scrollable frame
        for widget in self.chat_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Clear conversation history
        self.conversation_history.clear()
        self.save_profile()
        
        # Add welcome message
        self.add_to_chat("SAM", "Chat cleared. How can I help you today?", "info")

    def export_chat(self):
        try:
            if not self.conversation_history:
                self.add_to_chat("System", "No conversation to export.", "system")
                return
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Export Chat History"
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("SAM Chat History\n")
                    f.write("=" * 50 + "\n\n")
                    for entry in self.conversation_history:
                        f.write(f"[{entry['timestamp']}] {entry['sender']}: {entry['message']}\n\n")
                self.add_to_chat("System", f"Chat exported to {filename}", "system")
        except Exception as e:
            print(f"Error in export_chat: {e}")

    def open_website(self, url):
        try:
            if getattr(self, 'automation_strategy', 'direct') == 'simulate' and hasattr(self, 'browser_controller'):
                self.browser_controller.open_url_via_typing(url)
            else:
                webbrowser.open(url)
            self.add_to_chat("System", f"Opened {url} in browser", "system")
        except Exception as e:
            print(f"Error in open_website: {e}")
            self.add_to_chat("System", f"Failed to open website: {str(e)}", "error")

    def prompt_find_and_open(self):
        try:
            q = simpledialog.askstring("Find & Open", "Enter file name or part of it:", parent=self.root)
            if not q:
                return
            result = self.open_file_human_like(q)
            self.add_to_chat("SAM", result, "system")
        except Exception as e:
            self.add_to_chat("System", f"Failed: {e}", "error")

    def play_music_folder(self):
        try:
            music_folder = os.path.expanduser("~/Music")
            if os.path.exists(music_folder):
                os.startfile(music_folder)
                self.add_to_chat("System", "Opened Music folder", "system")
            else:
                self.add_to_chat("System", "Music folder not found", "error")
        except Exception as e:
            print(f"Error in play_music_folder: {e}")
            self.add_to_chat("System", f"Failed to open music folder: {str(e)}", "error")

    def open_notepad(self):
        try:
            subprocess.Popen(['notepad.exe'])
            self.add_to_chat("System", "Notepad opened", "system")
        except Exception as e:
            print(f"Error in open_notepad: {e}")
            self.add_to_chat("System", f"Failed to open notepad: {str(e)}", "error")

    def open_calculator(self):
        try:
            subprocess.Popen(['calc.exe'])
            self.add_to_chat("System", "Calculator opened", "system")
        except Exception as e:
            print(f"Error in open_calculator: {e}")
            self.add_to_chat("System", f"Failed to open calculator: {str(e)}", "error")

    def quick_screenshot(self):
        self.process_command("take screenshot")

    def show_system_info_popup(self):
        try:
            popup = tk.Toplevel(self.root)
            popup.title("System Information")
            popup.geometry("500x600")
            popup.configure(bg=THEMES[self.theme]["bg"])
            popup.transient(self.root)
            popup.grab_set()
            info_text = scrolledtext.ScrolledText(
                popup, font=("Segoe UI",11),
                bg=THEMES[self.theme]["scrolledbg"], fg=THEMES[self.theme]["textfg"],
                bd=0, padx=20, pady=20
            )
            info_text.pack(fill="both", expand=True, padx=20, pady=20)
            sys_info = self.get_detailed_system_info()
            try:
                platform_info = f"""
🖥️ Platform Details:
• OS: {platform.system()} {platform.release()}
• Version: {platform.version()}
• Machine: {platform.machine()}
• Processor: {platform.processor()}
                """
                sys_info += "\n" + platform_info
            except:
                pass
            info_text.insert("1.0", sys_info)
            info_text.configure(state="disabled")
            close_btn = tk.Button(
                popup, text="Close", font=("Segoe UI",11),
                bg=THEMES[self.theme]["btnbg"], fg=THEMES[self.theme]["btnfg"],
                command=popup.destroy, bd=0, padx=20, pady=5, cursor="hand2"
            )
            close_btn.pack(pady=10)
        except Exception as e:
            print(f"Error in show_system_info_popup: {e}")

    def show_help(self):
        help_text = self.get_help_text()
        popup = ctk.CTkToplevel(self.root)
        popup.title("SAM Help")
        popup.geometry("600x700")
        popup.configure(fg_color=THEMES[self.theme]["bg"])
        popup.transient(self.root)
        popup.grab_set()
        help_text_widget = ctk.CTkTextbox(
            popup, font=("Segoe UI",11),
            fg_color=THEMES[self.theme]["scrolledbg"], text_color=THEMES[self.theme]["textfg"],
            border_width=0, padx=20, pady=20, wrap="word"
        )
        help_text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        help_text_widget.insert("1.0", help_text)
        help_text_widget.configure(state="disabled")
        close_btn = ctk.CTkButton(
            popup, text="Close", font=("Segoe UI",11),
            fg_color=THEMES[self.theme]["btnbg"], text_color=THEMES[self.theme]["btnfg"],
            command=popup.destroy, corner_radius=8, padx=20, pady=5
        )
        close_btn.pack(pady=10)

    def show_about(self):
        about_text = """🤖 SAM AI Assistant v2.0
A modern AI assistant with voice interaction capabilities,
built to help with daily tasks and provide information.
Features:
• Natural language processing
• Voice commands and text-to-speech
• System monitoring and control
• File operations and calculations
• Information search and retrieval
• Weather updates and news
• Multi-language support
• Modern themes
Created with ❤️ using Python and Tkinter
"""
        popup = ctk.CTkToplevel(self.root)
        popup.title("About SAM")
        popup.geometry("400x500")
        popup.configure(fg_color=THEMES[self.theme]["bg"])
        popup.transient(self.root)
        popup.grab_set()
        about_label = ctk.CTkLabel(
            popup, text=about_text, font=("Segoe UI",11),
            fg_color=THEMES[self.theme]["bg"], text_color=THEMES[self.theme]["fg"],
            justify="left", padx=20, pady=20, wraplength=360
        )
        about_label.pack(fill="both", expand=True)
        close_btn = ctk.CTkButton(
            popup, text="Close", font=("Segoe UI",11),
            fg_color=THEMES[self.theme]["btnbg"], text_color=THEMES[self.theme]["btnfg"],
            command=popup.destroy, corner_radius=8, padx=20, pady=5
        )
        close_btn.pack(pady=10)

    def show_settings(self):
        """Show improved settings panel with better organization and user experience."""
        # Create main settings window
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("SAM Settings")
        settings_window.geometry("600x700")
        settings_window.configure(fg_color=THEMES[self.theme]["bg"])
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Center the window
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (settings_window.winfo_screenheight() // 2) - (700 // 2)
        settings_window.geometry(f"600x700+{x}+{y}")
        
        # Prevent resizing
        settings_window.resizable(False, False)
        
        # Create main container with scrollable frame
        main_container = ctk.CTkFrame(settings_window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_container,
            text="⚙️ SAM Settings",
            font=("Segoe UI", 20, "bold"),
            text_color=THEMES[self.theme]["accent"]
        )
        title_label.pack(pady=(0, 20))
        
        # Create scrollable frame for settings
        scrollable_frame = ctk.CTkScrollableFrame(
            main_container,
            fg_color="transparent",
            width=560,
            height=580
        )
        scrollable_frame.pack(fill="both", expand=True)
        
        # Create settings sections
        self._create_theme_section(scrollable_frame)
        self._create_voice_section(scrollable_frame)
        self._create_email_section(scrollable_frame)
        self._create_profile_section(scrollable_frame)
        self._create_commands_section(scrollable_frame)
        # Planner section to enable/disable and choose strategy
        self._create_planner_section(scrollable_frame)
        # Automation: choose how SAM performs web tasks (direct vs simulate)
        self._create_automation_section(scrollable_frame)
        self._create_language_section(scrollable_frame)
        
        # Bottom buttons frame
        buttons_frame = ctk.CTkFrame(settings_window, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Save and Close buttons
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Save All Settings",
            command=lambda: self._save_all_settings(settings_window),
            fg_color=THEMES[self.theme]["success"],
            hover_color=THEMES[self.theme]["success_hover"],
            font=("Segoe UI", 12, "bold")
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        close_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Close",
            command=settings_window.destroy,
            fg_color=THEMES[self.theme]["btnbg"],
            hover_color=THEMES[self.theme]["btnbg_hover"],
            font=("Segoe UI", 12)
        )
        close_btn.pack(side="right")
        
        # Bind escape key to close
        settings_window.bind("<Escape>", lambda e: settings_window.destroy())
        
        # Focus on window
        settings_window.focus_set()
        
        # Store reference to prevent garbage collection
        self.settings_window = settings_window

    def _create_theme_section(self, parent):
        """Create theme settings section."""
        # Theme section frame
        theme_frame = ctk.CTkFrame(parent, fg_color=THEMES[self.theme]["entrybg"])
        theme_frame.pack(fill="x", pady=(0, 15), padx=5)
        
        # Section title
        title_label = ctk.CTkLabel(
            theme_frame,
            text="🎨 Theme Settings",
            font=("Segoe UI", 14, "bold"),
            text_color=THEMES[self.theme]["accent"]
        )
        title_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Content container
        content_frame = ctk.CTkFrame(theme_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # Theme selection
        theme_label = ctk.CTkLabel(
            content_frame,
            text="Choose your theme:",
            font=("Segoe UI", 11),
            text_color=THEMES[self.theme]["fg"]
        )
        theme_label.pack(anchor="w", pady=(5, 5))
        
        # Theme selection frame
        theme_select_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        theme_select_frame.pack(fill="x", pady=(0, 10))
        
        # Create radio buttons for themes
        self.theme_var = tk.StringVar(value=self.theme)
        
        themes = list(THEMES.keys()) + ['auto']
        for theme in themes:
            theme_name = "Auto (System)" if theme == 'auto' else theme.title()
            
            radio_btn = ctk.CTkRadioButton(
                theme_select_frame,
                text=theme_name,
                variable=self.theme_var,
                value=theme,
                command=lambda t=theme: self._apply_theme_preview(t),
                fg_color=THEMES[self.theme]["accent"],
                hover_color=THEMES[self.theme]["accent_hover"],
                font=("Segoe UI", 10)
            )
            radio_btn.pack(anchor="w", pady=2)
        
        # Accent color picker
        color_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        color_frame.pack(fill="x", pady=(10, 10))
        
        color_label = ctk.CTkLabel(
            color_frame,
            text="Accent Color:",
            font=("Segoe UI", 11),
            text_color=THEMES[self.theme]["fg"]
        )
        color_label.pack(side="left")
        
        # Color preview button
        self.color_preview_btn = ctk.CTkButton(
            color_frame,
            text="",
            width=30,
            height=25,
            fg_color=self.accent_color,
            hover_color=self.accent_color,
            command=self._pick_accent_color
        )
        self.color_preview_btn.pack(side="right", padx=(10, 0))
        
        # Font size slider
        font_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        font_frame.pack(fill="x", pady=(10, 10))
        
        font_label = ctk.CTkLabel(
            font_frame,
            text=f"Chat Font Size: {self.chat_font_size}",
            font=("Segoe UI", 11),
            text_color=THEMES[self.theme]["fg"]
        )
        font_label.pack(anchor="w")
        
        # Font size slider
        self.font_slider = ctk.CTkSlider(
            font_frame,
            from_=8,
            to=24,
            number_of_steps=16,
            command=lambda value: self._update_font_size_label(font_label, int(value)),
            fg_color=THEMES[self.theme]["accent"],
            progress_color=THEMES[self.theme]["accent"],
            button_color=THEMES[self.theme]["accent"],
            button_hover_color=THEMES[self.theme]["accent_hover"]
        )
        self.font_slider.set(self.chat_font_size)

    def _create_automation_section(self, parent):
        """Create automation settings section to control how SAM interacts with the browser."""
        section_frame = ctk.CTkFrame(parent, fg_color=THEMES[self.theme]["entrybg"])
        section_frame.pack(fill="x", pady=(0, 15), padx=5)

        title_label = ctk.CTkLabel(
            section_frame,
            text="🖱️ Automation Settings",
            font=("Segoe UI", 14, "bold"),
            text_color=THEMES[self.theme]["accent"]
        )
        title_label.pack(anchor="w", padx=15, pady=(10, 5))

        content = ctk.CTkFrame(section_frame, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=(0, 10))

        desc = ctk.CTkLabel(
            content,
            text="Choose how SAM opens websites like YouTube:",
            font=("Segoe UI", 11),
            text_color=THEMES[self.theme]["fg"]
        )
        desc.pack(anchor="w")

        self.automation_strategy_var = tk.StringVar(value=getattr(self, 'automation_strategy', 'direct'))

        rb_frame = ctk.CTkFrame(content, fg_color="transparent")
        rb_frame.pack(fill="x", pady=(5, 5))

        direct_rb = ctk.CTkRadioButton(
            rb_frame,
            text="Direct (open URL via API)",
            variable=self.automation_strategy_var,
            value="direct",
            fg_color=THEMES[self.theme]["accent"],
            hover_color=THEMES[self.theme]["accent_hover"],
            font=("Segoe UI", 10)
        )
        direct_rb.pack(anchor="w", pady=2)

        simulate_rb = ctk.CTkRadioButton(
            rb_frame,
            text="Simulate (mouse/keyboard typing)",
            variable=self.automation_strategy_var,
            value="simulate",
            fg_color=THEMES[self.theme]["accent"],
            hover_color=THEMES[self.theme]["accent_hover"],
            font=("Segoe UI", 10)
        )
        simulate_rb.pack(anchor="w", pady=2)

        hint = ctk.CTkLabel(
            content,
            text="Tip: On macOS, grant Accessibility permissions to Python for simulated input.",
            font=("Segoe UI", 10),
            text_color=THEMES[self.theme]["subfg"]
        )
        hint.pack(anchor="w", pady=(6, 2))
        self.font_slider.pack(fill="x", pady=(5, 0))

    def _create_planner_section(self, parent):
        """Planner settings section (modular)."""
        frame = ctk.CTkFrame(parent, fg_color=THEMES[self.theme]["entrybg"])
        frame.pack(fill="x", pady=(0, 15), padx=5)

        title = ctk.CTkLabel(
            frame,
            text="🧭 Planner Settings",
            font=("Segoe UI", 14, "bold"),
            text_color=THEMES[self.theme]["accent"],
        )
        title.pack(anchor="w", padx=15, pady=(10, 5))

        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=(0, 10))

        # Enable/disable multi-intent planner
        self.planner_enabled_var = tk.BooleanVar(value=getattr(self, 'planner_enabled', True))
        enable_switch = ctk.CTkSwitch(
            content,
            text="Enable multi‑intent planner",
            variable=self.planner_enabled_var,
            onvalue=True,
            offvalue=False,
        )
        enable_switch.pack(anchor="w", pady=(0, 8))

        # Strategy selection
        ctk.CTkLabel(
            content,
            text="Planning strategy:",
            font=("Segoe UI", 11),
            text_color=THEMES[self.theme]["fg"],
        ).pack(anchor="w", pady=(6, 4))

        self.planning_strategy_var = tk.StringVar(value=getattr(self, 'planning_strategy', 'simple'))
        strat_frame = ctk.CTkFrame(content, fg_color="transparent")
        strat_frame.pack(fill="x")
        for label, value in [("Simple", "simple"), ("AI‑assisted", "ai_assisted")]:
            rb = ctk.CTkRadioButton(
                strat_frame,
                text=label,
                variable=self.planning_strategy_var,
                value=value,
                fg_color=THEMES[self.theme]["accent"],
                hover_color=THEMES[self.theme]["accent_hover"],
                font=("Segoe UI", 10)
            )
            rb.pack(side="left", padx=(0, 10))

    def _create_voice_section(self, parent):
        """Create voice settings section."""
        # Voice section frame
        voice_frame = ctk.CTkFrame(parent, fg_color=THEMES[self.theme]["entrybg"])
        voice_frame.pack(fill="x", pady=(0, 15), padx=5)
        
        # Section title
        title_label = ctk.CTkLabel(
            voice_frame,
            text="🗣️ Voice Settings",
            font=("Segoe UI", 14, "bold"),
            text_color=THEMES[self.theme]["accent"]
        )
        title_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Content container
        content_frame = ctk.CTkFrame(voice_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # Voice selection
        voice_label = ctk.CTkLabel(
            content_frame,
            text="Select TTS Voice:",
            font=("Segoe UI", 11),
            text_color=THEMES[self.theme]["fg"]
        )
        voice_label.pack(anchor="w", pady=(5, 5))
        
        # Voice selection frame
        voice_select_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        voice_select_frame.pack(fill="x", pady=(0, 10))
        
        # Get available voices
        voices = self.tts_engine.getProperty('voices')
        self.voice_var = tk.StringVar(value=self.tts_engine.getProperty('voice'))
        
        # Create voice options with preview
        for voice in voices:
            voice_option_frame = ctk.CTkFrame(voice_select_frame, fg_color="transparent")
            voice_option_frame.pack(fill="x", pady=2)
            
            # Radio button
            radio_btn = ctk.CTkRadioButton(
                voice_option_frame,
                text=voice.name,
                variable=self.voice_var,
                value=voice.id,
                command=lambda vid=voice.id: self.set_tts_voice(vid),
                fg_color=THEMES[self.theme]["accent"],
                hover_color=THEMES[self.theme]["accent_hover"],
                font=("Segoe UI", 10)
            )
            radio_btn.pack(side="left")
            
            # Preview button
            preview_btn = ctk.CTkButton(
                voice_option_frame,
                text="🔊 Preview",
                width=80,
                height=25,
                command=lambda vid=voice.id: self._preview_voice(vid),
                fg_color=THEMES[self.theme]["btnbg"],
                hover_color=THEMES[self.theme]["btnbg_hover"],
                font=("Segoe UI", 9)
            )
            preview_btn.pack(side="right")
        
        # Rate slider
        rate_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        rate_frame.pack(fill="x", pady=(10, 5))
        
        rate_label = ctk.CTkLabel(
            rate_frame,
            text=f"Speech Rate: {self.tts_rate}",
            font=("Segoe UI", 11),
            text_color=THEMES[self.theme]["fg"]
        )
        rate_label.pack(anchor="w")
        
        self.rate_slider = ctk.CTkSlider(
            rate_frame,
            from_=100,
            to=250,
            number_of_steps=150,
            command=lambda value: self._update_rate_label(rate_label, int(value)),
            fg_color=THEMES[self.theme]["accent"],
            progress_color=THEMES[self.theme]["accent"],
            button_color=THEMES[self.theme]["accent"],
            button_hover_color=THEMES[self.theme]["accent_hover"]
        )
        self.rate_slider.set(self.tts_rate)
        self.rate_slider.pack(fill="x", pady=(5, 0))
        
        # Volume slider
        volume_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        volume_frame.pack(fill="x", pady=(10, 10))
        
        volume_label = ctk.CTkLabel(
            volume_frame,
            text=f"Volume: {int(self.tts_volume * 100)}%",
            font=("Segoe UI", 11),
            text_color=THEMES[self.theme]["fg"]
        )
        volume_label.pack(anchor="w")
        
        self.volume_slider = ctk.CTkSlider(
            volume_frame,
            from_=0,
            to=100,
            number_of_steps=100,
            command=lambda value: self._update_volume_label(volume_label, int(value)),
            fg_color=THEMES[self.theme]["accent"],
            progress_color=THEMES[self.theme]["accent"],
            button_color=THEMES[self.theme]["accent"],
            button_hover_color=THEMES[self.theme]["accent_hover"]
        )
        self.volume_slider.set(int(self.tts_volume * 100))
        self.volume_slider.pack(fill="x", pady=(5, 0))
        
        # Hotword settings
        hotword_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        hotword_frame.pack(fill="x", pady=(10, 10))
        
        hotword_label = ctk.CTkLabel(
            hotword_frame,
            text="Wake Word:",
            font=("Segoe UI", 11),
            text_color=THEMES[self.theme]["fg"]
        )
        hotword_label.pack(anchor="w")
        
        # Hotword entry
        hotword_entry_frame = ctk.CTkFrame(hotword_frame, fg_color="transparent")
        hotword_entry_frame.pack(fill="x", pady=(5, 5))
        
        self.hotword_var = tk.StringVar(value=self.hotwords[0])
        hotword_entry = ctk.CTkEntry(
            hotword_entry_frame,
            textvariable=self.hotword_var,
            placeholder_text="Enter wake word (e.g., 'Hey SAM')",
            font=("Segoe UI", 10),
            fg_color=THEMES[self.theme]["entrybg"],
            text_color=THEMES[self.theme]["inputfg"]
        )
        hotword_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Save hotword button
        save_hotword_btn = ctk.CTkButton(
            hotword_entry_frame,
            text="💾 Save",
            width=80,
            command=self._save_hotword,
            fg_color=THEMES[self.theme]["success"],
            hover_color=THEMES[self.theme]["success_hover"],
            font=("Segoe UI", 10)
        )
        save_hotword_btn.pack(side="right")

    def _create_email_section(self, parent):
        """Create email settings section."""
        # Email section frame
        email_frame = ctk.CTkFrame(parent, fg_color=THEMES[self.theme]["entrybg"])
        email_frame.pack(fill="x", pady=(0, 15), padx=5)
        
        # Section title
        title_label = ctk.CTkLabel(
            email_frame,
            text="📧 Email Settings",
            font=("Segoe UI", 14, "bold"),
            text_color=THEMES[self.theme]["accent"]
        )
        title_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Content container
        content_frame = ctk.CTkFrame(email_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # Instructions
        instructions = ctk.CTkLabel(
            content_frame,
            text="To send emails via Gmail:\n1. Enable 2-factor authentication on your Google account\n2. Generate an App Password (Google Account → Security → App Passwords)\n3. Use your Gmail address and the generated app password below",
            font=("Segoe UI", 10),
            text_color=THEMES[self.theme]["subfg"],
            justify="left"
        )
        instructions.pack(anchor="w", pady=(5, 10))
        
        # Gmail address
        gmail_addr_label = ctk.CTkLabel(
            content_frame,
            text="Gmail Address:",
            font=("Segoe UI", 11),
            text_color=THEMES[self.theme]["fg"]
        )
        gmail_addr_label.pack(anchor="w")
        
        self.gmail_addr_var = tk.StringVar(value=getattr(self, 'gmail_address', ''))
        gmail_addr_entry = ctk.CTkEntry(
            content_frame,
            textvariable=self.gmail_addr_var,
            placeholder_text="your.email@gmail.com",
            font=("Segoe UI", 10),
            fg_color=THEMES[self.theme]["entrybg"],
            text_color=THEMES[self.theme]["inputfg"]
        )
        gmail_addr_entry.pack(fill="x", pady=(5, 10))
        
        # App password
        gmail_pass_label = ctk.CTkLabel(
            content_frame,
            text="App Password:",
            font=("Segoe UI", 11),
            text_color=THEMES[self.theme]["fg"]
        )
        gmail_pass_label.pack(anchor="w")
        
        self.gmail_pass_var = tk.StringVar(value=getattr(self, 'gmail_app_password', ''))
        gmail_pass_entry = ctk.CTkEntry(
            content_frame,
            textvariable=self.gmail_pass_var,
            placeholder_text="Enter your app password",
            font=("Segoe UI", 10),
            fg_color=THEMES[self.theme]["entrybg"],
            text_color=THEMES[self.theme]["inputfg"],
            show="*"
        )
        gmail_pass_entry.pack(fill="x", pady=(5, 10))
        
        # Test and Save buttons
        gmail_buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        gmail_buttons_frame.pack(fill="x", pady=(0, 10))
        
        test_gmail_btn = ctk.CTkButton(
            gmail_buttons_frame,
            text="🔍 Test Connection",
            command=self._test_gmail_connection,
            fg_color=THEMES[self.theme]["accent"],
            hover_color=THEMES[self.theme]["accent_hover"],
            font=("Segoe UI", 10)
        )
        test_gmail_btn.pack(side="left", padx=(0, 10))
        
        save_gmail_btn = ctk.CTkButton(
            gmail_buttons_frame,
            text="💾 Save Settings",
            command=self._save_gmail_settings,
            fg_color=THEMES[self.theme]["success"],
            hover_color=THEMES[self.theme]["success_hover"],
            font=("Segoe UI", 10)
        )
        save_gmail_btn.pack(side="right")

    def _create_profile_section(self, parent):
        """Create profile settings section."""
        # Profile section frame
        profile_frame = ctk.CTkFrame(parent, fg_color=THEMES[self.theme]["entrybg"])
        profile_frame.pack(fill="x", pady=(0, 15), padx=5)
        
        # Section title
        title_label = ctk.CTkLabel(
            profile_frame,
            text="👤 User Profile",
            font=("Segoe UI", 14, "bold"),
            text_color=THEMES[self.theme]["accent"]
        )
        title_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Content container
        content_frame = ctk.CTkFrame(profile_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # Current user info
        user_info = ctk.CTkLabel(
            content_frame,
            text=f"Current User: {self.username}",
            font=("Segoe UI", 11, "bold"),
            text_color=THEMES[self.theme]["accent"]
        )
        user_info.pack(anchor="w", pady=(5, 10))
        
        # Switch user button
        switch_user_btn = ctk.CTkButton(
            content_frame,
            text="🔄 Switch User",
            command=self._switch_user_profile,
            fg_color=THEMES[self.theme]["btnbg"],
            hover_color=THEMES[self.theme]["btnbg_hover"],
            font=("Segoe UI", 10)
        )
        switch_user_btn.pack(anchor="w")

    def _create_commands_section(self, parent):
        """Create custom commands section."""
        # Commands section frame
        commands_frame = ctk.CTkFrame(parent, fg_color=THEMES[self.theme]["entrybg"])
        commands_frame.pack(fill="x", pady=(0, 15), padx=5)
        
        # Section title
        title_label = ctk.CTkLabel(
            commands_frame,
            text="⚡ Custom Commands",
            font=("Segoe UI", 14, "bold"),
            text_color=THEMES[self.theme]["accent"]
        )
        title_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Content container
        content_frame = ctk.CTkFrame(commands_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # Add new command
        add_label = ctk.CTkLabel(
            content_frame,
            text="Add Custom Command:",
            font=("Segoe UI", 11),
            text_color=THEMES[self.theme]["fg"]
        )
        add_label.pack(anchor="w")
        
        # Command entry
        self.cmd_var = tk.StringVar()
        cmd_entry = ctk.CTkEntry(
            content_frame,
            textvariable=self.cmd_var,
            placeholder_text="Command (e.g., 'hello')",
            font=("Segoe UI", 10),
            fg_color=THEMES[self.theme]["entrybg"],
            text_color=THEMES[self.theme]["inputfg"]
        )
        cmd_entry.pack(fill="x", pady=(5, 5))
        
        # Response entry
        self.resp_var = tk.StringVar()
        resp_entry = ctk.CTkEntry(
            content_frame,
            textvariable=self.resp_var,
            placeholder_text="Response (e.g., 'Hello there!')",
            font=("Segoe UI", 10),
            fg_color=THEMES[self.theme]["entrybg"],
            text_color=THEMES[self.theme]["inputfg"]
        )
        resp_entry.pack(fill="x", pady=(0, 10))
        
        # Add button
        add_cmd_btn = ctk.CTkButton(
            content_frame,
            text="➕ Add Command",
            command=self._add_custom_command,
            fg_color=THEMES[self.theme]["success"],
            hover_color=THEMES[self.theme]["success_hover"],
            font=("Segoe UI", 10)
        )
        add_cmd_btn.pack(anchor="w")
        
        # Commands list
        list_label = ctk.CTkLabel(
            content_frame,
            text="Current Commands:",
            font=("Segoe UI", 11),
            text_color=THEMES[self.theme]["fg"]
        )
        list_label.pack(anchor="w", pady=(10, 5))
        
        # Commands listbox
        self.cmd_listbox = tk.Listbox(
            content_frame,
            height=4,
            font=("Segoe UI", 9),
            bg=THEMES[self.theme]["entrybg"],
            fg=THEMES[self.theme]["inputfg"],
            selectbackground=THEMES[self.theme]["accent"]
        )
        self.cmd_listbox.pack(fill="x", pady=(0, 5))
        
        # Delete button
        delete_cmd_btn = ctk.CTkButton(
            content_frame,
            text="🗑️ Delete Selected",
            command=self._delete_custom_command,
            fg_color=THEMES[self.theme]["error"],
            hover_color=THEMES[self.theme]["error_hover"],
            font=("Segoe UI", 10)
        )
        delete_cmd_btn.pack(anchor="w")
        
        # Update commands list
        self._update_commands_list()

    def _create_language_section(self, parent):
        """Create language settings section."""
        # Language section frame
        language_frame = ctk.CTkFrame(parent, fg_color=THEMES[self.theme]["entrybg"])
        language_frame.pack(fill="x", pady=(0, 15), padx=5)
        
        # Section title
        title_label = ctk.CTkLabel(
            language_frame,
            text="🌍 Language",
            font=("Segoe UI", 14, "bold"),
            text_color=THEMES[self.theme]["accent"]
        )
        title_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Content container
        content_frame = ctk.CTkFrame(language_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # Language selection
        lang_label = ctk.CTkLabel(
            content_frame,
            text="Select Language:",
            font=("Segoe UI", 11),
            text_color=THEMES[self.theme]["fg"]
        )
        lang_label.pack(anchor="w", pady=(5, 5))
        
        # Language selection frame
        lang_select_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        lang_select_frame.pack(fill="x", pady=(0, 10))
        
        # Create radio buttons for languages
        self.lang_var = tk.StringVar(value=self.language)
        
        for lang in LANGUAGES.keys():
            radio_btn = ctk.CTkRadioButton(
                lang_select_frame,
                text=lang,
                variable=self.lang_var,
                value=lang,
                command=lambda l=lang: self.change_language(l),
                fg_color=THEMES[self.theme]["accent"],
                hover_color=THEMES[self.theme]["accent_hover"],
                font=("Segoe UI", 10)
            )
            radio_btn.pack(anchor="w", pady=2)

    # ===== HELPER METHODS =====
    
    def _apply_theme_preview(self, theme):
        """Apply theme preview without saving."""
        if theme == 'auto':
            self.auto_theme_enabled = True
            self.apply_auto_theme()
        else:
            self.auto_theme_enabled = False
            self.change_theme(theme)

    def _pick_accent_color(self):
        """Open color picker for accent color."""
        from tkinter.colorchooser import askcolor
        color = askcolor(color=self.accent_color, parent=self.settings_window)[1]
        if color:
            self.accent_color = color
            # Update preview button
            self.color_preview_btn.configure(fg_color=color, hover_color=color)
            # Apply to current theme
            for theme in THEMES.values():
                theme["accent"] = color
            self.change_theme(self.theme)

    def _update_font_size_label(self, label, size):
        """Update font size label."""
        label.configure(text=f"Chat Font Size: {size}")

    def _update_rate_label(self, label, rate):
        """Update rate label."""
        label.configure(text=f"Speech Rate: {rate}")

    def _update_volume_label(self, label, volume):
        """Update volume label."""
        label.configure(text=f"Volume: {volume}%")

    def _preview_voice(self, voice_id):
        """Preview selected voice."""
        try:
            self.tts_engine.setProperty('voice', voice_id)
            self.tts_engine.say("This is a preview of the selected voice.")
            self.tts_engine.runAndWait()
        except Exception as e:
            messagebox.showerror("Voice Preview Error", f"Could not preview voice: {str(e)}")

    def _save_hotword(self):
        """Save hotword setting."""
        new_hotword = self.hotword_var.get().strip().lower()
        if new_hotword:
            self.hotwords[0] = new_hotword
            self.save_hotwords()
            messagebox.showinfo("Success", f"Wake word set to '{self.hotwords[0]}'!")
        else:
            messagebox.showerror("Error", "Please enter a wake word.")

    def _test_gmail_connection(self):
        """Test Gmail connection."""
        addr = self.gmail_addr_var.get().strip()
        pwd = self.gmail_pass_var.get().strip()
        
        if not addr or not pwd:
            messagebox.showerror("Error", "Please enter both Gmail address and app password.")
            return
        
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(addr, pwd)
            messagebox.showinfo("Success", "Gmail connection test successful!")
        except Exception as e:
            messagebox.showerror("Connection Failed", 
                               f"Failed to connect to Gmail:\n{str(e)}\n\n"
                               "Please check your credentials and ensure 2FA is enabled.")

    def _save_gmail_settings(self):
        """Save Gmail settings."""
        addr = self.gmail_addr_var.get().strip()
        pwd = self.gmail_pass_var.get().strip()
        
        if addr and pwd:
            self.gmail_address = addr
            self.gmail_app_password = pwd
            self.save_profile()
            self.update_gmail_status()
            messagebox.showinfo("Success", "Gmail settings saved successfully!")
        else:
            messagebox.showerror("Error", "Please enter both Gmail address and app password.")

    def _switch_user_profile(self):
        """Switch user profile."""
        self.load_or_prompt_profile()
        if hasattr(self, 'settings_window'):
            self.settings_window.destroy()

    def _add_custom_command(self):
        """Add custom command."""
        cmd = self.cmd_var.get().strip().lower()
        resp = self.resp_var.get().strip()
        
        if cmd and resp:
            self.user_commands[cmd] = resp
            self.save_user_commands()
            self._update_commands_list()
            self.cmd_var.set("")
            self.resp_var.set("")
            messagebox.showinfo("Success", f"Command '{cmd}' added successfully!")
        else:
            messagebox.showerror("Error", "Please enter both command and response.")

    def _delete_custom_command(self):
        """Delete selected custom command."""
        selection = self.cmd_listbox.curselection()
        if selection:
            key = list(self.user_commands.keys())[selection[0]]
            del self.user_commands[key]
            self.save_user_commands()
            self._update_commands_list()
            messagebox.showinfo("Success", f"Command '{key}' deleted successfully!")
        else:
            messagebox.showerror("Error", "Please select a command to delete.")

    def _update_commands_list(self):
        """Update commands listbox."""
        self.cmd_listbox.delete(0, 'end')
        for cmd, resp in self.user_commands.items():
            self.cmd_listbox.insert('end', f"{cmd} → {resp}")

    def _save_all_settings(self, window):
        """Save all settings and close window."""
        try:
            # Save theme
            if self.theme_var.get() != self.theme:
                self._apply_theme_preview(self.theme_var.get())
            
            # Save font size
            new_font_size = int(self.font_slider.get())
            if new_font_size != self.chat_font_size:
                self.set_chat_font_size(new_font_size)
            
            # Save voice settings
            new_rate = int(self.rate_slider.get())
            if new_rate != self.tts_rate:
                self.set_tts_rate(new_rate)
            
            new_volume = int(self.volume_slider.get()) / 100
            if new_volume != self.tts_volume:
                self.set_tts_volume(new_volume)

            # Save planner settings
            try:
                if hasattr(self, 'planner_enabled_var'):
                    self.planner_enabled = bool(self.planner_enabled_var.get())
                if hasattr(self, 'planning_strategy_var'):
                    self.planning_strategy = str(self.planning_strategy_var.get())
            except Exception:
                pass

            # Save automation settings
            try:
                if hasattr(self, 'automation_strategy_var'):
                    self.automation_strategy = str(self.automation_strategy_var.get())
            except Exception:
                pass
            
            # Save profile
            self.save_profile()
            
            messagebox.showinfo("Success", "All settings saved successfully!")
            window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    def setup_hotword_toggle(self):
        # No longer adds the button; now handled in setup_quick_actions
        pass

    def update_hotword_btn_state(self):
        if self.hotword_enabled:
            self.hotword_btn.configure(text="🎙️ Hotword: On", fg_color=THEMES[self.theme]["success"], state="normal")
        else:
            self.hotword_btn.configure(text="🎙️ Hotword: Off", fg_color=THEMES[self.theme]["btnbg"], state="normal")
        if self.is_listening:
            self.hotword_btn.configure(state="disabled")

    def toggle_hotword_detection(self):
        if not self.mic_available:
            self.add_to_chat("System", "Microphone not available. Please check your audio settings.", "error")
            return
        if self.is_listening:
            self.add_to_chat("System", "Already listening for a command. Please wait.", "warning")
            return
        self.hotword_enabled = not self.hotword_enabled
        self.update_hotword_btn_state()
        if self.hotword_enabled:
            try:
                if self.microphone and self.recognizer:
                    with self.microphone as src:
                        self.recognizer.adjust_for_ambient_noise(src, duration=1)
                        self.recognizer.dynamic_energy_threshold = True
                self.add_to_chat("System", "Hotword detection enabled. Say 'sam' to activate.", "system")
            except Exception:
                self.add_to_chat("System", "Hotword detection enabled.", "system")
            self.hotword_engine.start()
        else:
            self.add_to_chat("System", "Hotword detection disabled.", "system")
        

    def on_hotword_detected(self):
        self.update_hotword_btn_state()
        self.add_to_chat("System", f"Hotword '{self.hotwords[0]}' detected. Listening for your command...", "system")
        self.start_listening()

    def on_window_resize(self, event):
        if event.widget == self.root:
            for widget in self.root.winfo_children():
                if isinstance(widget, ModernButton):
                    widget.setup_button()

    def on_exit(self):
        """Enhanced exit with proper cleanup of animations and resources."""
        try:
            # Stop camera
            if hasattr(self, 'camera_active') and self.camera_active:
                try:
                    self.stop_camera()
                except:
                    pass
            
            # Stop all animations safely
            if hasattr(self, 'system_panel') and self.system_panel:
                try:
                    self.system_panel.stop_animations()
                except:
                    pass
            
            if hasattr(self, 'voice_visualizer') and self.voice_visualizer:
                try:
                    self.voice_visualizer.stop_animation()
                except:
                    pass
            
            if hasattr(self, 'typing_indicator') and self.typing_indicator:
                try:
                    self.typing_indicator.stop_animation()
                except:
                    pass
            
            # Stop hotword detection
            if hasattr(self, 'hotword_detection'):
                self.hotword_detection = False
            
            # Stop system tray and hotkeys
            try:
                self._stop_tray_and_hotkeys()
            except:
                pass
            
            # Stop speech and clean up audio files
            try:
                self.stop_speech()
            except:
                pass
                
            for file in os.listdir():
                if file.startswith("temp_audio_") and file.endswith(".mp3"):
                    try:
                        os.remove(file)
                    except:
                        pass
            
            # Save current state
            try:
                self.save_profile()
            except:
                pass
            
            # Show exit message
            try:
                self.add_to_chat("System", "👋 Shutting down SAM. Goodbye!", "system")
            except:
                pass
            
        except Exception as e:
            print(f"Error in on_exit: {e}")
        
        # Destroy the window safely
        try:
            if hasattr(self, 'root') and self.root:
                self.root.quit()
                self.root.destroy()
        except:
            pass

    def execute_user_code(self, code):
        import io
        import contextlib
        safe_builtins = {
            'abs': abs, 'min': min, 'max': max, 'sum': sum, 'len': len, 'range': range,
            'print': print, 'str': str, 'int': int, 'float': float, 'bool': bool, 'list': list, 'dict': dict, 'set': set, 'tuple': tuple
        }
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                exec(code, {'__builtins__': safe_builtins}, {})
            result = output.getvalue()
            if not result.strip():
                result = "✅ Code executed successfully. (No output)"
            return f"📝 Code Output:\n{result}"
        except Exception as e:
            print(f"Error in execute_user_code: {e}")
            return f"❌ Error executing code: {str(e)}\n⚠️ Only simple Python code is allowed."

    def update_tts_settings(self):
        """Update TTS engine settings, prioritizing language-specific voices."""
        try:
            if hasattr(self, 'tts_engine') and self.tts_engine:
                voices = self.tts_engine.getProperty('voices')
                
                # Try to find a voice matching the current speech recognition language code
                # For example, if sr_code is 'en-US', look for voices with 'en-us' in their ID or name
                target_lang_code = self.sr_code.lower()  # e.g., 'en-us', 'hi-in'
                
                found_voice_id = None
                # First, try to find an exact match for the current tts_voice_id if it's set
                if hasattr(self, 'tts_voice_id') and self.tts_voice_id:
                    for v in voices:
                        if v.id == self.tts_voice_id:
                            found_voice_id = v.id
                            break
                
                # If no specific voice was set or found, try to find one matching the language
                if not found_voice_id:
                    for v in voices:
                        # Check if language info is in the voice ID or name
                        if target_lang_code in v.id.lower() or target_lang_code.split('-')[0] in v.id.lower():
                            found_voice_id = v.id
                            break
                
                # Fallback to the first available voice if no language-specific voice is found
                if not found_voice_id and voices:
                    found_voice_id = voices[0].id
                
                if found_voice_id:
                    self.tts_engine.setProperty('voice', found_voice_id)
                    self.tts_voice_id = found_voice_id  # Update the stored voice ID
                else:
                    print("No TTS voices found or selected.")
                
                if hasattr(self, 'tts_rate'):
                    self.tts_engine.setProperty('rate', self.tts_rate)
                if hasattr(self, 'tts_volume'):
                    self.tts_engine.setProperty('volume', self.tts_volume)
        except Exception as e:
            print(f"Error updating TTS settings: {e}")

    def set_tts_voice(self, voice_id):
        self.tts_voice_id = voice_id
        self.update_tts_settings()
    def set_tts_rate(self, rate):
        self.tts_rate = rate
        self.update_tts_settings()
    def set_tts_volume(self, volume):
        self.tts_volume = volume
        self.update_tts_settings()

    def explain_code(self, code):
        # Very basic code explainer (static analysis, comments)
        if not code:
            return "❓ Please provide code to explain."
        lines = code.split('\n')
        explanation = []
        for line in lines:
            line = line.strip()
            if line.startswith('def '):
                explanation.append(f"Function definition: {line}")
            elif line.startswith('for '):
                explanation.append(f"For loop: {line}")
            elif line.startswith('while '):
                explanation.append(f"While loop: {line}")
            elif line.startswith('if '):
                explanation.append(f"If statement: {line}")
            elif line.startswith('return '):
                explanation.append(f"Returns: {line[7:]}")
            elif line.startswith('#'):
                explanation.append(f"Comment: {line[1:].strip()}")
            elif '=' in line:
                explanation.append(f"Assignment: {line}")
            else:
                explanation.append(f"Code: {line}")
        return "📝 Code Explanation:\n" + '\n'.join(explanation)
    def debug_code(self, code):
        # Very basic static check for common Python errors
        if not code:
            return "❓ Please provide code to debug."
        try:
            compile(code, '<string>', 'exec')
            return "✅ No syntax errors detected."
        except SyntaxError as e:
            return f"❌ Syntax error: {e}"
        except Exception as e:
            return f"⚠️ Error: {e}"
    def generate_code(self, prompt):
        """Enhanced code generation with more templates and patterns"""
        if not prompt:
            return "❓ Please provide a prompt for code generation."
        
        prompt_lower = prompt.lower()
        
        # Python function templates
        if 'fibonacci' in prompt_lower:
            return """def fibonacci(n):
    \"\"\"Generate Fibonacci sequence up to n terms\"\"\"
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    return sequence

# Example usage
print(fibonacci(10))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]"""

        elif 'factorial' in prompt_lower:
            return """def factorial(n):
    \"\"\"Calculate factorial of n\"\"\"
    if n < 0:
        return None
    elif n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)

# Example usage
print(factorial(5))  # 120"""

        elif 'sum' in prompt_lower and 'list' in prompt_lower:
            return """def sum_list(lst):
    \"\"\"Calculate sum of all elements in a list\"\"\"
    return sum(lst)

# Example usage
numbers = [1, 2, 3, 4, 5]
print(sum_list(numbers))  # 15"""

        elif 'sort' in prompt_lower and 'list' in prompt_lower:
            return """def sort_list(lst, reverse=False):
    \"\"\"Sort a list in ascending or descending order\"\"\"
    return sorted(lst, reverse=reverse)

# Example usage
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(sort_list(numbers))  # [1, 1, 2, 3, 4, 5, 6, 9]
print(sort_list(numbers, reverse=True))  # [9, 6, 5, 4, 3, 2, 1, 1]"""

        elif 'reverse' in prompt_lower and 'string' in prompt_lower:
            return """def reverse_string(text):
    \"\"\"Reverse a string\"\"\"
    return text[::-1]

# Example usage
print(reverse_string("Hello World"))  # dlroW olleH"""

        elif 'palindrome' in prompt_lower:
            return """def is_palindrome(text):
    \"\"\"Check if a string is a palindrome\"\"\"
    # Remove spaces and convert to lowercase
    cleaned = ''.join(char.lower() for char in text if char.isalnum())
    return cleaned == cleaned[::-1]

# Example usage
print(is_palindrome("A man a plan a canal Panama"))  # True
print(is_palindrome("Hello World"))  # False"""

        elif 'prime' in prompt_lower:
            return """def is_prime(n):
    \"\"\"Check if a number is prime\"\"\"
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_primes_up_to(n):
    \"\"\"Get all prime numbers up to n\"\"\"
    primes = []
    for num in range(2, n + 1):
        if is_prime(num):
            primes.append(num)
    return primes

# Example usage
print(is_prime(17))  # True
print(get_primes_up_to(20))  # [2, 3, 5, 7, 11, 13, 17, 19]"""

        elif 'calculator' in prompt_lower:
            return """def calculator():
    \"\"\"Simple calculator with basic operations\"\"\"
    print("Simple Calculator")
    print("Operations: +, -, *, /, **")
    
    while True:
        try:
            expression = input("Enter expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            
            result = eval(expression)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

# Example usage
calculator()"""

        elif 'file' in prompt_lower and 'read' in prompt_lower:
            return """def read_file(filename):
    \"\"\"Read and return contents of a file\"\"\"
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File '{filename}' not found"
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(filename, content):
    \"\"\"Write content to a file\"\"\"
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        return f"Successfully wrote to '{filename}'"
    except Exception as e:
        return f"Error writing file: {e}"

# Example usage
content = read_file('example.txt')
print(content)"""

        elif 'dictionary' in prompt_lower or 'dict' in prompt_lower:
            return """def create_dictionary():
    \"\"\"Create and manipulate a dictionary\"\"\"
    # Create a dictionary
    person = {
        'name': 'John Doe',
        'age': 30,
        'city': 'New York',
        'skills': ['Python', 'JavaScript', 'SQL']
    }
    
    # Access values
    print(f"Name: {person['name']}")
    print(f"Age: {person['age']}")
    
    # Add new key-value pair
    person['email'] = 'john@example.com'
    
    # Update value
    person['age'] = 31
    
    # Remove key
    if 'city' in person:
        del person['city']
    
    # Iterate through dictionary
    for key, value in person.items():
        print(f"{key}: {value}")
    
    return person

# Example usage
result = create_dictionary()"""

        elif 'class' in prompt_lower and 'student' in prompt_lower:
            return """class Student:
    \"\"\"A simple Student class\"\"\"
    
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade
        self.courses = []
    
    def add_course(self, course):
        \"\"\"Add a course to student's list\"\"\"
        self.courses.append(course)
        print(f"Added {course} to {self.name}'s courses")
    
    def get_average_grade(self):
        \"\"\"Calculate average grade\"\"\"
        if not self.courses:
            return 0
        return sum(self.courses) / len(self.courses)
    
    def display_info(self):
        \"\"\"Display student information\"\"\"
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Grade: {self.grade}")
        print(f"Courses: {self.courses}")
        print(f"Average: {self.get_average_grade():.2f}")

# Example usage
student = Student("Alice", 20, "A")
student.add_course(85)
student.add_course(92)
student.add_course(78)
student.display_info()"""

        elif 'web' in prompt_lower and 'scraper' in prompt_lower:
            return """import requests
from bs4 import BeautifulSoup

def web_scraper(url):
    \"\"\"Simple web scraper using requests and BeautifulSoup\"\"\"
    try:
        # Send GET request
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title = soup.title.string if soup.title else "No title found"
        
        # Extract all links
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        
        # Extract all text
        text = soup.get_text()
        
        return {
            'title': title,
            'links': links[:10],  # First 10 links
            'text_length': len(text)
        }
    except Exception as e:
        return f"Error scraping {url}: {e}"

# Example usage
result = web_scraper('https://example.com')
print(result)"""

        elif 'json' in prompt_lower:
            return """import json

def json_example():
    \"\"\"Demonstrate JSON operations\"\"\"
    
    # Create a Python dictionary
    data = {
        'name': 'John Doe',
        'age': 30,
        'city': 'New York',
        'hobbies': ['reading', 'gaming', 'coding'],
        'active': True
    }
    
    # Convert to JSON string
    json_string = json.dumps(data, indent=2)
    print("JSON String:")
    print(json_string)
    
    # Parse JSON string back to Python object
    parsed_data = json.loads(json_string)
    print(f"\\nParsed data type: {type(parsed_data)}")
    print(f"Name: {parsed_data['name']}")
    
    # Write JSON to file
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    # Read JSON from file
    with open('data.json', 'r') as f:
        loaded_data = json.load(f)
    
    return loaded_data

# Example usage
result = json_example()"""

        else:
            return f"""🤖 I can generate code for these topics:
• fibonacci - Fibonacci sequence generator
• factorial - Factorial calculation
• sum list - Sum of list elements
• sort list - Sort a list
• reverse string - Reverse a string
• palindrome - Check if string is palindrome
• prime - Prime number checker
• calculator - Simple calculator
• file read - File reading/writing
• dictionary - Dictionary operations
• class student - Student class example
• web scraper - Web scraping example
• json - JSON operations

Try asking for one of these specific topics, or ask me to explain any of these concepts!"""

        return "🤖 Code generated successfully! You can copy and run this code."

    def resize_sidebar(self, event):
        new_width = max(150, min(500, event.x_root - self.sidebar.winfo_rootx()))
        self.sidebar.configure(width=new_width)
        self.sidebar_width = new_width

    def set_chat_font_size(self, size):
        self.chat_font_size = size
        try:
            self.chat_text.configure(font=("Segoe UI", self.chat_font_size))
        except Exception:
            pass

    def load_or_prompt_profile(self):
        """Load or prompt for user profile."""
        try:
            # Try to load existing profile
            profile_files = glob.glob("profile_*.json")
            if profile_files:
                # Load the most recent profile
                latest_profile = max(profile_files, key=os.path.getctime)
                with open(latest_profile, 'r') as f:
                    profile_data = json.load(f)
                    self.profile_data = profile_data
                    self.username = profile_data.get('username', 'Default')
                    self.profile_picture_path = profile_data.get('profile_picture', None)
                    
                    # Load Gmail credentials if available
                    self.gmail_address = profile_data.get('gmail_address', None)
                    self.gmail_app_password = profile_data.get('gmail_app_password', None)
                    
                    # Load other settings
                    if 'theme' in profile_data:
                        self.theme = profile_data.get('theme', 'copilot_dark')
                    if 'language' in profile_data:
                        self.language = profile_data.get('language', 'English')
                        self.lang_code = LANGUAGES[self.language]["code"]
                        self.sr_code = LANGUAGES[self.language]["sr_code"]
                    if 'chat_font_size' in profile_data:
                        self.chat_font_size = profile_data.get('chat_font_size', 13)
                    if 'hotwords' in profile_data:
                        self.hotwords = profile_data.get('hotwords', ['sam', 'jarvis'])
                    if 'tts_voice_id' in profile_data:
                        self.tts_voice_id = profile_data.get('tts_voice_id', None)
                    # Planner settings
                    if 'planner_enabled' in profile_data:
                        self.planner_enabled = bool(profile_data.get('planner_enabled', True))
                    if 'planning_strategy' in profile_data:
                        self.planning_strategy = profile_data.get('planning_strategy', 'simple')
                    # Automation settings
                    if 'automation_strategy' in profile_data:
                        self.automation_strategy = profile_data.get('automation_strategy', 'direct')
                    self.profile_memory = profile_data.get('memory', {})
                    
                    # Update Gmail status if UI is available
                    if hasattr(self, 'update_gmail_status'):
                        self.update_gmail_status()
                    
                    # Update TTS settings after loading profile
                    if hasattr(self, 'update_tts_settings'):
                        self.update_tts_settings()
                    
                    return
            
            # If no profile exists, prompt for one
            self.username, self.profile_picture_path = self.prompt_for_profile()
        except Exception as e:
            print(f"Error loading profile: {e}")
            self.username = "Default"
            self.profile_picture_path = None

    def save_profile(self):
        """Save current profile settings to file."""
        # Ensure username is set
        if not hasattr(self, 'username') or self.username is None:
            self.username = "User"
        
        profile_data = {
            'username': self.username,
            'theme': self.theme,
            'language': self.language,
            'gmail_address': getattr(self, 'gmail_address', None),
            'gmail_app_password': getattr(self, 'gmail_app_password', None),
            'hotwords': self.hotwords,
            'chat_font_size': self.chat_font_size,
            'tts_voice_id': getattr(self, 'tts_voice_id', None),
            'planner_enabled': getattr(self, 'planner_enabled', True),
            'planning_strategy': getattr(self, 'planning_strategy', 'simple'),
            'automation_strategy': getattr(self, 'automation_strategy', 'direct'),
            'last_updated': datetime.datetime.now().isoformat(),
            'memory': (self.memory_manager.save() if hasattr(self, 'memory_manager') else getattr(self, 'profile_memory', {}))
        }
        try:
            # Clean username for filename
            clean_username = str(self.username).replace(' ', '_').replace('/', '_').replace('\\', '_')
            filename = f"profile_{clean_username}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            print(f"Profile saved to {filename}")
        except Exception as e:
            print(f"Could not save profile: {e}")
            try:
                # Show error dialog if GUI is available
                if hasattr(self, 'root'):
                    messagebox.showerror("Save Error", f"Could not save profile: {e}")
            except:
                pass

    def apply_auto_theme(self):
        import datetime
        now = datetime.datetime.now()
        hour = now.hour
        if 7 <= hour < 19:
            self.change_theme('light')
        else:
            self.change_theme('dark')
        # Schedule next check in 10 minutes
        self.root.after(600000, self.apply_auto_theme)

    def start_tictactoe(self):
        self.tictactoe_game = {
            'board': [[None]*3 for _ in range(3)],
            'turn': 'X',
            'over': False
        }
        self.display_response("🎮 Tic-Tac-Toe started! You are X. Enter your move as 'move row col' (e.g., 'move 1 1' for top-left).\n" + self.tictactoe_board_str())
    def tictactoe_move(self, row, col):
        g = self.tictactoe_game
        if g['over']:
            return "Game is over. Type 'play tic tac toe' to start a new game."
        if not (0 <= row < 3 and 0 <= col < 3):
            return "Invalid move. Row and column must be 1, 2, or 3."
        if g['board'][row][col] is not None:
            return "That cell is already taken. Try another move."
        g['board'][row][col] = 'X'
        if self.tictactoe_check_win('X'):
            g['over'] = True
            return self.tictactoe_board_str() + "\n🎉 You win! Type 'play tic tac toe' to play again."
        if all(cell for row_ in g['board'] for cell in row_):
            g['over'] = True
            return self.tictactoe_board_str() + "\n🤝 It's a draw! Type 'play tic tac toe' to play again."
        # Assistant's move (O, random)
        import random
        empty = [(r, c) for r in range(3) for c in range(3) if g['board'][r][c] is None]
        if empty:
            r, c = random.choice(empty)
            g['board'][r][c] = 'O'
            if self.tictactoe_check_win('O'):
                g['over'] = True
                return self.tictactoe_board_str() + "\n😢 Assistant wins! Type 'play tic tac toe' to play again."
        if all(cell for row_ in g['board'] for cell in row_):
            g['over'] = True
            return self.tictactoe_board_str() + "\n🤝 It's a draw! Type 'play tic tac toe' to play again."
        return self.tictactoe_board_str() + "\nYour turn! Enter your move as 'move row col'."
    def tictactoe_board_str(self):
        g = self.tictactoe_game
        board = g['board']
        def cell_str(cell):
            return cell if cell else ' '
        lines = []
        for row in board:
            lines.append(' | '.join(cell_str(c) for c in row))
        return '\n---------\n'.join(lines)
    def tictactoe_check_win(self, player):
        b = self.tictactoe_game['board']
        for i in range(3):
            if all(b[i][j] == player for j in range(3)) or all(b[j][i] == player for j in range(3)):
                return True
        if all(b[i][i] == player for i in range(3)) or all(b[i][2-i] == player for i in range(3)):
            return True
        return False

    def google_search(self, query):
        if not GoogleSearch:
            return "SerpAPI is not installed. Please run: pip install google-search-results"
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERPAPI_KEY,
            "num": 3
        }
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            if "error" in results:
                return f"SerpAPI error: {results['error']}"
            answer = ""
            if "answer_box" in results:
                answer += results["answer_box"].get("answer", "") + "\n"
            if "organic_results" in results:
                for res in results["organic_results"]:
                    answer += f"{res['title']}\n{res['link']}\n{res.get('snippet', '')}\n\n"
            return answer.strip() if answer else "No results found."
        except Exception as e:
            return f"Error using SerpAPI: {e}"

    def google_image_search(self, query):
        if not GoogleSearch:
            return "SerpAPI is not installed. Please run: pip install google-search-results"
        params = {
            "engine": "google_images",
            "q": query,
            "api_key": SERPAPI_KEY,
            "num": 3
        }
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            if "error" in results:
                return f"SerpAPI error: {results['error']}"
            images = results.get("images_results", [])
            if not images:
                return "No images found."
            answer = "🖼️ Top Images:\n\n"
            for img in images[:3]:
                title = img.get('title', '')
                url = img.get('original', img.get('thumbnail', ''))
                answer += f"{title}\n"
                self.insert_image_to_chat(url)
                answer += "\n"
            return answer.strip()
        except Exception as e:
            return f"Error using SerpAPI for images: {e}"

    def google_news_search(self, query):
        if not GoogleSearch:
            return "SerpAPI is not installed. Please run: pip install google-search-results"
        params = {
            "engine": "google_news",
            "q": query,
            "api_key": SERPAPI_KEY,
            "num": 5
        }
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            if "error" in results:
                return f"SerpAPI error: {results['error']}"
            news = results.get("news_results", [])
            if not news:
                return "No news found."
            answer = "📰 Top News Headlines:\n\n"
            for n in news[:5]:
                answer += f"{n.get('title', '')}\n{n.get('link', '')}\n{n.get('snippet', '')}\n\n"
            return answer.strip()
        except Exception as e:
            return f"Error using SerpAPI for news: {e}"

    def mistral_chat(self, prompt, model="mistral-medium"):
        """Human-like AI responses with natural conversation flow"""
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Build conversation context for more natural responses
        conversation_context = []
        
        # Add recent conversation history for context (last 5 messages)
        if hasattr(self, 'conversation_history') and len(self.conversation_history) > 0:
            recent_messages = self.conversation_history[-5:]
            for msg in recent_messages:
                if msg['sender'] == 'User':
                    conversation_context.append({"role": "user", "content": msg['message']})
                elif msg['sender'] == 'SAM':
                    conversation_context.append({"role": "assistant", "content": msg['message']})
        
        # Add current prompt with language context
        current_lang = getattr(self, 'language', 'English')
        if current_lang in ["Hindi", "Telugu"]:
            # Add language instruction for non-English prompts
            lang_instruction = f"Please respond in {current_lang} language. "
            conversation_context.append({"role": "user", "content": lang_instruction + prompt})
        else:
            conversation_context.append({"role": "user", "content": prompt})
        
        # Enhanced system prompt for human-like conversation with multi-language support
        current_lang = getattr(self, 'language', 'English')
        
        system_prompts = {
            "English": """You are SAM, a friendly and helpful AI assistant. You should:
- Respond naturally and conversationally, like a helpful friend
- Show personality and warmth in your responses
- Be concise but informative
- Use emojis occasionally to make responses more engaging
- Ask follow-up questions when appropriate
- Show enthusiasm for helping users
- Keep responses under 200 words unless detailed explanation is needed
- Use casual, friendly language while remaining professional""",
            
            "Hindi": """आप SAM हैं, एक मित्रवत और सहायक AI सहायक। आपको चाहिए:
- स्वाभाविक और बातचीत के तरीके से जवाब दें, जैसे एक सहायक दोस्त
- अपने जवाबों में व्यक्तित्व और गर्मजोशी दिखाएं
- संक्षिप्त लेकिन जानकारीपूर्ण रहें
- जवाबों को और आकर्षक बनाने के लिए कभी-कभी इमोजी का उपयोग करें
- जब उचित हो तो अनुवर्ती प्रश्न पूछें
- उपयोगकर्ताओं की मदद करने में उत्साह दिखाएं
- विस्तृत स्पष्टीकरण की आवश्यकता न होने पर 200 शब्दों से कम जवाब रखें
- पेशेवर रहते हुए आरामदायक, मित्रवत भाषा का उपयोग करें""",
            
            "Telugu": """మీరు SAM, ఒక స్నేహపూర్వక మరియు సహాయక AI సహాయకుడు. మీరు చేయాలి:
- సహాయక స్నేహితుడిలా సహజంగా మరియు సంభాషణా పద్ధతిలో సమాధానం ఇవ్వండి
- మీ సమాధానాలలో వ్యక్తిత్వం మరియు వెచ్చదనాన్ని చూపించండి
- సంక్షిప్తంగా కానీ సమాచారపూర్వకంగా ఉండండి
- సమాధానాలను మరింత ఆకర్షణీయంగా చేయడానికి కొన్నిసార్లు ఇమోజీలను ఉపయోగించండి
- తగినప్పుడు అనుసరణ ప్రశ్నలను అడగండి
- వినియోగదారులకు సహాయం చేయడంలో ఉత్సాహాన్ని చూపించండి
- వివరణాత్మక వివరణ అవసరం లేనప్పుడు 200 పదాల కంటే తక్కువ సమాధానాలను ఉంచండి
- వృత్తిపరంగా ఉండేటప్పుడు సౌకర్యవంతమైన, స్నేహపూర్వక భాషను ఉపయోగించండి"""
        }
        
        system_prompt = system_prompts.get(current_lang, system_prompts["English"])
        
        data = {
            "model": model,
            "messages": [{"role": "system", "content": system_prompt}] + conversation_context,
            "max_tokens": 300,  # Allow for more natural responses
            "temperature": 0.7,  # More creative and human-like
            "top_p": 0.9,
            "stream": False
        }
        try:
            response = requests.post(url, headers=headers, json=data, timeout=15)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            # Enhanced fallback with more personality
            print(f"Mistral API error: {e}")
            return self._get_fallback_response(prompt)
    
    def _get_fallback_response(self, prompt):
        """Provide helpful fallback responses when AI API is unavailable"""
        prompt_lower = prompt.lower()
        
        # Enhanced greeting responses with more personality and multi-language support
        greeting_keywords = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        if any(greeting in prompt_lower for greeting in greeting_keywords):
            current_lang = getattr(self, 'language', 'English')
            
            greetings = {
                "English": [
                    "👋 Hey there! How's your day going? I'm here to help with whatever you need!",
                    "😊 Hello! Great to see you! What can I assist you with today?",
                    "🌟 Hi! I'm excited to help you out. What's on your mind?",
                    "💫 Hey! Ready to tackle some tasks together? What would you like to work on?",
                    "🎉 Hi friend! I'm SAM and I'm here to make your day easier. What can I help with?",
                    "✨ Hello! I love helping people solve problems. What's your challenge today?"
                ],
                "Hindi": [
                    "👋 नमस्ते! आपका दिन कैसा जा रहा है? मैं आपकी मदद के लिए यहाँ हूं!",
                    "😊 हैलो! आपको देखकर अच्छा लगा! आज मैं आपकी क्या मदद कर सकता हूं?",
                    "🌟 हाय! मैं आपकी मदद करने के लिए उत्साहित हूं। आपके मन में क्या है?",
                    "💫 हैलो! चलिए कुछ काम करते हैं। आप क्या करना चाहते हैं?",
                    "🎉 हैलो दोस्त! मैं SAM हूं और मैं आपका दिन आसान बनाने के लिए यहाँ हूं।",
                    "✨ नमस्ते! मुझे लोगों की समस्याएं हल करना पसंद है। आज आपकी क्या चुनौती है?"
                ],
                "Telugu": [
                    "👋 నమస్కారం! మీ రోజు ఎలా జరుగుతోంది? నేను మీకు సహాయం చేయడానికి ఇక్కడ ఉన్నాను!",
                    "😊 హలో! మిమ్మల్ని చూసి మంచిగా ఉంది! నేను ఈరోజు మీకు ఎలా సహాయం చేయగలను?",
                    "🌟 హాయ్! నేను మీకు సహాయం చేయడానికి ఉత్సాహంతో ఉన్నాను. మీ మనస్సులో ఏమి ఉంది?",
                    "💫 హలో! కొన్ని పనులు చేద్దాం. మీరు ఏమి చేయాలనుకుంటున్నారు?",
                    "🎉 హలో స్నేహితుడా! నేను SAM మరియు మీ రోజును సులభతరం చేయడానికి ఇక్కడ ఉన్నాను.",
                    "✨ నమస్కారం! నాకు ప్రజల సమస్యలను పరిష్కరించడం ఇష్టం. ఈరోజు మీ సవాలు ఏమిటి?"
                ]
            }
            
            lang_greetings = greetings.get(current_lang, greetings["English"])
            return random.choice(lang_greetings)
        
        # Common questions and their responses
        fallback_responses = {
            "capital": {
                "france": "🇫🇷 The capital of France is Paris.",
                "india": "🇮🇳 The capital of India is New Delhi.",
                "usa": "🇺🇸 The capital of the USA is Washington, D.C.",
                "uk": "🇬🇧 The capital of the UK is London.",
                "germany": "🇩🇪 The capital of Germany is Berlin.",
                "japan": "🇯🇵 The capital of Japan is Tokyo.",
                "china": "🇨🇳 The capital of China is Beijing.",
                "russia": "🇷🇺 The capital of Russia is Moscow.",
                "canada": "🇨🇦 The capital of Canada is Ottawa.",
                "australia": "🇦🇺 The capital of Australia is Canberra."
            },
            "weather": "🌤️ I can't access real-time weather data right now. Please check a weather website for current conditions.",
            "time": f"🕐 Current time: {datetime.datetime.now().strftime('%H:%M:%S')}",
            "date": f"📅 Today's date: {datetime.datetime.now().strftime('%B %d, %Y')}",
            "help": "🤖 I can help with calculations, system info, web searches, and more. Try asking about specific topics!",
            "thanks": "😊 You're welcome! Is there anything else I can help with?",
            "thank you": "😊 You're welcome! Is there anything else I can help with?",
            "bye": "👋 Goodbye! Feel free to come back anytime.",
            "goodbye": "👋 Goodbye! Feel free to come back anytime."
        }
        
        # Check for capital questions
        for country, response in fallback_responses["capital"].items():
            if country in prompt_lower:
                return response
        
        # Check for other common patterns
        for key, response in fallback_responses.items():
            if key != "capital" and key in prompt_lower:
                return response
        
        # Check for "what is" questions
        if "what is" in prompt_lower:
            topic = prompt_lower.replace("what is", "").strip()
            if topic:
                return f"🤔 {topic.title()} is a topic I can help explain. Could you be more specific about what aspect you'd like to know?"
        
        # Check for "how to" questions
        if "how to" in prompt_lower or "how do" in prompt_lower:
            return f"🛠️ I'd be happy to help with that! What specific aspect would you like me to focus on?"
        
        # Enhanced default response with more personality and multi-language support
        current_lang = getattr(self, 'language', 'English')
        
        default_responses = {
            "English": [
                "🤖 I'm having a bit of trouble connecting to my AI service right now, but I can still help with system tasks, calculations, and basic information! What would you like to work on?",
                "😊 Hey, my AI connection is a bit slow right now, but I'm still here to help! Try asking about system info, weather, or use the quick action buttons!",
                "🌟 I'm experiencing some connection issues, but don't worry - I can still assist with many tasks! What can I help you with today?",
                "💫 My AI service is taking a break, but I'm still fully functional for system tasks and calculations. What would you like to explore?"
            ],
            "Hindi": [
                "🤖 मेरे AI सेवा से कनेक्ट करने में थोड़ी समस्या आ रही है, लेकिन मैं अभी भी सिस्टम कार्यों, गणनाओं और बुनियादी जानकारी में मदद कर सकता हूं! आप क्या करना चाहते हैं?",
                "😊 हैलो, मेरा AI कनेक्शन थोड़ा धीमा है, लेकिन मैं अभी भी यहाँ मदद के लिए हूं! सिस्टम जानकारी, मौसम के बारे में पूछें, या त्वरित कार्य बटन का उपयोग करें!",
                "🌟 मुझे कुछ कनेक्शन समस्याएं आ रही हैं, लेकिन चिंता न करें - मैं अभी भी कई कार्यों में सहायता कर सकता हूं! आज मैं आपकी क्या मदद कर सकता हूं?",
                "💫 मेरी AI सेवा थोड़ा ब्रेक ले रही है, लेकिन मैं अभी भी सिस्टम कार्यों और गणनाओं के लिए पूरी तरह से कार्यात्मक हूं। आप क्या खोजना चाहते हैं?"
            ],
            "Telugu": [
                "🤖 నా AI సేవతో కనెక్ట్ చేయడంలో కొంత సమస్య ఉంది, కానీ నేను ఇంకా సిస్టమ్ పనులు, గణనలు మరియు ప్రాథమిక సమాచారంలో సహాయం చేయగలను! మీరు ఏమి చేయాలనుకుంటున్నారు?",
                "😊 హలో, నా AI కనెక్షన్ కొంచెం నెమ్మదిగా ఉంది, కానీ నేను ఇంకా సహాయం కోసం ఇక్కడ ఉన్నాను! సిస్టమ్ సమాచారం, వాతావరణం గురించి అడగండి, లేదా త్వరిత చర్య బటన్లను ఉపయోగించండి!",
                "🌟 నాకు కొన్ని కనెక్షన్ సమస్యలు ఉన్నాయి, కానీ చింతించకండి - నేను ఇంకా చాలా పనులలో సహాయం చేయగలను! నేను ఈరోజు మీకు ఎలా సహాయం చేయగలను?",
                "💫 నా AI సేవ కొంచెం విరామం తీసుకుంటోంది, కానీ నేను ఇంకా సిస్టమ్ పనులు మరియు గణనల కోసం పూర్తిగా పని చేస్తున్నాను. మీరు ఏమి అన్వేషించాలనుకుంటున్నారు?"
            ]
        }
        
        lang_responses = default_responses.get(current_lang, default_responses["English"])
        return random.choice(lang_responses)

    def insert_image_to_chat(self, image_url):
        try:
            import requests
            from PIL import Image
            from io import BytesIO
            response = requests.get(image_url, timeout=10)
            img = Image.open(BytesIO(response.content))
            img.thumbnail((200, 200))  # Resize for chat
            photo = ImageTk.PhotoImage(img)
            self.chat_images.append(photo)  # Prevent garbage collection
            self.chat_text.image_create("end", image=photo)
            self.chat_text.insert("end", "\n")  # Newline after image
        except Exception as e:
            self.add_to_chat("System", f"Failed to load image: {e}", "error")

    def open_3d_model_viewer(self):
        """Open the 3D model viewer with various 3D shapes."""
        try:
            if not MATPLOTLIB_AVAILABLE:
                return "❌ 3D viewer not available. Install matplotlib: pip install matplotlib"
            
            self.add_to_chat("SAM", "🎲 Opening 3D Model Viewer...", "system")
            threading.Thread(target=self._show_3d_viewer, daemon=True).start()
            return "🎲 3D Model Viewer opened! You can view cubes, spheres, cylinders, and more."
            
        except Exception as e:
            return f"❌ Error opening 3D viewer: {str(e)}"

    def _show_3d_viewer(self):
        """Show the 3D model viewer window."""
        try:
            # Create 3D viewer window
            viewer_window = tk.Toplevel(self.root)
            viewer_window.title("SAM - 3D Model Viewer")
            viewer_window.geometry("800x600")
            viewer_window.configure(bg=THEMES[self.theme]["bg"])
            
            # Center the window
            viewer_window.update_idletasks()
            x = (viewer_window.winfo_screenwidth() // 2) - (800 // 2)
            y = (viewer_window.winfo_screenheight() // 2) - (600 // 2)
            viewer_window.geometry(f"800x600+{x}+{y}")
            
            # Make it modal
            viewer_window.transient(self.root)
            viewer_window.grab_set()
            
            # Create main frame
            main_frame = tk.Frame(viewer_window, bg=THEMES[self.theme]["bg"])
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Title
            title_label = tk.Label(
                main_frame, 
                text="🎲 3D Model Viewer", 
                font=("Segoe UI", 18, "bold"), 
                bg=THEMES[self.theme]["bg"], 
                fg=THEMES[self.theme]["fg"]
            )
            title_label.pack(pady=(0, 20))
            
            # Control frame
            control_frame = tk.Frame(main_frame, bg=THEMES[self.theme]["bg"])
            control_frame.pack(fill="x", pady=(0, 20))
            
            # Model selection
            tk.Label(
                control_frame, 
                text="Select 3D Model:", 
                font=("Segoe UI", 12, "bold"), 
                bg=THEMES[self.theme]["bg"], 
                fg=THEMES[self.theme]["fg"]
            ).pack(side="left", padx=(0, 10))
            
            model_var = tk.StringVar(value="cube")
            models = [
                ("Cube", "cube"),
                ("Sphere", "sphere"), 
                ("Cylinder", "cylinder"),
                ("Pyramid", "pyramid"),
                ("Torus", "torus"),
                ("Helix", "helix")
            ]
            
            model_menu = tk.OptionMenu(
                control_frame, 
                model_var, 
                *[model[1] for model in models],
                command=lambda x: self._update_3d_model(canvas, model_var.get())
            )
            model_menu.configure(
                font=("Segoe UI", 10),
                bg=THEMES[self.theme]["btnbg"],
                fg=THEMES[self.theme]["btnfg"],
                activebackground=THEMES[self.theme]["btnactive"],
                activeforeground=THEMES[self.theme]["btnfg"]
            )
            model_menu.pack(side="left", padx=(0, 20))
            
            # Rotation controls
            tk.Label(
                control_frame, 
                text="Rotation:", 
                font=("Segoe UI", 12, "bold"), 
                bg=THEMES[self.theme]["bg"], 
                fg=THEMES[self.theme]["fg"]
            ).pack(side="left", padx=(0, 10))
            
            # X rotation
            tk.Label(control_frame, text="X:", bg=THEMES[self.theme]["bg"], fg=THEMES[self.theme]["fg"]).pack(side="left")
            x_rot_var = tk.DoubleVar(value=45)
            x_rot_scale = tk.Scale(
                control_frame, 
                from_=0, 
                to=360, 
                orient="horizontal", 
                variable=x_rot_var,
                command=lambda x: self._update_3d_model(canvas, model_var.get(), x_rot_var.get(), y_rot_var.get()),
                bg=THEMES[self.theme]["bg"],
                fg=THEMES[self.theme]["fg"],
                highlightbackground=THEMES[self.theme]["bg"]
            )
            x_rot_scale.pack(side="left", padx=(0, 10))
            
            # Y rotation
            tk.Label(control_frame, text="Y:", bg=THEMES[self.theme]["bg"], fg=THEMES[self.theme]["fg"]).pack(side="left")
            y_rot_var = tk.DoubleVar(value=45)
            y_rot_scale = tk.Scale(
                control_frame, 
                from_=0, 
                to=360, 
                orient="horizontal", 
                variable=y_rot_var,
                command=lambda x: self._update_3d_model(canvas, model_var.get(), x_rot_var.get(), y_rot_var.get()),
                bg=THEMES[self.theme]["bg"],
                fg=THEMES[self.theme]["fg"],
                highlightbackground=THEMES[self.theme]["bg"]
            )
            y_rot_scale.pack(side="left", padx=(0, 10))
            
            # Create matplotlib figure
            fig = plt.figure(figsize=(8, 6))
            fig.patch.set_facecolor(THEMES[self.theme]["bg"])
            
            ax = fig.add_subplot(111, projection='3d')
            ax.set_facecolor(THEMES[self.theme]["bg"])
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
            ax.xaxis.pane.set_edgecolor(THEMES[self.theme]["fg"])
            ax.yaxis.pane.set_edgecolor(THEMES[self.theme]["fg"])
            ax.zaxis.pane.set_edgecolor(THEMES[self.theme]["fg"])
            ax.tick_params(colors=THEMES[self.theme]["fg"])
            
            # Create canvas
            canvas = FigureCanvasTkAgg(fig, main_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Initial model
            self._update_3d_model(canvas, "cube", 45, 45)
            
            # Auto-rotation
            auto_rot_var = tk.BooleanVar(value=False)
            auto_rot_check = tk.Checkbutton(
                control_frame,
                text="Auto Rotate",
                variable=auto_rot_var,
                command=lambda: self._toggle_auto_rotation(canvas, model_var, auto_rot_var),
                bg=THEMES[self.theme]["bg"],
                fg=THEMES[self.theme]["fg"],
                selectcolor=THEMES[self.theme]["card"],
                font=("Segoe UI", 10)
            )
            auto_rot_check.pack(side="right", padx=(20, 0))
            
        except Exception as e:
            print(f"Error creating 3D viewer: {e}")
            self.add_to_chat("System", f"Error creating 3D viewer: {str(e)}", "error")

    def _update_3d_model(self, canvas, model_type, x_rot=45, y_rot=45):
        """Update the 3D model display."""
        try:
            fig = canvas.figure
            ax = fig.axes[0]
            ax.clear()
            
            # Set theme colors
            ax.set_facecolor(THEMES[self.theme]["bg"])
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
            ax.xaxis.pane.set_edgecolor(THEMES[self.theme]["fg"])
            ax.yaxis.pane.set_edgecolor(THEMES[self.theme]["fg"])
            ax.zaxis.pane.set_edgecolor(THEMES[self.theme]["fg"])
            ax.tick_params(colors=THEMES[self.theme]["fg"])
            
            # Generate 3D model based on type
            if model_type == "cube":
                self._draw_cube(ax, x_rot, y_rot)
            elif model_type == "sphere":
                self._draw_sphere(ax, x_rot, y_rot)
            elif model_type == "cylinder":
                self._draw_cylinder(ax, x_rot, y_rot)
            elif model_type == "pyramid":
                self._draw_pyramid(ax, x_rot, y_rot)
            elif model_type == "torus":
                self._draw_torus(ax, x_rot, y_rot)
            elif model_type == "helix":
                self._draw_helix(ax, x_rot, y_rot)
            
            ax.set_xlabel('X', color=THEMES[self.theme]["fg"])
            ax.set_ylabel('Y', color=THEMES[self.theme]["fg"])
            ax.set_zlabel('Z', color=THEMES[self.theme]["fg"])
            ax.set_title(f'{model_type.title()} - 3D Model', color=THEMES[self.theme]["fg"])
            
            canvas.draw()
            
        except Exception as e:
            print(f"Error updating 3D model: {e}")

    def _draw_cube(self, ax, x_rot, y_rot):
        """Draw a 3D cube."""
        vertices = np.array([
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
        ])
        
        # Apply rotation
        theta_x = np.radians(x_rot)
        theta_y = np.radians(y_rot)
        
        rot_x = np.array([
            [1, 0, 0],
            [0, np.cos(theta_x), -np.sin(theta_x)],
            [0, np.sin(theta_x), np.cos(theta_x)]
        ])
        
        rot_y = np.array([
            [np.cos(theta_y), 0, np.sin(theta_y)],
            [0, 1, 0],
            [-np.sin(theta_y), 0, np.cos(theta_y)]
        ])
        
        vertices = vertices @ rot_x.T @ rot_y.T
        
        # Define faces
        faces = [
            [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
            [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]
        ]
        
        # Draw faces
        for face in faces:
            x = [vertices[i][0] for i in face]
            y = [vertices[i][1] for i in face]
            z = [vertices[i][2] for i in face]
            ax.plot_trisurf(x, y, z, alpha=0.7, color='skyblue')

    def _draw_sphere(self, ax, x_rot, y_rot):
        """Draw a 3D sphere."""
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        x = 0.5 * np.outer(np.cos(u), np.sin(v))
        y = 0.5 * np.outer(np.sin(u), np.sin(v))
        z = 0.5 * np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Apply rotation
        theta_x = np.radians(x_rot)
        theta_y = np.radians(y_rot)
        
        rot_x = np.array([
            [1, 0, 0],
            [0, np.cos(theta_x), -np.sin(theta_x)],
            [0, np.sin(theta_x), np.cos(theta_x)]
        ])
        
        rot_y = np.array([
            [np.cos(theta_y), 0, np.sin(theta_y)],
            [0, 1, 0],
            [-np.sin(theta_y), 0, np.cos(theta_y)]
        ])
        
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                point = np.array([x[i,j], y[i,j], z[i,j]])
                rotated_point = point @ rot_x.T @ rot_y.T
                x[i,j] = rotated_point[0]
                y[i,j] = rotated_point[1]
                z[i,j] = rotated_point[2]
        
        ax.plot_surface(x, y, z, alpha=0.7, color='lightgreen')

    def _draw_cylinder(self, ax, x_rot, y_rot):
        """Draw a 3D cylinder."""
        theta = np.linspace(0, 2*np.pi, 20)
        z = np.linspace(0, 1, 20)
        theta_grid, z_grid = np.meshgrid(theta, z)
        
        x = 0.5 * np.cos(theta_grid)
        y = 0.5 * np.sin(theta_grid)
        
        # Apply rotation
        theta_x = np.radians(x_rot)
        theta_y = np.radians(y_rot)
        
        rot_x = np.array([
            [1, 0, 0],
            [0, np.cos(theta_x), -np.sin(theta_x)],
            [0, np.sin(theta_x), np.cos(theta_x)]
        ])
        
        rot_y = np.array([
            [np.cos(theta_y), 0, np.sin(theta_y)],
            [0, 1, 0],
            [-np.sin(theta_y), 0, np.cos(theta_y)]
        ])
        
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                point = np.array([x[i,j], y[i,j], z_grid[i,j]])
                rotated_point = point @ rot_x.T @ rot_y.T
                x[i,j] = rotated_point[0]
                y[i,j] = rotated_point[1]
                z_grid[i,j] = rotated_point[2]
        
        ax.plot_surface(x, y, z_grid, alpha=0.7, color='lightcoral')

    def _draw_pyramid(self, ax, x_rot, y_rot):
        """Draw a 3D pyramid."""
        vertices = np.array([
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # base
            [0.5, 0.5, 1]  # apex
        ])
        
        # Apply rotation
        theta_x = np.radians(x_rot)
        theta_y = np.radians(y_rot)
        
        rot_x = np.array([
            [1, 0, 0],
            [0, np.cos(theta_x), -np.sin(theta_x)],
            [0, np.sin(theta_x), np.cos(theta_x)]
        ])
        
        rot_y = np.array([
            [np.cos(theta_y), 0, np.sin(theta_y)],
            [0, 1, 0],
            [-np.sin(theta_y), 0, np.cos(theta_y)]
        ])
        
        vertices = vertices @ rot_x.T @ rot_y.T
        
        # Define faces
        faces = [
            [0, 1, 2, 3],  # base
            [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]  # sides
        ]
        
        # Draw faces
        for face in faces:
            x = [vertices[i][0] for i in face]
            y = [vertices[i][1] for i in face]
            z = [vertices[i][2] for i in face]
            ax.plot_trisurf(x, y, z, alpha=0.7, color='gold')

    def _draw_torus(self, ax, x_rot, y_rot):
        """Draw a 3D torus."""
        R = 0.5  # major radius
        r = 0.2  # minor radius
        
        theta = np.linspace(0, 2*np.pi, 30)
        phi = np.linspace(0, 2*np.pi, 30)
        theta_grid, phi_grid = np.meshgrid(theta, phi)
        
        x = (R + r * np.cos(phi_grid)) * np.cos(theta_grid)
        y = (R + r * np.cos(phi_grid)) * np.sin(theta_grid)
        z = r * np.sin(phi_grid)
        
        # Apply rotation
        theta_x = np.radians(x_rot)
        theta_y = np.radians(y_rot)
        
        rot_x = np.array([
            [1, 0, 0],
            [0, np.cos(theta_x), -np.sin(theta_x)],
            [0, np.sin(theta_x), np.cos(theta_x)]
        ])
        
        rot_y = np.array([
            [np.cos(theta_y), 0, np.sin(theta_y)],
            [0, 1, 0],
            [-np.sin(theta_y), 0, np.cos(theta_y)]
        ])
        
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                point = np.array([x[i,j], y[i,j], z[i,j]])
                rotated_point = point @ rot_x.T @ rot_y.T
                x[i,j] = rotated_point[0]
                y[i,j] = rotated_point[1]
                z[i,j] = rotated_point[2]
        
        ax.plot_surface(x, y, z, alpha=0.7, color='plum')

    def _draw_helix(self, ax, x_rot, y_rot):
        """Draw a 3D helix."""
        t = np.linspace(0, 4*np.pi, 100)
        x = 0.3 * np.cos(t)
        y = 0.3 * np.sin(t)
        z = t / (4*np.pi)
        
        # Apply rotation
        theta_x = np.radians(x_rot)
        theta_y = np.radians(y_rot)
        
        rot_x = np.array([
            [1, 0, 0],
            [0, np.cos(theta_x), -np.sin(theta_x)],
            [0, np.sin(theta_x), np.cos(theta_x)]
        ])
        
        rot_y = np.array([
            [np.cos(theta_y), 0, np.sin(theta_y)],
            [0, 1, 0],
            [-np.sin(theta_y), 0, np.cos(theta_y)]
        ])
        
        for i in range(len(x)):
            point = np.array([x[i], y[i], z[i]])
            rotated_point = point @ rot_x.T @ rot_y.T
            x[i] = rotated_point[0]
            y[i] = rotated_point[1]
            z[i] = rotated_point[2]
        
        ax.plot(x, y, z, linewidth=3, color='orange')

    def _toggle_auto_rotation(self, canvas, model_var, auto_rot_var):
        """Toggle auto-rotation for 3D models."""
        if auto_rot_var.get():
            self._auto_rotate(canvas, model_var, auto_rot_var)

    def _auto_rotate(self, canvas, model_var, auto_rot_var):
        """Auto-rotate the 3D model."""
        if auto_rot_var.get():
            # Get current rotation values
            scales = canvas.get_tk_widget().master.master.winfo_children()[1].winfo_children()
            x_scale = scales[4]  # X rotation scale
            y_scale = scales[6]  # Y rotation scale
            
            current_x = x_scale.get()
            current_y = y_scale.get()
            
            # Update rotation
            new_x = (current_x + 5) % 360
            new_y = (current_y + 3) % 360
            
            x_scale.set(new_x)
            y_scale.set(new_y)
            
            # Schedule next rotation
            canvas.get_tk_widget().after(100, lambda: self._auto_rotate(canvas, model_var, auto_rot_var))

    def _handle_3d_model_command(self, command):
        """Handle 3D model related commands."""
        command_lower = command.lower()
        
        if 'cube' in command_lower:
            return "🎲 Opening 3D Cube viewer..."
        elif 'sphere' in command_lower:
            return "🔵 Opening 3D Sphere viewer..."
        elif 'cylinder' in command_lower:
            return "📏 Opening 3D Cylinder viewer..."
        elif 'pyramid' in command_lower:
            return "🔺 Opening 3D Pyramid viewer..."
        elif 'torus' in command_lower:
            return "🍩 Opening 3D Torus viewer..."
        elif 'helix' in command_lower:
            return "🌀 Opening 3D Helix viewer..."
        elif any(word in command_lower for word in ['load', 'open', 'file', 'stl', 'obj', 'ply']):
            return self.load_custom_3d_model()
        else:
            return self.open_3d_model_viewer()

    def load_custom_3d_model(self):
        """Load and display a custom 3D model file."""
        try:
            if not TRIMESH_AVAILABLE and not STL_AVAILABLE:
                return "❌ 3D file support not available. Install: pip install trimesh numpy-stl"
            
            # Open file dialog for 3D model files
            file_types = [
                ("3D Model Files", "*.obj *.stl *.ply *.dae *.fbx *.3ds"),
                ("OBJ Files", "*.obj"),
                ("STL Files", "*.stl"),
                ("PLY Files", "*.ply"),
                ("All Files", "*.*")
            ]
            
            filename = filedialog.askopenfilename(
                title="Select 3D Model File",
                filetypes=file_types,
                initialdir=os.path.expanduser("~/Downloads")  # Start in Downloads folder
            )
            
            if not filename:
                return "❌ No file selected."
            
            self.add_to_chat("SAM", f"📁 Loading 3D model: {os.path.basename(filename)}", "system")
            
            # Load and display the model
            threading.Thread(target=self._show_custom_3d_model, args=(filename,), daemon=True).start()
            
            return f"📁 Loading 3D model: {os.path.basename(filename)}"
            
        except Exception as e:
            return f"❌ Error loading 3D model: {str(e)}"

    def _show_custom_3d_model(self, filename):
        """Show a custom 3D model in the viewer."""
        try:
            # Load the 3D model
            mesh = self._load_3d_file(filename)
            if mesh is None:
                self.add_to_chat("System", f"❌ Failed to load 3D model: {os.path.basename(filename)}", "error")
                return
            
            # Create 3D viewer window
            viewer_window = tk.Toplevel(self.root)
            viewer_window.title(f"SAM - 3D Model Viewer - {os.path.basename(filename)}")
            viewer_window.geometry("900x700")
            viewer_window.configure(bg=THEMES[self.theme]["bg"])
            
            # Center the window
            viewer_window.update_idletasks()
            x = (viewer_window.winfo_screenwidth() // 2) - (900 // 2)
            y = (viewer_window.winfo_screenheight() // 2) - (700 // 2)
            viewer_window.geometry(f"900x700+{x}+{y}")
            
            # Make it modal
            viewer_window.transient(self.root)
            viewer_window.grab_set()
            
            # Create main frame
            main_frame = tk.Frame(viewer_window, bg=THEMES[self.theme]["bg"])
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Title
            title_label = tk.Label(
                main_frame, 
                text=f"🎲 3D Model: {os.path.basename(filename)}", 
                font=("Segoe UI", 16, "bold"), 
                bg=THEMES[self.theme]["bg"], 
                fg=THEMES[self.theme]["fg"]
            )
            title_label.pack(pady=(0, 20))
            
            # Model info frame
            info_frame = tk.Frame(main_frame, bg=THEMES[self.theme]["bg"])
            info_frame.pack(fill="x", pady=(0, 20))
            
            # Display model information
            model_info = self._get_model_info(mesh)
            info_text = f"📊 Model Info: {model_info['vertices']} vertices, {model_info['faces']} faces, {model_info['volume']:.2f} volume"
            info_label = tk.Label(
                info_frame,
                text=info_text,
                font=("Segoe UI", 10),
                bg=THEMES[self.theme]["bg"],
                fg=THEMES[self.theme]["fg"]
            )
            info_label.pack()
            
            # Control frame
            control_frame = tk.Frame(main_frame, bg=THEMES[self.theme]["bg"])
            control_frame.pack(fill="x", pady=(0, 20))
            
            # Rotation controls
            tk.Label(
                control_frame, 
                text="Rotation:", 
                font=("Segoe UI", 12, "bold"), 
                bg=THEMES[self.theme]["bg"], 
                fg=THEMES[self.theme]["fg"]
            ).pack(side="left", padx=(0, 10))
            
            # X rotation
            tk.Label(control_frame, text="X:", bg=THEMES[self.theme]["bg"], fg=THEMES[self.theme]["fg"]).pack(side="left")
            x_rot_var = tk.DoubleVar(value=0)
            x_rot_scale = tk.Scale(
                control_frame, 
                from_=0, 
                to=360, 
                orient="horizontal", 
                variable=x_rot_var,
                command=lambda x: self._update_custom_3d_model(canvas, mesh, x_rot_var.get(), y_rot_var.get(), z_rot_var.get()),
                bg=THEMES[self.theme]["bg"],
                fg=THEMES[self.theme]["fg"],
                highlightbackground=THEMES[self.theme]["bg"]
            )
            x_rot_scale.pack(side="left", padx=(0, 10))
            
            # Y rotation
            tk.Label(control_frame, text="Y:", bg=THEMES[self.theme]["bg"], fg=THEMES[self.theme]["fg"]).pack(side="left")
            y_rot_var = tk.DoubleVar(value=0)
            y_rot_scale = tk.Scale(
                control_frame, 
                from_=0, 
                to=360, 
                orient="horizontal", 
                variable=y_rot_var,
                command=lambda x: self._update_custom_3d_model(canvas, mesh, x_rot_var.get(), y_rot_var.get(), z_rot_var.get()),
                bg=THEMES[self.theme]["bg"],
                fg=THEMES[self.theme]["fg"],
                highlightbackground=THEMES[self.theme]["bg"]
            )
            y_rot_scale.pack(side="left", padx=(0, 10))
            
            # Z rotation
            tk.Label(control_frame, text="Z:", bg=THEMES[self.theme]["bg"], fg=THEMES[self.theme]["fg"]).pack(side="left")
            z_rot_var = tk.DoubleVar(value=0)
            z_rot_scale = tk.Scale(
                control_frame, 
                from_=0, 
                to=360, 
                orient="horizontal", 
                variable=z_rot_var,
                command=lambda x: self._update_custom_3d_model(canvas, mesh, x_rot_var.get(), y_rot_var.get(), z_rot_var.get()),
                bg=THEMES[self.theme]["bg"],
                fg=THEMES[self.theme]["fg"],
                highlightbackground=THEMES[self.theme]["bg"]
            )
            z_rot_scale.pack(side="left", padx=(0, 10))
            
            # Auto-rotation
            auto_rot_var = tk.BooleanVar(value=False)
            auto_rot_check = tk.Checkbutton(
                control_frame,
                text="Auto Rotate",
                variable=auto_rot_var,
                command=lambda: self._toggle_custom_auto_rotation(canvas, mesh, auto_rot_var, x_rot_var, y_rot_var, z_rot_var),
                bg=THEMES[self.theme]["bg"],
                fg=THEMES[self.theme]["fg"],
                selectcolor=THEMES[self.theme]["card"],
                font=("Segoe UI", 10)
            )
            auto_rot_check.pack(side="right", padx=(20, 0))
            
            # Create matplotlib figure
            fig = plt.figure(figsize=(10, 8))
            fig.patch.set_facecolor(THEMES[self.theme]["bg"])
            
            ax = fig.add_subplot(111, projection='3d')
            ax.set_facecolor(THEMES[self.theme]["bg"])
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
            ax.xaxis.pane.set_edgecolor(THEMES[self.theme]["fg"])
            ax.yaxis.pane.set_edgecolor(THEMES[self.theme]["fg"])
            ax.zaxis.pane.set_edgecolor(THEMES[self.theme]["fg"])
            ax.tick_params(colors=THEMES[self.theme]["fg"])
            
            # Create canvas
            canvas = FigureCanvasTkAgg(fig, main_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Store references for auto-rotation
            canvas.mesh = mesh
            canvas.x_rot_var = x_rot_var
            canvas.y_rot_var = y_rot_var
            canvas.z_rot_var = z_rot_var
            canvas.auto_rot_var = auto_rot_var
            
            # Initial display
            self._update_custom_3d_model(canvas, mesh, 0, 0, 0)
            
            self.add_to_chat("System", f"✅ 3D model loaded successfully: {os.path.basename(filename)}", "system")
            
        except Exception as e:
            print(f"Error showing custom 3D model: {e}")
            self.add_to_chat("System", f"Error displaying 3D model: {str(e)}", "error")

    def _load_3d_file(self, filename):
        """Load a 3D model file using appropriate library."""
        try:
            file_ext = os.path.splitext(filename)[1].lower()
            
            if file_ext == '.stl' and STL_AVAILABLE:
                # Load STL file using numpy-stl
                mesh_data = stl_mesh.Mesh.from_file(filename)
                vertices = mesh_data.vectors.reshape(-1, 3)
                faces = np.arange(len(vertices)).reshape(-1, 3)
                return {'vertices': vertices, 'faces': faces, 'type': 'stl'}
            
            elif TRIMESH_AVAILABLE:
                # Load using trimesh (supports OBJ, PLY, DAE, FBX, 3DS, etc.)
                mesh = trimesh.load(filename)
                if hasattr(mesh, 'vertices') and hasattr(mesh, 'faces'):
                    return {
                        'vertices': np.array(mesh.vertices),
                        'faces': np.array(mesh.faces),
                        'type': file_ext[1:]
                    }
                else:
                    print(f"Unsupported mesh type: {type(mesh)}")
                    return None
            
            else:
                print(f"Unsupported file format: {file_ext}")
                return None
                
        except Exception as e:
            print(f"Error loading 3D file: {e}")
            return None

    def _get_model_info(self, mesh):
        """Get information about the loaded 3D model."""
        try:
            vertices = len(mesh['vertices'])
            faces = len(mesh['faces'])
            
            # Calculate approximate volume (simplified)
            if faces > 0:
                # Simple volume estimation
                volume = vertices * 0.001  # Rough estimate
            else:
                volume = 0.0
            
            return {
                'vertices': vertices,
                'faces': faces,
                'volume': volume
            }
        except Exception as e:
            print(f"Error getting model info: {e}")
            return {'vertices': 0, 'faces': 0, 'volume': 0.0}

    def _update_custom_3d_model(self, canvas, mesh, x_rot, y_rot, z_rot):
        """Update the custom 3D model display with rotation."""
        try:
            fig = canvas.figure
            ax = fig.axes[0]
            ax.clear()
            
            # Set theme colors
            ax.set_facecolor(THEMES[self.theme]["bg"])
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
            ax.xaxis.pane.set_edgecolor(THEMES[self.theme]["fg"])
            ax.yaxis.pane.set_edgecolor(THEMES[self.theme]["fg"])
            ax.zaxis.pane.set_edgecolor(THEMES[self.theme]["fg"])
            ax.tick_params(colors=THEMES[self.theme]["fg"])
            
            # Get vertices and faces
            vertices = mesh['vertices']
            faces = mesh['faces']
            
            # Apply rotation
            rotated_vertices = self._apply_rotation(vertices, x_rot, y_rot, z_rot)
            
            # Draw the mesh
            if len(faces) > 0:
                # Draw as triangulated surface
                for face in faces:
                    if len(face) >= 3:  # Ensure we have at least 3 vertices
                        x = [rotated_vertices[i][0] for i in face[:3]]
                        y = [rotated_vertices[i][1] for i in face[:3]]
                        z = [rotated_vertices[i][2] for i in face[:3]]
                        ax.plot_trisurf(x, y, z, alpha=0.7, color='lightblue')
            else:
                # Draw as point cloud
                ax.scatter(rotated_vertices[:, 0], rotated_vertices[:, 1], rotated_vertices[:, 2], 
                          c='lightblue', alpha=0.7, s=1)
            
            # Set labels and title
            ax.set_xlabel('X', color=THEMES[self.theme]["fg"])
            ax.set_ylabel('Y', color=THEMES[self.theme]["fg"])
            ax.set_zlabel('Z', color=THEMES[self.theme]["fg"])
            ax.set_title(f'Custom 3D Model - {mesh["type"].upper()}', color=THEMES[self.theme]["fg"])
            
            canvas.draw()
            
        except Exception as e:
            print(f"Error updating custom 3D model: {e}")

    def _apply_rotation(self, vertices, x_rot, y_rot, z_rot):
        """Apply rotation matrices to vertices."""
        try:
            # Convert to radians
            theta_x = np.radians(x_rot)
            theta_y = np.radians(y_rot)
            theta_z = np.radians(z_rot)
            
            # Rotation matrices
            rot_x = np.array([
                [1, 0, 0],
                [0, np.cos(theta_x), -np.sin(theta_x)],
                [0, np.sin(theta_x), np.cos(theta_x)]
            ])
            
            rot_y = np.array([
                [np.cos(theta_y), 0, np.sin(theta_y)],
                [0, 1, 0],
                [-np.sin(theta_y), 0, np.cos(theta_y)]
            ])
            
            rot_z = np.array([
                [np.cos(theta_z), -np.sin(theta_z), 0],
                [np.sin(theta_z), np.cos(theta_z), 0],
                [0, 0, 1]
            ])
            
            # Apply rotations
            rotated = vertices @ rot_x.T @ rot_y.T @ rot_z.T
            return rotated
            
        except Exception as e:
            print(f"Error applying rotation: {e}")
            return vertices

    def _toggle_custom_auto_rotation(self, canvas, mesh, auto_rot_var, x_rot_var, y_rot_var, z_rot_var):
        """Toggle auto-rotation for custom 3D models."""
        if auto_rot_var.get():
            self._auto_rotate_custom_model(canvas, mesh, auto_rot_var, x_rot_var, y_rot_var, z_rot_var)

    def _auto_rotate_custom_model(self, canvas, mesh, auto_rot_var, x_rot_var, y_rot_var, z_rot_var):
        """Auto-rotate the custom 3D model."""
        if auto_rot_var.get():
            # Update rotation values
            current_x = x_rot_var.get()
            current_y = y_rot_var.get()
            current_z = z_rot_var.get()
            
            new_x = (current_x + 2) % 360
            new_y = (current_y + 3) % 360
            new_z = (current_z + 1) % 360
            
            x_rot_var.set(new_x)
            y_rot_var.set(new_y)
            z_rot_var.set(new_z)
            
            # Schedule next rotation
            canvas.get_tk_widget().after(50, lambda: self._auto_rotate_custom_model(canvas, mesh, auto_rot_var, x_rot_var, y_rot_var, z_rot_var))



    def load_user_commands(self):
        """Load user-defined commands from file."""
        try:
            with open(resource_path('user_commands.json'), 'r', encoding='utf-8') as f:
                self.user_commands = json.load(f)
        except Exception:
            self.user_commands = {}

    def save_user_commands(self):
        try:
            with open(resource_path('user_commands.json'), 'w', encoding='utf-8') as f:
                json.dump(self.user_commands, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving user commands: {e}")

    def ascii_art_generator(self):
        """Generate ASCII art using built-in characters."""
        popup = tk.Toplevel(self.root)
        popup.title("ASCII Art Generator")
        popup.geometry("600x500")
        popup.configure(bg=THEMES[self.theme]["bg"])
        popup.transient(self.root)
        popup.grab_set()
        
        # Main frame
        main_frame = tk.Frame(popup, bg=THEMES[self.theme]["bg"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(main_frame, text="ASCII Art Generator", 
                font=("Segoe UI", 16, "bold"), 
                bg=THEMES[self.theme]["bg"], 
                fg=THEMES[self.theme]["fg"]).pack(pady=(0, 10))
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg=THEMES[self.theme]["bg"])
        input_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(input_frame, text="Enter text to convert to ASCII art:", 
                font=("Segoe UI", 12), 
                bg=THEMES[self.theme]["bg"], 
                fg=THEMES[self.theme]["fg"]).pack(anchor="w")
        
        entry = tk.Entry(input_frame, font=("Segoe UI", 12), width=40)
        entry.pack(pady=5, fill="x")
        entry.focus()
        
        # Style selection
        style_frame = tk.Frame(main_frame, bg=THEMES[self.theme]["bg"])
        style_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(style_frame, text="Select style:", 
                font=("Segoe UI", 12), 
                bg=THEMES[self.theme]["bg"], 
                fg=THEMES[self.theme]["fg"]).pack(anchor="w")
        
        style_var = tk.StringVar(value="block")
        styles = [("Block", "block"), ("Simple", "simple"), ("Fancy", "fancy"), ("Stars", "stars")]
        
        for text, value in styles:
            tk.Radiobutton(style_frame, text=text, variable=style_var, value=value,
                          font=("Segoe UI", 10), bg=THEMES[self.theme]["bg"], 
                          fg=THEMES[self.theme]["fg"], selectcolor=THEMES[self.theme]["card"]).pack(side="left", padx=(0, 20))
        
        # Output area
        output_frame = tk.Frame(main_frame, bg=THEMES[self.theme]["bg"])
        output_frame.pack(fill="both", expand=True)
        
        output = tk.Text(output_frame, font=("Courier New", 10), 
                        bg=THEMES[self.theme]["scrolledbg"], 
                        fg=THEMES[self.theme]["textfg"], 
                        height=15, wrap="none")
        output.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(output_frame, orient="vertical", command=output.yview)
        scrollbar.pack(side="right", fill="y")
        output.configure(yscrollcommand=scrollbar.set)
        
        def generate_ascii_art():
            """Generate ASCII art using built-in patterns."""
            text = entry.get().strip().upper()
            if not text:
                output.delete(1.0, 'end')
                output.insert('end', "Please enter some text!")
                return
            
            style = style_var.get()
            art = ""
            
            # ASCII art patterns
            patterns = {
                "block": {
                    'A': ["  ██  ", " ████ ", "██  ██", "██████", "██  ██"],
                    'B': ["█████ ", "██  ██", "█████ ", "██  ██", "█████ "],
                    'C': [" █████", "██    ", "██    ", "██    ", " █████"],
                    'D': ["█████ ", "██  ██", "██  ██", "██  ██", "█████ "],
                    'E': ["██████", "██    ", "████  ", "██    ", "██████"],
                    'F': ["██████", "██    ", "████  ", "██    ", "██    "],
                    'G': [" █████", "██    ", "██ ███", "██  ██", " █████"],
                    'H': ["██  ██", "██  ██", "██████", "██  ██", "██  ██"],
                    'I': ["██████", "  ██  ", "  ██  ", "  ██  ", "██████"],
                    'J': ["██████", "    ██", "    ██", "██  ██", " ████ "],
                    'K': ["██  ██", "██ ██ ", "████  ", "██ ██ ", "██  ██"],
                    'L': ["██    ", "██    ", "██    ", "██    ", "██████"],
                    'M': ["██  ██", "██████", "██  ██", "██  ██", "██  ██"],
                    'N': ["██  ██", "████ ██", "██ ████", "██  ██", "██  ██"],
                    'O': [" ████ ", "██  ██", "██  ██", "██  ██", " ████ "],
                    'P': ["█████ ", "██  ██", "█████ ", "██    ", "██    "],
                    'Q': [" ████ ", "██  ██", "██  ██", "██ ██ ", " ████ "],
                    'R': ["█████ ", "██  ██", "█████ ", "██ ██ ", "██  ██"],
                    'S': [" █████", "██    ", " ████ ", "    ██", "█████ "],
                    'T': ["██████", "  ██  ", "  ██  ", "  ██  ", "  ██  "],
                    'U': ["██  ██", "██  ██", "██  ██", "██  ██", " ████ "],
                    'V': ["██  ██", "██  ██", "██  ██", " ████ ", "  ██  "],
                    'W': ["██  ██", "██  ██", "██  ██", "██████", "██  ██"],
                    'X': ["██  ██", " ████ ", "  ██  ", " ████ ", "██  ██"],
                    'Y': ["██  ██", "██  ██", " ████ ", "  ██  ", "  ██  "],
                    'Z': ["██████", "    ██", "  ██  ", "██    ", "██████"],
                    ' ': ["      ", "      ", "      ", "      ", "      "],
                    '0': [" ████ ", "██  ██", "██  ██", "██  ██", " ████ "],
                    '1': ["  ██  ", " ████  ", "  ██  ", "  ██  ", "██████"],
                    '2': [" ████ ", "██  ██", "   ██ ", " ██   ", "██████"],
                    '3': [" ████ ", "██  ██", "  ███ ", "██  ██", " ████ "],
                    '4': ["██  ██", "██  ██", "██████", "    ██", "    ██"],
                    '5': ["██████", "██    ", "█████ ", "    ██", "█████ "],
                    '6': [" ████ ", "██    ", "█████ ", "██  ██", " ████ "],
                    '7': ["██████", "    ██", "  ██  ", " ██   ", " ██   "],
                    '8': [" ████ ", "██  ██", " ████ ", "██  ██", " ████ "],
                    '9': [" ████ ", "██  ██", " █████", "    ██", " ████ "],
                },
                "simple": {
                    'A': [" AAA ", "A   A", "AAAAA", "A   A", "A   A"],
                    'B': ["AAAA ", "A   A", "AAAA ", "A   A", "AAAA "],
                    'C': [" AAAA", "A    ", "A    ", "A    ", " AAAA"],
                    'D': ["AAAA ", "A   A", "A   A", "A   A", "AAAA "],
                    'E': ["AAAAA", "A    ", "AAAA ", "A    ", "AAAAA"],
                    'F': ["AAAAA", "A    ", "AAAA ", "A    ", "A    "],
                    'G': [" AAAA", "A    ", "A AAA", "A   A", " AAAA"],
                    'H': ["A   A", "A   A", "AAAAA", "A   A", "A   A"],
                    'I': ["AAAAA", "  A  ", "  A  ", "  A  ", "AAAAA"],
                    'J': ["AAAAA", "    A", "    A", "A   A", " AAA "],
                    'K': ["A   A", "A  A ", "AAA  ", "A  A ", "A   A"],
                    'L': ["A    ", "A    ", "A    ", "A    ", "AAAAA"],
                    'M': ["A   A", "AA AA", "A A A", "A   A", "A   A"],
                    'N': ["A   A", "AA  A", "A A A", "A  AA", "A   A"],
                    'O': [" AAA ", "A   A", "A   A", "A   A", " AAA "],
                    'P': ["AAAA ", "A   A", "AAAA ", "A    ", "A    "],
                    'Q': [" AAA ", "A   A", "A   A", "A  A ", " AAA "],
                    'R': ["AAAA ", "A   A", "AAAA ", "A  A ", "A   A"],
                    'S': [" AAAA", "A    ", " AAA ", "    A", "AAAA "],
                    'T': ["AAAAA", "  A  ", "  A  ", "  A  ", "  A  "],
                    'U': ["A   A", "A   A", "A   A", "A   A", " AAA "],
                    'V': ["A   A", "A   A", "A   A", " A A ", "  A  "],
                    'W': ["A   A", "A   A", "A   A", "A A A", " A A "],
                    'X': ["A   A", " A A ", "  A  ", " A A ", "A   A"],
                    'Y': ["A   A", "A   A", " A A ", "  A  ", "  A  "],
                    'Z': ["AAAAA", "    A", "   A ", "  A  ", "AAAAA"],
                    ' ': ["     ", "     ", "     ", "     ", "     "],
                    '0': [" AAA ", "A   A", "A   A", "A   A", " AAA "],
                    '1': ["  A  ", " AA  ", "  A  ", "  A  ", "AAAAA"],
                    '2': [" AAA ", "A   A", "   A ", "  A  ", "AAAAA"],
                    '3': [" AAA ", "A   A", "  AAA", "A   A", " AAA "],
                    '4': ["A   A", "A   A", "AAAAA", "    A", "    A"],
                    '5': ["AAAAA", "A    ", "AAAA ", "    A", "AAAA "],
                    '6': [" AAA ", "A    ", "AAAA ", "A   A", " AAA "],
                    '7': ["AAAAA", "    A", "   A ", "  A  ", "  A  "],
                    '8': [" AAA ", "A   A", " AAA ", "A   A", " AAA "],
                    '9': [" AAA ", "A   A", " AAAA", "    A", " AAA "],
                },
                "fancy": {
                    'A': ["  /\  ", " /  \ ", "/____\\", "/    \\", "/    \\"],
                    'B': ["|~~~\\ ", "|    |", "|~~~/ ", "|    |", "|___/ "],
                    'C': [" /~~~\\", "/     ", "|     ", "\\     ", " \\___/"],
                    'D': ["|~~~\\ ", "|    |", "|    |", "|    |", "|___/ "],
                    'E': ["|~~~~~", "|     ", "|~~~~ ", "|     ", "|~~~~~"],
                    'F': ["|~~~~~", "|     ", "|~~~~ ", "|     ", "|     "],
                    'G': [" /~~~\\", "/     ", "|  ~~~", "\\    |", " \\___/"],
                    'H': ["|    |", "|    |", "|~~~~|", "|    |", "|    |"],
                    'I': ["~~~~~", "  |  ", "  |  ", "  |  ", "~~~~~"],
                    'J': ["~~~~~", "    |", "    |", "|   |", " \\__/"],
                    'K': ["|   /", "|  / ", "| /  ", "|  \\ ", "|   \\"],
                    'L': ["|     ", "|     ", "|     ", "|     ", "|~~~~~"],
                    'M': ["|\\  /|", "| \\/ |", "|    |", "|    |", "|    |"],
                    'N': ["|\\   |", "| \\  |", "|  \\ |", "|   \\|", "|    |"],
                    'O': [" /~~~\\", "/     \\", "|     |", "\\     /", " \\___/"],
                    'P': ["|~~~\\ ", "|    |", "|___/ ", "|     ", "|     "],
                    'Q': [" /~~~\\", "/     \\", "|     |", "\\  \\  /", " \\__\\/"],
                    'R': ["|~~~\\ ", "|    |", "|___/ ", "|  \\ ", "|   \\"],
                    'S': [" /~~~\\", "/     ", " \\___/", "     \\", "\\___/"],
                    'T': ["~~~~~", "  |  ", "  |  ", "  |  ", "  |  "],
                    'U': ["|    |", "|    |", "|    |", "|    |", " \\__/"],
                    'V': ["\\    /", " \\  / ", "  \\/  ", "  ||  ", "  ||  "],
                    'W': ["\\    /", "\\    /", "|    |", "|    |", " \\__/"],
                    'X': ["\\   /", " \\ / ", "  |  ", " / \\ ", "/   \\"],
                    'Y': ["\\   /", " \\ / ", "  |  ", "  |  ", "  |  "],
                    'Z': ["~~~~~", "   / ", "  /  ", " /   ", "~~~~~"],
                    ' ': ["     ", "     ", "     ", "     ", "     "],
                    '0': [" /~~~\\", "/  |  \\", "|   |  |", "\\  |  /", " \\___/"],
                    '1': ["  |  ", " /|  ", "  |  ", "  |  ", "~~~~~"],
                    '2': [" /~~~\\", "/     \\", "    / ", "  /   ", "~~~~~"],
                    '3': [" /~~~\\", "/     \\", "  ~~~ ", "\\     /", " \\___/"],
                    '4': ["|    |", "|    |", "~~~~~|", "    |", "    |"],
                    '5': ["~~~~~", "|     ", "~~~~~", "     |", "~~~~~"],
                    '6': [" /~~~\\", "/     ", "|~~~~~", "|     |", " \\___/"],
                    '7': ["~~~~~", "    /", "   / ", "  /  ", " /   "],
                    '8': [" /~~~\\", "/     \\", " \\___/", "/     \\", " \\___/"],
                    '9': [" /~~~\\", "/     \\", " \\~~~/", "     /", " \\___/"],
                },
                "stars": {
                    'A': [" * * ", "*   *", "*****", "*   *", "*   *"],
                    'B': ["**** ", "*   *", "**** ", "*   *", "**** "],
                    'C': [" ****", "*    ", "*    ", "*    ", " ****"],
                    'D': ["**** ", "*   *", "*   *", "*   *", "**** "],
                    'E': ["*****", "*    ", "**** ", "*    ", "*****"],
                    'F': ["*****", "*    ", "**** ", "*    ", "*    "],
                    'G': [" ****", "*    ", "* ***", "*   *", " ****"],
                    'H': ["*   *", "*   *", "*****", "*   *", "*   *"],
                    'I': ["*****", "  *  ", "  *  ", "  *  ", "*****"],
                    'J': ["*****", "    *", "    *", "*   *", " *** "],
                    'K': ["*   *", "*  * ", "***  ", "*  * ", "*   *"],
                    'L': ["*    ", "*    ", "*    ", "*    ", "*****"],
                    'M': ["*   *", "** **", "* * *", "*   *", "*   *"],
                    'N': ["*   *", "**  *", "* * *", "*  **", "*   *"],
                    'O': [" *** ", "*   *", "*   *", "*   *", " *** "],
                    'P': ["**** ", "*   *", "**** ", "*    ", "*    "],
                    'Q': [" *** ", "*   *", "*   *", "*  * ", " *** "],
                    'R': ["**** ", "*   *", "**** ", "*  * ", "*   *"],
                    'S': [" ****", "*    ", " *** ", "    *", "**** "],
                    'T': ["*****", "  *  ", "  *  ", "  *  ", "  *  "],
                    'U': ["*   *", "*   *", "*   *", "*   *", " *** "],
                    'V': ["*   *", "*   *", "*   *", " * * ", "  *  "],
                    'W': ["*   *", "*   *", "*   *", "* * *", " * * "],
                    'X': ["*   *", " * * ", "  *  ", " * * ", "*   *"],
                    'Y': ["*   *", "*   *", " * * ", "  *  ", "  *  "],
                    'Z': ["*****", "    *", "   * ", "  *  ", "*****"],
                    ' ': ["     ", "     ", "     ", "     ", "     "],
                    '0': [" *** ", "*   *", "*   *", "*   *", " *** "],
                    '1': ["  *  ", " **  ", "  *  ", "  *  ", "*****"],
                    '2': [" *** ", "*   *", "   * ", "  *  ", "*****"],
                    '3': [" *** ", "*   *", "  ***", "*   *", " *** "],
                    '4': ["*   *", "*   *", "*****", "    *", "    *"],
                    '5': ["*****", "*    ", "**** ", "    *", "**** "],
                    '6': [" *** ", "*    ", "**** ", "*   *", " *** "],
                    '7': ["*****", "    *", "   * ", "  *  ", "  *  "],
                    '8': [" *** ", "*   *", " *** ", "*   *", " *** "],
                    '9': [" *** ", "*   *", " ****", "    *", " *** "],
                }
            }
            
            # Get the pattern for the selected style
            pattern = patterns.get(style, patterns["block"])
            
            # Generate ASCII art
            height = 5  # Height of each character
            for row in range(height):
                line = ""
                for char in text:
                    if char in pattern:
                        line += pattern[char][row] + " "
                    else:
                        line += "     "  # Default space for unknown characters
                art += line + "\n"
            
            # Display the result
                output.delete(1.0, 'end')
                output.insert('end', art)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg=THEMES[self.theme]["bg"])
        button_frame.pack(pady=10)
        
        # Generate button
        generate_btn = tk.Button(button_frame, text="Generate ASCII Art", 
                               command=generate_ascii_art, 
                               font=("Segoe UI", 11, "bold"),
                               bg=THEMES[self.theme]["accent"], 
                               fg="white",
                               relief="flat", padx=20, pady=5)
        generate_btn.pack(side="left", padx=5)
        
        # Clear button
        clear_btn = tk.Button(button_frame, text="Clear", 
                            command=lambda: output.delete(1.0, 'end'), 
                            font=("Segoe UI", 11),
                            bg=THEMES[self.theme]["btnbg"], 
                            fg=THEMES[self.theme]["btnfg"],
                            relief="flat", padx=20, pady=5)
        clear_btn.pack(side="left", padx=5)
        
        # Close button
        close_btn = tk.Button(button_frame, text="Close", 
                            command=popup.destroy, 
                            font=("Segoe UI", 11),
                            bg=THEMES[self.theme]["error"], 
                            fg="white",
                            relief="flat", padx=20, pady=5)
        close_btn.pack(side="left", padx=5)
        
        # Bind Enter key to generate
        entry.bind('<Return>', lambda e: generate_ascii_art())
        
        # Center the popup
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (600 // 2)
        y = (popup.winfo_screenheight() // 2) - (500 // 2)
        popup.geometry(f"600x500+{x}+{y}")

    def load_hotwords(self):
        """Load hotwords from file."""
        try:
            with open(resource_path('hotwords.json'), 'r', encoding='utf-8') as f:
                hotwords = json.load(f)
                if isinstance(hotwords, list) and hotwords:
                    self.hotwords = hotwords
                else:
                    self.hotwords = ["hey sam", "hello sam", "sam"]
        except Exception:
            self.hotwords = ["hey sam", "hello sam", "sam"]

    def save_hotwords(self):
        try:
            with open(resource_path('hotwords.json'), 'w', encoding='utf-8') as f:
                json.dump(self.hotwords, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving hotwords: {e}")

    def send_gmail(self, to, subject, body):
        """
        Send email via Gmail with improved error handling and validation.
        
        Args:
            to (str): Recipient email address
            subject (str): Email subject
            body (str): Email body content
            
        Returns:
            str: Success message or detailed error message
        """
        try:
            # Validate Gmail credentials
            if not self.gmail_address or not self.gmail_app_password:
                return "❌ Gmail not configured. Please go to Settings → Gmail Settings and configure your Gmail credentials.\n\nTo set up Gmail:\n1. Enable 2-factor authentication on your Google account\n2. Generate an App Password (Google Account → Security → App Passwords)\n3. Use your Gmail address and the generated app password in settings."
            
            # Validate email format
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, to):
                return f"❌ Invalid email address format: {to}\nPlease provide a valid email address."
            
            if not re.match(email_pattern, self.gmail_address):
                return f"❌ Invalid Gmail address in settings: {self.gmail_address}\nPlease check your Gmail configuration in settings."
            
            # Validate input parameters
            if not subject or not subject.strip():
                subject = "Message from SAM"
            
            if not body or not body.strip():
                return "❌ Email body cannot be empty. Please provide a message to send."
            
            # Create email message
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.gmail_address
            msg['To'] = to
            
            # Send email with detailed error handling
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30) as server:
                    # Test connection
                    server.ehlo()
                    
                    # Login with detailed error handling
                    try:
                        server.login(self.gmail_address, self.gmail_app_password)
                    except smtplib.SMTPAuthenticationError:
                        return "❌ Gmail authentication failed. Please check:\n1. Your Gmail address is correct\n2. Your app password is correct\n3. 2-factor authentication is enabled\n4. App password was generated for 'Mail' or 'Other'\n\nGo to Settings → Gmail Settings to update your credentials."
                    except smtplib.SMTPException as e:
                        return f"❌ Gmail login error: {str(e)}\n\nPlease check your Gmail settings and try again."
                    
                    # Send email
                    try:
                        server.sendmail(self.gmail_address, [to], msg.as_string())
                        return f"✅ Email sent successfully!\n\n📧 To: {to}\n📝 Subject: {subject}\n📄 Message: {body[:100]}{'...' if len(body) > 100 else ''}"
                    except smtplib.SMTPRecipientsRefused:
                        return f"❌ Email delivery failed. The recipient address '{to}' was rejected by Gmail.\n\nPossible reasons:\n• Invalid email address\n• Recipient's email server is blocking the message\n• Email address doesn't exist"
                    except smtplib.SMTPException as e:
                        return f"❌ Email sending failed: {str(e)}\n\nPlease try again or check your internet connection."
                        
            except smtplib.SMTPConnectError:
                return "❌ Could not connect to Gmail servers.\n\nPlease check:\n1. Your internet connection\n2. Gmail servers are accessible\n3. No firewall is blocking the connection"
            except smtplib.SMTPException as e:
                return f"❌ SMTP error: {str(e)}\n\nPlease try again later."
            except Exception as e:
                return f"❌ Connection error: {str(e)}\n\nPlease check your internet connection and try again."
                
        except Exception as e:
            return f"❌ Unexpected error while sending email: {str(e)}\n\nPlease try again or contact support if the problem persists."

class ModernPopup(ctk.CTkToplevel):
    def __init__(self, parent, title, message, button_text="OK"):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x200")
        self.configure(fg_color="#22223b")
        self.resizable(False, False)
        ctk.CTkLabel(self, text=message, font=("Segoe UI", 12), text_color="#f2e9e4", wraplength=360, fg_color="#22223b").pack(pady=30, padx=20)
        ctk.CTkButton(self, text=button_text, command=self.destroy, fg_color="#4a4e69", text_color="#f2e9e4", corner_radius=8).pack(pady=10)
        self.grab_set()
        self.focus_force()

# --- Animated GIF helper class ---


# Add resource_path helper
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    full_path = os.path.join(base_path, relative_path)
    # Check if file exists
    if not os.path.exists(full_path):
        print(f"Warning: Resource file not found: {full_path}")
        return relative_path  # Return original path as fallback
    return full_path

class SystemNavigationService:
    def __init__(self):
        self.bundle_cache = {
            'safari': 'com.apple.Safari',
            'chrome': 'com.google.Chrome',
            'terminal': 'com.apple.Terminal',
            'finder': 'com.apple.finder',
            'notes': 'com.apple.Notes',
            'system settings': 'com.apple.systempreferences',
        }
        self.pane_map = {
            'display': 'x-apple.systempreferences:com.apple.preference.displays',
            'sound': 'x-apple.systempreferences:com.apple.preference.sound',
            'wifi': 'x-apple.systempreferences:com.apple.preference.network',
            'network': 'x-apple.systempreferences:com.apple.preference.network',
            'bluetooth': 'x-apple.systempreferences:com.apple.preference.bluetooth',
            'battery': 'x-apple.systempreferences:com.apple.preference.battery',
            'keyboard': 'x-apple.systempreferences:com.apple.preference.keyboard',
            'trackpad': 'x-apple.systempreferences:com.apple.preference.trackpad',
            'mouse': 'x-apple.systempreferences:com.apple.preference.mouse',
            'privacy': 'x-apple.systempreferences:com.apple.preference.security',
        }

    def open_settings(self, section=None):
        try:
            if section and section in self.pane_map:
                subprocess.run(['open', self.pane_map[section]], check=False)
            else:
                subprocess.run(['open', '-a', 'System Settings'], check=False)
            subprocess.run(['osascript', '-e', 'tell application "System Settings" to activate'], check=False)
            return f"⚙️ Opening System Settings{(' → ' + section) if section else ''}"
        except Exception as e:
            try:
                subprocess.Popen(['open', '/System/Applications/System Settings.app'])
                return "⚙️ Opening System Settings"
            except Exception:
                return f"❌ Failed to open System Settings: {e}"

    def open_app(self, app_name):
        try:
            key = app_name.strip().lower()
            bid = self.bundle_cache.get(key)
            if bid:
                subprocess.run(['open', '-b', bid], check=False)
            else:
                subprocess.run(['open', '-a', app_name], check=False)
            subprocess.run(['osascript', '-e', f'tell application "{app_name}" to activate'], check=False)
            return f"🚀 Opening {app_name}"
        except Exception as e:
            return f"❌ Failed to open {app_name}: {e}"

    def open_folder(self, name):
        try:
            n = name.strip()
            home = os.path.expanduser('~')
            known = {
                'downloads': os.path.join(home, 'Downloads'),
                'documents': os.path.join(home, 'Documents'),
                'desktop': os.path.join(home, 'Desktop'),
                'pictures': os.path.join(home, 'Pictures'),
                'music': os.path.join(home, 'Music'),
                'videos': os.path.join(home, 'Videos'),
            }
            path = known.get(n.lower())
            if not path:
                path = os.path.expanduser(n)
            if os.path.isdir(path):
                subprocess.run(['open', path], check=False)
                return f"📁 Opening '{os.path.basename(path)}'"
            return f"❌ Folder not found: {name}"
        except Exception as e:
            return f"❌ Failed to open folder '{name}': {e}"

 
class VoiceInputManager:
    def __init__(self, app):
        self.app = app
        self.recognizer = app.recognizer
        self.microphone = app.microphone
        self.language = getattr(app, 'sr_code', 'en-US')
        self.vad_available = False
        try:
            import webrtcvad  # optional
            self.vad = webrtcvad.Vad(2)
            self.vad_available = True
        except Exception:
            self.vad = None

    def listen_once(self, timeout=5, phrase_time_limit=8):
        if not self.microphone:
            return None, 'mic_unavailable'
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            try:
                # offline fallback via vosk if available
                text = None
                try:
                    import vosk  # optional
                    text = None  # placeholder: full integration can be added later
                except Exception:
                    pass
                if not text:
                    text = self.recognizer.recognize_google(audio, language=self.language)
                return text, None
            except sr.UnknownValueError:
                return None, 'no_speech'
            except sr.RequestError:
                return None, 'network_error'
        except Exception:
            return None, 'listen_error'

class HotwordEngine:
    def __init__(self, app):
        self.app = app
        self.enabled = False
        self.thread = None
        self.last_trigger = 0
        self.detector_available = False
        self.hotwords = getattr(app, 'hotwords', ["sam"])
        try:
            import openwakeword  # optional
            self.detector_available = True
        except Exception:
            self.detector_available = False

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        self.enabled = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.enabled = False

    def _loop(self):
        recognizer = self.app.recognizer
        mic = self.app.microphone
        missed = 0
        while self.enabled:
            try:
                with mic as source:
                    audio = recognizer.listen(source, timeout=4, phrase_time_limit=2)
                try:
                    text = recognizer.recognize_google(audio, language=self.app.sr_code)
                    if text and any(hw in text.lower() for hw in self.hotwords):
                        now = time.time()
                        if now - self.last_trigger > 1.0:
                            self.last_trigger = now
                            self.app.root.after(0, self.app.on_hotword_detected)
                            while self.app.is_listening and self.enabled:
                                time.sleep(0.2)
                        missed = 0
                    else:
                        missed += 1
                except Exception:
                    missed += 1
            except Exception:
                time.sleep(0.3)

class WindowManager:
    def focus(self, app_name):
        try:
            subprocess.run(['osascript', '-e', f'tell application "{app_name}" to activate'], check=False)
            return f"🔲 Focused {app_name}"
        except Exception as e:
            return f"❌ Focus failed: {e}"

    def maximize(self, app_name):
        try:
            script = (
                f'tell application "System Events" to tell process "{app_name}" '
                'to set value of attribute "AXFullScreen" of window 1 to true'
            )
            subprocess.run(['osascript', '-e', script], check=False)
            return f"🟦 Maximized {app_name}"
        except Exception as e:
            return f"❌ Maximize failed: {e}"

    def minimize(self, app_name):
        try:
            script = (
                f'tell application "System Events" to tell process "{app_name}" '
                'to set value of attribute "AXMinimized" of window 1 to true'
            )
            subprocess.run(['osascript', '-e', script], check=False)
            return f"🟨 Minimized {app_name}"
        except Exception as e:
            return f"❌ Minimize failed: {e}"

    def snap(self, app_name, side='left'):
        try:
            # Simple snap using half-screen size; can be refined with screen bounds
            bounds = subprocess.check_output(['osascript', '-e', 'tell application "Finder" to get bounds of window 1'], text=True).strip()
            # Fallback to default resolution halves
            x, y, w, h = 0, 0, 1440, 900
            if side == 'left':
                pos = '{0,0}'; size = '{720,900}'
            else:
                pos = '{720,0}'; size = '{720,900}'
            script = (
                f'tell application "System Events" to tell process "{app_name}" '
                f'to set position of window 1 to {pos}\n'
                f'tell application "System Events" to tell process "{app_name}" '
                f'to set size of window 1 to {size}'
            )
            subprocess.run(['osascript', '-e', script], check=False)
            return f"🧭 Snapped {app_name} {side}"
        except Exception as e:
            return f"❌ Snap failed: {e}"

if __name__ == "__main__":
    app = EnhancedJarvisGUI()
    app.root.mainloop()
