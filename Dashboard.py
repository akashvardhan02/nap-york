import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')

# Streamlit config
st.set_page_config(page_title="GitHub Repository Dashboard", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart: GitHub Repository Dashboard")

# File uploader
fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(f"Uploaded file: {filename}")
    
    # Handling CSV tokenization issues
    try:
        df = pd.read_csv(fl, delimiter=',', encoding="ISO-8859-1", on_bad_lines='skip')
    except pd.errors.ParserError as e:
        st.error(f"Error reading CSV file: {str(e)}")
        st.stop()
else:
    os.chdir(r"C:\Users\akash\OneDrive\Desktop\dashboard\project")
    df = pd.read_csv("github_dataset.csv", encoding="ISO-8859-1", on_bad_lines='skip')

# Ensure necessary columns exist
if 'language' in df.columns and 'repositories' in df.columns and 'contributors' in df.columns:
    # Drop rows with NaN values in required columns
    df = df.dropna(subset=['language', 'repositories', 'contributors'])

    # Sidebar Filters
    st.sidebar.header("Filter the data: ")

    # Language filter
    language = st.sidebar.multiselect("Pick your language", df["language"].unique())
    
    # Repositories filter
    repositories = st.sidebar.multiselect("Pick the repository", df["repositories"].unique())
    
    # Contributors filter
    contributors = st.sidebar.multiselect("Pick the contributors count", df["contributors"].unique())
    
    # Stars Count Filter
    min_stars = st.sidebar.number_input("Minimum Stars Count", min_value=0, value=0)
    max_stars = st.sidebar.number_input("Maximum Stars Count", min_value=0, value=df["stars_count"].max())

    # Date Filter (if you have a 'created_at' column)
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'])
        min_date = st.sidebar.date_input("Start Date", df['created_at'].min())
        max_date = st.sidebar.date_input("End Date", df['created_at'].max())
    else:
        min_date, max_date = None, None

    # Filter DataFrame based on selections
    df_filtered = df.copy()
    
    if language:
        df_filtered = df_filtered[df_filtered["language"].isin(language)]
    
    if repositories:
        df_filtered = df_filtered[df_filtered["repositories"].isin(repositories)]
    
    if contributors:
        df_filtered = df_filtered[df_filtered["contributors"].isin(contributors)]
    
    # Apply stars count filter
    df_filtered = df_filtered[(df_filtered["stars_count"] >= min_stars) & (df_filtered["stars_count"] <= max_stars)]
    
    # Apply date filter
    if min_date and max_date:
        df_filtered = df_filtered[(df_filtered['created_at'] >= pd.Timestamp(min_date)) & (df_filtered['created_at'] <= pd.Timestamp(max_date))]

    # Grouped data for analysis
    category_df = df_filtered.groupby(by=["language", "repositories"], as_index=False)["stars_count"].sum()

    # Display filtered data and grouped data
    st.write("Filtered Data:")
    st.write(df_filtered)  # Display the filtered dataframe
    st.write("Grouped Data:")
    st.write(category_df)  # Display the grouped dataframe

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Stars Count by Language and Repository")
        fig1 = px.bar(category_df, x="repositories", y="stars_count", color="language", text=['{:.2f}'.format(x) for x in category_df["stars_count"]], template="seaborn")
        st.plotly_chart(fig1, use_container_width=True)

        # Download button for Stars Count by Language and Repository
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Stars Count Data", data=csv, file_name="stars_count_by_language_repository.csv", mime="text/csv", help="Download the stars count data")

    # Updated Pie Chart: Distribution of Programming Languages
    with col2:
        st.subheader("Distribution of Programming Languages (by Repositories)")
        language_distribution = df.groupby("language")["repositories"].count().reset_index().rename(columns={"repositories": "repository_count"})
        fig2 = px.pie(language_distribution, values="repository_count", names="language", hole=0.5, title="Repository Distribution by Language")
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)

        # Download button for Language Distribution Pie Chart
        csv = language_distribution.to_csv(index=False).encode('utf-8')
        st.download_button("Download Language Distribution Data", data=csv, file_name="language_distribution.csv", mime="text/csv", help="Download the language distribution data")

    # Heatmap for correlation analysis
    st.subheader("Correlation Heatmap")
    corr_matrix = df_filtered[['stars_count', 'forks_count', 'issues_count', 'pull_requests', 'contributors']].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    # Download button for Heatmap correlation data
    corr_csv = corr_matrix.to_csv().encode('utf-8')
    st.download_button("Download Correlation Data", data=corr_csv, file_name="correlation_data.csv", mime="text/csv", help="Download the correlation data")

    # Bubble Chart: Stars vs Forks with Contributors as Size
    st.subheader("Stars vs Forks with Contributors as Bubble Size")
    fig3 = px.scatter(df_filtered, x='stars_count', y='forks_count', size='contributors', color='language', title="Stars vs Forks",
                     hover_name='repositories', log_x=True, size_max=60)
    st.plotly_chart(fig3, use_container_width=True)

    # Download button for Bubble chart data
    bubble_data = df_filtered[['stars_count', 'forks_count', 'contributors', 'language']].to_csv(index=False).encode('utf-8')
    st.download_button("Download Bubble Chart Data", data=bubble_data, file_name="bubble_chart_data.csv", mime="text/csv", help="Download the bubble chart data")

    # Treemap for stars distribution by language and repository
    st.subheader("Treemap of Stars by Language and Repository")
    fig4 = px.treemap(df_filtered, path=['language', 'repositories'], values='stars_count', title="Stars Distribution by Language and Repositories")
    st.plotly_chart(fig4, use_container_width=True)

    # Download button for Treemap data
    treemap_data = df_filtered[['language', 'repositories', 'stars_count']].to_csv(index=False).encode('utf-8')
    st.download_button("Download Treemap Data", data=treemap_data, file_name="treemap_data.csv", mime="text/csv", help="Download the treemap data")

    # Additional Chart: Contributors by Language
    st.subheader("Contributors per Language")
    contributors_chart = df_filtered.groupby("language")["contributors"].sum().reset_index()
    fig5 = px.bar(contributors_chart, x="language", y="contributors", title="Total Contributors per Language", template="plotly_white")
    st.plotly_chart(fig5, use_container_width=True)

    # Download button for Contributors per Language
    contributors_csv = contributors_chart.to_csv(index=False).encode('utf-8')
    st.download_button("Download Contributors Data", data=contributors_csv, file_name="contributors_by_language.csv", mime="text/csv", help="Download the contributors data")

    # Line Chart: Stars Over Time (assuming you have a 'created_at' column)
    if 'created_at' in df.columns:
        st.subheader("Stars Over Time")
        stars_over_time = df_filtered.groupby(df_filtered['created_at'].dt.to_period('M'))['stars_count'].sum().reset_index()
        fig6 = px.line(stars_over_time, x='created_at', y='stars_count', title='Stars Over Time')
        st.plotly_chart(fig6, use_container_width=True)

        # Download button for Stars Over Time data
        stars_time_csv = stars_over_time.to_csv(index=False).encode('utf-8')
        st.download_button("Download Stars Over Time Data", data=stars_time_csv, file_name="stars_over_time.csv", mime="text/csv", help="Download the stars over time data")
else:
    st.error("The required columns are not available in the dataset.")
