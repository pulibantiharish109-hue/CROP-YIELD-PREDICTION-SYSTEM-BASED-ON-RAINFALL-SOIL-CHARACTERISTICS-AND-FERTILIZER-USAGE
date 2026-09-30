"""
Crop Yield Prediction System Based on Rainfall, Soil Characteristics, and Fertilizer Usage
Predicts agricultural production using machine learning and agricultural data
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# ============================================================================
# 1. GENERATE SYNTHETIC AGRICULTURAL DATASET
# ============================================================================

def generate_crop_dataset(n_samples=500, random_state=42):
    """Generate synthetic crop yield dataset with realistic agricultural patterns"""
    np.random.seed(random_state)
    
    # Generate agricultural features
    rainfall = np.random.uniform(400, 2000, n_samples)  # mm per season
    soil_nitrogen = np.random.uniform(10, 60, n_samples)  # mg/kg
    soil_phosphorus = np.random.uniform(5, 40, n_samples)  # mg/kg
    soil_potassium = np.random.uniform(80, 300, n_samples)  # mg/kg
    soil_ph = np.random.uniform(5.5, 8.0, n_samples)
    soil_organic_matter = np.random.uniform(1, 5, n_samples)  # %
    fertilizer_npk = np.random.uniform(50, 300, n_samples)  # kg/hectare
    pesticide_usage = np.random.uniform(0, 50, n_samples)  # liters/hectare
    temperature = np.random.uniform(15, 35, n_samples)  # Celsius
    humidity = np.random.uniform(40, 90, n_samples)  # %
    irrigation_hours = np.random.uniform(0, 200, n_samples)  # hours per season
    
    # Generate crop yield with realistic relationships
    base_yield = 2000  # baseline yield in kg/hectare
    
    # Rainfall impact (optimal around 1000-1500mm)
    rainfall_impact = -0.5 * ((rainfall - 1200) ** 2) / 100000
    
    # Soil nutrients impact
    nutrient_score = (soil_nitrogen / 60 + soil_phosphorus / 40 + soil_potassium / 300) / 3
    nutrient_impact = nutrient_score * 800
    
    # Soil pH impact (optimal 6.5-7.5)
    ph_impact = -200 * ((soil_ph - 7.0) ** 2)
    
    # Organic matter impact
    organic_impact = soil_organic_matter * 300
    
    # Fertilizer impact (diminishing returns)
    fertilizer_impact = np.log1p(fertilizer_npk) * 200
    
    # Pesticide impact (too much is harmful)
    pesticide_impact = -0.3 * (pesticide_usage ** 1.5)
    
    # Temperature impact (optimal 20-28°C)
    temp_impact = -50 * ((temperature - 24) ** 2)
    
    # Irrigation impact
    irrigation_impact = np.log1p(irrigation_hours) * 100
    
    # Combine all impacts with noise
    crop_yield = (base_yield + rainfall_impact + nutrient_impact + ph_impact + 
                  organic_impact + fertilizer_impact + pesticide_impact + 
                  temp_impact + irrigation_impact + np.random.normal(0, 200, n_samples))
    
    crop_yield = np.maximum(crop_yield, 500)  # Minimum yield
    
    # Create DataFrame
    df = pd.DataFrame({
        'Rainfall_mm': rainfall,
        'Soil_Nitrogen_mg_kg': soil_nitrogen,
        'Soil_Phosphorus_mg_kg': soil_phosphorus,
        'Soil_Potassium_mg_kg': soil_potassium,
        'Soil_pH': soil_ph,
        'Soil_Organic_Matter_percent': soil_organic_matter,
        'Fertilizer_NPK_kg_ha': fertilizer_npk,
        'Pesticide_Usage_liters_ha': pesticide_usage,
        'Temperature_C': temperature,
        'Humidity_percent': humidity,
        'Irrigation_Hours': irrigation_hours,
        'Crop_Yield_kg_ha': crop_yield
    })
    
    print("=" * 90)
    print("CROP YIELD PREDICTION SYSTEM - DATASET OVERVIEW")
    print("=" * 90)
    print(f"\nTotal Samples: {len(df)}")
    print(f"\nCrop Yield Statistics (kg/hectare):")
    print(f"  Mean: {df['Crop_Yield_kg_ha'].mean():.2f}")
    print(f"  Min: {df['Crop_Yield_kg_ha'].min():.2f}")
    print(f"  Max: {df['Crop_Yield_kg_ha'].max():.2f}")
    print(f"  Std Dev: {df['Crop_Yield_kg_ha'].std():.2f}")
    print(f"\nRainfall Statistics (mm):")
    print(f"  Mean: {df['Rainfall_mm'].mean():.2f}")
    print(f"  Range: {df['Rainfall_mm'].min():.2f} - {df['Rainfall_mm'].max():.2f}")
    print(f"\nSoil Nutrients Statistics:")
    print(f"  Nitrogen: {df['Soil_Nitrogen_mg_kg'].mean():.2f} mg/kg")
    print(f"  Phosphorus: {df['Soil_Phosphorus_mg_kg'].mean():.2f} mg/kg")
    print(f"  Potassium: {df['Soil_Potassium_mg_kg'].mean():.2f} mg/kg")
    
    return df

# ============================================================================
# 2. FEATURE ENGINEERING
# ============================================================================

def engineer_features(df):
    """Create advanced features from raw agricultural data"""
    print("\n" + "=" * 90)
    print("FEATURE ENGINEERING")
    print("=" * 90)
    
    df_features = df.copy()
    
    # Soil nutrient ratios
    df_features['N_P_Ratio'] = df_features['Soil_Nitrogen_mg_kg'] / (df_features['Soil_Phosphorus_mg_kg'] + 1)
    df_features['N_K_Ratio'] = df_features['Soil_Nitrogen_mg_kg'] / (df_features['Soil_Potassium_mg_kg'] + 1)
    df_features['Total_Nutrients'] = (df_features['Soil_Nitrogen_mg_kg'] + 
                                      df_features['Soil_Phosphorus_mg_kg'] + 
                                      df_features['Soil_Potassium_mg_kg'])
    
    # Soil quality score
    df_features['Soil_Quality_Score'] = (
        (df_features['Soil_Nitrogen_mg_kg'] / 60) * 0.3 +
        (df_features['Soil_Phosphorus_mg_kg'] / 40) * 0.2 +
        (df_features['Soil_Potassium_mg_kg'] / 300) * 0.2 +
        (df_features['Soil_Organic_Matter_percent'] / 5) * 0.2 +
        (1 - abs(df_features['Soil_pH'] - 7.0) / 2) * 0.1
    )
    
    # Environmental stress indicators
    df_features['Rainfall_Stress'] = np.abs(df_features['Rainfall_mm'] - 1200) / 1200
    df_features['Temperature_Stress'] = np.abs(df_features['Temperature_C'] - 24) / 10
    df_features['pH_Stress'] = np.abs(df_features['Soil_pH'] - 7.0) / 1.5
    
    # Fertilizer efficiency
    df_features['Fertilizer_Efficiency'] = (df_features['Fertilizer_NPK_kg_ha'] / 
                                            (df_features['Total_Nutrients'] + 1))
    
    # Water management index
    df_features['Water_Management_Index'] = (df_features['Rainfall_mm'] + 
                                             df_features['Irrigation_Hours'] * 2)
    
    print(f"\nOriginal features: {len(df.columns) - 1}")  # Exclude target
    print(f"Engineered features: {len(df_features.columns) - 1}")
    print(f"Total samples: {len(df_features)}")
    
    return df_features

# ============================================================================
# 3. VISUALIZATION FUNCTIONS
# ============================================================================

def visualize_crop_factors(df):
    """Visualize agricultural factors and their relationships"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Rainfall vs Crop Yield
    axes[0, 0].scatter(df['Rainfall_mm'], df['Crop_Yield_kg_ha'], alpha=0.6, s=30, color='#2E86AB', edgecolor='black')
    z = np.polyfit(df['Rainfall_mm'], df['Crop_Yield_kg_ha'], 2)
    p = np.poly1d(z)
    axes[0, 0].plot(df['Rainfall_mm'].sort_values(), p(df['Rainfall_mm'].sort_values()), "r--", linewidth=2)
    axes[0, 0].set_title('Rainfall Impact on Crop Yield', fontweight='bold', fontsize=12)
    axes[0, 0].set_xlabel('Rainfall (mm)')
    axes[0, 0].set_ylabel('Crop Yield (kg/ha)')
    axes[0, 0].grid(alpha=0.3)
    
    # Fertilizer vs Crop Yield
    axes[0, 1].scatter(df['Fertilizer_NPK_kg_ha'], df['Crop_Yield_kg_ha'], alpha=0.6, s=30, color='#A23B72', edgecolor='black')
    z = np.polyfit(df['Fertilizer_NPK_kg_ha'], df['Crop_Yield_kg_ha'], 2)
    p = np.poly1d(z)
    axes[0, 1].plot(df['Fertilizer_NPK_kg_ha'].sort_values(), p(df['Fertilizer_NPK_kg_ha'].sort_values()), "r--", linewidth=2)
    axes[0, 1].set_title('Fertilizer Impact on Crop Yield', fontweight='bold', fontsize=12)
    axes[0, 1].set_xlabel('Fertilizer NPK (kg/ha)')
    axes[0, 1].set_ylabel('Crop Yield (kg/ha)')
    axes[0, 1].grid(alpha=0.3)
    
    # Soil pH vs Crop Yield
    axes[1, 0].scatter(df['Soil_pH'], df['Crop_Yield_kg_ha'], alpha=0.6, s=30, color='#F18F01', edgecolor='black')
    z = np.polyfit(df['Soil_pH'], df['Crop_Yield_kg_ha'], 2)
    p = np.poly1d(z)
    axes[1, 0].plot(df['Soil_pH'].sort_values(), p(df['Soil_pH'].sort_values()), "r--", linewidth=2)
    axes[1, 0].set_title('Soil pH Impact on Crop Yield', fontweight='bold', fontsize=12)
    axes[1, 0].set_xlabel('Soil pH')
    axes[1, 0].set_ylabel('Crop Yield (kg/ha)')
    axes[1, 0].grid(alpha=0.3)
    
    # Temperature vs Crop Yield
    axes[1, 1].scatter(df['Temperature_C'], df['Crop_Yield_kg_ha'], alpha=0.6, s=30, color='#C73E1D', edgecolor='black')
    z = np.polyfit(df['Temperature_C'], df['Crop_Yield_kg_ha'], 2)
    p = np.poly1d(z)
    axes[1, 1].plot(df['Temperature_C'].sort_values(), p(df['Temperature_C'].sort_values()), "r--", linewidth=2)
    axes[1, 1].set_title('Temperature Impact on Crop Yield', fontweight='bold', fontsize=12)
    axes[1, 1].set_xlabel('Temperature (°C)')
    axes[1, 1].set_ylabel('Crop Yield (kg/ha)')
    axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/crop_factors.png', dpi=300, bbox_inches='tight')
    print("✓ Crop factors visualization saved")
    plt.close()

