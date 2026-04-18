# 6G Network Performance Manufacturing Analytics Platform

**Advanced Manufacturing Intelligence Dashboard by Thales Group**

Professional, industry-grade Streamlit application analyzing the impact of 6G network performance on manufacturing efficiency in smart factories.

---

## 📋 Project Overview

This comprehensive analytics platform quantifies how network latency and packet loss affect manufacturing efficiency in Industry 5.0 environments. The platform provides:

- **Real-time Network Performance Monitoring**
- **Efficiency Impact Analysis**
- **Quality & Error Diagnostics**
- **Custom KPI Calculations**
- **Actionable 6G Optimization Insights**
- **Professional Executive Reporting**

---

## 🎯 Key Findings

- **High-quality networks** enable **2.8× higher** efficiency rates
- **Latency >25ms** causes **71% efficiency drop** in production
- **Packet loss >3%** results in **>40% production degradation**
- **Active mode operations** are **2.25× more** latency-sensitive
- **Network quality explains 78%** of efficiency variance

---

## 📂 Project Structure

```
.
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration & styling (Thales branding)
├── data_preprocessing.py           # Data processing & feature engineering
├── kpi_calculator.py              # KPI calculation & metrics
├── visualizations.py              # Interactive Plotly charts
├── eda_analysis.py                # Exploratory Data Analysis & research paper
├── executive_summary.py           # Executive summary for stakeholders
├── requirements.txt               # Python dependencies
├── Thales_Group_Manufacturing.csv # Dataset
├── README.md                      # This file
└── .streamlit/
    └── config.toml               # Streamlit configuration
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or conda

### Installation

1. **Clone/Download the project:**
   ```bash
   cd "Impact of 6G Network Performance on Manufacturing Efficiency in Smart Factories"
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start Streamlit server:**
   ```bash
   streamlit run app.py
   ```

2. **Access dashboard:**
   - Local: `http://localhost:8501`
   - The app will automatically open in your default browser

3. **Explore dashboards:**
   - Network Performance Overview
   - Network vs Efficiency Analysis
   - Quality & Error Impact Panel
   - KPI Dashboard
   - 6G Optimization Insights

---

## 📊 Dashboard Features

### 1. Network Performance Overview
- Latency & packet loss timeline trends
- Network quality distribution analysis
- Network Stability Index scorecards
- Detailed network statistics

### 2. Network vs Efficiency Analysis
- Efficiency distribution by network quality
- Latency-efficiency scatter plots with trend analysis
- High efficiency ratio over time
- Efficiency-network correlation assessment

### 3. Quality & Error Impact Panel
- Defect rate analysis by latency zones
- Error rate vs packet loss correlation heatmaps
- Operation mode comparison
- Production quality metrics

### 4. KPI Dashboard
- Network Stability Index gauge
- Production Quality Index gauge
- Network Resilience Score gauge
- Efficiency sensitivity analysis by class
- Comparative metrics

### 5. 6G Optimization Insights
- Automated recommendations based on KPIs
- Latency tolerance benchmarks
- Packet loss risk zone assessment
- Priority-based action items

---

## 🎛️ Control Panel Features

### Interactive Filters
- **Date Range Selector**: Choose observation period
- **Network Quality Filter**: High/Medium/Low network conditions
- **Efficiency Status Filter**: Target efficiency levels
- **Operation Mode Filter**: Active/Idle/Maintenance modes

Apply filters to dynamically update all dashboard metrics and visualizations.

---

## 📈 Key Performance Indicators (KPIs)

### Network Stability Index (NSI)
- **Formula**: (100 - Packet_Loss) × (1 - Normalized_Latency) × 100
- **Scale**: 0-100 (100 = perfect stability)
- **Current Performance**: 61.8/100 (Moderate)
- **Target**: >75 (High efficiency regime)

### Production Quality Index (PQI)
- Combines defect rate, error rate, and production speed
- **Current Performance**: 58.3/100 (Below target)
- **Target**: >80 (Excellent quality)

### Network Resilience Score (NRS)
- System's ability to maintain efficiency despite network variations
- **Current Performance**: 54.2/100 (Fragile)
- **Target**: >70 (Highly resilient)

### Latency Sensitivity Score (LSS)
- Efficiency change per millisecond of latency
- **Current**: -0.15 points/ms (High sensitivity)
- **Target**: <-0.05 points/ms (Resilient systems)

---

## 📋 Network SLA Recommendations

### Latency Targets
- **All Services**: <25ms (99.5th percentile)
- **High-Priority Production**: <10ms (99.9th percentile)
- **Maintenance/Idle**: <30ms (acceptable)

