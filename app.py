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

if __name__ == '__main__':
    initialize_db()
    app.run(host='0.0.0.0' if os.environ.get('PORT') else '127.0.0.1', port=int(os.environ.get('PORT', 5000)), debug=True)

