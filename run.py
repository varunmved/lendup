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
    with resp.gather(numDigits=2, action="/handle-key", method="POST") as g:
        g.say("To play fizz buzz, please enter a 2 digit number")
 
    return str(resp)
 
@app.route("/handle-key", methods=['GET', 'POST'])
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
    else:
        # If the dial fails:
        resp.say("The call failed, or the remote party hung up. Goodbye.")
        return redirect("/")

@app.route("/handle-fizzbuzz/<fizzbuzzInt>",methods=['GET','POST'])
def handle_fizzbuzz(fizzbuzzInt):
    """Handles fizzbuzz"""

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
