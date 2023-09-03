import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
university_rankings = pd.read_csv('World University Rankings 2023.csv')

# --- Data Cleaning ---

# Convert 'International Student' column to numeric by stripping the % sign and handling NaN values
university_rankings['International Student'] = pd.to_numeric(university_rankings['International Student'].str.rstrip('%'), errors='coerce')

# Convert 'OverAll Score' column to numeric
university_rankings['OverAll Score'] = pd.to_numeric(university_rankings['OverAll Score'], errors='coerce')

# Convert 'No of student' column to numeric by stripping commas
university_rankings['No of student'] = pd.to_numeric(university_rankings['No of student'].str.replace(',', ''), errors='coerce')

# Extract female and male ratios and compute the actual ratio as a single number (female / male)
ratios = university_rankings['Female:Male Ratio'].str.split(':', expand=True)
university_rankings['Female Ratio'] = pd.to_numeric(ratios[0], errors='coerce')
university_rankings['Male Ratio'] = pd.to_numeric(ratios[1], errors='coerce')
university_rankings['F:M Numeric Ratio'] = university_rankings['Female Ratio'] / university_rankings['Male Ratio']

# --- Data Visualization ---

# Distribution Plots for numeric scores
score_columns = [
    "OverAll Score", "Teaching Score", "Research Score", "Citations Score",
    "Industry Income Score", "International Outlook Score"
]
plt.figure(figsize=(20, 12))
for i, col in enumerate(score_columns, 1):
    plt.subplot(2, 3, i)
    sns.histplot(university_rankings[col], kde=True, bins=30)
    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Bar Plot for number of universities by country
plt.figure(figsize=(15, 10))
country_counts = university_rankings['Location'].value_counts().nlargest(30)
sns.barplot(y=country_counts.index, x=country_counts.values, palette="viridis")
plt.title('Number of Universities by Country (Top 30)')
plt.xlabel('Number of Universities')
plt.ylabel('Country')
plt.show()

# Pie Chart for Female-to-Male Ratios
bins = [0, 0.5, 0.75, 1, 1.5, 2, 3, float('inf')]
labels = ['<0.5', '0.5-0.75', '0.75-1', '1-1.5', '1.5-2', '2-3', '>3']
university_rankings['Ratio Bins'] = pd.cut(university_rankings['F:M Numeric Ratio'], bins=bins, labels=labels, right=False)
ratio_counts = university_rankings['Ratio Bins'].value_counts()
plt.figure(figsize=(10, 7))
ratio_counts.plot.pie(autopct='%1.1f%%', startangle=140, cmap='Pastel1')
plt.title('Distribution of Female-to-Male Ratios')
plt.ylabel('')  # Hide y-label
plt.show()

# Heatmap for Correlation Matrix
correlation_matrix = university_rankings[score_columns].corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Matrix of Scores')
plt.show()
