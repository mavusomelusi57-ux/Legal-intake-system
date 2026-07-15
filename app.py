from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/google8ac4eb74c3700bb7.html', methods=['GET'])
def google_verify():
    return "google-site-verification: google8ac4eb74c3700bb7.html"

if __name__ == '__main__':
    app.run(host='0.0.0.0' if os.environ.get('PORT') else '127.0.0.1', port=int(os.environ.get('PORT', 5000)), debug=True)
