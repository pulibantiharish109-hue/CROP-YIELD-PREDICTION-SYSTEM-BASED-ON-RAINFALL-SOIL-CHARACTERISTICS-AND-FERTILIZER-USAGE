"""
Agricultural Analytics Utilities for Crop Yield Prediction System
Provides data generation, analysis, and insights for crop yield forecasting
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ============================================================================
# 1. SAMPLE DATASET GENERATION
# ============================================================================

def generate_crop_dataset_csv(n_samples=500, filename='/home/ubuntu/crop_data.csv'):
    """Generate and save crop yield dataset to CSV"""
    np.random.seed(42)
    
    rainfall = np.random.uniform(400, 2000, n_samples)
    soil_nitrogen = np.random.uniform(10, 60, n_samples)
    soil_phosphorus = np.random.uniform(5, 40, n_samples)
    soil_potassium = np.random.uniform(80, 300, n_samples)
    soil_ph = np.random.uniform(5.5, 8.0, n_samples)
    soil_organic_matter = np.random.uniform(1, 5, n_samples)
    fertilizer_npk = np.random.uniform(50, 300, n_samples)
    pesticide_usage = np.random.uniform(0, 50, n_samples)
    temperature = np.random.uniform(15, 35, n_samples)
    humidity = np.random.uniform(40, 90, n_samples)
    irrigation_hours = np.random.uniform(0, 200, n_samples)
    
    # Generate crop yield
    base_yield = 2000
    rainfall_impact = -0.5 * ((rainfall - 1200) ** 2) / 100000
    nutrient_score = (soil_nitrogen / 60 + soil_phosphorus / 40 + soil_potassium / 300) / 3
    nutrient_impact = nutrient_score * 800
    ph_impact = -200 * ((soil_ph - 7.0) ** 2)
    organic_impact = soil_organic_matter * 300
    fertilizer_impact = np.log1p(fertilizer_npk) * 200
    pesticide_impact = -0.3 * (pesticide_usage ** 1.5)
    temp_impact = -50 * ((temperature - 24) ** 2)
    irrigation_impact = np.log1p(irrigation_hours) * 100
    
    crop_yield = (base_yield + rainfall_impact + nutrient_impact + ph_impact + 
                  organic_impact + fertilizer_impact + pesticide_impact + 
                  temp_impact + irrigation_impact + np.random.normal(0, 200, n_samples))
    crop_yield = np.maximum(crop_yield, 500)
    
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
    
    df.to_csv(filename, index=False)
    print(f"✓ Crop dataset saved: {filename}")
    return df

def generate_soil_analysis_csv(n_samples=500, filename='/home/ubuntu/soil_analysis.csv'):
    """Generate and save soil analysis dataset"""
    np.random.seed(42)
    
    soil_nitrogen = np.random.uniform(10, 60, n_samples)
    soil_phosphorus = np.random.uniform(5, 40, n_samples)
    soil_potassium = np.random.uniform(80, 300, n_samples)
    soil_ph = np.random.uniform(5.5, 8.0, n_samples)
    soil_organic_matter = np.random.uniform(1, 5, n_samples)
    soil_texture = np.random.choice(['Sandy', 'Loamy', 'Clay'], n_samples)
    soil_moisture = np.random.uniform(15, 35, n_samples)
    
    # Calculate soil quality score
    soil_quality = (
        (soil_nitrogen / 60) * 0.3 +
        (soil_phosphorus / 40) * 0.2 +
        (soil_potassium / 300) * 0.2 +
        (soil_organic_matter / 5) * 0.2 +
        (1 - abs(soil_ph - 7.0) / 2) * 0.1
    )
    
    df = pd.DataFrame({
        'Soil_Nitrogen_mg_kg': soil_nitrogen,
        'Soil_Phosphorus_mg_kg': soil_phosphorus,
        'Soil_Potassium_mg_kg': soil_potassium,
        'Soil_pH': soil_ph,
        'Soil_Organic_Matter_percent': soil_organic_matter,
        'Soil_Texture': soil_texture,
        'Soil_Moisture_percent': soil_moisture,
        'Soil_Quality_Score': soil_quality
    })
    
    df.to_csv(filename, index=False)
    print(f"✓ Soil analysis dataset saved: {filename}")
    return df

def generate_weather_analysis_csv(n_samples=365, filename='/home/ubuntu/weather_analysis.csv'):
    """Generate and save weather analysis dataset"""
    np.random.seed(42)
    
    dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(n_samples)]
    rainfall = np.random.uniform(0, 50, n_samples)
    temperature = 20 + 10 * np.sin(np.arange(n_samples) * 2 * np.pi / 365) + np.random.normal(0, 2, n_samples)
    humidity = 60 + 20 * np.sin(np.arange(n_samples) * 2 * np.pi / 365) + np.random.normal(0, 5, n_samples)
    wind_speed = np.random.uniform(5, 25, n_samples)
    
    df = pd.DataFrame({
        'Date': dates,
        'Rainfall_mm': rainfall,
        'Temperature_C': temperature,
        'Humidity_percent': humidity,
        'Wind_Speed_kmh': wind_speed
    })
    
    df.to_csv(filename, index=False)
    print(f"✓ Weather analysis dataset saved: {filename}")
    return df

def generate_fertilizer_analysis_csv(n_samples=500, filename='/home/ubuntu/fertilizer_analysis.csv'):
    """Generate and save fertilizer usage analysis"""
    np.random.seed(42)
    
    fertilizer_npk = np.random.uniform(50, 300, n_samples)
    nitrogen_percent = np.random.uniform(10, 30, n_samples)
    phosphorus_percent = np.random.uniform(5, 20, n_samples)
    potassium_percent = np.random.uniform(5, 20, n_samples)
    fertilizer_type = np.random.choice(['Organic', 'Inorganic', 'Hybrid'], n_samples)
    application_method = np.random.choice(['Broadcast', 'Banding', 'Fertigation'], n_samples)
    
    # Calculate fertilizer efficiency
    efficiency = (nitrogen_percent + phosphorus_percent + potassium_percent) / 100
    
    df = pd.DataFrame({
        'Fertilizer_NPK_kg_ha': fertilizer_npk,
        'Nitrogen_percent': nitrogen_percent,
        'Phosphorus_percent': phosphorus_percent,
        'Potassium_percent': potassium_percent,
        'Fertilizer_Type': fertilizer_type,
        'Application_Method': application_method,
        'Fertilizer_Efficiency': efficiency
    })
    
    df.to_csv(filename, index=False)
    print(f"✓ Fertilizer analysis dataset saved: {filename}")
    return df

def generate_yield_statistics_csv(n_samples=500, filename='/home/ubuntu/yield_statistics.csv'):
    """Generate and save yield statistics"""
    np.random.seed(42)
    
    rainfall = np.random.uniform(400, 2000, n_samples)
    soil_nitrogen = np.random.uniform(10, 60, n_samples)
    soil_phosphorus = np.random.uniform(5, 40, n_samples)
    soil_potassium = np.random.uniform(80, 300, n_samples)
    soil_ph = np.random.uniform(5.5, 8.0, n_samples)
    soil_organic_matter = np.random.uniform(1, 5, n_samples)
    fertilizer_npk = np.random.uniform(50, 300, n_samples)
    pesticide_usage = np.random.uniform(0, 50, n_samples)
    temperature = np.random.uniform(15, 35, n_samples)
    humidity = np.random.uniform(40, 90, n_samples)
    irrigation_hours = np.random.uniform(0, 200, n_samples)
    
    base_yield = 2000
    rainfall_impact = -0.5 * ((rainfall - 1200) ** 2) / 100000
    nutrient_score = (soil_nitrogen / 60 + soil_phosphorus / 40 + soil_potassium / 300) / 3
    nutrient_impact = nutrient_score * 800
    ph_impact = -200 * ((soil_ph - 7.0) ** 2)
    organic_impact = soil_organic_matter * 300
    fertilizer_impact = np.log1p(fertilizer_npk) * 200
    pesticide_impact = -0.3 * (pesticide_usage ** 1.5)
    temp_impact = -50 * ((temperature - 24) ** 2)
    irrigation_impact = np.log1p(irrigation_hours) * 100
    
    crop_yield = (base_yield + rainfall_impact + nutrient_impact + ph_impact + 
                  organic_impact + fertilizer_impact + pesticide_impact + 
                  temp_impact + irrigation_impact + np.random.normal(0, 200, n_samples))
    crop_yield = np.maximum(crop_yield, 500)
    
    # Categorize yields
    yield_category = pd.cut(crop_yield, bins=[0, 2000, 3000, 4000, 5000], 
                           labels=['Low', 'Medium', 'High', 'Very High'])
    
    df = pd.DataFrame({
        'Crop_Yield_kg_ha': crop_yield,
        'Yield_Category': yield_category,
        'Rainfall_mm': rainfall,
        'Soil_Nitrogen_mg_kg': soil_nitrogen,
        'Fertilizer_NPK_kg_ha': fertilizer_npk,
        'Temperature_C': temperature
    })
    
    df.to_csv(filename, index=False)
    print(f"✓ Yield statistics dataset saved: {filename}")
    return df

# ============================================================================
# 2. ANALYTICS FUNCTIONS
# ============================================================================

def analyze_crop_performance(df):
    """Analyze crop performance metrics"""
    print("\n" + "=" * 80)
    print("CROP PERFORMANCE ANALYSIS")
    print("=" * 80)
    
    yield_stats = {
        'Mean': df['Crop_Yield_kg_ha'].mean(),
        'Median': df['Crop_Yield_kg_ha'].median(),
        'Std Dev': df['Crop_Yield_kg_ha'].std(),
        'Min': df['Crop_Yield_kg_ha'].min(),
        'Max': df['Crop_Yield_kg_ha'].max(),
        'Q1': df['Crop_Yield_kg_ha'].quantile(0.25),
        'Q3': df['Crop_Yield_kg_ha'].quantile(0.75)
    }
    
    print("\nCrop Yield Statistics (kg/hectare):")
    for key, value in yield_stats.items():
        print(f"  {key}: {value:.2f}")
    
    return yield_stats

def analyze_soil_quality(df):
    """Analyze soil quality metrics"""
    print("\n" + "=" * 80)
    print("SOIL QUALITY ANALYSIS")
    print("=" * 80)
    
    print("\nSoil Nitrogen (mg/kg):")
    print(f"  Mean: {df['Soil_Nitrogen_mg_kg'].mean():.2f}")
    print(f"  Range: {df['Soil_Nitrogen_mg_kg'].min():.2f} - {df['Soil_Nitrogen_mg_kg'].max():.2f}")
    
    print("\nSoil Phosphorus (mg/kg):")
    print(f"  Mean: {df['Soil_Phosphorus_mg_kg'].mean():.2f}")
    print(f"  Range: {df['Soil_Phosphorus_mg_kg'].min():.2f} - {df['Soil_Phosphorus_mg_kg'].max():.2f}")
    
    print("\nSoil Potassium (mg/kg):")
    print(f"  Mean: {df['Soil_Potassium_mg_kg'].mean():.2f}")
    print(f"  Range: {df['Soil_Potassium_mg_kg'].min():.2f} - {df['Soil_Potassium_mg_kg'].max():.2f}")
    
    print("\nSoil pH:")
    print(f"  Mean: {df['Soil_pH'].mean():.2f}")
    print(f"  Range: {df['Soil_pH'].min():.2f} - {df['Soil_pH'].max():.2f}")
    print(f"  Optimal Range: 6.5 - 7.5")
    
    print("\nSoil Organic Matter (%):")
    print(f"  Mean: {df['Soil_Organic_Matter_percent'].mean():.2f}")
    print(f"  Range: {df['Soil_Organic_Matter_percent'].min():.2f} - {df['Soil_Organic_Matter_percent'].max():.2f}")

def analyze_environmental_factors(df):
    """Analyze environmental factors"""
    print("\n" + "=" * 80)
    print("ENVIRONMENTAL FACTORS ANALYSIS")
    print("=" * 80)
    
    print("\nRainfall (mm):")
    print(f"  Mean: {df['Rainfall_mm'].mean():.2f}")
    print(f"  Range: {df['Rainfall_mm'].min():.2f} - {df['Rainfall_mm'].max():.2f}")
    print(f"  Optimal Range: 1000 - 1500 mm")
    
    print("\nTemperature (°C):")
    print(f"  Mean: {df['Temperature_C'].mean():.2f}")
    print(f"  Range: {df['Temperature_C'].min():.2f} - {df['Temperature_C'].max():.2f}")
    print(f"  Optimal Range: 20 - 28°C")
    
    print("\nHumidity (%):")
    print(f"  Mean: {df['Humidity_percent'].mean():.2f}")
    print(f"  Range: {df['Humidity_percent'].min():.2f} - {df['Humidity_percent'].max():.2f}")
    print(f"  Optimal Range: 60 - 80%")

def identify_high_yield_factors(df, top_n=10):
    """Identify factors contributing to high yields"""
    print("\n" + "=" * 80)
    print("HIGH YIELD FACTORS ANALYSIS")
    print("=" * 80)
    
    # Get top yield samples
    top_yields = df.nlargest(top_n, 'Crop_Yield_kg_ha')
    
    print(f"\nTop {top_n} Yield Samples Average Characteristics:")
    print(f"  Rainfall: {top_yields['Rainfall_mm'].mean():.2f} mm")
    print(f"  Soil Nitrogen: {top_yields['Soil_Nitrogen_mg_kg'].mean():.2f} mg/kg")
    print(f"  Soil Phosphorus: {top_yields['Soil_Phosphorus_mg_kg'].mean():.2f} mg/kg")
    print(f"  Soil Potassium: {top_yields['Soil_Potassium_mg_kg'].mean():.2f} mg/kg")
    print(f"  Soil pH: {top_yields['Soil_pH'].mean():.2f}")
    print(f"  Fertilizer NPK: {top_yields['Fertilizer_NPK_kg_ha'].mean():.2f} kg/ha")
    print(f"  Temperature: {top_yields['Temperature_C'].mean():.2f}°C")
    print(f"  Irrigation: {top_yields['Irrigation_Hours'].mean():.2f} hours")

def identify_low_yield_factors(df, bottom_n=10):
    """Identify factors contributing to low yields"""
    print("\n" + "=" * 80)
    print("LOW YIELD FACTORS ANALYSIS")
    print("=" * 80)
    
    # Get bottom yield samples
    low_yields = df.nsmallest(bottom_n, 'Crop_Yield_kg_ha')
    
    print(f"\nBottom {bottom_n} Yield Samples Average Characteristics:")
    print(f"  Rainfall: {low_yields['Rainfall_mm'].mean():.2f} mm")
    print(f"  Soil Nitrogen: {low_yields['Soil_Nitrogen_mg_kg'].mean():.2f} mg/kg")
    print(f"  Soil Phosphorus: {low_yields['Soil_Phosphorus_mg_kg'].mean():.2f} mg/kg")
    print(f"  Soil Potassium: {low_yields['Soil_Potassium_mg_kg'].mean():.2f} mg/kg")
    print(f"  Soil pH: {low_yields['Soil_pH'].mean():.2f}")
    print(f"  Fertilizer NPK: {low_yields['Fertilizer_NPK_kg_ha'].mean():.2f} kg/ha")
    print(f"  Temperature: {low_yields['Temperature_C'].mean():.2f}°C")
    print(f"  Irrigation: {low_yields['Irrigation_Hours'].mean():.2f} hours")

# ============================================================================
# 3. MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print("\n" + "=" * 80)
    print("AGRICULTURAL ANALYTICS UTILITIES")
    print("=" * 80)
    
    print("\n[Step 1] Generating Datasets...")
    df = generate_crop_dataset_csv()
    generate_soil_analysis_csv()
    generate_weather_analysis_csv()
    generate_fertilizer_analysis_csv()
    generate_yield_statistics_csv()
    
    print("\n[Step 2] Analyzing Crop Performance...")
    analyze_crop_performance(df)
    
    print("\n[Step 3] Analyzing Soil Quality...")
    analyze_soil_quality(df)
    
    print("\n[Step 4] Analyzing Environmental Factors...")
    analyze_environmental_factors(df)
    
    print("\n[Step 5] Identifying High Yield Factors...")
    identify_high_yield_factors(df)
    
    print("\n[Step 6] Identifying Low Yield Factors...")
    identify_low_yield_factors(df)
    
    print("\n" + "=" * 80)
    print("ANALYTICS COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print("\nGenerated Datasets:")
    print("  1. crop_data.csv")
    print("  2. soil_analysis.csv")
    print("  3. weather_analysis.csv")
    print("  4. fertilizer_analysis.csv")
    print("  5. yield_statistics.csv")

if __name__ == "__main__":
    main()
