# 💻 Laptop Price Prediction - Flask Web Application

A professional Flask-based web application for laptop price prediction with user authentication, admin panel, and comprehensive features.

## 🎯 Features

### 🔐 Authentication & User Management
- **User Registration**: Create account with strong password requirements
- **User Login**: Secure authentication with remember-me functionality
- **Password Management**: Change password with current password verification
- **Admin Credentials**: Default admin (Username: `admin`, Password: `Admin@123`)
- **Session Management**: Secure session handling with configurable expiration

### 👤 User Features
1. **🎯 Price Predictor**
   - Enter laptop specifications (Brand, Processor, RAM, Storage, Screen, GPU)
   - Get instant price predictions using ML model
   - View prediction history

2. **📊 Market Dashboard**
   - Price distribution visualization
   - Brand-wise price comparison
   - Processor performance analysis
   - Market trends and analytics

3. **💡 Smart Recommendations**
   - Filter laptops by price range
   - Sort by price, RAM, or storage
   - View detailed laptop specifications
   - Market statistics for price range

4. **📋 User Profile**
   - View account information
   - See recent predictions
   - Access full prediction history

### 👨‍💼 Admin Features

1. **📊 Admin Dashboard**
   - System overview metrics
   - User and prediction statistics
   - Recent activity feeds

2. **👥 User Management**
   - View all users with filtering/search
   - Activate/Deactivate user accounts
   - Delete user accounts (non-admin only)
   - User statistics and info

3. **📈 Data Management**
   - View laptop database
   - Add new laptop entries
   - Delete laptop entries
   - Manage price data

4. **📋 Audit Logs**
   - Track all admin actions
   - Log admin, action, target user, and timestamp
   - Monitor system activity

5. **📋 System Information**
   - User statistics (total, active, admin, inactive)
   - Prediction metrics
   - Database information
   - Price range statistics

## 📦 Installation

### 1. Clone/Download Project
```bash
cd computer-price-project1
```

### 2. Configure Python Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
# or
source .venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Prepare Data
Ensure `data/laptop.csv` exists with columns:
```
Brand, RAM, Storage, Processor, GPU, ScreenSize, Price
```

### 5. Train ML Model
```bash
python train_model.py
```

Should output:
```
✅ Model Accuracy (R2 Score): 0.XX
✅ Model & Encoder saved!
```

### 6. Run Flask Application
```bash
python run.py
```

Application will be available at: `http://localhost:5000`

## 🚀 Running the Application

### Development Mode
```bash
python run.py
```

### Production Mode
```bash
export FLASK_ENV=production  # Linux/macOS
# or
set FLASK_ENV=production  # Windows PowerShell
python run.py
```

## 📂 Project Structure

```
computer-price-project1/
├── app.py                      # Flask app factory
├── run.py                      # Application entry point
├── config.py                   # Configuration management
├── models.py                   # Database models (User, Prediction, AuditLog)
├── forms.py                    # WTForms for validation
├── plots.py                    # Chart generation utilities
├── train_model.py              # ML model training script
├── requirements.txt            # Python dependencies
│
├── routes/                     # Application routes
│   ├── __init__.py
│   ├── auth.py                # Authentication (login, register, password)
│   ├── main.py                # Main/Home routes
│   ├── user.py                # User prediction & recommendations
│   └── admin.py               # Admin panel routes
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── dashboard.html         # User dashboard
│   ├── error.html             # Error page
│   ├── auth/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── change_password.html
│   ├── user/
│   │   ├── profile.html
│   │   ├── predict.html
│   │   ├── recommendations.html
│   │   └── prediction_history.html
│   └── admin/
│       ├── dashboard.html
│       ├── manage_users.html
│       ├── data_management.html
│       ├── audit_logs.html
│       └── system_info.html
│
├── static/
│   └── style.css              # Custom CSS styling
│
├── data/
│   └── laptop.csv             # Dataset (CSV format)
│
└── model/
    ├── model.pkl              # Trained ML model
    └── encoder.pkl            # OneHotEncoder
```

## 🔐 User Credentials

### Default Admin Account
- **Username**: `admin`
- **Password**: `Admin@123`

### Create New Users
- Visit `/auth/register` to create new user accounts
- Password requirements:
  - Minimum 8 characters
  - At least 1 uppercase letter
  - At least 1 lowercase letter
  - At least 1 digit
  - At least 1 special character

## 📊 Database Models

### User Model
- `id`: Primary key
- `username`: Unique username
- `email`: User email
- `password_hash`: Hashed password
- `is_admin`: Admin flag
- `is_active`: Account status
- `created_at`: Registration date
- `last_login`: Last login timestamp

### Prediction Model
- `id`: Primary key
- `user_id`: User reference
- `brand`, `processor`, `ram`, `storage`, `screen_size`, `gpu`: Specifications
- `predicted_price`: ML model prediction
- `created_at`: Prediction timestamp

### AuditLog Model
- `id`: Primary key
- `admin_id`: Admin performing action
- `action`: Action description
- `target_user_id`: User affected
- `details`: Additional details
- `ip_address`: Admin IP address
- `created_at`: Timestamp

## 🛡️ Security Features

- ✅ Password hashing with Werkzeug
- ✅ Session-based authentication
- ✅ CSRF protection with Flask-WTF
- ✅ Role-based access control (Admin/User)
- ✅ Audit logging for admin actions
- ✅ Account activation/deactivation
- ✅ Password strength validation
- ✅ Secure password storage

## 🔄 API Routes

### Authentication Routes (`/auth`)
- `GET/POST /auth/login` - User login
- `GET/POST /auth/register` - User registration
- `POST /auth/logout` - User logout
- `GET/POST /auth/change-password` - Change password

### User Routes (`/user`)
- `GET /user/profile` - User profile
- `GET/POST /user/predict` - Price prediction
- `GET/POST /user/recommendations` - Get recommendations
- `GET /user/prediction-history` - View predictions

### Admin Routes (`/admin`)
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/users` - User management
- `POST /admin/users/<id>/delete` - Delete user
- `POST /admin/users/<id>/toggle-status` - Activate/Deactivate user
- `GET/POST /admin/data-management` - Manage laptop data
- `GET /admin/audit-logs` - View audit logs
- `GET /admin/system-info` - System information

### Main Routes (`/`)
- `GET /` - Home page
- `GET /dashboard` - Market dashboard

## 🛠️ Configuration

Edit `config.py` to customize:

```python
class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # True in production
```

## 📈 Model Information

**Algorithm**: RandomForest Regressor
- Estimators: 100
- Features: Brand, Processor, RAM, Storage, Screen Size
- Train/Test Split: 80/20

## 🎨 Styling

- Bootstrap 5 for responsive UI
- Custom CSS in `static/style.css`
- Professional cards and components
- Smooth animations and transitions

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**: Activate virtual environment and run:
```bash
pip install -r requirements.txt
```

### Issue: Database locked
**Solution**: Delete `app.db` and restart:
```bash
del app.db
python run.py
```

### Issue: Model not found
**Solution**: Train the model:
```bash
python train_model.py
```

### Issue: Port 5000 already in use
**Solution**: Change port in `run.py`:
```python
app.run(debug=True, port=5001)
```

## 📝 License

This project is open source and available for educational and personal use.

## 🤝 Support

For issues or questions, please check the terminal output and error messages for debugging information.

---

**Version**: 3.0 (Flask Web Application)  
**Last Updated**: 2026  
**Python Version**: 3.8+