def visualize_soil_nutrients(df):
    """Visualize soil nutrient relationships"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Soil nutrients vs Crop Yield
    ax1 = axes[0]
    scatter1 = ax1.scatter(df['Soil_Nitrogen_mg_kg'], df['Crop_Yield_kg_ha'], 
                          c=df['Soil_Phosphorus_mg_kg'], cmap='viridis', s=50, alpha=0.7, edgecolor='black')
    ax1.set_title('Soil Nitrogen vs Crop Yield (colored by Phosphorus)', fontweight='bold', fontsize=12)
    ax1.set_xlabel('Soil Nitrogen (mg/kg)')
    ax1.set_ylabel('Crop Yield (kg/ha)')
    cbar1 = plt.colorbar(scatter1, ax=ax1)
    cbar1.set_label('Phosphorus (mg/kg)')
    ax1.grid(alpha=0.3)
    
    # Organic matter vs Crop Yield
    ax2 = axes[1]
    scatter2 = ax2.scatter(df['Soil_Organic_Matter_percent'], df['Crop_Yield_kg_ha'],
                          c=df['Soil_pH'], cmap='coolwarm', s=50, alpha=0.7, edgecolor='black')
    ax2.set_title('Soil Organic Matter vs Crop Yield (colored by pH)', fontweight='bold', fontsize=12)
    ax2.set_xlabel('Soil Organic Matter (%)')
    ax2.set_ylabel('Crop Yield (kg/ha)')
    cbar2 = plt.colorbar(scatter2, ax=ax2)
    cbar2.set_label('Soil pH')
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/soil_nutrients.png', dpi=300, bbox_inches='tight')
    print("✓ Soil nutrients visualization saved")
    plt.close()

def visualize_correlations(df):
    """Visualize feature correlations"""
    features_to_plot = ['Rainfall_mm', 'Soil_Nitrogen_mg_kg', 'Soil_Phosphorus_mg_kg',
                       'Soil_Potassium_mg_kg', 'Soil_pH', 'Soil_Organic_Matter_percent',
                       'Fertilizer_NPK_kg_ha', 'Temperature_C', 'Humidity_percent', 'Crop_Yield_kg_ha']
    corr_matrix = df[features_to_plot].corr()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
    
    ax.set_title('Feature Correlation Matrix', fontweight='bold', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/crop_correlations.png', dpi=300, bbox_inches='tight')
    print("✓ Feature correlations visualization saved")
    plt.close()

def visualize_model_comparison(results):
    """Visualize model performance comparison"""
    models = list(results.keys())
    mae = [results[m]['MAE'] for m in models]
    rmse = [results[m]['RMSE'] for m in models]
    r2 = [results[m]['R2'] for m in models]
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # MAE comparison
    axes[0].bar(models, mae, color=['#2E86AB', '#A23B72', '#F18F01'], alpha=0.8, edgecolor='black')
    axes[0].set_title('Mean Absolute Error (MAE)', fontweight='bold', fontsize=12)
    axes[0].set_ylabel('MAE (kg/ha)')
    axes[0].grid(axis='y', alpha=0.3)
    
    # RMSE comparison
    axes[1].bar(models, rmse, color=['#2E86AB', '#A23B72', '#F18F01'], alpha=0.8, edgecolor='black')
    axes[1].set_title('Root Mean Squared Error (RMSE)', fontweight='bold', fontsize=12)
    axes[1].set_ylabel('RMSE (kg/ha)')
    axes[1].grid(axis='y', alpha=0.3)
    
    # R² comparison
    axes[2].bar(models, r2, color=['#2E86AB', '#A23B72', '#F18F01'], alpha=0.8, edgecolor='black')
    axes[2].set_title('R² Score', fontweight='bold', fontsize=12)
    axes[2].set_ylabel('R² Score')
    axes[2].set_ylim([0, 1])
    axes[2].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/model_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Model comparison visualization saved")
    plt.close()

def visualize_predictions(y_test, y_pred_lr, y_pred_rf, y_pred_gb):
    """Visualize actual vs predicted crop yields"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    models_data = [
        ('Linear Regression', y_pred_lr),
        ('Random Forest', y_pred_rf),
        ('Gradient Boosting', y_pred_gb)
    ]
    
    for idx, (name, y_pred) in enumerate(models_data):
        axes[idx].scatter(y_test, y_pred, alpha=0.6, s=30, color='#2E86AB', edgecolor='black')
        
        # Perfect prediction line
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        axes[idx].plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')
        
        axes[idx].set_title(f'{name}', fontweight='bold', fontsize=12)
        axes[idx].set_xlabel('Actual Yield (kg/ha)')
        axes[idx].set_ylabel('Predicted Yield (kg/ha)')
        axes[idx].legend()
        axes[idx].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/predictions_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Predictions comparison visualization saved")
    plt.close()

