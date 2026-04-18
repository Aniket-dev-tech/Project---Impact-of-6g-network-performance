# Professional styling configuration for Thales Group 6G Analytics
# Inspired by Thales Group's modern, professional design language

THALES_COLORS = {
    "primary_dark": "#0F1419",      # Dark blue/black (Thales brand)
    "primary_blue": "#003DA5",       # Deep Thales blue
    "secondary_blue": "#0056D2",     # Lighter blue
    "accent_cyan": "#00D4FF",        # Cyan accent
    "success_green": "#22C55E",      # Success/positive
    "warning_orange": "#F97316",     # Warning
    "danger_red": "#EF4444",         # Danger/negative
    "neutral_gray": "#6B7280",       # Neutral gray
    "light_gray": "#F3F4F6",         # Light background
    "white": "#FFFFFF",
}

CUSTOM_CSS = """
<style>
    /* Main app styling */
    .main {
        background-color: #0F1419;
        color: #FFFFFF;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #003DA5 0%, #0056D2 100%);
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .header-title {
        font-size: 42px;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0;
        margin-bottom: 10px;
    }
    
    .header-subtitle {
        font-size: 16px;
        color: #E0E7FF;
        margin: 0;
        font-weight: 300;
    }
    
    /* Card styling */
    .metric-card {
        background-color: #1A1F2E;
        border: 1px solid #003DA5;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #00D4FF;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 14px;
        color: #A0AEC0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* KPI Grid */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    /* Section headers */
    .section-header {
        font-size: 24px;
        font-weight: 700;
        color: #00D4FF;
        margin: 40px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #003DA5;
    }
    
    /* Tab styling */
    .tab-content {
        background-color: #1A1F2E;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* Charts container */
    .chart-container {
        background-color: #1A1F2E;
        border: 1px solid #003DA5;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
    }
    
    /* Filter panel */
    .filter-panel {
        background-color: #1A1F2E;
        border: 1px solid #003DA5;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
    }
    
    /* Status badges */
    .status-high {
        background-color: rgba(34, 197, 94, 0.2);
        color: #22C55E;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    
    .status-medium {
        background-color: rgba(249, 115, 22, 0.2);
        color: #F97316;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    
    .status-low {
        background-color: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #003DA5;
        color: #6B7280;
        font-size: 12px;
    }
    
    /* Streamlit input styling */
    .stSelectbox, .stSlider, .stDateInput, .stMultiSelect {
        background-color: #1A1F2E;
        border: 1px solid #003DA5;
        border-radius: 6px;
        color: #FFFFFF;
    }
</style>
"""

# Network quality segmentation thresholds
NETWORK_QUALITY_THRESHOLDS = {
    "high": {"latency_max": 10, "packet_loss_max": 1},
    "medium": {"latency_max": 30, "packet_loss_max": 3},
    "low": {"latency_max": 100, "packet_loss_max": 10}
}

# Efficiency sensitivity zones
LATENCY_SENSITIVITY_ZONES = {
    "critical": (0, 10),      # Ultra-low latency zone
    "optimal": (10, 25),      # Optimal operating zone
    "degraded": (25, 50),     # Performance degradation zone
    "critical_impact": (50, 100)  # Critical impact zone
}

# KPI Benchmarks
KPI_BENCHMARKS = {
    "excellent_efficiency": 0.8,
    "good_efficiency": 0.6,
    "acceptable_efficiency": 0.4,
    "critical_defect_rate": 0.05,
    "warning_defect_rate": 0.03,
    "acceptable_defect_rate": 0.01
}
