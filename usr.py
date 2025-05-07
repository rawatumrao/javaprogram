
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

