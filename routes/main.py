"""Main routes (index, dashboard, etc)"""
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from plots import create_price_distribution, create_brand_analysis, create_processor_analysis

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with market analytics"""
    try:
        df = pd.read_csv("data/laptop.csv")
        
        # Calculate metrics
        avg_price = int(df['Price'].mean())
        min_price = int(df['Price'].min())
        max_price = int(df['Price'].max())
        total_models = len(df)
        
        # Create visualizations
        price_dist = create_price_distribution(df)
        brand_analysis = create_brand_analysis(df)
        processor_analysis = create_processor_analysis(df)
        
        return render_template('dashboard.html',
                             avg_price=avg_price,
                             min_price=min_price,
                             max_price=max_price,
                             total_models=total_models,
                             price_dist=price_dist,
                             brand_analysis=brand_analysis,
                             processor_analysis=processor_analysis)
    except Exception as e:
        return render_template('error.html', error=str(e)), 400
