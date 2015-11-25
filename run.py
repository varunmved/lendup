from flask import Flask, request, redirect
import twilio.twiml
import os
 
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
    with resp.gather(numDigits=1, action="/handle-key", method="POST") as g:
        g.say("To play fizz buzz, press 1. Press any other key to start over.")
 
    return str(resp)
 
@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
    """Handle key press from a user."""
 
    # Get the digit pressed by the user
    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == "1":
        resp = twilio.twiml.Response()
        # Dial (310) 555-1212 - connect that number to the incoming caller.
        #resp.dial("+13105551212")
        with resp.gather(numDigits=3, action="/handle-key", method="POST", finishOnKey= "*") as g:
            hello  = fizzbuzz(int(g))
        # If the dial fails:
        
        resp.say("The call failed, or the remote party hung up. Goodbye.")
        
 
        return str(hello)
 
    # If the caller pressed anything but 1, redirect them to the homepage.
    else:
        return redirect("/")
'''
@app.route("/handle-fizzbuzz",methods=['GET','POST'])
def handle_fizzbuzz():
    """Handles fizzbuzz"""
'''
'''
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    # Get the caller's phone number from the incoming Twilio request
    from_number = request.values.get('From', None)
    resp = twilio.twiml.Response()
 
    # if the caller is someone we know:
    if from_number in callers:
        # Greet the caller by name
        user_input = 0
        resp.say("Hello " + callers[from_number]+ "Please type in the fizzbuzz sequence you want, up to 999 and press *")
        with resp.gather(action="/handle-key", method="POST",finishOnKey = "*") as g:
            g.say("To speak to a real monkey, press 1. Press any other key to start over.")
    
    else:
        resp.say("Hello Monkey")
 
    return str(resp)

@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
    """Handle key press from a user."""
 
    # Get the digit pressed by the user
    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == "*":
        resp = twilio.twiml.Response()
        # Dial (310) 555-1212 - connect that number to the incoming caller.
        #resp.dial(varun_twilio)
        # If the dial fails:
        resp.say("The call failed, or the remote party hung up. Goodbye.")
 
        return str(resp)
    # If the caller pressed anything but 1, redirect them to the homepage.
    else:
        return redirect("/")
   
    num_in = request.values.get('Digits',None)
    out = fizzbuzz(num_in)
    resp = twilio.twiml.Response()
    resp.say(out)
    return redirect("/")
  
'''
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


if __name__ == "__main__":
    app.run(debug=True) 
