from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)

# Folder to temporarily store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    # Save uploaded file temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Read Excel
    df = pd.read_excel(file_path)
    
    # Calculate total marks
    required_columns = ['Session1', 'Session2', 'Attendance', 'Assignments']
    if all(col in df.columns for col in required_columns):
        df['Total'] = df['Session1'] + df['Session2'] + df['Attendance'] + df['Assignments']
    else:
        df['Total'] = 'Columns missing'
    
    # Add Processed column
    df['Processed'] = 'Yes'
    
    # Save processed file
    output_path = os.path.join(UPLOAD_FOLDER, 'processed_' + file.filename)
    df.to_excel(output_path, index=False)
    
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
