import qr_code_scan
import event_generator_calender
import mail
from flask import Flask
from flask import request

# app = Flask(__name__)

# @app.route('/qr_scan')

def qr_scanner():
    qr_code_scan.scan_code()
    event_generator_calender.generate_ics()
    mail.send_email()


if __name__ == '__main__':
    # app.run()
    qr_scanner()

    
