from flask import Flask, request, redirect,flash, render_template
from flask.ext.wtf import Form
from twilio.rest import TwilioRestClient
import twilio.twiml
from wtforms import TextField
from flask import jsonify
from wtforms.validators import Required, Length, ValidationError
import os
import re
 
app = Flask(__name__)
 
# Try adding your own number to this list!
callers = {
    "+14158675309": "Curious George",
    "+14158675310": "Boots",
    "+14158675311": "Virgil",
    "+19167516308": "Varun",
    "+19164762325": "VarunTwilio"


}
url = "https://tranquil-savannah-8709.herokuapp.com"
varun_number_twilio = "+19164762325"
varun_number_verizon = "+19167516308"
'''
utils
'''
def call(numIn):
    resp = twilio.twiml.Response()
    # Get these credentials from http://twilio.com/user/account
    # This is copy pasta, I swear I usually put ID/AUTH as a enviorment variable on heroku
    account_sid = "AC1cc3d40a4dca1cd0ff1af031ff1b14ca"
    auth_token = "5011a96781ef26d63904ca3b8e3ccb35"
    client = TwilioRestClient(account_sid, auth_token)
 
    # Make the call
    call = client.calls.create(to=varun_number_twilio,  # Any phone number
                           from_=varun_number_verizon, # Must be a valid Twilio number
                           url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")
    print call.sid

    return "called"

def fizzbuzz(digit_in):
    output_str = ""
    for i in range (0,digit_in):
        if i % 3 == 0 and i % 5 == 0:
            output_str+=(' Fizz Buzz ')
        elif i % 3 ==0:
            output_str+=(' Fizz ')
        elif i % 5 ==0:
            output_str+=(' Buzz ')
        else:
            output_str+=(' '+str(i) + ' ')
    return output_str


def startsWithPlus(form, phone_num):
  p = re.compile("^\+")
  if p.match(phone_num.data) == None:
    raise ValidationError('Phone number should start with a plus.')

def containsDigits(form, phone_num):
  p = re.compile('\+?\d{1,15}')
  if p.match(phone_num.data) == None:
    raise ValidationError('Phone number should only contain upto 15 digits.')


'''
classes
'''
class MyForm(Form):
  call_failed = False
  phone_num = TextField('phone_num', validators=[Required(), Length(min=1, max=16),startsWithPlus, containsDigits])

'''
routes
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
        '''
        with resp.gather(numDigits=3, action="/handle-fizzbuzz", method="POST", finishOnKey= "*") as g:
            hello  = fizzbuzz(int(g))
        '''
        fizzBuzzString = fizzbuzz(rawVal)
        resp.say(fizzBuzzString)
        return str(resp)
        #return render_template('template.html',name=name)
    else:
        # If the dial fails:
        resp.say("The call failed, or the remote party hung up. Goodbye.")
        return redirect("/")

'''
frontend routes
'''
'''
@app.route("/view")
def my_form():
    return render_template("my-form.html")

@app.route("/view",methods = ['GET','POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    #if processed_text[:1] == "+1" and len(processed_text == 12):
        #print("ayy lmao")
    call(processed_text)
    return my_form()
'''

@app.route("/views", methods=['GET', 'POST'])
def outbound_call_initiate(call_failed=False):
  resp = twilio.twiml.Response()
  form = MyForm(request.form, call_failed=call_failed, csrf_enabled = False)
  if form.validate_on_submit():
      return call(form.data['phone_num'])
  return render_template('form.html',
        title = 'Enter A Phone Number',
        form = form)

if __name__ == "__main__":
    app.run(debug=True) 
