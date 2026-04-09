import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import os

# Configure Streamlit
st.set_page_config(layout="wide", page_title="Laptop Price Platform", initial_sidebar_state="expanded")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "role" not in st.session_state:
    st.session_state["role"] = None

# ============================
# LOGIN & AUTHENTICATION
# ============================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# 🔐 Login Portal")
        st.markdown("---")
        
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        role = st.radio("Login As", ["User", "Admin"])
        
        if st.button("Login", use_container_width=True):
            if role == "Admin":
                if username == "admin" and password == "1234":
                    st.session_state["logged_in"] = True
                    st.session_state["role"] = "admin"
                    st.success("Admin Login Successful ✅")
                    st.rerun()
                else:
                    st.error("Invalid Admin Credentials ❌")
            else:
                if username and password:
                    st.session_state["logged_in"] = True
                    st.session_state["role"] = "user"
                    st.success("User Login Successful ✅")
                    st.rerun()
                else:
                    st.error("Please enter credentials ❌")

# ============================
# ADMIN PANEL
# ============================
def admin_panel():
    st.markdown("# 👨‍💼 Admin Panel")
    
    admin_menu = st.sidebar.radio("Admin Options", [
        "📊 Dashboard",
        "📈 Data Management",
        "🤖 Model Training",
        "📋 System Info"
    ])
    
    if admin_menu == "📊 Dashboard":
        admin_dashboard()
    elif admin_menu == "📈 Data Management":
        data_management()
    elif admin_menu == "🤖 Model Training":
        model_training()
    elif admin_menu == "📋 System Info":
        system_info()

