from flask import Flask, render_template, request, send_file, flash,abort,Response
import pandas as pd
# import numpy as np
# import os
from ydata_profiling import ProfileReport
import io


app = Flask(__name__)

# Set the maximum file size to 5MB (5 * 1024 * 1024 bytes)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

##reports generating about of dataset function
report_html = None
@app.route("/", methods=['GET', 'POST'])
# Initialize report_html as a global variable
def generate_and_display_profile():
    global report_html  # Use the global report_html variable
    profile = None
    report_generated = False  # Add a variable to track report generation

    if request.method == 'POST':
        if 'csvFile' not in request.files:
            return "No file part"

        file = request.files['csvFile']

        if file.filename == '':
            return "No selected file"

        if not file.filename.endswith('.csv'):
            return "Invalid file format. Please upload a CSV file."

        # Check the file size
        if file.content_length > app.config['MAX_CONTENT_LENGTH']:
            return "File size exceeds the limit of 5MB."

        df = pd.read_csv(file)
        # Create a Pandas Profiling Report
        profile = ProfileReport(df, title="DataSet's Report")

        # Convert the report to HTML as a string
        report_html = profile.to_html()
        report_generated = True  # Set report_generated to True when the report is generated

        if report_html:
            # Option 1: Render the report HTML
            return render_template("generated_report.html", report_html=report_html, report_generated=report_generated)
    else:
        # Option 2: Provide a download link for the generated report
        return render_template('datasets_report.html')


@app.route('/download_report')
def download_report():
    global report_html  # Use the global report_html variable
    if report_html is not None:
        # Create an in-memory file object to store the HTML content
        report_file = io.BytesIO()
        report_file.write(report_html.encode('utf-8'))
        report_file.seek(0)

        # Return the HTML file as an attachment for download
        return send_file(report_file, as_attachment=True, download_name='report.html')

    return "Report not found"


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
