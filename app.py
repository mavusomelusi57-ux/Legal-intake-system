from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)
DB_FILE = 'consultations.csv'

def initialize_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Client Name', 'Phone Number', 'Service Needed', 'Message'])

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('client_name')
    phone = request.form.get('client_phone')
    service = request.form.get('service_type')
    message = request.form.get('message')

    with open(DB_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([name, phone, service, message])
        
    return f"Thank you, {name}. Your consultation request for {service} has been received. E.M. Mavuso Attorneys will contact you shortly."

@app.route('/view-consultations', methods=['GET'])
def view_consultations():
    data = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader, None)  # Skip the header row
            for row in reader:
                if row:  # Make sure the row isn't empty
                    data.append(row)
    
    # Generate a quick, clean HTML table to look at the data
    html_output = "<h2>Submitted Client Consultations</h2><table border='1' cellpadding='10'>"
    html_output += "<tr><th>Name</th><th>Phone</th><th>Service</th><th>Message</th></tr>"
    for row in data:
        html_output += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
    html_output += "</table><br><a href='/'>Back to Home</a>"
    
    return html_output

if __name__ == '__main__':
    initialize_db()
    app.run(host='0.0.0.0' if os.environ.get('PORT') else '127.0.0.1', port=int(os.environ.get('PORT', 5000)), debug=True)

