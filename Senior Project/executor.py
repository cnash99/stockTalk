from flask import Flask, redirect, url_for, request, render_template, request
from threading import Thread
import stockTalk
import express
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

@app.route('/home')
def home():
   stockSymbols = stockTalk.getSymbols()
   return render_template('gui.html', stockSymbols = stockSymbols)

@app.route('/data/<name>')
def data(name):
    d = stockTalk.run(name)
    return render_template('dataScreen.html', company=d['company'], currentPrice = d['currentPrice'], totalVolume = d['totalVolume'], percentPos = d['percentPos'], percentNeg = d['percentNeg'], first = d['first'], second = d['second'], third = d['third'], fourth = d['fourth'], fifth = d['fifth'], sixth = d['sixth'], seventh = d['seventh'], advice = d['advice'], displayTweets1 = d['displayTweets1'], displayTweets2 = d['displayTweets2'], displayTweets3 = d['displayTweets3'], displayTweets4 = d['displayTweets4'], displayTweets5 = d['displayTweets5'], displayTweets6 = d['displayTweets6'], displayTweets7 = d['displayTweets7'], displayTweets8 = d['displayTweets8'], displayTweets9 = d['displayTweets9'], displayTweets10 = d['displayTweets10'])

@app.route('/about')
def about():
   return render_template('about.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('data',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('data',name = user))

if __name__ == '__main__':
   app.run(debug = True)
   