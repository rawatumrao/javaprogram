
 Plot the distribution of the target variable
plt.figure(figsize=(6, 4))
sns.countplot(x=y_train, palette='pastel')
plt.title("Class Distribution of Target Variable (fraud_reported)", fontsize=14)
plt.xlabel("Fraud Reported")
plt.ylabel("Number of Records")

# Show percentage on top of bars
total = len(y_train)
for p in plt.gca().patches:
    percentage = f'{100 * p.get_height() / total:.1f}%'
    plt.gca().annotate(percentage, (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha='center', va='center', fontsize=11, color='black', xytext=(0, 8),
                       textcoords='offset points')

plt.tight_layout()
plt.show()

-------
def target_likelihood_analysis(X, y, target_value='Y', top_n=None)
    likelihood_dict = {}
    categorical_cols = X.select_dtypes(include='object').columns

    for col in categorical_cols:
        temp = pd.concat([X[col], y], axis=1)
        temp['is_target'] = temp[y.name] == target_value
        summary = temp.groupby(col)['is_target'].agg(['mean', 'count']).rename(
            columns={'mean': f'{target_value}_likelihood', 'count': 'count'}
        )
        summary = summary.sort_values(by=f'{target_value}_likelihood', ascending=False)
        likelihood_dict[col] = summary

    return likelihood_dict




# Assuming you have X_train and y_train defined
likelihood_results = target_likelihood_analysis(X_train, y_train)

# View results for one specific categorical feature (e.g., 'incident_type')
print(likelihood_results['incident_type'])

# View all:
for col, df in likelihood_results.items():
    print(f"\n--- {col} ---")
    print(df)



# Step 1: Select numerical columns
numerical_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()

# Step 2: Combine features and target for plotting
df_plot = X_train.copy()
df_plot['fraud_reported'] = y_train

# Step 3: Plot
plt.figure(figsize=(20, 5 * len(numerical_cols) // 3))
for i, col in enumerate(numerical_cols, 1):
    plt.subplot((len(numerical_cols) + 2) // 3, 3, i)
    sns.boxplot(data=df_plot, x='fraud_reported', y=col, palette='Set2')
    plt.title(f'{col} vs fraud_reported')
    plt.xlabel('Fraud Reported')
    plt.ylabel(col)
    plt.tight_layout()

plt.suptitle("Bivariate Analysis: Numerical Features vs Target (Box Plots)", fontsize=20, y=1.02)
plt.show()



def create_features(df):
    df = df.copy()

    # Ratio features
    df['claim_to_vehicle_ratio'] = df['total_claim_amount'] / (df['vehicle_claim'] + 1)  # +1 to avoid division by zero
    df['claim_intensity'] = df['total_claim_amount'] / (df['months_as_customer'] + 1)

    # Binary feature
    df['is_high_deductible'] = (df['policy_deductable'] > 1000).astype(int)

    # Age groups
    df['age_group'] = pd.cut(df['age'],
                             bins=[0, 25, 45, 65, 100],
                             labels=['young', 'adult', 'senior', 'elder'])

    return df

# Apply to both sets
X_train_fe = create_features(X_train)
X_test_fe = create_features(X_test)

# Optional: check new columns
print("New features added:", set(X_train_fe.columns) - set(X_train.columns))



['months_as_customer', 'age', 'policy_state', 'policy_csl', 'policy_deductable', 'umbrella_limit', 'insured_sex', 'insured_education_level', 'insured_occupation', 'insured_hobbies', 'insured_relationship', 'capital-gains', 'capital-loss', 'incident_date', 'incident_type', 'collision_type', 'incident_severity', 'authorities_contacted', 'incident_state', 'incident_city', 'incident_hour_of_the_day', 'number_of_vehicles_involved', 'property_damage', 'bodily_injuries', 'witnesses', 'police_report_available', 'auto_make', 'auto_model', 'auto_year']


# Step 1: Drop redundant columns — based on your feature engineering
redundant_columns = [
    'vehicle_claim', 
    'months_as_customer', 
    'policy_deductable', 
    'total_claim_amount'
    # Add any other columns you found to be highly correlated or no longer needed
]

# Use errors='ignore' to safely skip missing columns
X_train_fe.drop(columns=redundant_columns, inplace=True, errors='ignore')
X_test_fe.drop(columns=redundant_columns, inplace=True, errors='ignore')

# Step 2: Check the updated data
print("✅ Remaining columns in training set:", X_train_fe.columns.tolist())
print("🔢 Training shape:", X_train_fe.shape)
print("🔢 Validation shape:", X_test_fe.shape)

# Optional: preview first few rows
print("\n📄 Preview of training data:")
print(X_train_fe.head())



------------

# Combine categories that have low frequency or provide limited predictive information
def combine_rare_categories(df, threshold=0.02):
  df = df.copy()
    cat_cols = df.select_dtypes(include='object').columns

    for col in cat_cols:
        freq = df[col].value_counts(normalize=True)
        rare_levels = freq[freq < threshold].index
        df[col] = df[col].apply(lambda x: 'Other' if x in rare_levels else x)

    return df


X_train = combine_rare_categories(X_train, threshold=0.02)
X_test = combine_rare_categories(X_test, threshold=0.02)

# Optional: check if it's working
for col in X_train.select_dtypes(include='object').columns:
    print(f"{col}: {X_train[col].nunique()} unique categories after collapsing")


---------------

# Dummy variable creation

# Step: Identify categorical columns in training data
categorical_columns = X_train.select_dtypes(include='object').columns.tolist()

# Show the list
print("✅ Categorical columns for dummy variable creation:")
print(categorical_columns)

# Create dummy variables using the 'get_dummies' for categorical columns in training data

# Step 1: Identify categorical columns
categorical_columns = X_train.select_dtypes(include='object').columns.tolist()

# Step 2: Create dummy variables using get_dummies
X_train_encoded = pd.get_dummies(X_train, columns=categorical_columns, drop_first=True)

# Preview result
print("✅ Shape after encoding:", X_train_encoded.shape)
print("📄 Encoded columns preview:")
print(X_train_encoded.head())


#Create dummy variables using the 'get_dummies' for categorical columns in validation data

# Step 1: Use same categorical columns as training
categorical_columns = X_test.select_dtypes(include='object').columns.tolist()

# Step 2: Create dummy variables for validation data
X_test_encoded = pd.get_dummies(X_test, columns=categorical_columns, drop_first=True)

# Step 3: Align validation data with training data columns
X_test_encoded = X_test_encoded.reindex(columns=X_train_encoded.columns, fill_value=0)

# Preview
print("✅ Validation data dummy encoded and aligned.")
print("📐 Shape of encoded X_test:", X_test_encoded.shape)



# Create dummy variable for dependent feature in training data
# Convert target labels from 'Y'/'N' to 1/0
y_train_encoded = y_train.map({'Y': 1, 'N': 0})
y_test_encoded = y_test.map({'Y': 1, 'N': 0})

# Check distribution
print("✅ Target class distribution (y_train):")
print(y_train_encoded.value_counts())



# Create dummy variable for dependent feature in validation data

# Convert target labels from 'Y'/'N' to 1/0 in validation data
y_test_encoded = y_test.map({'Y': 1, 'N': 0})

# Check the result
print("✅ Encoded target variable (y_test):")
print(y_test_encoded.value_counts())


----------------


# Import the necessary scaling tool from scikit-learn
from sklearn.preprocessing import StandardScaler


# Scale the numeric features present in the training data
# Identify numeric columns
numeric_cols = X_train_encoded.select_dtypes(include=['int64', 'float64']).columns

# Initialize the scaler
scaler = StandardScaler()

# Scale numeric features in training data
X_train_scaled = X_train_encoded.copy()
X_train_scaled[numeric_cols] = scaler.fit_transform(X_train_encoded[numeric_cols])


# Scale the numeric features present in the validation data

# Scale numeric features in validation data using the same scaler
X_test_scaled = X_test_encoded.copy()
X_test_scaled[numeric_cols] = scaler.transform(X_test_encoded[numeric_cols])
