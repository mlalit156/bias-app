from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)

# Temporary upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Attendance marks function (same as your JS)
def calculate_attendance_marks(percent):
    if percent >= 90:
        return 10
    elif percent >= 85:
        return 9
    elif percent >= 80:
        return 8
    elif percent >= 75:
        return 7
    else:
        return 6

# Assignment marks function (same as your JS)
def calculate_assignment_marks(count):
    if count >= 5:
        return 10
    elif count == 4:
        return 8
    elif 1 <= count <= 3:
        return 6
    else:
        return 0

# Total marks calculation
def calculate_total_marks(sess1, sess2, attendance_percent, assignment_count):
    total_sess = sess1 + sess2
    if total_sess > 30:  # Cap sessional at 30
        total_sess = 30
    attendance_marks = calculate_attendance_marks(attendance_percent)
    assignment_marks = calculate_assignment_marks(assignment_count)
    total = total_sess + attendance_marks + assignment_marks
    return total

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return "No file uploaded!"
    file = request.files['file']
    if file.filename == '':
        return "No file selected!"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Read Excel file
    df = pd.read_excel(filepath)

    # Check required columns
    required_cols = ['Roll No','Name','Session1','Session2','Attendance','Assignments']
    for col in required_cols:
        if col not in df.columns:
            return f"Missing column: {col}"

    # Apply the JS logic for each row
    df['Total'] = df.apply(lambda r: calculate_total_marks(
        r['Session1'], r['Session2'], r['Attendance'], r['Assignments']), axis=1)

    df['Processed'] = 'Yes'

    # Save processed file
    output_path = os.path.join(UPLOAD_FOLDER, 'processed_' + file.filename)
    df.to_excel(output_path, index=False)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
