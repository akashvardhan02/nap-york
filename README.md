# Nap York GitHub Repository Dashboard - Streamlit Application


## Overview

The **GitHub Repository Dashboard** is an interactive web application built using **Streamlit**. It allows users to upload a dataset of GitHub repositories and explore various metrics like stars, forks, contributors, and language distributions through dynamic visualizations. This repository purely based on github_dataset.csv dataset 

### Key Features

- **File Upload**: Supports uploading `.csv`, `.txt`, `.xlsx` files for analysis.
- **Data Filtering**: Users can filter the dataset by programming language, repository name, contributors count, stars count, and date range.
- **Visualizations**:
  - **Bar Chart**: Stars count by language and repository.
  - **Pie Chart**: Repository distribution by programming language.
  - **Correlation Heatmap**: Analyze relationships between stars, forks, contributors, and issues.
  - **Bubble Chart**: Compare stars vs. forks with contributors as the bubble size.
  - **Treemap**: Visualize stars distribution by language and repository.
  - **Line Chart** (Optional): Stars over time.
- **Data Export**: Download the displayed data from the visualizations as CSV files.

## Installation

### Prerequisites

- Python 3.7 or higher
- Required Python libraries:
  - `streamlit`
  - `pandas`
  - `plotly`
  - `matplotlib`
  - `seaborn`

### Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repository/github-dashboard
    cd github-dashboard
    ```

2. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

## How to Use

1. **Upload Dataset**: Upload a dataset containing GitHub repository data in `.csv`, `.txt`, or `.xlsx` format.
2. **Filter Data**: Use the sidebar to filter by language, repositories, contributors count, stars, and more.
3. **Visualize Data**:
   - **Bar Chart**: Visualize stars count by language and repository.
   - **Pie Chart**: See the distribution of repositories across programming languages.
   - **Heatmap**: Check correlation between stars, forks, issues, and contributors.
   - **Bubble Chart**: Compare stars vs. forks with contributors as the bubble size.
   - **Treemap**: Shows the stars distribution across languages and repositories.
   - **Line Chart**: Stars count trends over time (if applicable).
4. **Download Data**: Use the download buttons to export filtered or chart data as CSV files.

## Dataset Requirements

For full functionality, the dataset should contain the following columns:
- **language**: Programming language of the repository.
- **repositories**: Name of the repository.
- **contributors**: Number of contributors.
- **stars_count**: Stars the repository has received.
- **forks_count**: Number of forks.
- **issues_count**: Number of issues.
- **pull_requests**: Number of pull requests.
- **created_at**: (Optional) Repository creation date for time-based analysis.

## Sample Dataset

You can use a sample dataset of GitHub repositories from Kaggle for testing:
[GitHub Repositories Dataset][(https://www.kaggle.com/)](https://www.kaggle.com/datasets/nikhil25803/github-dataset/data)

## License

This project is licensed under the MIT License.

## Contact

For questions or suggestions, feel free to contact akashvardhanadla@gmail.com
