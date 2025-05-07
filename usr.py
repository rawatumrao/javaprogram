
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
