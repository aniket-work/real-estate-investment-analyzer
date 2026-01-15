"""
Generate statistical charts for property analysis
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import numpy as np


# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.facecolor'] = '#f8f9fa'
plt.rcParams['axes.facecolor'] = '#ffffff'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']


def create_property_comparison_chart():
    """Creates bar chart comparing key metrics across properties"""
    
    properties = ['PROP-001\nAustin', 'PROP-002\nSan Diego', 'PROP-003\nPhoenix', 
                  'PROP-004\nNashville', 'PROP-005\nCharlotte']
    
    prices = [425, 785, 320, 550, 380]  # in thousands
    rents = [2.4, 3.2, 2.1, 3.8, 2.2]  # in thousands
    cap_rates = [6.8, 4.2, 8.5, 9.2, 7.1]  # percentages
    
    x = np.arange(len(properties))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    bars1 = ax.bar(x - width, prices, width, label='Price ($K)', color='#2196F3', alpha=0.8)
    bars2 = ax.bar(x, [r * 100 for r in rents], width, label='Monthly Rent ($100s)', color='#4CAF50', alpha=0.8)
    bars3 = ax.bar(x + width, [c * 10 for c in cap_rates], width, label='Cap Rate (×10%)', color='#FF9800', alpha=0.8)
    
    ax.set_xlabel('Properties', fontsize=14, fontweight='bold')
    ax.set_ylabel('Value', fontsize=14, fontweight='bold')
    ax.set_title('Property Investment Metrics Comparison', fontsize=18, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(properties, fontsize=11)
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.0f}',
                   ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('images/property_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Created property_comparison.png")
    plt.close()


def create_investment_scores_chart():
    """Creates radar chart showing multi-dimensional investment scores"""
    
    categories = ['Market\nScore', 'Property\nCondition', 'Financial\nMetrics', 
                  'Location\nQuality', 'ROI\nPotential']
    
    # Scores for top 3 properties
    prop_004 = [88, 95, 92, 88, 90]  # Nashville - Best
    prop_003 = [75, 78, 95, 75, 92]  # Phoenix - Second
    prop_001 = [85, 82, 78, 85, 82]  # Austin - Third
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    prop_004 += prop_004[:1]
    prop_003 += prop_003[:1]
    prop_001 += prop_001[:1]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    ax.plot(angles, prop_004, 'o-', linewidth=2, label='PROP-004 (Nashville)', color='#4CAF50')
    ax.fill(angles, prop_004, alpha=0.25, color='#4CAF50')
    
    ax.plot(angles, prop_003, 'o-', linewidth=2, label='PROP-003 (Phoenix)', color='#FF9800')
    ax.fill(angles, prop_003, alpha=0.25, color='#FF9800')
    
    ax.plot(angles, prop_001, 'o-', linewidth=2, label='PROP-001 (Austin)', color='#2196F3')
    ax.fill(angles, prop_001, alpha=0.25, color='#2196F3')
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=10)
    ax.set_title('Investment Score Comparison (Top 3 Properties)', 
                 fontsize=16, fontweight='bold', pad=30)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('images/investment_radar.png', dpi=300, bbox_inches='tight')
    print("✓ Created investment_radar.png")
    plt.close()


def create_roi_projection_chart():
    """Creates line chart showing 5-year ROI projections"""
    
    years = [0, 1, 2, 3, 4, 5]
    
    # ROI projections for top properties
    nashville = [0, 18, 38, 60, 85, 112]
    phoenix = [0, 20, 42, 66, 92, 120]
    austin = [0, 15, 32, 51, 72, 95]
    san_diego = [0, 12, 26, 42, 60, 80]
    charlotte = [0, 14, 30, 48, 68, 90]
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    ax.plot(years, nashville, marker='o', linewidth=3, label='Nashville (PROP-004)', color='#4CAF50', markersize=8)
    ax.plot(years, phoenix, marker='s', linewidth=3, label='Phoenix (PROP-003)', color='#FF9800', markersize=8)
    ax.plot(years, austin, marker='^', linewidth=3, label='Austin (PROP-001)', color='#2196F3', markersize=8)
    ax.plot(years, san_diego, marker='D', linewidth=2, label='San Diego (PROP-002)', color='#9C27B0', markersize=7, linestyle='--')
    ax.plot(years, charlotte, marker='v', linewidth=2, label='Charlotte (PROP-005)', color='#F44336', markersize=7, linestyle='--')
    
    ax.set_xlabel('Years', fontsize=14, fontweight='bold')
    ax.set_ylabel('ROI (%)', fontsize=14, fontweight='bold')
    ax.set_title('5-Year ROI Projection Comparison', fontsize=18, fontweight='bold', pad=20)
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(years)
    
    # Add value labels at year 5
    for y_vals, color in [(nashville, '#4CAF50'), (phoenix, '#FF9800'), (austin, '#2196F3')]:
        ax.text(5, y_vals[-1], f'{y_vals[-1]}%', fontsize=11, fontweight='bold', 
               color=color, ha='left', va='center')
    
    plt.tight_layout()
    plt.savefig('images/roi_projection.png', dpi=300, bbox_inches='tight')
    print("✓ Created roi_projection.png")
    plt.close()


def create_cash_flow_analysis_chart():
    """Creates stacked bar chart showing cash flow breakdown"""
    
    properties = ['Austin', 'San Diego', 'Phoenix', 'Nashville', 'Charlotte']
    
    # Monthly values
    gross_rent = [2400, 3200, 2100, 3800, 2200]
    mortgage = [1650, 2850, 1250, 2100, 1500]
    expenses = [550, 750, 450, 900, 500]
    net_cash_flow = [200, -400, 400, 800, 200]
    
    x = np.arange(len(properties))
    width = 0.6
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Stacked bars for costs
    p1 = ax.bar(x, mortgage, width, label='Mortgage', color='#FF5252', alpha=0.8)
    p2 = ax.bar(x, expenses, width, bottom=mortgage, label='Operating Expenses', color='#FFA726', alpha=0.8)
    
    # Gross rent as line
    ax.plot(x, gross_rent, marker='o', linewidth=3, markersize=10, 
           label='Gross Rent', color='#4CAF50', zorder=5)
    
    # Net cash flow markers
    for i, (prop, cash) in enumerate(zip(properties, net_cash_flow)):
        color = '#4CAF50' if cash > 0 else '#F44336'
        ax.scatter(i, gross_rent[i] + 200, s=200, marker='v' if cash > 0 else '^', 
                  color=color, zorder=6, edgecolors='black', linewidth=2)
        ax.text(i, gross_rent[i] + 350, f'${cash}', ha='center', va='bottom',
               fontsize=11, fontweight='bold', color=color)
    
    ax.set_xlabel('Properties', fontsize=14, fontweight='bold')
    ax.set_ylabel('Monthly Amount ($)', fontsize=14, fontweight='bold')
    ax.set_title('Monthly Cash Flow Analysis', fontsize=18, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(properties, fontsize=12)
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('images/cash_flow_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Created cash_flow_analysis.png")
    plt.close()


def main():
    """Generate all charts"""
    
    # Create images directory
    Path("images").mkdir(exist_ok=True)
    
    print("Generating statistical charts...")
    
    create_property_comparison_chart()
    create_investment_scores_chart()
    create_roi_projection_chart()
    create_cash_flow_analysis_chart()
    
    print("\nChart generation complete!")


if __name__ == "__main__":
    main()
