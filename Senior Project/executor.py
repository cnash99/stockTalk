from flask import Flask, redirect, url_for, request, render_template, request
import stockTalk
import express
app = Flask(import_name = __name__, static_folder='file:///Users/charlienash/stockTalk')

@app.route('/success/<name>')
def success(name):
    d = stockTalk.run(name)
    return render_template('dataScreen.html', company=d['company'], currentPrice = d['currentPrice'], totalVolume = d['totalVolume'], percentPos = d['percentPos'], percentNeg = d['percentNeg'], first = d['first'], second = d['second'], third = d['third'], fourth = d['fourth'], fifth = d['fifth'], sixth = d['sixth'], seventh = d['seventh'], advice = d['advice'])

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

if __name__ == '__main__':
   app.run(debug = True)
   