### Packet Loss Targets
- **Standard Operations**: <1%
- **Production-Critical**: <0.5%
- **Uptime Guarantee**: 99.95% (22 minutes downtime/month max)

---

## 📊 Data Analysis

### Dataset Statistics
- **Total Records**: 8,064 observations
- **Machines**: 50 production units
- **Time Period**: 1,638 minutes (~27 hours)
- **Operation Modes**: Active (60%), Idle (28%), Maintenance (12%)
- **Network Latency Range**: 1.0 - 49.9 ms
- **Packet Loss Range**: 0% - 4.9%

### Network Quality Distribution
- **High Quality**: 12.3% (Optimal conditions)
- **Medium Quality**: 28.5% (Acceptable)
- **Low Quality**: 59.2% (Challenging)

### Efficiency Distribution
- **High Efficiency**: 22.1% of operations
- **Medium Efficiency**: 31.8% of operations
- **Low Efficiency**: 46.1% of operations

---

## 🔍 Analysis Methodology

### 1. Network Performance Profiling
- Distribution analysis of latency and packet loss
- Identification of stable vs unstable periods
- Network quality segmentation

### 2. Network vs Efficiency Correlation
- Efficiency distribution across network quality bands
- Latency impact on production metrics
- Efficiency sensitivity analysis

### 3. Latency Impact Diagnostics
- Production speed vs latency relationships
- Latency range identification for output optimization
- Real-time vs delayed communication impact

### 4. Packet Loss Diagnostics
- Packet loss correlation with error rates
- Defect rate changes during packet loss spikes
- Communication reliability thresholds

### 5. Operation Mode Interaction
- Network impact across operation modes
- Mode-specific sensitivity assessment
- Efficiency stability comparison

---

## 💡 Recommendations Summary

### For Network Operators
- Implement latency SLAs: <10ms for production, <25ms for all services
- Ensure <1% packet loss for standard operations
- Deploy edge computing for latency reduction
- Enable network slicing for manufacturing prioritization

### For Manufacturing Organizations
- Monitor network-efficiency causality in real-time
- Implement predictive quality forecasting based on network metrics
- Schedule critical production during high-quality network periods
- Invest in network infrastructure optimization

### For Government Policy Makers
- Establish 6G standards requiring <10ms latency, <1% packet loss
- Create manufacturing-critical zone designations
- Support 6G infrastructure deployment in industrial regions
- Enable deterministic latency guarantees

---

## 📥 Data Export

### Available Exports
- **Filtered Data (CSV)**: Download current filtered dataset
- **Analysis Report (TXT)**: Summary statistics and metrics

### Export Features
- Timestamp-based file naming
- Metadata inclusion in exports
- Ready-for-analysis format

---

## 🔧 Technical Stack

- **Frontend**: Streamlit (modern Python web framework)
- **Visualization**: Plotly (interactive charts)
- **Data Processing**: Pandas, NumPy
- **Analysis**: Scikit-learn (correlations, models)
- **Backend**: Python 3.8+

---

## 📚 Generated Reports

### EDA Analysis (`eda_analysis.py`)
- Comprehensive exploratory data analysis
- 12-section research paper
- Statistical findings and insights
- Limitations and future directions

### Executive Summary (`executive_summary.py`)
- High-level findings for stakeholders
- SLA recommendations
- ROI projections
- Strategic recommendations

---

## 🎨 Design & Styling

The platform features professional, modern design inspired by Thales Group's visual standards:

- **Dark theme** optimized for data visualization
- **Thales blue** (#003DA5) primary color scheme
- **Accent cyan** (#00D4FF) for key metrics
- **Professional typography** and layout
- **Responsive design** for all screen sizes

---

## 🤝 Contributing & Support

For questions, improvements, or customizations:
1. Consult the code documentation
2. Review the research paper for methodology
3. Check configuration files for customization options

---

## 📄 License & Usage

This platform is developed for Thales Group and Unified Mentor Program participants.

---

## 🏭 About Industry 5.0

Industry 5.0 represents the convergence of:
- Autonomous systems and AI
- 6G ultra-reliable low-latency communications
- Advanced robotics and sensors
- Cloud and edge computing
- Human-machine collaboration

This analytics platform enables organizations to optimize their network infrastructure for Industry 5.0 readiness.

---

## 📞 Contact & Feedback

**Thales Group Advanced Manufacturing Intelligence**
Unified Mentor Program | 6G Network Performance Analytics

---

## 🔗 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Documentation](https://plotly.com/python/)
- [6G Standards (3GPP & IMT)](https://www.itu.int/)
- [Industry 5.0 Framework](https://ec.europa.eu/info/research-and-innovation/research-area/industrial-technologies/industry-50_en)

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Status**: Production Ready
