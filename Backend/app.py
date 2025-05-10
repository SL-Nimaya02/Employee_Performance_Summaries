from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_service import generate_summary
import csv
import io

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Welcome to the AI Employee Summary API!'

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)
        employees = list(reader)

        summaries = []
        for employee in employees:
            try:
                summary = generate_summary(employee)
            except Exception as inner_e:
                summary = f"Error generating summary: {str(inner_e)}"

            summaries.append({
                "Employee ID": employee.get("Employee ID"),
                "Employee Name": employee.get("Employee Name"),
                "Summary": summary
            })

        return jsonify(summaries), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
