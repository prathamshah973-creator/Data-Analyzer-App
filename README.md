Automated EDA Expert System
Overview
The Automated EDA Expert System is a full-stack data engineering web application built with Python and Flask. It is designed to automate the unglamorous groundwork of Exploratory Data Analysis (EDA) and dirty data wrangling.

Users can upload raw structured datasets (.csv or .xlsx), and the Flask backend routes the data through a Pandas processing engine. The application physically reads the mathematical shape of the data and generates automated, actionable engineering solutions.

🔗 Live Demo: https://data-analyzer-app-f4rb.onrender.com

🚀 Core Features & Heuristics
Rather than just printing raw numbers, this application acts as an expert system by evaluating the dataset against machine learning prerequisites:

Missing Data Imputation: Flags missing values and recommends dropping severe columns (>40% missing) or applying Median Imputation.

IQR Outlier Detection: Calculates the 25th and 75th percentiles to flag anomalies outside the 1.5 * IQR boundaries, recommending RobustScaler when necessary.

Scale Variance Monitoring: Detects massive numerical imbalances between features, alerting the user to enforce StandardScaler for distance-based algorithms like KNN.

Cardinality Checks: Identifies high-cardinality text columns (like IDs or names) that would cause algorithmic overfitting.

Dynamic Visualizations: Generates background plots using matplotlib and passes them to the frontend via Base64 encoding—no file saving required.

🛠️ Tech Stack
Backend: Python, Flask, Gunicorn
Data Engine: Pandas, OpenPyXL, Scikit-Learn logic
Visualization: Matplotlib
Frontend: HTML5, CSS3, Bootstrap 5
CI/CD & Hosting: GitHub, Render
