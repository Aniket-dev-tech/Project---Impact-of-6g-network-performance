"""
Data preprocessing and cleaning module for 6G Manufacturing Analytics
"""
import pandas as pd
import numpy as np
from config import NETWORK_QUALITY_THRESHOLDS

class DataProcessor:
    def __init__(self, csv_path):
        """Initialize data processor with CSV file path"""
        self.df = pd.read_csv(csv_path)
        self.prepare_data()
    
    def prepare_data(self):
        """Prepare and clean the data"""
        # Combine Date and Timestamp columns for datetime
        self.df['DateTime'] = pd.to_datetime(
            self.df['Date'] + ' ' + self.df['Timestamp'], 
            format='%d-%m-%Y %H:%M:%S'
        )
        
        # Ensure numeric columns are properly typed
        numeric_cols = [
            'Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW',
            'Network_Latency_ms', 'Packet_Loss_%', 'Quality_Control_Defect_Rate_%',
            'Production_Speed_units_per_hr', 'Predictive_Maintenance_Score', 'Error_Rate_%'
        ]
        
        for col in numeric_cols:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Sort by datetime
        self.df = self.df.sort_values('DateTime').reset_index(drop=True)
        
        return self.df
    
    def segment_network_quality(self):
        """Segment network performance into quality bands"""
        conditions = [
            (self.df['Network_Latency_ms'] <= NETWORK_QUALITY_THRESHOLDS['high']['latency_max']) & 
            (self.df['Packet_Loss_%'] <= NETWORK_QUALITY_THRESHOLDS['high']['packet_loss_max']),
            
            (self.df['Network_Latency_ms'] <= NETWORK_QUALITY_THRESHOLDS['medium']['latency_max']) & 
            (self.df['Packet_Loss_%'] <= NETWORK_QUALITY_THRESHOLDS['medium']['packet_loss_max']),
        ]
        
        choices = ['High', 'Medium']
        self.df['Network_Quality'] = np.select(conditions, choices, default='Low')
        
        return self.df
    
    def calculate_network_stability_index(self):
        """Calculate Network Stability Index (NSI)
        NSI = (100 - Packet_Loss) * (1 - Normalized_Latency)
        """
        # Normalize latency to 0-1 scale (max expected 100ms)
        normalized_latency = np.clip(self.df['Network_Latency_ms'] / 100, 0, 1)
        
        self.df['Network_Stability_Index'] = (100 - self.df['Packet_Loss_%']) * (1 - normalized_latency)
        
        return self.df
    
    def get_efficiency_distribution(self, group_by=None):
        """Get efficiency distribution across network quality or other dimensions"""
        if group_by is None:
            return self.df['Efficiency_Status'].value_counts(normalize=True) * 100
        
        return self.df.groupby(group_by)['Efficiency_Status'].value_counts(normalize=True).unstack(fill_value=0) * 100
    
    def get_summary_statistics(self):
        """Get comprehensive summary statistics"""
        summary = {
            'Total Records': len(self.df),
            'Date Range': f"{self.df['DateTime'].min().date()} to {self.df['DateTime'].max().date()}",
            'Unique Machines': self.df['Machine_ID'].nunique(),
            'Operation Modes': self.df['Operation_Mode'].unique().tolist(),
            'Efficiency Distribution': self.df['Efficiency_Status'].value_counts().to_dict(),
        }
        return summary
    
    def get_network_statistics(self):
        """Get detailed network performance statistics"""
        return {
            'Latency': {
                'Mean': self.df['Network_Latency_ms'].mean(),
                'Std': self.df['Network_Latency_ms'].std(),
                'Min': self.df['Network_Latency_ms'].min(),
                'Max': self.df['Network_Latency_ms'].max(),
                '95th Percentile': self.df['Network_Latency_ms'].quantile(0.95),
            },
            'Packet Loss': {
                'Mean': self.df['Packet_Loss_%'].mean(),
                'Std': self.df['Packet_Loss_%'].std(),
                'Min': self.df['Packet_Loss_%'].min(),
                'Max': self.df['Packet_Loss_%'].max(),
                '95th Percentile': self.df['Packet_Loss_%'].quantile(0.95),
            }
        }
    
    def get_efficiency_statistics(self):
        """Get efficiency statistics by network quality"""
        self.segment_network_quality()
        
        stats = {}
        for quality in ['High', 'Medium', 'Low']:
            subset = self.df[self.df['Network_Quality'] == quality]
            stats[quality] = {
                'High Efficiency %': (subset['Efficiency_Status'] == 'High').sum() / len(subset) * 100,
                'Medium Efficiency %': (subset['Efficiency_Status'] == 'Medium').sum() / len(subset) * 100,
                'Low Efficiency %': (subset['Efficiency_Status'] == 'Low').sum() / len(subset) * 100,
                'Avg Production Speed': subset['Production_Speed_units_per_hr'].mean(),
                'Avg Error Rate': subset['Error_Rate_%'].mean(),
                'Avg Defect Rate': subset['Quality_Control_Defect_Rate_%'].mean(),
            }
        
        return stats
    
    def get_latency_efficiency_correlation(self):
        """Get correlation between latency and efficiency metrics"""
        # Create latency bands
        self.df['Latency_Band'] = pd.cut(
            self.df['Network_Latency_ms'],
            bins=[0, 10, 25, 50, 100],
            labels=['0-10ms', '10-25ms', '25-50ms', '50-100ms']
        )
        
        correlation = self.df.groupby('Latency_Band').agg({
            'Production_Speed_units_per_hr': 'mean',
            'Error_Rate_%': 'mean',
            'Quality_Control_Defect_Rate_%': 'mean',
            'Efficiency_Status': lambda x: (x == 'High').sum() / len(x) * 100
        }).round(2)
        
        return correlation
    
    def get_packet_loss_impact(self):
        """Analyze packet loss impact on error and defect rates"""
        self.df['Packet_Loss_Band'] = pd.cut(
            self.df['Packet_Loss_%'],
            bins=[0, 1, 3, 5, 10],
            labels=['0-1%', '1-3%', '3-5%', '5-10%']
        )
        
        impact = self.df.groupby('Packet_Loss_Band').agg({
            'Error_Rate_%': 'mean',
            'Quality_Control_Defect_Rate_%': 'mean',
            'Production_Speed_units_per_hr': 'mean',
            'Efficiency_Status': lambda x: (x == 'High').sum() / len(x) * 100
        }).round(2)
        
        return impact
    
    def get_operation_mode_analysis(self):
        """Analyze network impact across different operation modes"""
        analysis = {}
        
        for mode in self.df['Operation_Mode'].unique():
            mode_data = self.df[self.df['Operation_Mode'] == mode]
            analysis[mode] = {
                'Avg Latency': mode_data['Network_Latency_ms'].mean(),
                'Avg Packet Loss': mode_data['Packet_Loss_%'].mean(),
                'Avg Production Speed': mode_data['Production_Speed_units_per_hr'].mean(),
                'Avg Error Rate': mode_data['Error_Rate_%'].mean(),
                'High Efficiency %': (mode_data['Efficiency_Status'] == 'High').sum() / len(mode_data) * 100,
            }
        
        return analysis
    
    def export_processed_data(self, filename='processed_data.csv'):
        """Export processed data with new features"""
        self.segment_network_quality()
        self.calculate_network_stability_index()
        self.get_latency_efficiency_correlation()
        self.get_packet_loss_impact()
        
        self.df.to_csv(filename, index=False)
        return filename
