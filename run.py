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
    # Get the caller's phone number from the incoming Twilio request
    from_number = request.values.get('From', None)
    resp = twilio.twiml.Response()
 
    # if the caller is someone we know:
    if from_number in callers:
        # Greet the caller by name
        user_input = 0
        resp.say("Hello " + callers[from_number]+ "Please type in the fizzbuzz sequence you want, up to 999 and press *")
        with resp.gather(numDigits=3, action="/handle-key", method="POST",finishOnKey = "*") as g:
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
        resp.dial(varun_twilio)
        # If the dial fails:
        resp.say("The call failed, or the remote party hung up. Goodbye.")
 
        return str(resp)
 
    # If the caller pressed anything but 1, redirect them to the homepage.
    else:
        return redirect("/")

def fizzbuzz(digit_in):
    output_str = ""
    for i in (0,digit_in):
        if i % 3 == 0 and i % 5 == 0:
            output_str.append('Fizz Buzz')
        elif i % 3 ==0:
            output_str.append('Fizz')
        elif i % 5 ==0:
            output_str.append('Buzz')
        else:
            output_str.append(str(i))
    return output_str


if __name__ == "__main__":
    app.run(debug=True)
