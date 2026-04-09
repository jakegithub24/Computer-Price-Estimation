"""User routes (profile, predictions, recommendations)"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
import pickle
import numpy as np
import pandas as pd
from models import db, User, Prediction
from forms import PricePredictor, RecommendationForm

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.created_at.desc()).all()
    return render_template('user/profile.html', user=current_user, predictions=predictions)

@user_bp.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    """Price prediction page"""
    if current_user.is_admin:
        flash('Admins cannot access prediction pages. Use the admin dashboard instead.', 'warning')
        return redirect(url_for('admin.dashboard'))

    df = pd.read_csv("data/laptop.csv")
    brands = sorted(df['Brand'].astype(str).unique().tolist())
    processors = sorted(df['Processor'].astype(str).unique().tolist())
    
    form = PricePredictor()
    form.brand.choices = [(str(b), b) for b in brands]
    form.processor.choices = [(str(p), p) for p in processors]
    
    prediction_result = None
    
    if form.validate_on_submit():
        try:
            # Load model
            model = pickle.load(open("model/model.pkl", "rb"))
            encoder = pickle.load(open("model/encoder.pkl", "rb"))
            
            # Prepare input
            cat = [[form.brand.data, form.processor.data]]
            cat_encoded = encoder.transform(cat)
            final_input = np.concatenate([
                cat_encoded[0],
                [form.ram.data, form.storage.data, form.screen_size.data]
            ]).reshape(1, -1)
            
            # Predict
            predicted_price = model.predict(final_input)[0]
            
            # Save prediction
            prediction = Prediction(
                user_id=current_user.id,
                brand=form.brand.data,
                processor=form.processor.data,
                ram=form.ram.data,
                storage=form.storage.data,
                screen_size=form.screen_size.data,
                gpu=form.gpu.data,
                predicted_price=predicted_price
            )
            db.session.add(prediction)
            db.session.commit()
            
            prediction_result = {
                'price': int(predicted_price),
                'brand': form.brand.data,
                'processor': form.processor.data,
                'ram': form.ram.data,
                'storage': form.storage.data,
                'screen_size': form.screen_size.data,
                'gpu': form.gpu.data
            }
            
            flash(f'Prediction successful! Estimated price: ₹{int(predicted_price):,}', 'success')
            
        except Exception as e:
            flash(f'Error in prediction: {str(e)}', 'danger')
    
    return render_template('user/predict.html', form=form, result=prediction_result, 
                         brands=brands, processors=processors)

@user_bp.route('/recommendations', methods=['GET', 'POST'])
@login_required
def recommendations():
    """Laptop recommendations by price range"""
    if current_user.is_admin:
        flash('Admins cannot access recommendations. Use the admin dashboard for insights.', 'warning')
        return redirect(url_for('admin.dashboard'))

    df = pd.read_csv("data/laptop.csv")
    form = RecommendationForm()
    
    # Set default values
    if request.method == 'GET':
        form.min_price.data = int(df['Price'].min())
        form.max_price.data = int(df['Price'].max())
    
    recommendations_list = []
    stats = None
    
    if form.validate_on_submit():
        min_price = form.min_price.data
        max_price = form.max_price.data
        
        if min_price > max_price:
            flash('Minimum price cannot be greater than maximum price', 'danger')
        else:
            # Filter laptops
            filtered_df = df[(df['Price'] >= min_price) & (df['Price'] <= max_price)].copy()
            
            if len(filtered_df) == 0:
                flash('No laptops found in this price range', 'warning')
            else:
                # Sort
                if form.sort_by.data == 'price_asc':
                    filtered_df = filtered_df.sort_values('Price')
                elif form.sort_by.data == 'price_desc':
                    filtered_df = filtered_df.sort_values('Price', ascending=False)
                elif form.sort_by.data == 'ram_desc':
                    filtered_df = filtered_df.sort_values('RAM', ascending=False)
                elif form.sort_by.data == 'storage_desc':
                    filtered_df = filtered_df.sort_values('Storage', ascending=False)
                
                recommendations_list = filtered_df.to_dict('records')
                
                # Calculate statistics
                stats = {
                    'count': len(filtered_df),
                    'avg_price': int(filtered_df['Price'].mean()),
                    'avg_ram': int(filtered_df['RAM'].mean()),
                    'avg_storage': int(filtered_df['Storage'].mean()),
                    'gpu_count': len(filtered_df[filtered_df['GPU'] == 'Yes']),
                    'price_variance': int(filtered_df['Price'].std()) if len(filtered_df) > 1 else 0,
                    'most_common_brand': filtered_df['Brand'].mode().values[0] if len(filtered_df) > 0 else 'N/A'
                }
    
    return render_template('user/recommendations.html', form=form, 
                         recommendations=recommendations_list, stats=stats)

@user_bp.route('/prediction-history')
@login_required
def prediction_history():
    """View prediction history"""
    if current_user.is_admin:
        flash('Admins cannot view prediction history. Use the admin dashboard instead.', 'warning')
        return redirect(url_for('admin.dashboard'))

    page = request.args.get('page', 1, type=int)
    predictions = Prediction.query.filter_by(user_id=current_user.id)\
        .order_by(Prediction.created_at.desc())\
        .paginate(page=page, per_page=10)
    
    return render_template('user/prediction_history.html', predictions=predictions)
