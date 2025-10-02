from flask import Flask, request, render_template, send_file
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Save uploaded file
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Read Excel
            df = pd.read_excel(filepath)

            # Calculate Attendance marks
            def attendance_marks(att):
                if att >= 90: return 10
                elif att >= 85: return 9
                elif att >= 80: return 8
                elif att >= 75: return 7
                else: return 6

            # Calculate Assignment marks
            def assignment_marks(assign):
                if assign == 5: return 10
                elif assign == 4: return 8
                elif assign in [1,2,3]: return 6
                else: return 0

            df['Attendance Marks'] = df['Attendance'].apply(attendance_marks)
            df['Assignment Marks'] = df['Assignments'].apply(assignment_marks)
            df['Total Marks'] = df['Session1'] + df['Session2'] + df['Attendance Marks'] + df['Assignment Marks']

            # Save processed file
            output_path = os.path.join(PROCESSED_FOLDER, 'Final_Marks.xlsx')
            df.to_excel(output_path, index=False)

            # Send file to user
            return send_file(output_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
