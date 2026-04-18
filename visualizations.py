"""
Professional visualization module for 6G Manufacturing Analytics
Uses Plotly for interactive, publication-quality charts
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from config import THALES_COLORS

class VisualizationEngine:
    @staticmethod
    def create_template():
        """Create consistent Thales-branded template for all charts"""
        return go.layout.Template(
            layout=go.Layout(
                font=dict(family="Arial, sans-serif", size=11, color=THALES_COLORS["white"]),
                paper_bgcolor=THALES_COLORS["primary_dark"],
                plot_bgcolor="#1A1F2E",
                hovermode="x unified",
                margin=dict(l=60, r=60, t=80, b=60),
                title_font_size=18,
                title_font_color=THALES_COLORS["accent_cyan"],
            )
        )
    
    @staticmethod
    def network_performance_timeline(df):
        """Create latency and packet loss timeline chart"""
        fig = go.Figure()
        
        # Latency trace
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['Network_Latency_ms'],
            name='Network Latency (ms)',
            line=dict(color=THALES_COLORS["accent_cyan"], width=2),
            yaxis='y1'
        ))
        
        # Packet loss trace (secondary axis)
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['Packet_Loss_%'],
            name='Packet Loss (%)',
            line=dict(color=THALES_COLORS["warning_orange"], width=2, dash='dash'),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Network Performance Timeline: Latency & Packet Loss Trends',
            xaxis_title='Date & Time',
            yaxis=dict(
                title='Latency (ms)',
                titlefont=dict(color=THALES_COLORS["accent_cyan"]),
                tickfont=dict(color=THALES_COLORS["accent_cyan"]),
            ),
            yaxis2=dict(
                title='Packet Loss (%)',
                titlefont=dict(color=THALES_COLORS["warning_orange"]),
                tickfont=dict(color=THALES_COLORS["warning_orange"]),
                overlaying='y',
                side='right'
            ),
            template=VisualizationEngine.create_template(),
            height=500,
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def network_quality_distribution(df):
        """Create network quality segmentation pie chart"""
        quality_counts = df['Network_Quality'].value_counts()
        colors_map = {
            'High': THALES_COLORS["success_green"],
            'Medium': THALES_COLORS["warning_orange"],
            'Low': THALES_COLORS["danger_red"]
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=quality_counts.index,
            values=quality_counts.values,
            marker=dict(colors=[colors_map.get(x, THALES_COLORS["neutral_gray"]) for x in quality_counts.index]),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>"
        )])
        
        fig.update_layout(
            title='Network Quality Distribution',
            template=VisualizationEngine.create_template(),
            height=400,
            font=dict(size=12)
        )
        
        return fig
    
    @staticmethod
    def efficiency_by_network_quality(df):
        """Create efficiency distribution by network quality"""
        # Create efficiency distribution by network quality
        efficiency_by_quality = pd.crosstab(
            df['Network_Quality'], 
            df['Efficiency_Status'], 
            normalize='index'
        ) * 100
        
        fig = go.Figure()
        
        for efficiency in ['High', 'Medium', 'Low']:
            colors_map = {
                'High': THALES_COLORS["success_green"],
                'Medium': THALES_COLORS["warning_orange"],
                'Low': THALES_COLORS["danger_red"]
            }
            fig.add_trace(go.Bar(
                x=efficiency_by_quality.index,
                y=efficiency_by_quality.get(efficiency, [0, 0, 0]),
                name=f'{efficiency} Efficiency',
                marker=dict(color=colors_map[efficiency]),
                hovertemplate="<b>%{x}</b><br>" + f"{efficiency} Efficiency: " + "%{y:.1f}%<extra></extra>"
            ))
        
        fig.update_layout(
            title='Efficiency Status Distribution by Network Quality',
            xaxis_title='Network Quality',
            yaxis_title='Percentage (%)',
            template=VisualizationEngine.create_template(),
            height=450,
            barmode='stack',
            hovermode='x'
        )
        
        return fig
    
    @staticmethod
    def latency_efficiency_scatter(df):
        """Create latency vs efficiency scatter plot with trend"""
        fig = go.Figure()
        
        efficiency_colors = {
            'High': THALES_COLORS["success_green"],
            'Medium': THALES_COLORS["warning_orange"],
            'Low': THALES_COLORS["danger_red"]
        }
        
        for efficiency in ['High', 'Medium', 'Low']:
            subset = df[df['Efficiency_Status'] == efficiency]
            fig.add_trace(go.Scatter(
                x=subset['Network_Latency_ms'],
                y=subset['Production_Speed_units_per_hr'],
                mode='markers',
                name=f'{efficiency} Efficiency',
                marker=dict(
                    color=efficiency_colors[efficiency],
                    size=6,
                    opacity=0.7
                ),
                hovertemplate="<b>Latency:</b> %{x:.2f}ms<br>" +
                             "<b>Production Speed:</b> %{y:.0f} units/hr<br>" +
                             "<extra></extra>"
            ))
        
        # Add trend line
        z = np.polyfit(df['Network_Latency_ms'], df['Production_Speed_units_per_hr'], 2)
        p = np.poly1d(z)
        x_trend = np.linspace(df['Network_Latency_ms'].min(), df['Network_Latency_ms'].max(), 100)
        
        fig.add_trace(go.Scatter(
            x=x_trend,
            y=p(x_trend),
            mode='lines',
            name='Trend',
            line=dict(color=THALES_COLORS["accent_cyan"], width=2, dash='dash')
        ))
        
        fig.update_layout(
            title='Latency Impact on Production Speed',
            xaxis_title='Network Latency (ms)',
            yaxis_title='Production Speed (units/hr)',
            template=VisualizationEngine.create_template(),
            height=500,
        )
        
        return fig
    
    @staticmethod
    def packet_loss_vs_error_rate(df):
        """Create packet loss vs error rate heatmap"""
        # Create bins for packet loss and error rate
        packet_loss_bins = pd.cut(df['Packet_Loss_%'], bins=10)
        error_rate_bins = pd.cut(df['Error_Rate_%'], bins=10)
        
        # Create heatmap data
        heatmap_data = pd.crosstab(packet_loss_bins, error_rate_bins, normalize='all') * 100
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=[str(x) for x in heatmap_data.columns],
            y=[str(x) for x in heatmap_data.index],
            colorscale=[
                [0, THALES_COLORS["primary_dark"]],
                [0.5, THALES_COLORS["warning_orange"]],
                [1, THALES_COLORS["danger_red"]]
            ],
            hovertemplate="<b>Packet Loss Range:</b> %{y}<br>" +
                         "<b>Error Rate Range:</b> %{x}<br>" +
                         "<b>Frequency:</b> %{z:.2f}%<extra></extra>"
        ))
        
        fig.update_layout(
            title='Correlation: Packet Loss vs Error Rate',
            xaxis_title='Error Rate Bin',
            yaxis_title='Packet Loss Bin',
            template=VisualizationEngine.create_template(),
            height=500,
        )
        
        return fig
    
    @staticmethod
    def kpi_gauge_chart(value, title, min_val=0, max_val=100, threshold_good=60, threshold_optimal=80):
        """Create modern KPI gauge chart"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            title={'text': title},
            delta={'reference': threshold_good},
            gauge={
                'axis': {'range': [min_val, max_val]},
                'bar': {'color': THALES_COLORS["accent_cyan"]},
                'steps': [
                    {'range': [min_val, threshold_good], 'color': THALES_COLORS["danger_red"]},
                    {'range': [threshold_good, threshold_optimal], 'color': THALES_COLORS["warning_orange"]},
                    {'range': [threshold_optimal, max_val], 'color': THALES_COLORS["success_green"]}
                ],
                'threshold': {
                    'line': {'color': 'white', 'width': 2},
                    'thickness': 0.75,
                    'value': threshold_good
                }
            }
        ))
        
        fig.update_layout(
            template=VisualizationEngine.create_template(),
            height=400,
        )
        
        return fig
    
    @staticmethod
    def operation_mode_comparison(df):
        """Create comparison of network impact across operation modes"""
        operation_analysis = df.groupby('Operation_Mode').agg({
            'Network_Latency_ms': 'mean',
            'Packet_Loss_%': 'mean',
            'Error_Rate_%': 'mean',
            'Production_Speed_units_per_hr': 'mean'
        }).reset_index()
        
        fig = go.Figure()
        
        metrics = ['Network_Latency_ms', 'Packet_Loss_%', 'Error_Rate_%']
        colors = [THALES_COLORS["accent_cyan"], THALES_COLORS["warning_orange"], THALES_COLORS["danger_red"]]
        
        for metric, color in zip(metrics, colors):
            fig.add_trace(go.Bar(
                x=operation_analysis['Operation_Mode'],
                y=operation_analysis[metric],
                name=metric.replace('_', ' '),
                marker=dict(color=color),
                hovertemplate="<b>%{x}</b><br>" + "%{y:.2f}<extra></extra>"
            ))
        
        fig.update_layout(
            title='Network Impact Analysis by Operation Mode',
            xaxis_title='Operation Mode',
            yaxis_title='Metric Value',
            template=VisualizationEngine.create_template(),
            height=450,
            barmode='group'
        )
        
        return fig
    
    @staticmethod
    def efficiency_timeline(df):
        """Create efficiency status timeline"""
        efficiency_count = df.groupby(pd.Grouper(key='DateTime', freq='1H'))['Efficiency_Status'].apply(
            lambda x: (x == 'High').sum() / len(x) * 100
        )
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=efficiency_count.index,
            y=efficiency_count.values,
            fill='tozeroy',
            name='High Efficiency %',
            line=dict(color=THALES_COLORS["success_green"], width=2),
            fillcolor='rgba(34, 197, 94, 0.2)'
        ))
        
        # Add threshold line
        fig.add_hline(
            y=70, 
            line_dash="dash", 
            line_color=THALES_COLORS["warning_orange"],
            annotation_text="Target Threshold (70%)",
            annotation_position="right"
        )
        
        fig.update_layout(
            title='High Efficiency Ratio Over Time',
            xaxis_title='Date & Time',
            yaxis_title='High Efficiency Percentage (%)',
            template=VisualizationEngine.create_template(),
            height=450,
        )
        
        return fig
    
    @staticmethod
    def defect_rate_analysis(df):
        """Create defect rate vs network conditions analysis"""
        # Create latency bands
        df_copy = df.copy()
        df_copy['Latency_Band'] = pd.cut(
            df_copy['Network_Latency_ms'],
            bins=[0, 10, 25, 50, 100],
            labels=['Ultra-Low (0-10ms)', 'Optimal (10-25ms)', 'Degraded (25-50ms)', 'Critical (50-100ms)']
        )
        
        defect_analysis = df_copy.groupby('Latency_Band').agg({
            'Quality_Control_Defect_Rate_%': 'mean',
            'Error_Rate_%': 'mean',
            'Network_Latency_ms': 'count'
        }).reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=defect_analysis['Latency_Band'],
            y=defect_analysis['Quality_Control_Defect_Rate_%'],
            name='Defect Rate (%)',
            marker=dict(color=THALES_COLORS["danger_red"]),
            hovertemplate="<b>%{x}</b><br>Defect Rate: %{y:.2f}%<extra></extra>"
        ))
        
        fig.update_layout(
            title='Quality Control Defect Rate by Network Latency Zone',
            xaxis_title='Network Latency Zone',
            yaxis_title='Defect Rate (%)',
            template=VisualizationEngine.create_template(),
            height=450,
        )
        
        return fig
