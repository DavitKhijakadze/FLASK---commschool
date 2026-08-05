from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    trading_pairs = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'BTC/USD']
    return render_template('home.html', pairs=trading_pairs)

@app.route('/about')
def about():
    strategies = [
        {'name': 'Day Trading', 'risk': 'მაღალი', 'timeframe': 'M15 / H1'},
        {'name': 'Swing Trading', 'risk': 'საშუალო', 'timeframe': 'H4 / Daily'},
        {'name': 'Scalping', 'risk': 'ძალიან მაღალი', 'timeframe': 'M1 / M5'}
    ]
    return render_template('about.html', strategies=strategies)

@app.route('/contact')
def contact():
    is_market_open = True
    return render_template('contact.html', market_open=is_market_open)

if __name__ == '__main__':
    app.run(debug=True)