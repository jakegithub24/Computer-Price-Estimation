"""Plotting utilities for generating charts"""
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import io
import base64

def fig_to_base64(fig):
    """Convert matplotlib figure to base64 encoded string"""
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    return plot_url

def create_price_distribution(df):
    """Create price distribution chart"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df['Price'], bins=15, color='steelblue', edgecolor='black', alpha=0.7)
    ax.set_xlabel('Price (₹)', fontsize=12)
    ax.set_ylabel('Number of Laptops', fontsize=12)
    ax.set_title('Price Distribution', fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)
    return fig_to_base64(fig)

def create_brand_analysis(df):
    """Create brand analysis chart"""
    fig, ax = plt.subplots(figsize=(10, 5))
    brand_data = df.groupby('Brand')['Price'].mean().sort_values()
    ax.barh(brand_data.index, brand_data.values, color='coral', edgecolor='black')
    ax.set_xlabel('Average Price (₹)', fontsize=12)
    ax.set_title('Average Price by Brand', fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3, axis='x')
    return fig_to_base64(fig)

def create_processor_analysis(df):
    """Create processor analysis chart"""
    fig, ax = plt.subplots(figsize=(10, 5))
    processor_data = df.groupby('Processor')['Price'].mean().sort_values(ascending=False)
    ax.bar(processor_data.index, processor_data.values, color='lightgreen', edgecolor='black')
    ax.set_ylabel('Average Price (₹)', fontsize=12)
    ax.set_xlabel('Processor', fontsize=12)
    ax.set_title('Average Price by Processor', fontsize=14, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(alpha=0.3, axis='y')
    return fig_to_base64(fig)

def create_ram_analysis(df):
    """Create RAM vs price analysis chart"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ram_data = df.groupby('RAM')['Price'].mean()
    ax.plot(ram_data.index, ram_data.values, marker='o', linewidth=2, markersize=8, color='purple')
    ax.set_xlabel('RAM (GB)', fontsize=12)
    ax.set_ylabel('Average Price (₹)', fontsize=12)
    ax.set_title('RAM vs Price', fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)
    return fig_to_base64(fig)
