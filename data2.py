import pandas as pd

df = pd.read_csv("ml/data/raw/cooling_tower_dataset.csv")

# Select numerical columns
numeric_df = df.select_dtypes(include="number")

# Correlation with Water Consumption
correlation = numeric_df.corr()["Water Consumption (L)"].sort_values(
    ascending=False
)

print("===== CORRELATION WITH WATER CONSUMPTION =====")
print(correlation)

print("\n===== WATER CONSUMPTION RELATIONSHIPS =====")

print("\nWater Flow Rate:")
print(df["Water Flow Rate (L/s)"].describe())

print("\nCooling Capacity:")
print(df["Cooling Capacity (kW)"].describe())

print("\nEnergy Consumption:")
print(df["Energy Consumption (kWh)"].describe())

print("\nWater Consumption:")
print(df["Water Consumption (L)"].describe())



df = pd.read_csv("ml/data/raw/cooling_tower_dataset.csv")

targets = [
    "Cooling Tower Efficiency (%)",
    "Energy Savings (%)",
    "Water Consumption (L)",
    "CO2 Emissions (kg)"
]

features = [
    "Outdoor Temp (°C)",
    "Outdoor Humidity (%)",
    "Wind Speed (m/s)",
    "Water Inlet Temp (°C)",
    "Water Outlet Temp (°C)",
    "Water Flow Rate (L/s)",
    "Air Velocity (m/s)",
    "Cooling Capacity (kW)",
    "Energy Consumption (kWh)",
    "PID Output"
]

for target in targets:
    print(f"\n===== {target} =====")
    
    corr = df[features + [target]].corr()[target]
    print(corr.sort_values(ascending=False))


import matplotlib.pyplot as plt

df = pd.read_csv("ml/data/raw/cooling_tower_dataset.csv")

# Water consumption distribution
plt.figure(figsize=(8,5))
plt.hist(df["Water Consumption (L)"], bins=30)
plt.xlabel("Water Consumption (L)")
plt.ylabel("Frequency")
plt.title("Water Consumption Distribution")
plt.show()


# Water flow vs water consumption
plt.figure(figsize=(8,5))
plt.scatter(
    df["Water Flow Rate (L/s)"],
    df["Water Consumption (L)"],
    alpha=0.5
)
plt.xlabel("Water Flow Rate (L/s)")
plt.ylabel("Water Consumption (L)")
plt.title("Water Flow Rate vs Water Consumption")
plt.show()


# Cooling capacity vs water consumption
plt.figure(figsize=(8,5))
plt.scatter(
    df["Cooling Capacity (kW)"],
    df["Water Consumption (L)"],
    alpha=0.5
)
plt.xlabel("Cooling Capacity (kW)")
plt.ylabel("Water Consumption (L)")
plt.title("Cooling Capacity vs Water Consumption")
plt.show()