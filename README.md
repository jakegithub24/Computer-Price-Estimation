# 💻 Laptop Price Prediction & Recommendation Platform

A comprehensive Streamlit application for laptop price prediction with admin panel, analytics dashboard, and intelligent recommendation system.

## Features

### 🔐 Authentication
- **User Login**: Access prediction and recommendation features
- **Admin Login**: Manage data, train models, and view analytics
- Credentials:
  - Admin: `admin` / `1234`
  - Users: Any credentials work (flexible user access)

### 👨‍💼 Admin Panel

#### 📊 Dashboard
- **Key Metrics**: Total laptops, average price, price range, unique brands
- **Visualizations**:
  - Price distribution histogram
  - Laptops by brand bar chart
  - Average price by processor type

#### 📈 Data Management
- **View Data**: Browse all laptop entries in the database
- **Add New Entry**: Insert new laptop specifications and prices
- **Delete Entry**: Remove records from the database

#### 🤖 Model Training
- **Train New Model**: Retrain the RandomForest model with current data
- **Performance Metrics**: R² Score and Mean Absolute Error display
- **Auto-save**: Model and encoder automatically saved to `model/` folder

#### 📋 System Info
- View dataset statistics
- Check model training status
- See available brands and processors

### 👤 User Interface

#### 🎯 Price Predictor
Enter laptop specifications and get price predictions:
- Brand selection
- Processor type
- RAM capacity
- Storage
- Screen size
- GPU availability

#### 📊 Market Dashboard
Comprehensive market analytics:
- Average, minimum, and maximum prices
- Price distribution chart
- Average price by brand
- Processor performance comparison
- RAM vs Price correlation
- Total models in database

#### 💡 Smart Recommendations
Find laptops based on your budget:
- **Price Range Filter**: Set minimum and maximum budget
- **Dynamic Sorting**:
  - Price (Low to High)
  - Price (High to Low)
  - RAM (High to Low)
  - Storage (High to Low)

- **Detailed Display**: Each recommendation shows:
  - Brand and processor
  - RAM and storage
  - Screen size
  - GPU availability
  - Price

- **Price Range Analytics**:
  - Average price in range
  - Most common brand
  - Average specifications
  - GPU availability count
  - Price variance

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare Data
Ensure `data/laptop.csv` exists with the following columns:
- Brand
- RAM
- Storage  
- Processor
- GPU (Yes/No)
- ScreenSize
- Price

### 3. Train the Model
```bash
python train_model.py
```

### 4. Run the Application
```bash
streamlit run streamlit_app.py
```

## Project Structure
```
computer-price-project1/
├── streamlit_app.py          # Main application
├── train_model.py             # Model training script
├── requirements.txt           # Python dependencies
├── data/
│   └── laptop.csv            # Dataset
└── model/
    ├── model.pkl             # Trained RandomForest model
    └── encoder.pkl           # OneHotEncoder for categorical features
```

## Model Details

**Algorithm**: RandomForest Regressor
- **Estimators**: 100 trees
- **Features**: Brand, Processor, RAM, Storage, Screen Size
- **Target**: Price
- **Train/Test Split**: 80/20

**Performance Metrics**:
- R² Score: Displays model accuracy
- Mean Absolute Error: Average prediction error

## Usage Examples

### As Admin:
1. Login with credentials (admin/1234)
2. View comprehensive dashboard with market analytics
3. Add new laptop entries to the database
4. Retrain the model with updated data
5. Monitor system status

### As User:
1. Login with any credentials
2. Predict prices for specific laptop configurations
3. View market trends in the dashboard
4. Get budget-friendly recommendations based on price range
5. Sort recommendations by your preferred criteria

## Tips

- **Better Predictions**: Add more diverse laptop data to improve model accuracy
- **Recommendations**: Adjust price range sliders to find laptops in your budget
- **Analytics**: Check the dashboard regularly to understand market trends
- **Model Training**: Retrain the model after adding significant new data

## Technologies Used
- **Streamlit**: Web application framework
- **Scikit-learn**: Machine learning model
- **Pandas**: Data manipulation
- **Matplotlib**: Data visualization
- **NumPy**: Numerical computing

## Future Enhancements
- Multi-user admin system with roles
- Database integration (instead of CSV)
- Advanced ML models (XGBoost, Neural Networks)
- Real-time price tracking
- User preferences and saved recommendations
- Mobile app version

---

**Author**: Computer Price Predictor Team  
**Version**: 2.0  
**Last Updated**: 2026
