
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
