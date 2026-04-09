"""Admin routes (user management, analytics, data management)"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
import pandas as pd
from models import db, User, AuditLog, Prediction
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to check if user is admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def log_audit(action, target_user_id=None, details=None):
    """Log admin action"""
    audit = AuditLog(
        admin_id=current_user.id,
        action=action,
        target_user_id=target_user_id,
        details=details,
        ip_address=request.remote_addr
    )
    db.session.add(audit)
    db.session.commit()

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    total_users = User.query.count()
    admin_count = User.query.filter_by(is_admin=True).count()
    active_users = User.query.filter_by(is_active=True).count()
    total_predictions = Prediction.query.count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_predictions = Prediction.query.order_by(Prediction.created_at.desc()).limit(5).all()
    
    df = pd.read_csv("data/laptop.csv")
    avg_price = int(df['Price'].mean())
    total_laptops = len(df)
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         admin_count=admin_count,
                         active_users=active_users,
                         total_predictions=total_predictions,
                         recent_users=recent_users,
                         recent_predictions=recent_predictions,
                         avg_price=avg_price,
                         total_laptops=total_laptops)

@admin_bp.route('/users', methods=['GET'])
@login_required
@admin_required
def manage_users():
    """View all users"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) | 
            (User.email.ilike(f'%{search}%'))
        )
    
    users = query.order_by(User.created_at.desc()).paginate(page=page, per_page=20)
    
    return render_template('admin/manage_users.html', users=users, search=search)

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user account"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot delete your own account', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    if user.is_admin:
        flash('Cannot delete admin accounts', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    username = user.username
    
    # Delete user's predictions first
    Prediction.query.filter_by(user_id=user_id).delete()
    
    # Delete user
    db.session.delete(user)
    db.session.commit()
    
    # Log audit
    log_audit(f'Deleted user', target_user_id=user_id, details=f'Username: {username}')
    
    flash(f'User {username} has been deleted successfully', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    """Activate or deactivate user account"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot deactivate your own account', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    log_audit(f'{status.capitalize()} user', target_user_id=user_id)
    
    flash(f'User {user.username} has been {status}', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/data-management', methods=['GET', 'POST'], strict_slashes=False)
@admin_bp.route('/data_management', methods=['GET', 'POST'], strict_slashes=False)
@login_required
@admin_required
def data_management():
    """Manage laptop data"""
    df = pd.read_csv("data/laptop.csv")
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            new_entry = {
                'Brand': request.form.get('brand'),
                'RAM': int(request.form.get('ram')),
                'Storage': int(request.form.get('storage')),
                'Processor': request.form.get('processor'),
                'GPU': request.form.get('gpu'),
                'ScreenSize': float(request.form.get('screen_size')),
                'Price': int(request.form.get('price'))
            }
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv("data/laptop.csv", index=False)
            log_audit('Added new laptop entry', details=f"{new_entry['Brand']} {new_entry['Processor']}")
            flash('Laptop entry added successfully', 'success')
        
        elif action == 'delete':
            row_id = int(request.form.get('row_id'))
            deleted_entry = df.iloc[row_id].to_dict()
            df = df.drop(row_id).reset_index(drop=True)
            df.to_csv("data/laptop.csv", index=False)
            log_audit('Deleted laptop entry', details=f"{deleted_entry['Brand']} {deleted_entry['Processor']}")
            flash('Laptop entry deleted successfully', 'success')
    
    return render_template('admin/data_management.html', data=df.to_dict('records'), total=len(df))

@admin_bp.route('/audit-logs', methods=['GET'])
@login_required
@admin_required
def audit_logs():
    """View audit logs"""
    page = request.args.get('page', 1, type=int)
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).paginate(page=page, per_page=20)
    
    return render_template('admin/audit_logs.html', logs=logs)

@admin_bp.route('/system-info', methods=['GET'])
@login_required
@admin_required
def system_info():
    """View system information"""
    df = pd.read_csv("data/laptop.csv")
    
    info = {
        'total_users': User.query.count(),
        'admin_users': User.query.filter_by(is_admin=True).count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        'inactive_users': User.query.filter_by(is_active=False).count(),
        'total_predictions': Prediction.query.count(),
        'total_laptop_models': len(df),
        'brands': df['Brand'].nunique(),
        'processors': df['Processor'].nunique(),
        'avg_price': int(df['Price'].mean()),
        'min_price': int(df['Price'].min()),
        'max_price': int(df['Price'].max()),
    }
    
    return render_template('admin/system_info.html', info=info)
