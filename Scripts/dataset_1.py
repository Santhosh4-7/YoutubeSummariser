from sklearn.linear_model import LinearRegression
from scipy.stats import ttest_ind, norm
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from scipy.stats import ttest_ind, chi2_contingency, norm
# Set Streamlit page config
st.set_page_config(page_title="Comprehensive Data Analysis", layout="wide")

# Cache Data Collection
@st.cache_data
def collect_data():
    file_path = r"C:\DAV_dashboard\scisumm.csv"
    data = pd.read_csv(file_path)
    return data

# Data Preparation
def prepare_data(data):
    """
    Enhances data preparation:
    - Calculate article and summary lengths.
    - Handle missing values.
    - Summarize data statistics.
    """
    # Add article and summary lengths
    data['article_length'] = data['text'].apply(lambda x: len(str(x).split()))
    data['summary_length'] = data['summary'].apply(lambda x: len(str(x).split()))
    
    # Handle missing values
    missing_values = data.isnull().sum()
    st.header("2. DATA PREPARATION")
    st.write(missing_values)
    data = data.dropna()  # Drop rows with missing values
    
    # Summary Statistics
    st.header("3. Statistical Analysis of Lengths")
    stats = data[['article_length', 'summary_length']].describe()
    st.write(stats)
    
    # Add any additional feature transformations if required
    return data
file_path = r"C:\DAV_dashboard\scisumm.csv"
data = pd.read_csv(file_path)
# Feature Analysis
def feature_analysis(data):
    correlation = data.corr()
    return correlation

