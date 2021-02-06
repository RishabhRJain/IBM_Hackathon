import qr_code_scan
import event_generator_calender
import mail
from flask import Flask
from flask import request
import json
from flask import request

app = Flask(__name__)

@app.route('/qr_scan')

def qr_scanner():
    # email = request.args.get('email')
    qr_code_scan.scan_code()
    ingredients = event_generator_calender.generate_ics()
    mail.send_email()

    data = {'message': 'QR Scan successful. We have sent you the reminder and recipes on your email. Please check your inbox.'}
    json_data = json.dumps(data)
    return json_data

if __name__ == '__main__':
    app.run()
    # qr_scanner()