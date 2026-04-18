"""
Professional Streamlit Application for 6G Network Performance Analysis
Thales Group - Manufacturing Efficiency Dashboard
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from config import THALES_COLORS, CUSTOM_CSS
from data_preprocessing import DataProcessor
from kpi_calculator import KPICalculator
from visualizations import VisualizationEngine

# Configure page
st.set_page_config(
    page_title="6G Network Analytics | Thales Group",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize session state
@st.cache_resource
def load_data():
    """Load and preprocess data"""
    processor = DataProcessor('Thales_Group_Manufacturing.csv')
    processor.segment_network_quality()
    processor.calculate_network_stability_index()
    return processor.df

# Load data
df = load_data()

# Initialize KPI Calculator
@st.cache_resource
def calculate_kpis(dataframe):
    """Calculate all KPIs"""
    calculator = KPICalculator(dataframe)
    return calculator

kpi_calc = calculate_kpis(df)

# ============================================================================
# HEADER SECTION
# ============================================================================
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🏭 6G Network Performance Analytics</h1>
    <p class="header-subtitle">Impact on Manufacturing Efficiency in Smart Factories | Thales Group</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    
    # Time range filter - Convert pandas Timestamps to Python datetime
    min_date = df['DateTime'].min().to_pydatetime()
    max_date = df['DateTime'].max().to_pydatetime()
    
    date_range = st.slider(
        "Select Date Range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        format="MM/DD/YY"
    )
    
    # Network quality filter
    network_quality = st.multiselect(
        "Network Quality Filter:",
        options=['High', 'Medium', 'Low'],
        default=['High', 'Medium', 'Low']
    )
    
    # Efficiency class selector
    efficiency_class = st.multiselect(
        "Efficiency Status Filter:",
        options=['High', 'Medium', 'Low'],
        default=['High', 'Medium', 'Low']
    )
    
    # Operation mode filter
    operation_modes = st.multiselect(
        "Operation Mode Filter:",
        options=df['Operation_Mode'].unique(),
        default=df['Operation_Mode'].unique()
    )
    
    # Apply filters
    filtered_df = df[
        (df['DateTime'] >= date_range[0]) &
        (df['DateTime'] <= date_range[1]) &
        (df['Network_Quality'].isin(network_quality)) &
        (df['Efficiency_Status'].isin(efficiency_class)) &
        (df['Operation_Mode'].isin(operation_modes))
    ]

# ============================================================================
# MAIN CONTENT - TAB STRUCTURE
# ============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Network Performance",
    "⚡ Network vs Efficiency",
    "🔍 Quality & Error Analysis",
    "🎯 KPI Dashboard",
    "💡 6G Optimization Insights"
])

# ============================================================================
# TAB 1: NETWORK PERFORMANCE OVERVIEW
# ============================================================================
with tab1:
    st.markdown("### Network Performance Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("#### Latency Statistics")
        avg_latency = filtered_df['Network_Latency_ms'].mean()
        st.metric(
            label="Avg Latency",
            value=f"{avg_latency:.2f} ms",
            delta=f"{filtered_df['Network_Latency_ms'].std():.2f} ms (σ)"
        )
        st.caption(f"Range: {filtered_df['Network_Latency_ms'].min():.1f} - {filtered_df['Network_Latency_ms'].max():.1f} ms")
    
    with col2:
        st.markdown("#### Packet Loss Statistics")
        avg_packet_loss = filtered_df['Packet_Loss_%'].mean()
        st.metric(
            label="Avg Packet Loss",
            value=f"{avg_packet_loss:.3f} %",
            delta=f"{filtered_df['Packet_Loss_%'].std():.3f} % (σ)"
        )
        st.caption(f"Range: {filtered_df['Packet_Loss_%'].min():.2f} - {filtered_df['Packet_Loss_%'].max():.2f} %")
    
    with col3:
        st.markdown("#### Network Quality Distribution")
        quality_dist = filtered_df['Network_Quality'].value_counts()
        quality_high_pct = (quality_dist.get('High', 0) / len(filtered_df) * 100)
        st.metric(
            label="High Quality %",
            value=f"{quality_high_pct:.1f} %",
            delta="Network health indicator"
        )
    
    with col4:
        st.markdown("#### Network Stability Index")
        avg_nsi = filtered_df['Network_Stability_Index'].mean()
        st.metric(
            label="Avg NSI",
            value=f"{avg_nsi:.2f} / 100",
            delta="Higher is better" if avg_nsi > 70 else "Needs improvement"
        )
    
    # Network Performance Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.plotly_chart(
            VisualizationEngine.network_performance_timeline(filtered_df),
            use_container_width=True
        )
    
    with col_chart2:
        st.plotly_chart(
            VisualizationEngine.network_quality_distribution(filtered_df),
            use_container_width=True
        )
    
    # Network Statistics Table
    with st.expander("📋 Detailed Network Statistics"):
        network_stats = filtered_df[['Network_Latency_ms', 'Packet_Loss_%']].describe()
        st.dataframe(network_stats, use_container_width=True)

# ============================================================================
# TAB 2: NETWORK VS EFFICIENCY ANALYSIS
# ============================================================================
with tab2:
    st.markdown("### Network Impact on Manufacturing Efficiency")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        high_eff = (filtered_df['Efficiency_Status'] == 'High').sum() / len(filtered_df) * 100
        st.metric("High Efficiency %", f"{high_eff:.1f}%")
    
    with col2:
        med_eff = (filtered_df['Efficiency_Status'] == 'Medium').sum() / len(filtered_df) * 100
        st.metric("Medium Efficiency %", f"{med_eff:.1f}%")
    
    with col3:
        low_eff = (filtered_df['Efficiency_Status'] == 'Low').sum() / len(filtered_df) * 100
        st.metric("Low Efficiency %", f"{low_eff:.1f}%")
    
    # Efficiency Distribution by Network Quality
    st.plotly_chart(
        VisualizationEngine.efficiency_by_network_quality(filtered_df),
        use_container_width=True
    )
    
    # Latency-Efficiency Scatter
    st.plotly_chart(
        VisualizationEngine.latency_efficiency_scatter(filtered_df),
        use_container_width=True
    )
    
    # Efficiency Timeline
    st.plotly_chart(
        VisualizationEngine.efficiency_timeline(filtered_df),
        use_container_width=True
    )

# ============================================================================
# TAB 3: QUALITY & ERROR IMPACT ANALYSIS
# ============================================================================
with tab3:
    st.markdown("### Quality Control & Error Rate Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_defect = filtered_df['Quality_Control_Defect_Rate_%'].mean()
        st.metric(
            label="Avg Defect Rate",
            value=f"{avg_defect:.2f}%",
            delta="Quality KPI"
        )
    
    with col2:
        avg_error = filtered_df['Error_Rate_%'].mean()
        st.metric(
            label="Avg Error Rate",
            value=f"{avg_error:.2f}%",
            delta="Operational KPI"
        )
    
    with col3:
        avg_speed = filtered_df['Production_Speed_units_per_hr'].mean()
        st.metric(
            label="Avg Production Speed",
            value=f"{avg_speed:.0f}",
            delta="units/hr"
        )
    
    with col4:
        avg_maintenance = filtered_df['Predictive_Maintenance_Score'].mean()
        st.metric(
            label="Maintenance Score",
            value=f"{avg_maintenance:.3f}",
            delta="Machine health"
        )
    
    # Quality Analysis Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.plotly_chart(
            VisualizationEngine.packet_loss_vs_error_rate(filtered_df),
            use_container_width=True
        )
    
    with col_chart2:
        st.plotly_chart(
            VisualizationEngine.defect_rate_analysis(filtered_df),
            use_container_width=True
        )
    
    # Machine-level analysis
    with st.expander("🔧 Operation Mode Comparison"):
        st.plotly_chart(
            VisualizationEngine.operation_mode_comparison(filtered_df),
            use_container_width=True
        )

# ============================================================================
# TAB 4: KPI DASHBOARD
# ============================================================================
with tab4:
    st.markdown("### Key Performance Indicators (KPIs)")
    
    # KPI Summary metrics
    kpi_summary = kpi_calc.get_kpi_summary()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nsi_value = filtered_df['Network_Stability_Index'].mean()
        st.plotly_chart(
            VisualizationEngine.kpi_gauge_chart(
                nsi_value, 
                "Network Stability Index",
                threshold_good=50,
                threshold_optimal=75
            ),
            use_container_width=True
        )
    
    with col2:
        pqi_value = filtered_df['PQI'].mean()
        st.plotly_chart(
            VisualizationEngine.kpi_gauge_chart(
                pqi_value,
                "Production Quality Index"
            ),
            use_container_width=True
        )
    
    with col3:
        nrs_value = filtered_df['NRS'].mean()
        st.plotly_chart(
            VisualizationEngine.kpi_gauge_chart(
                nrs_value,
                "Network Resilience Score"
            ),
            use_container_width=True
        )
    
    # Detailed KPI Analysis
    st.markdown("### Detailed KPI Sensitivity Analysis")
    sensitivity_analysis = kpi_calc.get_efficiency_sensitivity_analysis()
    
    col1, col2, col3 = st.columns(3)
    
    for idx, (efficiency, metrics) in enumerate(sensitivity_analysis.items()):
        with st.columns(3)[idx]:
            with st.container():
                st.markdown(f"### {efficiency} Efficiency")
                st.metric("Records", f"{int(metrics['Record Count'])}")
                st.metric("Percentage", f"{metrics['Percentage']:.1f}%")
                st.metric("Avg Latency", f"{metrics['Avg Latency']:.1f} ms")
                st.metric("Avg Error Rate", f"{metrics['Avg Error Rate']:.2f}%")

# ============================================================================
# TAB 5: 6G OPTIMIZATION INSIGHTS
# ============================================================================
with tab5:
    st.markdown("### 6G Network Optimization Recommendations")
    
    recommendations = kpi_calc.get_recommendation_engine()
    
    if recommendations:
        for idx, rec in enumerate(recommendations, 1):
            priority_color = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }.get(rec['Priority'], '⚪')
            
            with st.container():
                st.markdown(f"### {priority_color} {rec['Category']} - {rec['Priority']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Finding:**")
                    st.info(rec['Finding'])
                
                with col2:
                    st.markdown("**Impact:**")
                    st.warning(rec['Impact'])
                
                st.markdown("**Recommendation:**")
                st.success(rec['Recommendation'])
                st.divider()
    
    # Latency Tolerance Benchmarks
    st.markdown("### Latency Tolerance Benchmarks")
    
    latency_correlation = kpi_calc.network_efficiency_correlation()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Critical Latency Threshold",
            value=f"{latency_correlation['critical_latency_ms']:.2f} ms",
            delta="Beyond this, efficiency drops significantly"
        )
    
    with col2:
        st.metric(
            label="Critical Packet Loss Threshold",
            value=f"{latency_correlation['critical_packet_loss_%']:.3f}%",
            delta="Maximum acceptable packet loss"
        )
    
    # Packet Loss Risk Zones
    st.markdown("### Packet Loss Risk Assessment")
    
    risk_zones = {
        'Safe Zone': (0, 1),
        'Warning Zone': (1, 3),
        'Risk Zone': (3, 5),
        'Critical Zone': (5, 10)
    }
    
    col1, col2, col3, col4 = st.columns(4)
    risk_colors = {
        'Safe Zone': 'green',
        'Warning Zone': 'yellow',
        'Risk Zone': 'orange',
        'Critical Zone': 'red'
    }
    
    for (zone, (min_val, max_val)), color in zip(risk_zones.items(), risk_colors.values()):
        count = len(filtered_df[(filtered_df['Packet_Loss_%'] >= min_val) & (filtered_df['Packet_Loss_%'] <= max_val)])
        pct = count / len(filtered_df) * 100
        
        with st.columns(4)[list(risk_zones.keys()).index(zone)]:
            st.metric(
                label=zone,
                value=f"{pct:.1f}%",
                delta=f"{count} records"
            )

# ============================================================================
# DATA EXPORT & DOWNLOAD
# ============================================================================
st.divider()

st.markdown("### 📥 Data Export")

col1, col2, col3 = st.columns(3)

with col1:
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data (CSV)",
        data=csv,
        file_name=f"6g_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

with col2:
    # Export summary report
    summary_text = f"""
    6G NETWORK PERFORMANCE ANALYSIS REPORT
    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    NETWORK STATISTICS:
    - Average Latency: {filtered_df['Network_Latency_ms'].mean():.2f} ms
    - Average Packet Loss: {filtered_df['Packet_Loss_%'].mean():.3f}%
    - Network Quality: {filtered_df['Network_Quality'].value_counts().to_dict()}
    
    EFFICIENCY METRICS:
    - High Efficiency Records: {(filtered_df['Efficiency_Status'] == 'High').sum()}
    - Medium Efficiency Records: {(filtered_df['Efficiency_Status'] == 'Medium').sum()}
    - Low Efficiency Records: {(filtered_df['Efficiency_Status'] == 'Low').sum()}
    
    PRODUCTION METRICS:
    - Average Production Speed: {filtered_df['Production_Speed_units_per_hr'].mean():.0f} units/hr
    - Average Defect Rate: {filtered_df['Quality_Control_Defect_Rate_%'].mean():.2f}%
    - Average Error Rate: {filtered_df['Error_Rate_%'].mean():.2f}%
    """
    
    st.download_button(
        label="Download Analysis Report",
        data=summary_text,
        file_name=f"6g_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
<div class="footer">
    <p>© 2025 Thales Group | 6G Network Performance Analytics Platform</p>
    <p>Advanced Manufacturing Intelligence for Industry 5.0</p>
</div>
""", unsafe_allow_html=True)
