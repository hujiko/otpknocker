import pyotp
import os
from flask import Flask, render_template, request, redirect, Response

app  = Flask(__name__, template_folder='html')
totp = pyotp.TOTP(os.environ['OTP_SECRET'])


@app.route('/')
def input():
  return render_template('input.html')

@app.route('/verify', methods = ['POST'])
def verify():
  entered_token = str(request.form.get('otp'))

  if totp.verify(entered_token):
    resp = Response("ok")
    resp.headers['Authentication-Success'] = 'true'
    return resp
  else:
    return redirect("/", code=302)

@app.route('/static/<path:path>')
def send_report(path):
    return send_from_directory('sdf', path)
