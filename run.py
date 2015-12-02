'''
from flask import Flask, request, redirect,flash, render_template
from flask.ext.wtf import Form
from twilio.rest import TwilioRestClient
import twilio.twiml
from wtforms import TextField
from flask import jsonify
from wtforms.validators import Required, Length, ValidationError
import os
'''
from flask import Flask
import flask.ext.wtf
import wtforms
from twilio.rest import TwilioRestClient
import twilio.twiml
import os

app = Flask(__name__)

'''
consts
'''
# Try adding your own number to this list!
callers = {
    "+14158675309": "Curious George",
    "+14158675310": "Boots",
    "+14158675311": "Virgil",
    "+19167516308": "Varun",
    "+19164762325": "VarunTwilio"
}

urlHeroku = "https://tranquil-savannah-8709.herokuapp.com"
varun_number_twilio = "+19164762325"
varun_number_verizon = "+19167516308"

'''
utils
'''
def call(numIn):
    resp = twilio.twiml.Response()
    # Get these credentials from http://twilio.com/user/account
    account_sid = os.getenv(TWILIO_USER,default_value)
    auth_token = os.getenv(TWILIO_SECRET,default_value)
    client = TwilioRestClient(account_sid, auth_token)

    # Make the call
    call = client.calls.create(to=numIn,  # Any phone number
                           from_=varun_number_twilio, # Must be a valid Twilio number
                           url=urlHeroku)
    print call.sid
    return "called"

def fizzbuzz(fizzBuzzCalcValue):
    output_str = ""
    for i in range (0,fizzBuzzCalcValue):
        if i % 3 == 0 and i % 5 == 0:
            output_str+=(' Fizz Buzz ')
        elif i % 3 ==0:
            output_str+=(' Fizz ')
        elif i % 5 ==0:
            output_str+=(' Buzz ')
        else:
            output_str+=(' '+str(i) + ' ')
    return output_str


def isValid(form, phoneNumber):
  rawTextField = str(phoneNumber)
  valueDesiredString = "value="
  valueIndex = rawTextField.index(valueDesiredString) +6
  numStr = rawTextField[valueIndex:len(rawTextField)-1]
  numStr = (numStr[1:13])
  print(numStr)
  print(len(numStr))
  if len(numStr)!= 12 or numStr[0] != "+" or not str.isdigit(numStr[1:13]):
      raise ValidationError("Your phone number isn't a valid US/Canada number")

'''
classes
'''
class MyForm(Form):
  failedCall = False
  phoneNumber = TextField('phoneNumber', validators=[Required(), Length(min=12, max=12),isValid])

'''
twilio routes
'''
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    from_number = request.values.get('From', None)
    if from_number in callers:
        caller = callers[from_number]
    else:
        caller = "Monkey"

    resp = twilio.twiml.Response()
    # Greet the caller by name
    resp.say("Hello " + caller)

    # Say a command, and listen for the caller to press a key. When they press
    # a key, redirect them to /handle-key.
    with resp.gather(numDigits=2, action="/handle-key", method="POST") as g:
        g.say("To play fizz buzz, please enter a 2 digit number")

    return str(resp)
    #return render_template('template.html')

@app.route("/handle-key/", methods=['GET', 'POST'])
def handle_key():
    """Handle key press from a user."""

    # Get the digit pressed by the user
    digit_pressed = request.values.get('Digits', None)
    if digit_pressed.isdigit():
        rawVal = int(digit_pressed)
        resp = twilio.twiml.Response()
        fizzBuzzString = fizzbuzz(rawVal)
        resp.say(fizzBuzzString)
        return str(resp)
    else:
        # If the dial fails:
        resp.say("The call failed, or the remote party hung up. Goodbye.")
        return redirect("/")

'''
frontend routes
'''
@app.route("/views/", methods=['GET', 'POST'])
def callRoute(failedCall=False):
  form = MyForm(request.form, failedCall=failedCall, csrf_enabled = False)
  resp = twilio.twiml.Response()
  if form.validate_on_submit():
      return call(form.data['phoneNumber'])
  return render_template('form.html',
        title = 'Enter A Phone Number',
        form = form)

if __name__ == "__main__":
    app.run(debug=True)
