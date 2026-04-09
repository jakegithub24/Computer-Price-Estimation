from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from models import User
import re

class LoginForm(FlaskForm):
    """Form for user login"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    """Form for user registration"""
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=80, message='Username must be 3-80 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')
    
    def validate_username(self, field):
        """Check if username already exists"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken!')
    
    def validate_email(self, field):
        """Check if email already exists"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered!')
    
    def validate_password(self, field):
        """Validate password strength"""
        password = field.data
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character')

class ChangePasswordForm(FlaskForm):
    """Form for changing password"""
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')
    
    def validate_new_password(self, field):
        """Validate new password strength"""
        password = field.data
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character')

class PricePredictor(FlaskForm):
    """Form for laptop price prediction"""
    brand = SelectField('Brand', validators=[DataRequired()])
    processor = SelectField('Processor', validators=[DataRequired()])
    ram = SelectField('RAM (GB)', choices=[(4, '4GB'), (8, '8GB'), (16, '16GB'), (32, '32GB')], 
                     coerce=int, validators=[DataRequired()])
    storage = SelectField('Storage (GB)', choices=[(128, '128GB'), (256, '256GB'), (512, '512GB'), (1024, '1024GB')], 
                         coerce=int, validators=[DataRequired()])
    screen_size = FloatField('Screen Size (inches)', validators=[DataRequired()])
    gpu = SelectField('GPU', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    submit = SubmitField('Predict Price')

class RecommendationForm(FlaskForm):
    """Form for laptop recommendations"""
    min_price = IntegerField('Minimum Price (₹)', validators=[DataRequired()])
    max_price = IntegerField('Maximum Price (₹)', validators=[DataRequired()])
    sort_by = SelectField('Sort By', choices=[
        ('price_asc', 'Price (Low to High)'),
        ('price_desc', 'Price (High to Low)'),
        ('ram_desc', 'RAM (High to Low)'),
        ('storage_desc', 'Storage (High to Low)')
    ], validators=[DataRequired()])
    submit = SubmitField('Get Recommendations')