def admin_dashboard():
    st.subheader("📊 Admin Dashboard")
    
    df = pd.read_csv("data/laptop.csv")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Laptops", len(df))
    with col2:
        st.metric("Avg Price", f"₹{int(df['Price'].mean()):,}")
    with col3:
        st.metric("Price Range", f"₹{int(df['Price'].min()):,} - ₹{int(df['Price'].max()):,}")
    with col4:
        st.metric("Unique Brands", df['Brand'].nunique())
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Price Distribution")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(df['Price'], bins=15, color='skyblue', edgecolor='black')
        ax.set_xlabel("Price (₹)")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    
    with col2:
        st.subheader("Laptops by Brand")
        brand_count = df['Brand'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(brand_count.index, brand_count.values, color='lightcoral')
        ax.set_xlabel("Brand")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    
    st.subheader("Price by Processor")
    processor_price = df.groupby('Processor')['Price'].mean().sort_values()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.barh(processor_price.index, processor_price.values, color='lightgreen')
    ax.set_xlabel("Average Price (₹)")
    st.pyplot(fig)

def data_management():
    st.subheader("📈 Data Management")
    
    data_action = st.radio("Select Action", ["View Data", "Add New Entry", "Delete Entry"])
    
    df = pd.read_csv("data/laptop.csv")
    
    if data_action == "View Data":
        st.dataframe(df, use_container_width=True)
        st.write(f"Total Records: {len(df)}")
    
    elif data_action == "Add New Entry":
        st.write("Add a new laptop entry:")
        col1, col2 = st.columns(2)
        
        with col1:
            brand = st.selectbox("Brand", df['Brand'].unique(), key="add_brand")
            processor = st.selectbox("Processor", df['Processor'].unique(), key="add_proc")
            ram = st.number_input("RAM (GB)", 4, 64, 8)
            storage = st.number_input("Storage (GB)", 128, 2048, 256)
        
        with col2:
            gpu = st.selectbox("GPU", ["Yes", "No"])
            screen_size = st.number_input("Screen Size (inches)", 10.0, 18.0, 15.6)
            price = st.number_input("Price (₹)", 10000, 200000, 50000)
        
        if st.button("Add Entry"):
            new_entry = pd.DataFrame({
                "Brand": [brand],
                "RAM": [ram],
                "Storage": [storage],
                "Processor": [processor],
                "GPU": [gpu],
                "ScreenSize": [screen_size],
                "Price": [price]
            })
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv("data/laptop.csv", index=False)
            st.success("✅ Entry Added Successfully!")
    
    elif data_action == "Delete Entry":
        st.dataframe(df, use_container_width=True)
        row_index = st.number_input("Enter row number to delete", 0, len(df)-1)
        if st.button("Delete Row"):
            df = df.drop(row_index).reset_index(drop=True)
            df.to_csv("data/laptop.csv", index=False)
            st.success("✅ Entry Deleted!")

def model_training():
    st.subheader("🤖 Model Training")
    
    if st.button("Train New Model"):
        with st.spinner("Training model..."):
            df = pd.read_csv("data/laptop.csv")
            
            # Prepare data
            X = df[["Brand", "Processor", "RAM", "Storage", "ScreenSize"]]
            y = df["Price"]
            
            encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            X_cat = encoder.fit_transform(X[["Brand", "Processor"]])
            X_num = X[["RAM", "Storage", "ScreenSize"]].values
            X_final = np.concatenate([X_cat, X_num], axis=1)
            
            # Split and train
            X_train, X_test, y_train, y_test = train_test_split(
                X_final, y, test_size=0.2, random_state=42
            )
            
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test)
            r2 = r2_score(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            
            # Save
            os.makedirs("model", exist_ok=True)
            pickle.dump(model, open("model/model.pkl", "wb"))
            pickle.dump(encoder, open("model/encoder.pkl", "wb"))
            
            st.success(f"✅ Model Trained Successfully!")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("R² Score", f"{r2:.4f}")
            with col2:
                st.metric("MAE", f"₹{int(mae):,}")

def system_info():
    st.subheader("📋 System Information")
    
    df = pd.read_csv("data/laptop.csv")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Data Statistics:**")
        st.write(f"- Total Records: {len(df)}")
        st.write(f"- Brands: {', '.join(df['Brand'].unique())}")
        st.write(f"- Processors: {', '.join(df['Processor'].unique())}")
    
    with col2:
        st.write("**Model Files:**")
        model_exists = os.path.exists("model/model.pkl") and os.path.exists("model/encoder.pkl")
        st.write(f"- Model Status: {'✅ Loaded' if model_exists else '❌ Not Found'}")

# ============================
# USER INTERFACE
# ============================
def user_interface():
    st.markdown("# 💻 Laptop Price Prediction Platform")
    
    page = st.sidebar.radio("Select Page", [
        "🎯 Price Predictor",
        "📊 Dashboard",
        "💡 Recommendations"
    ])
    
    if page == "🎯 Price Predictor":
        price_predictor()
    elif page == "📊 Dashboard":
        user_dashboard()
    elif page == "💡 Recommendations":
        recommendation_system()

def price_predictor():
    st.subheader("🎯 Predict Laptop Price")
    
    model = pickle.load(open("model/model.pkl", "rb"))
    encoder = pickle.load(open("model/encoder.pkl", "rb"))
    df = pd.read_csv("data/laptop.csv")
    
    col1, col2 = st.columns(2)
    
    with col1:
        brand = st.selectbox("Brand", df['Brand'].unique())
        processor = st.selectbox("Processor", df['Processor'].unique())
        ram = st.selectbox("RAM (GB)", sorted(df['RAM'].unique()))
    
    with col2:
        storage = st.selectbox("Storage (GB)", sorted(df['Storage'].unique()))
        screen_size = st.slider("Screen Size (inches)", 13.0, 18.0, 15.6, 0.1)
        gpu = st.selectbox("GPU", ["Yes", "No"])
    
    if st.button("Predict Price 💰", use_container_width=True):
        try:
            cat = [[brand, processor]]
            cat_encoded = encoder.transform(cat)
            final_input = np.concatenate([
                cat_encoded[0],
                [ram, storage, screen_size]
            ]).reshape(1, -1)
            
            predicted_price = model.predict(final_input)[0]
            
            st.success(f"💰 Estimated Price: **₹{int(predicted_price):,}**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Brand", brand)
            with col2:
                st.metric("Processor", processor)
            with col3:
                st.metric("RAM", f"{ram}GB")
        except Exception as e:
            st.error(f"Error in prediction: {str(e)}")

def user_dashboard():
    st.subheader("📊 Market Dashboard")
    
    df = pd.read_csv("data/laptop.csv")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Price", f"₹{int(df['Price'].mean()):,}")
    with col2:
        st.metric("Min Price", f"₹{int(df['Price'].min()):,}")
    with col3:
        st.metric("Max Price", f"₹{int(df['Price'].max()):,}")
    with col4:
        st.metric("Total Models", len(df))
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Price Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(df['Price'], bins=15, color='steelblue', edgecolor='black', alpha=0.7)
        ax.set_xlabel("Price (₹)")
        ax.set_ylabel("Number of Laptops")
        ax.grid(alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Price by Brand")
        fig, ax = plt.subplots(figsize=(8, 5))
        brand_data = df.groupby('Brand')['Price'].mean().sort_values()
        ax.barh(brand_data.index, brand_data.values, color='coral', edgecolor='black')
        ax.set_xlabel("Average Price (₹)")
        ax.grid(alpha=0.3, axis='x')
        st.pyplot(fig)
    
    st.subheader("Price by Processor Type")
    fig, ax = plt.subplots(figsize=(10, 5))
    processor_data = df.groupby('Processor')['Price'].mean().sort_values(ascending=False)
    ax.bar(processor_data.index, processor_data.values, color='lightgreen', edgecolor='black')
    ax.set_ylabel("Average Price (₹)")
    ax.set_xlabel("Processor")
    ax.tick_params(axis='x', rotation=45)
    ax.grid(alpha=0.3, axis='y')
    st.pyplot(fig)
    
    st.subheader("RAM vs Price")
    fig, ax = plt.subplots(figsize=(10, 5))
    ram_data = df.groupby('RAM')['Price'].mean()
    ax.plot(ram_data.index, ram_data.values, marker='o', linewidth=2, markersize=8, color='purple')
    ax.set_xlabel("RAM (GB)")
    ax.set_ylabel("Average Price (₹)")
    ax.grid(alpha=0.3)
    st.pyplot(fig)

def recommendation_system():
    st.subheader("💡 Laptop Recommendations by Price Range")
    
    df = pd.read_csv("data/laptop.csv")
    
    # Price range selection
    min_price = st.slider("Minimum Price (₹)", int(df['Price'].min()), int(df['Price'].max()), int(df['Price'].min()))
    max_price = st.slider("Maximum Price (₹)", int(df['Price'].min()), int(df['Price'].max()), int(df['Price'].max()))
    
    if min_price > max_price:
        st.error("Minimum price cannot be greater than maximum price!")
        return
    
    # Filter laptops in price range
    filtered_df = df[(df['Price'] >= min_price) & (df['Price'] <= max_price)].copy()
    
    if len(filtered_df) == 0:
        st.warning("No laptops found in this price range!")
        return
    
    st.success(f"✅ Found {len(filtered_df)} laptop(s) in ₹{min_price:,} - ₹{max_price:,} range")
    
    # Sorting options
    sort_by = st.selectbox("Sort By", ["Price (Low to High)", "Price (High to Low)", "RAM (High to Low)", "Storage (High to Low)"])
    
    if sort_by == "Price (Low to High)":
        filtered_df = filtered_df.sort_values('Price')
    elif sort_by == "Price (High to Low)":
        filtered_df = filtered_df.sort_values('Price', ascending=False)
    elif sort_by == "RAM (High to Low)":
        filtered_df = filtered_df.sort_values('RAM', ascending=False)
    elif sort_by == "Storage (High to Low)":
        filtered_df = filtered_df.sort_values('Storage', ascending=False)
    
    # Display recommendations
    st.markdown("---")
    
    for idx, row in filtered_df.iterrows():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {row['Brand']} - {row['Processor']}")
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.write(f"**RAM:** {row['RAM']}GB")
            with col_b:
                st.write(f"**Storage:** {row['Storage']}GB")
            with col_c:
                st.write(f"**Screen:** {row['ScreenSize']}\"")
            with col_d:
                st.write(f"**GPU:** {row['GPU']}")
        
        with col2:
            st.markdown(f"### ₹{int(row['Price']):,}")
        
        st.divider()
    
    # Statistics for price range
    st.subheader("📈 Statistics for this Price Range")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Avg Price", f"₹{int(filtered_df['Price'].mean()):,}")
        st.metric("Most Common Brand", filtered_df['Brand'].mode().values[0] if len(filtered_df) > 0 else "N/A")
    
    with col2:
        st.metric("Avg RAM", f"{int(filtered_df['RAM'].mean())}GB")
        st.metric("Avg Storage", f"{int(filtered_df['Storage'].mean())}GB")
    
    with col3:
        st.metric("GPU Available", f"{len(filtered_df[filtered_df['GPU'] == 'Yes'])} models")
        st.metric("Price Variance", f"₹{int(filtered_df['Price'].std()):,}")

# ============================
# MAIN APP FLOW
# ============================
if not st.session_state["logged_in"]:
    login_page()
else:
    # Sidebar logout
    with st.sidebar:
        st.markdown("---")
        if st.button("🔓 Logout", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["role"] = None
            st.rerun()
    
    # Route to appropriate page
    if st.session_state["role"] == "admin":
        admin_panel()
    else:
        user_interface()