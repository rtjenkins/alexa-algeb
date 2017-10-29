import logging
import time
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, audio

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_game():
    session.attributes['score'] = 0
    session.attributes['total'] = 0
    welcome_msg = render_template('welcome') #render_template looks for the templates.yaml file
    return question(welcome_msg) #return is what gets returned to Alexa, in this case the welcome message as found in the yaml template above

@ask.intent("YesIntent")
def next_round():
    score = session.attributes['score']
    total = session.attributes['total']
    number1 = randint(2,5)
    number2 = randint(2,4) 
    numberx = randint(1,5)
    number3 = number1 * numberx + number2
	
    round_msg = render_template('round', score=score, total=total, number1=number1, number2=number2, number3=number3) # calls the render template passing the numbers above to the function 
    
    session.attributes['number1'] = number1  # session attribute is a flask-ask method that keeps a variable in memory throughout the session
    session.attributes['number2'] = number2
    session.attributes['number3'] = number3  # session attribute is a flask-ask method that keeps a variable in memory throughout the session
    session.attributes['answer_number'] = numberx # assigns the correct anwser to a session attribute
    print'finished ask.intent', number1, ': ', number2, ': ', number3  # prints to console for debugging
    return question(round_msg) \
        .reprompt("What's your answer") # tells Alexa to speak the question, and if there is no response after 6 seconds to reprompt for an answer
    
@ask.intent("NoIntent")
def no_intent():
    bye_text = "Ok, Your final score is " + str(session.attributes['score']) + " out of " + str(session.attributes['total']) + "...Thanks for playing. "
    return statement(bye_text)
    session.attributes['answer_number'] = result  # assigns the correct anser to a session attribute
    print 'finished ask.intent', number1, ':', number2, ':', number3 # prints to console for debugging
    return question(round_msg) \
        .reprompt("What's your answer") # tells Alexa to speak the question, and if there is no response after 6 seconds to reprompt for an answer

@ask.intent("AnswerIntent", convert={'number': int}) #Alexa's Skillkit API always returns a string, so we have to conver it to an integer
def answer(number):
    print 'starting answer-intent', number # for debugging
    winning_number = session.attributes['answer_number'] # assign the correct answer to a new variable
    #uttered_number = session.attributes['number']
    session.attributes['total'] += 1
    if number == winning_number: # if the number the user uttered = to correct answer that read back the win message in the template
        msg = render_template('win')
        session.attributes['score'] += 1
    else:
        msg = render_template('lose') # else read the lose message
    return question(msg)

if __name__ == '__main__':
    app.run(debug=True) #standard flask method to begin listening on port 5000 (flask's default port)
	
	