# ============================================================================
# 4. MODEL BUILDING AND TRAINING
# ============================================================================

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple regression models"""
    print("\n" + "=" * 90)
    print("MODEL TRAINING")
    print("=" * 90)
    
    results = {}
    models = {}
    predictions = {}
    
    # Linear Regression
    print("\nTraining Linear Regression...")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    
    results['Linear Regression'] = {
        'MAE': mean_absolute_error(y_test, y_pred_lr),
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_lr)),
        'R2': r2_score(y_test, y_pred_lr)
    }
    models['Linear Regression'] = lr_model
    predictions['Linear Regression'] = y_pred_lr
    
    # Random Forest
    print("Training Random Forest Regressor...")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    
    results['Random Forest'] = {
        'MAE': mean_absolute_error(y_test, y_pred_rf),
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_rf)),
        'R2': r2_score(y_test, y_pred_rf)
    }
    models['Random Forest'] = rf_model
    predictions['Random Forest'] = y_pred_rf
    
    # Gradient Boosting
    print("Training Gradient Boosting Regressor...")
    gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    gb_model.fit(X_train, y_train)
    y_pred_gb = gb_model.predict(X_test)
    
    results['Gradient Boosting'] = {
        'MAE': mean_absolute_error(y_test, y_pred_gb),
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_gb)),
        'R2': r2_score(y_test, y_pred_gb)
    }
    models['Gradient Boosting'] = gb_model
    predictions['Gradient Boosting'] = y_pred_gb
    
    return results, models, predictions, y_pred_lr, y_pred_rf, y_pred_gb

# ============================================================================
# 5. MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print("\n" + "=" * 90)
    print("CROP YIELD PREDICTION SYSTEM")
    print("=" * 90)
    
    # Generate dataset
    print("\n[Step 1] Generating Agricultural Dataset...")
    df = generate_crop_dataset(n_samples=500)
    
    # Engineer features
    print("\n[Step 2] Engineering Features...")
    df_features = engineer_features(df)
    
    # Prepare data for modeling
    print("\n[Step 3] Preparing Data for Modeling...")
    feature_cols = [col for col in df_features.columns if col != 'Crop_Yield_kg_ha']
    X = df_features[feature_cols].values
    y = df_features['Crop_Yield_kg_ha'].values
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    print("\n[Step 4] Splitting Data...")
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    print(f"Training set size: {len(X_train)} samples")
    print(f"Test set size: {len(X_test)} samples")
    
    # Generate visualizations
    print("\n[Step 5] Generating Visualizations...")
    print("Creating crop factors visualization...")
    visualize_crop_factors(df)
    
    print("Creating soil nutrients visualization...")
    visualize_soil_nutrients(df)
    
    print("Creating feature correlations...")
    visualize_correlations(df)
    
    # Train models
    print("\n[Step 6] Training Regression Models...")
    results, models, predictions, y_pred_lr, y_pred_rf, y_pred_gb = train_models(
        X_train, X_test, y_train, y_test
    )
    
    # Print results
    print("\n" + "=" * 90)
    print("MODEL PERFORMANCE RESULTS")
    print("=" * 90)
    for model_name, metrics in results.items():
        print(f"\n{model_name}:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.4f}")
    
    # Generate additional visualizations
    print("\n[Step 7] Generating Additional Visualizations...")
    print("Creating model comparison...")
    visualize_model_comparison(results)
    
    print("Creating predictions comparison...")
    visualize_predictions(y_test, y_pred_lr, y_pred_rf, y_pred_gb)
    
    print("\n" + "=" * 90)
    print("EXECUTION COMPLETED SUCCESSFULLY")
    print("=" * 90)
    print("\nGenerated Visualizations:")
    print("  1. crop_factors.png")
    print("  2. soil_nutrients.png")
    print("  3. crop_correlations.png")
    print("  4. model_comparison.png")
    print("  5. predictions_comparison.png")
    
    return df, df_features, X_train, X_test, y_train, y_test, results, models

if __name__ == "__main__":
    df, df_features, X_train, X_test, y_train, y_test, results, models = main()