# Outliers Detection
def detect_outliers(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers, lower_bound, upper_bound

def chi_square_test(data):
    # Creating a contingency table with article and summary length as categorical bins
    data['article_bins'] = pd.qcut(data['article_length'], q=4, labels=["Low", "Medium", "High", "Very High"])
    data['summary_bins'] = pd.qcut(data['summary_length'], q=4, labels=["Low", "Medium", "High", "Very High"])
    contingency_table = pd.crosstab(data['article_bins'], data['summary_bins'])
    
    chi2, p, dof, _ = chi2_contingency(contingency_table)
    return chi2, p, dof

def t_test(data):
    # Splitting data into two groups based on median article length
    median_length = data['article_length'].median()
    group1 = data[data['article_length'] <= median_length]['summary_length']
    group2 = data[data['article_length'] > median_length]['summary_length']
    
    t_stat, p_value = ttest_ind(group1, group2, equal_var=False)
    return t_stat, p_value

def z_test(data):
    # Z-test comparing article length and summary length mean
    mean_diff = data['article_length'].mean() - data['summary_length'].mean()
    pooled_std = np.sqrt((data['article_length'].std()**2 + data['summary_length'].std()**2) / 2)
    z_stat = mean_diff / (pooled_std / np.sqrt(len(data)))
    p_value = 2 * (1 - norm.cdf(abs(z_stat)))
    return z_stat, p_value
# Predictive Modeling
def predictive_modeling(data):
    X = data[['article_length']]
    y = data['summary_length']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    
    predictions = model.predict(X_test)
    return model, score, X_test, y_test, predictions

# Interactive Sidebar
st.sidebar.header("Interactive Options")
show_bar_chart = st.sidebar.checkbox("Show Bar Chart", value=True)
show_boxplot = st.sidebar.checkbox("Show Boxplot", value=True)
show_scatter = st.sidebar.checkbox("Show Scatter Plot", value=True)

# Main App
st.title("Comprehensive Data Analysis with Custom Dataset")
st.write("""
This app demonstrates an advanced workflow for analyzing the dataset with detailed statistics, 
visualizations, outliers detection, predictive modeling, hypothesis testing, and more.
""")

# Load and Prepare Data
data = collect_data()


# 1. Data Overview
st.header("1. Data Overview")
st.write("### Sample Data")
st.write(data.head())
prepared_data = prepare_data(data)
# 2. Statistical Analysis

st.write("Analyzing central tendencies (mean, median) and dispersion (standard deviation).")

mean_article_length = prepared_data['article_length'].mean()
median_article_length = prepared_data['article_length'].median()
std_article_length = prepared_data['article_length'].std()

mean_summary_length = prepared_data['summary_length'].mean()
median_summary_length = prepared_data['summary_length'].median()
std_summary_length = prepared_data['summary_length'].std()

st.write(f"- **Mean Article Length**: {mean_article_length:.2f}")
st.write(f"- **Median Article Length**: {median_article_length:.2f}")
st.write(f"- **Standard Deviation of Article Length**: {std_article_length:.2f}")
st.write(f"- **Mean Summary Length**: {mean_summary_length:.2f}")
st.write(f"- **Median Summary Length**: {median_summary_length:.2f}")
st.write(f"- **Standard Deviation of Summary Length**: {std_summary_length:.2f}")


# 3. Visualizations
st.header("4.Exploratory Data Analyis")
st.header(" Visualizations")
def plot_histogram(data, column, bins=20):
    """
    Function to plot a histogram for a specified column.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data[column], bins=bins, kde=True, color="skyblue", ax=ax)
    ax.set_title(f"Histogram of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")
    return fig

st.write("### Histogram: Article Length")
fig_article_hist = plot_histogram(prepared_data, 'article_length', bins=30)
st.pyplot(fig_article_hist)

# Histogram for Summary Length
st.write("### Histogram: Summary Length")
fig_summary_hist = plot_histogram(prepared_data, 'summary_length', bins=30)
st.pyplot(fig_summary_hist)

if show_bar_chart:
    st.write("### Bar Chart")
    average_lengths = pd.DataFrame({
        "Type": ["Article", "Summary"],
        "Average Length": [mean_article_length, mean_summary_length]
    })
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=average_lengths, x="Type", y="Average Length", palette="viridis", ax=ax)
    ax.set_title("Average Lengths of Articles and Summaries")
    st.pyplot(fig)

if show_boxplot:
    st.write("### Boxplot")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=prepared_data, palette="Set2", ax=ax)
    ax.set_title("Distribution of Article and Summary Lengths")
    st.pyplot(fig)

if show_scatter:
    st.write("### Scatter Plot")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=prepared_data, x="article_length", y="summary_length", alpha=0.5, ax=ax)
    ax.set_title("Article Length vs Summary Length")
    st.pyplot(fig)

# 4. Outliers Analysis
st.header("  Outliers Analysis")
article_outliers, lower_article, upper_article = detect_outliers(prepared_data, 'article_length')
summary_outliers, lower_summary, upper_summary = detect_outliers(prepared_data, 'summary_length')

st.write(f"### Article Length Outliers: {len(article_outliers)}")
st.write(f"Lower Bound: {lower_article:.2f}, Upper Bound: {upper_article:.2f}")

st.write(f"### Summary Length Outliers: {len(summary_outliers)}")
st.write(f"Lower Bound: {lower_summary:.2f}, Upper Bound: {upper_summary:.2f}")

# Outliers Visualization
def plot_outliers(data, column, lower_bound, upper_bound):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=data, x=data.index, y=column, ax=ax, color="blue", alpha=0.7, label="Data Points")
    ax.axhline(lower_bound, color="red", linestyle="--", label="Lower Bound")
    ax.axhline(upper_bound, color="red", linestyle="--", label="Upper Bound")
    
    # Highlight Outliers
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    sns.scatterplot(data=outliers, x=outliers.index, y=column, ax=ax, color="orange", label="Outliers", s=50)
    
    ax.set_title(f"Outlier Detection for {column}")
    ax.set_xlabel("Index")
    ax.set_ylabel(column)
    ax.legend()
    return fig



# Article Length Outliers
st.write("### Article Length Outliers Visualization")
article_outliers, lower_article, upper_article = detect_outliers(prepared_data, 'article_length')
fig_article = plot_outliers(prepared_data, 'article_length', lower_article, upper_article)
st.pyplot(fig_article)

# Summary Length Outliers
st.write("### Summary Length Outliers Visualization")
summary_outliers, lower_summary, upper_summary = detect_outliers(prepared_data, 'summary_length')
fig_summary = plot_outliers(prepared_data, 'summary_length', lower_summary, upper_summary)
st.pyplot(fig_summary)


# 5. Feature Analysis
# 5. Feature Analysis# 5. Feature Analysis
st.header("5. Feature Analysis")
correlation = feature_analysis(prepared_data)
st.write("### Correlation Matrix")
st.write(correlation)

fig, ax = plt.subplots()
sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Feature Correlation")
st.pyplot(fig)


# 6. Linear Regression
st.header("6. PREDICTIVE MODELING")
model, score, X_test, y_test, predictions = predictive_modeling(prepared_data)
st.write(f"### Model R^2 Score: {score:.2f}")

fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(X_test, y_test, label="Actual", alpha=0.5)
ax.scatter(X_test, predictions, label="Predicted", alpha=0.5, color='red')
ax.set_title("Actual vs Predicted Summary Lengths")
ax.set_xlabel("Article Length")
ax.set_ylabel("Summary Length")
ax.legend()
st.pyplot(fig)


st.header("7. Hypothesis Testing")
# Chi-Square Test
chi2, p_chi, dof = chi_square_test(prepared_data)
st.write(f"**Chi-Square Test**: chi2 = {chi2:.2f}, p-value = {p_chi:.50f}, dof = {dof}")
if p_chi < 0.05:
    st.write("Result: Significant difference between article and summary lengths (p < 0.05).")
else:
    st.write("Result: No significant association between article and summary lengths (p > 0.05).")

# T-Test
t_stat, p_t = t_test(prepared_data)
st.write(f"**T-Test**: t-statistic = {t_stat:.2f}, p-value = {p_t:.50f}")
if p_t < 0.05:
    st.write("Result: Significant difference in summary lengths based on article length (p < 0.05).")
else:
    st.write("Result: No significant difference in summary lengths based on article length (p > 0.05).")

# Z-Test
z_stat, p_z = z_test(prepared_data)
st.write(f"**Z-Test**: z-statistic = {z_stat:.2f}, p-value = {p_z:.50f}")
if p_z < 0.05:
    st.write("Result: Significant difference between article and summary lengths (p < 0.05).")
else:
    st.write("Result: No significant difference between article and summary lengths (p > 0.05).")

st.write("---")
st.write("This comprehensive analysis demonstrates the integration of multiple data science tasks in Streamlit.")
    
