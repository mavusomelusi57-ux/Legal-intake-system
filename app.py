from flask import Flask, render_template, request
import csv
import os
import urllib.parse

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

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('client_name')
    phone = request.form.get('client_phone')
    service = request.form.get('service_type')
    message = request.form.get('message')

    # 1. Save to your local cloud file
    with open(DB_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([name, phone, service, message])
        
    # 2. Build the pre-typed message text
    whatsapp_message = (
        f"Hello E.M. Mavuso Attorneys, I would like to book a consultation.\n\n"
        f"👤 Name: {name}\n"
        f"📞 My Phone: {phone}\n"
        f"⚖️ Service Needed: {service}\n"
        f"📝 Case Overview: {message}"
    )
    
    # 3. Format the text safely for web link rules
    encoded_message = urllib.parse.quote(whatsapp_message)
    
    # 4. Paste your real Eswatini phone number below (Include country code 268)
    YOUR_WHATSAPP_NUMBER = "26876713590"  # <-- Change this to your real number!
    
    # 5. Create the launch link
    whatsapp_link = f"https://wa.me{YOUR_WHATSAPP_NUMBER}?text={encoded_message}"
    
    # 6. Redirect the client's screen straight into WhatsApp!
    return f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="3;url={whatsapp_link}">
        <script src="https://tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-slate-100 flex items-center justify-center min-h-screen p-4 text-center">
        <div class="max-w-sm bg-slate-800 p-8 rounded-xl border border-slate-700 shadow-xl">
            <h2 class="text-xl font-bold text-amber-400 mb-2">Application Received!</h2>
            <p class="text-sm text-slate-300 mb-6">Thank you {name}. Redirecting you to secure your booking on WhatsApp...</p>
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-400 mx-auto mb-6"></div>
            <a href="{whatsapp_link}" class="bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold uppercase tracking-wider py-3 px-6 rounded-lg block">Click here if not redirected</a>
        </div>
    </body>
    </html>
if __name__ == '__main__':
    initialize_db()
    app.run(host='0.0.0.0' if os.environ.get('PORT') else '127.0.0.1', port=int(os.environ.get('PORT', 5000)), debug=True)

