import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import urllib.request

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

url = 'https://raw.githubusercontent.com/OxHobbs/words/master/words.txt'
spelling_words = urllib.request.urlopen(url).read().strip().decode().split("\n")


def remove_word(words_list, word):
    words_list.remove(word)


def get_word():
    if len(spelling_words) == 0:
        return None
    index = randint(0, len(spelling_words) - 1)
    word = spelling_words[index]
    remove_word(spelling_words, word)
    return word


@ask.launch
def new_game():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent('YesIntent')
def next_round():
    # spelling_words = urllib.request.urlopen(url).read().strip().decode().split("\n")
    # session.attributes['spelling_words'] = spelling_words
    word = get_word()
    session.attributes['word'] = word
    round_msg = render_template('round', word=word)
    return question(round_msg)


@ask.intent('SkipIntent')
def skip_intent():
    return next_round()


@ask.intent('NoIntent')
def no_intent():
    return statement(render_template('no_play'))


@ask.intent('SpellingIntent')
def answer(spelling):
    word = session.attributes['word']
    if spelling.replace('.', '').lower() == word.lower():
        msg = render_template('win')
    else:
        msg = render_template('lose')

    new_word = get_word()
    if not new_word:
        return statement(render_template('thanks'))

    session.attributes['word'] = new_word
    round_msg = render_template('round', word=new_word)    
    full_msg = msg + "... " + round_msg
    return question(full_msg)


@ask.intent('AMAZON.CancelIntent')
def cancel_intent():
    cancel_msg = render_template('cancel')
    return statement(cancel_msg)


@ask.intent('AMAZON.StopIntent')
def stop_intent():
    return statement('Goodbye')


if __name__ == '__main__':
    app.run(debug=True)
