# 🚀 Flask Web App - Quick Start Guide

## ⚡ Start the Application

```bash
cd computer-price-project1
.venv\Scripts\python.exe run.py
```

Then open: **http://localhost:5000**

---

## 🔐 Login Credentials

### Admin Account (Pre-configured)
```
Username: admin
Password: Admin@123
```

### Create New User
- Click "Register" on login page
- Fill form with valid credentials
- Password requires: 1 uppercase, 1 lowercase, 1 digit, 1 special character, min 8 chars

---

## 📋 What's New in Flask Version

### ✅ User Registration & Authentication
- [x] User account creation with email validation
- [x] Secure password hashing with strength requirements
- [x] Password change functionality for all users
- [x] Admin account pre-configured with `admin / Admin@123`
- [x] Session management with remember-me option

### ✅ Admin Panel Features
- [x] Dashboard with system metrics
- [x] User management (view, activate, deactivate, delete)
- [x] Data management (add, view, delete laptop entries)
- [x] Audit logs tracking all admin actions
- [x] System information and statistics

### ✅ User Features (Retained from Streamlit)
- [x] Price prediction with ML model
- [x] Market dashboard with analytics
- [x] Smart recommendations by price range
- [x] Prediction history tracking
- [x] User profile page

### ✅ Database & Security
- [x] SQLite database with user accounts
- [x] Role-based access control (Admin/User)
- [x] Audit logging for compliance
- [x] Password strength validation
- [x] Session-based authentication

---

## 📂 Key Files Created

### Flask Application
- `app.py` - Flask app factory and initialization
- `run.py` - Application entry point
- `config.py` - Configuration management
- `models.py` - Database models
- `forms.py` - Form validation
- `plots.py` - Chart generation

### Routes (Controllers)
- `routes/auth.py` - Authentication (login, register, password change)
- `routes/main.py` - Home and dashboard
- `routes/user.py` - User predictions and recommendations
- `routes/admin.py` - Admin panel and user management

### Templates (UI)
- `templates/base.html` - Base template
- `templates/auth/` - Login, register, password change
- `templates/user/` - Profile, predict, recommendations
- `templates/admin/` - Dashboard, user management, data management

### Static Files
- `static/style.css` - Professional styling

### Documentation
- `FLASK_README.md` - Complete Flask documentation
- `requirements.txt` - Python dependencies

---

## 🎯 Key Features by Role

### User Capabilities
1. **Register** → Create account with strong password
2. **Login** → Secure authentication
3. **Profile** → View account info and recent predictions
4. **Predict** → Enter specs, get price prediction
5. **Dashboard** → View market analytics
6. **Recommend** → Find laptops in price range
7. **History** → View all past predictions
8. **Change Password** → Update account password

### Admin Capabilities
1. **Dashboard** → System overview and metrics
2. **Users** → View, activate, deactivate, delete users
3. **Data** → Add/delete laptop entries
4. **Logs** → Track all admin actions
5. **System** → View system statistics

---

## 📊 Database Structure

### Users Table
- id, username, email, password_hash
- is_admin, is_active, created_at, last_login, updated_at

### Predictions Table
- id, user_id, brand, processor, ram, storage, screen_size, gpu
- predicted_price, created_at

### Audit Logs Table
- id, admin_id, action, target_user_id, details
- ip_address, created_at

---

## 🔄 Workflow Example

### User Workflow
1. Visit http://localhost:5000
2. Click "Register" → Create account
3. Login with new credentials
4. Go to "Predict Price" → Enter specs → See prediction
5. Go to "Get Recommendations" → Set budget → Browse laptops
6. View "Prediction History" → See all past predictions
7. Change password in profile dropdown

### Admin Workflow
1. Login with `admin / Admin@123`
2. Click admin profile → Select "Admin Panel"
3. View dashboard for system overview
4. Go to "User Management" → Manage user accounts
5. Go to "Data Management" → Add/delete laptops
6. Check "Audit Logs" → See actions performed
7. View "System Info" → Check statistics

---

## 📦 Dependencies Installed

- **Flask** - Web framework
- **Flask-SQLAlchemy** - Database ORM
- **Flask-Login** - Authentication
- **Flask-WTF** - Form handling
- **WTForms** - Form validation
- **Email-Validator** - Email validation
- **SQLAlchemy** - Database management
- **Werkzeug** - Security tools

---

## 🛠️ Common Commands

### Start Flask App
```bash
.venv\Scripts\python.exe run.py
```

### Train ML Model
```bash
.venv\Scripts\python.exe train_model.py
```

### Run Streamlit Version (Alternative)
```bash
.venv\Scripts\streamlit.exe run streamlit_app.py
```

### Check Python Environment
```bash
.venv\Scripts\python.exe -c "import flask; print(flask.__version__)"
```

### Delete Database & Start Fresh
```bash
del app.db
.venv\Scripts\python.exe run.py
```

---

## 🌐 Accessing the Application

| URL | Purpose |
|-----|---------|
| http://localhost:5000 | Home page |
| http://localhost:5000/auth/login | Login |
| http://localhost:5000/auth/register | Register |
| http://localhost:5000/dashboard | Market dashboard |
| http://localhost:5000/user/predict | Price predictor |
| http://localhost:5000/user/recommendations | Get recommendations |
| http://localhost:5000/user/profile | User profile |
| http://localhost:5000/admin/dashboard | Admin panel |

---

## 💡 Tips

1. **First Time Setup**: After running app, admin user is auto-created
2. **Create Users**: Use register page or admin can manage users
3. **Delete Accounts**: Only admins can delete non-admin users  
4. **Strong Passwords**: Required format with uppercase, lowercase, digit, special char
5. **Price Predictions**: Saved to history for each user
6. **Audit Trail**: All admin actions are logged

---

## ⚠️ Troubleshooting

### If app won't start:
```bash
del app.db
.venv\Scripts\python.exe train_model.py
.venv\Scripts\python.exe run.py
```

### If you see "Port already in use":
Edit `run.py`, change `port=5000` to `port=5001`

### If templates not found:
Make sure you're in the project directory:
```bash
cd c:\Users\LENOVO\Desktop\computer-price-project1
```

---

## 📞 Version Info

- **Flask Version**: 3.0+
- **Python Version**: 3.8+
- **Database**: SQLite (app.db)
- **Type**: Professional Web Application

---

**Ready to use! Start the app with:** `.venv\Scripts\python.exe run.py`
