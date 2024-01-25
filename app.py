from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from validate_email_address import validate_email
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Gmail account credentials
gmail_user = "miggzc1@gmail.com"
gmail_password = "deos wxeq gmji ynfp"

# Route to handle form submissions from React frontend
@app.route('/submit-form', methods=['POST'])
def receive_form():
    try:
        # Receive form data from React frontend
        data = request.json
        name = data['name']
        email = data['email']
        message = data['message']

        # Validate email address
        if not validate_email(email):
            return jsonify({'message': 'Invalid email address'}), 400

        # Send email
        sender_email = email
        receiver_email = gmail_user

        msg = MIMEMultipart()   
        msg['From'] = sender_email  # Set sender's email dynamically
        msg['To'] = receiver_email
        msg['Subject'] = 'MetroBreathe Email'

        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(gmail_user, gmail_password)
            smtp.sendmail(sender_email, receiver_email, msg.as_string())

        return jsonify({'message': 'Form received and processed successfully'}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
