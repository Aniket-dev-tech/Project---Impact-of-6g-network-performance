"""
KPI (Key Performance Indicator) Calculation Module
Calculates specialized KPIs for 6G network performance impact analysis
"""
import pandas as pd
import numpy as np

class KPICalculator:
    def __init__(self, dataframe):
        self.df = dataframe  # Remove .copy() to modify original dataframe
        self.calculate_all_kpis()
    
    def calculate_all_kpis(self):
        """Calculate all KPIs"""
        self.network_stability_index()
        self.latency_sensitivity_score()
        self.packet_loss_impact_ratio()
        self.network_efficiency_correlation()
        self.production_quality_index()
        self.network_resilience_score()
    
    def network_stability_index(self):
        """
        Network Stability Index (NSI)
        Combines latency and packet loss into single stability metric
        Scale: 0-100 (100 = perfect stability)
        """
        # Normalize metrics to 0-1 range
        latency_normalized = np.clip(self.df['Network_Latency_ms'] / 100, 0, 1)
        packet_loss_normalized = np.clip(self.df['Packet_Loss_%'] / 10, 0, 1)
        
        # NSI = (1 - latency_factor) * (1 - packet_loss_factor) * 100
        self.df['NSI'] = (
            (1 - latency_normalized * 0.6) * 
            (1 - packet_loss_normalized * 0.4) * 
            100
        ).clip(0, 100)
        
        return self.df['NSI']
    
    def latency_sensitivity_score(self):
        """
        Latency Sensitivity Score (LSS)
        Measures how much efficiency changes per ms of latency increase
        Scale: -10 to 0 (more negative = more sensitive)
        """
        # Create latency bands
        latency_bands = pd.cut(
            self.df['Network_Latency_ms'],
            bins=[0, 10, 25, 50, 100],
            labels=['ultra_low', 'optimal', 'degraded', 'critical']
        )
        
        # Calculate efficiency score for each band
        efficiency_mapping = {'High': 100, 'Medium': 50, 'Low': 0}
        self.df['Efficiency_Score'] = self.df['Efficiency_Status'].map(efficiency_mapping)
        
        # Group by latency band and calculate average efficiency drop
        lss_values = []
        for idx, row in self.df.iterrows():
            latency = row['Network_Latency_ms']
            efficiency = row['Efficiency_Score']
            
            # Sensitivity: change in efficiency per latency unit
            if latency > 0:
                sensitivity = (efficiency - 100) / latency
            else:
                sensitivity = 0
            
            lss_values.append(sensitivity)
        
        self.df['LSS'] = np.array(lss_values).clip(-10, 0)
        
        return self.df['LSS']
    
    def packet_loss_impact_ratio(self):
        """
        Packet Loss Impact Ratio (PLIR)
        Measures production degradation caused by packet loss
        Scale: 0-1 (0 = no impact, 1 = complete degradation)
        """
        # Baseline production speed at zero packet loss
        baseline_speed = self.df[self.df['Packet_Loss_%'] < 0.5]['Production_Speed_units_per_hr'].mean()
        
        # Production degradation due to packet loss
        production_degradation = (
            (baseline_speed - self.df['Production_Speed_units_per_hr']) / baseline_speed
        ).clip(0, 1)
        
        # Error rate increase factor
        error_increase_factor = np.clip(self.df['Error_Rate_%'] / 10, 0, 1)
        
        # PLIR combines both factors
        self.df['PLIR'] = (production_degradation * 0.6 + error_increase_factor * 0.4).clip(0, 1)
        
        return self.df['PLIR']
    
    def network_efficiency_correlation(self):
        """
        Network-Efficiency Correlation (NEC)
        Identifies the network threshold where efficiency drops significantly
        Returns correlation coefficient and recommendation
        """
        # Calculate correlation between network metrics and efficiency score
        self.df['Efficiency_Numeric'] = self.df['Efficiency_Status'].map({'High': 3, 'Medium': 2, 'Low': 1})
        
        latency_corr = self.df['Network_Latency_ms'].corr(self.df['Efficiency_Numeric'])
        packet_loss_corr = self.df['Packet_Loss_%'].corr(self.df['Efficiency_Numeric'])
        
        # Find critical threshold (where efficiency becomes Medium or Low)
        high_efficiency = self.df[self.df['Efficiency_Status'] == 'High']
        
        if len(high_efficiency) > 0:
            critical_latency = high_efficiency['Network_Latency_ms'].quantile(0.95)
            critical_packet_loss = high_efficiency['Packet_Loss_%'].quantile(0.95)
        else:
            critical_latency = self.df['Network_Latency_ms'].median()
            critical_packet_loss = self.df['Packet_Loss_%'].median()
        
        self.df['NEC'] = abs(latency_corr) + abs(packet_loss_corr)
        
        return {
            'correlation_strength': self.df['NEC'].values[0],
            'critical_latency_ms': critical_latency,
            'critical_packet_loss_%': critical_packet_loss,
            'latency_correlation': latency_corr,
            'packet_loss_correlation': packet_loss_corr
        }
    
    def production_quality_index(self):
        """
        Production Quality Index (PQI)
        Measures overall production quality considering defects, errors, and speed
        Scale: 0-100 (100 = perfect quality)
        """
        # Normalize metrics
        defect_rate_norm = np.clip(self.df['Quality_Control_Defect_Rate_%'] / 10, 0, 1)
        error_rate_norm = np.clip(self.df['Error_Rate_%'] / 15, 0, 1)
        
        # Production speed relative to maximum observed
        max_speed = self.df['Production_Speed_units_per_hr'].max()
        speed_norm = self.df['Production_Speed_units_per_hr'] / max_speed
        
        # PQI combines all factors
        self.df['PQI'] = (
            (1 - defect_rate_norm * 0.4) * 
            (1 - error_rate_norm * 0.3) * 
            (speed_norm * 0.3 + 0.7) * 
            100
        ).clip(0, 100)
        
        return self.df['PQI']
    
    def network_resilience_score(self):
        """
        Network Resilience Score (NRS)
        Measures system's ability to maintain efficiency despite network variations
        Scale: 0-100 (100 = highly resilient)
        """
        # Calculate stability of efficiency during network variations
        # Group by consecutive time windows and measure consistency
        window_size = 60  # 60 minute windows
        self.df['Hour'] = self.df['DateTime'].dt.hour if hasattr(self.df['DateTime'].dtype, 'dt') else pd.to_datetime(self.df['DateTime']).dt.hour
        
        resilience_scores = []
        for idx, row in self.df.iterrows():
            # Look at nearby records to assess resilience
            window = self.df.iloc[max(0, idx-window_size):min(len(self.df), idx+window_size)]
            
            # Consistency of high efficiency despite network variations
            high_efficiency_ratio = (window['Efficiency_Status'] == 'High').sum() / len(window) * 100
            network_variation = window['Network_Latency_ms'].std()
            
            # Resilience = maintaining efficiency despite network variations
            if network_variation > 0:
                resilience = high_efficiency_ratio / (1 + network_variation / 10)
            else:
                resilience = high_efficiency_ratio
            
            resilience_scores.append(np.clip(resilience, 0, 100))
        
        self.df['NRS'] = resilience_scores
        
        return self.df['NRS']
    
    def get_kpi_summary(self):
        """Get summary statistics for all KPIs"""
        kpi_summary = {
            'Network Stability Index': {
                'Mean': self.df['NSI'].mean(),
                'Std': self.df['NSI'].std(),
                'Min': self.df['NSI'].min(),
                'Max': self.df['NSI'].max(),
                'Status': 'Excellent' if self.df['NSI'].mean() > 80 else 'Good' if self.df['NSI'].mean() > 60 else 'Fair'
            },
            'Latency Sensitivity Score': {
                'Mean': self.df['LSS'].mean(),
                'Std': self.df['LSS'].std(),
                'Min': self.df['LSS'].min(),
                'Max': self.df['LSS'].max(),
                'Interpretation': 'High sensitivity to latency' if abs(self.df['LSS'].mean()) > 2 else 'Moderate sensitivity'
            },
            'Packet Loss Impact Ratio': {
                'Mean': self.df['PLIR'].mean(),
                'Std': self.df['PLIR'].std(),
                'Min': self.df['PLIR'].min(),
                'Max': self.df['PLIR'].max(),
                'Status': 'Low impact' if self.df['PLIR'].mean() < 0.3 else 'Moderate impact' if self.df['PLIR'].mean() < 0.6 else 'High impact'
            },
            'Production Quality Index': {
                'Mean': self.df['PQI'].mean(),
                'Std': self.df['PQI'].std(),
                'Min': self.df['PQI'].min(),
                'Max': self.df['PQI'].max(),
                'Status': 'Excellent' if self.df['PQI'].mean() > 80 else 'Good' if self.df['PQI'].mean() > 60 else 'Fair'
            },
            'Network Resilience Score': {
                'Mean': self.df['NRS'].mean(),
                'Std': self.df['NRS'].std(),
                'Min': self.df['NRS'].min(),
                'Max': self.df['NRS'].max(),
                'Status': 'Highly Resilient' if self.df['NRS'].mean() > 70 else 'Resilient' if self.df['NRS'].mean() > 50 else 'Fragile'
            }
        }
        
        return kpi_summary
    
    def get_efficiency_sensitivity_analysis(self):
        """Detailed sensitivity analysis showing efficiency change per network metric unit"""
        # Segment data by efficiency status
        analysis = {}
        
        for efficiency in ['High', 'Medium', 'Low']:
            subset = self.df[self.df['Efficiency_Status'] == efficiency]
            if len(subset) > 0:
                analysis[efficiency] = {
                    'Avg Latency': subset['Network_Latency_ms'].mean(),
                    'Avg Packet Loss': subset['Packet_Loss_%'].mean(),
                    'Avg Error Rate': subset['Error_Rate_%'].mean(),
                    'Avg Defect Rate': subset['Quality_Control_Defect_Rate_%'].mean(),
                    'Avg Production Speed': subset['Production_Speed_units_per_hr'].mean(),
                    'Record Count': len(subset),
                    'Percentage': len(subset) / len(self.df) * 100
                }
        
        return analysis
    
    def get_recommendation_engine(self):
        """Generate automated recommendations based on KPIs"""
        recommendations = []
        
        # Latency recommendations
        if self.df['Network_Latency_ms'].mean() > 40:
            recommendations.append({
                'Category': 'Network Latency',
                'Priority': 'HIGH',
                'Finding': f"Average latency is {self.df['Network_Latency_ms'].mean():.2f}ms",
                'Recommendation': 'Implement network optimization protocols; Consider edge computing deployment',
                'Impact': 'System sensitive to latency increases'
            })
        
        # Packet loss recommendations
        if self.df['Packet_Loss_%'].mean() > 2:
            recommendations.append({
                'Category': 'Packet Loss',
                'Priority': 'CRITICAL',
                'Finding': f"Average packet loss is {self.df['Packet_Loss_%'].mean():.2f}%",
                'Recommendation': 'Upgrade network infrastructure; Implement error correction protocols',
                'Impact': f"Production speed degraded by {(self.df['PLIR'].mean() * 100):.1f}%"
            })
        
        # Efficiency recommendations
        high_eff_ratio = (self.df['Efficiency_Status'] == 'High').sum() / len(self.df) * 100
        if high_eff_ratio < 30:
            recommendations.append({
                'Category': 'Production Efficiency',
                'Priority': 'HIGH',
                'Finding': f"Only {high_eff_ratio:.1f}% of operations achieve high efficiency",
                'Recommendation': 'Review network-machine integration; Conduct latency tolerance testing',
                'Impact': 'Significant efficiency improvement potential'
            })
        
        return recommendations
