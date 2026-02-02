
# Description: This script cleans the Medical Appointment No-Shows dataset step-by-step.

# Step 1: Import libraries
import pandas as pd
import numpy as np

# Step 2: Load the dataset
df = pd.read_csv('KaggleV2-May-2016.csv')

# Step 3: View first few rows
print("🔹 First 5 rows of data:")
print(df.head())

# Step 4: Check general info
print("\n--- Dataset Info ---")
df.info()

# Step 5: Check for missing values
print("\n--- Missing Values ---")
print(df.isnull().sum())

# Step 6: Remove duplicate rows (if any)
before = df.shape[0]
df = df.drop_duplicates()
after = df.shape[0]
print(f"\n✅ Removed {before - after} duplicate rows")

# Step 7: Clean column names (lowercase and replace spaces)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
print("\n✅ Renamed Columns:")
print(df.columns.tolist())

# Step 8: Check data types
print("\n--- Data Types ---")
print(df.dtypes)

# Step 9: Fix date columns
df['scheduledday'] = pd.to_datetime(df['scheduledday'], errors='coerce')
df['appointmentday'] = pd.to_datetime(df['appointmentday'], errors='coerce')

# Step 10: Standardize text columns (Gender and No-show)
df['gender'] = df['gender'].str.strip().str.upper()
df['no-show'] = df['no-show'].str.strip().str.upper()


# Step 11: Handle missing values (if any)
df = df.fillna({
    'age': df['age'].median(),
    'scholarship': 0,
    'hipertension': 0,
    'diabetes': 0,
    'alcoholism': 0,
    'handcap': 0
})

# Step 12: Remove invalid ages (negative values)
invalid_ages = df[df['age'] < 0].shape[0]
df = df[df['age'] >= 0]
print(f"\n✅ Removed {invalid_ages} rows with invalid ages")

# Step 13: Convert selected columns to integer
int_cols = ['age', 'scholarship', 'hipertension', 'diabetes', 'alcoholism', 'handcap']
for col in int_cols:
    df[col] = df[col].astype(int)

# Step 14: Check unique values for categorical columns
print("\nUnique values in 'gender':", df['gender'].unique())
print("Unique values in 'no-show':", df['no-show'].unique())

# Step 15: Standardize 'no_show' to 'Yes' and 'No'
df['no-show'] = df['no-show'].replace({'NO': 'No', 'YES': 'Yes'})

# Step 16: Check for outliers in 'age'
print("\nAge Summary Before Capping:")
print(df['age'].describe())

# Optional: Cap extreme ages above 100
df['age'] = np.where(df['age'] > 100, 100, df['age'])

print("\nAge Summary After Capping:")
print(df['age'].describe())

# Step 17: Final structure check
print("\n--- Final Data Overview ---")
df.info()

# Step 18: Save cleaned dataset
df.to_csv('cleaned_medical_appointments.csv', index=False)
print("\n💾 Cleaned dataset saved as 'cleaned_medical_appointments.csv'")

# Step 19: Write cleaning summary
summary = """
SUMMARY OF CLEANING - Medical Appointment No Shows

1. Removed duplicate records.
2. Renamed columns to lowercase and replaced spaces with underscores.
3. Converted ScheduledDay and AppointmentDay to datetime format.
4. Standardized text fields (Gender and No-show).
5. Filled missing values (if any).
6. Removed invalid ages (negative values).
7. Converted numerical columns to integer types.
8. Capped age above 100.
9. Saved cleaned dataset to 'cleaned_medical_appointments.csv'
"""
with open("cleaning_summary.txt", "w") as f:
    f.write(summary)

print("\n📝 Summary saved as 'cleaning_summary.txt'")

