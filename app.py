from flask import Flask, render_template, request
import pandas as pd
import matplotlib
matplotlib.use('Agg') # Required to generate graphs in the background of a web server
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        uploaded_file = request.files['dataset'] 
        filename = uploaded_file.filename
        
        if filename != '':
            try:
                # 1. Read the Data
                if filename.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                elif filename.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(uploaded_file)
                elif filename.endswith('.pdf'):
                    return render_template('index.html', error_msg="PDF table extraction is currently in the development roadmap!")
                else:
                    return render_template('index.html', error_msg="Unsupported file format. Please upload CSV or Excel.")

                # 2. Statistical Parameters & Dirty Data Analysis
                row_count, col_count = df.shape
                missing_values = df.isnull().sum()
                total_missing = missing_values.sum()
                
                # Filter for numeric columns to do mathematical checks (and silence the Pandas warning!)
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                cat_cols = df.select_dtypes(exclude=['float64', 'int64']).columns
                
                # Generate a statistical summary table for numeric columns
                if len(numeric_cols) > 0:
                    stats_html = df[numeric_cols].describe().to_html(classes="table table-striped table-hover", border=0)
                else:
                    stats_html = "<p class='text-muted'>No numeric columns available for statistical summary.</p>"

                # 3. Generate Strategic Insights / Solutions (The "Expert System")
                insights = []
                
                # A. Missing Data Solutions
                if total_missing == 0:
                    insights.append("✅ Data Completeness: The dataset has no missing values. It is structurally intact.")
                else:
                    for col, missing in missing_values.items():
                        if missing > 0:
                            missing_percent = (missing / row_count) * 100
                            if missing_percent > 40:
                                insights.append(f"❌ Severe Missing Data: '{col}' is missing {missing_percent:.1f}% of its data. Solution: Drop this column completely.")
                            else:
                                insights.append(f"⚠️ Minor Missing Data: '{col}' is missing {missing} values. Solution: Apply Median Imputation.")

                # B. Outlier Detection (Using IQR)
                for col in numeric_cols:
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
                    
                    if outliers > 0:
                        outlier_percent = (outliers / row_count) * 100
                        if outlier_percent > 5:
                            insights.append(f"⚠️ Extreme Outliers Detected: '{col}' contains {outliers} anomalies ({outlier_percent:.1f}% of data). Solution: Use RobustScaler or cap anomalies.")

                # C. Feature Scaling Solutions
                if len(numeric_cols) > 1:
                    max_vals = df[numeric_cols].max()
                    if max_vals.max() > (max_vals.median() * 100):
                        insights.append("⚖️ Scale Variance Warning: Features have drastically different numerical ranges. Solution: You must apply StandardScaler before feeding this data into distance-based models.")
                
                # D. Categorical Data Solutions
                for col in cat_cols:
                    unique_count = df[col].nunique()
                    if unique_count > (row_count * 0.5) and row_count > 10:
                        insights.append(f"🗑️ High Cardinality: The text column '{col}' has too many unique values ({unique_count}). Solution: Drop it before model training to prevent overfitting.")

                # 4. Generate a Graph (ONLY if missing data exists)
                graph_url = None
                if total_missing > 0:
                    plt.figure(figsize=(8, 4))
                    missing_values[missing_values > 0].plot(kind='bar', color='tomato')
                    plt.title("Missing Values per Feature (Dirty Data Audit)")
                    plt.ylabel("Number of Missing Values")
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()

                    img = io.BytesIO()
                    plt.savefig(img, format='png')
                    img.seek(0)
                    graph_url = base64.b64encode(img.getvalue()).decode('utf8')
                    plt.close()

                return render_template('index.html', 
                                       success=True,
                                       filename=filename,
                                       rows=row_count, 
                                       cols=col_count,
                                       missing=total_missing,
                                       stats_table=stats_html,
                                       insights=insights,
                                       graph_url=graph_url)

            except Exception as e:
                return render_template('index.html', error_msg=f"An error occurred: {str(e)}")
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)