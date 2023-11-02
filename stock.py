from flask import Flask, request, render_template
import yfinance as yf
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import base64
from io import BytesIO
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    stock_symbol = request.form['stock_symbol']

    stock_data = yf.download(stock_symbol, period="30d")

    volume_today = round(stock_data['Volume'][-1], 2)

    average_volume = round(stock_data['Volume'].mean(), 2)

    fig = px.line(stock_data, x=stock_data.index, y="Close", title=f'Stock Price for {stock_symbol}')
    fig.update_layout(
        font=dict(color='white', family='Nunito'),
        paper_bgcolor='rgba(0, 0, 0, 0)', 
        xaxis=dict(showgrid=True, gridcolor='black'), 
        yaxis=dict(showgrid=True, gridcolor='black'),

    )
    graph_json = fig.to_json()

    # Analyze the trend
    recent_close_prices = stock_data['Close']
    average_price = round(recent_close_prices.mean(), 2)
    current_price = round(recent_close_prices[-1], 2)
    previous_price = round(recent_close_prices[-2], 2)

    # Additional variables for analysis
    price_change = round(current_price - previous_price, 2)
    percentage_change = round((price_change / previous_price) * 100, 2)
    advice = ""

    # Enhanced trend analysis: Consider percentage change and volume.
    if current_price > average_price and percentage_change > 0 and volume_today > average_volume:
        if current_price > average_price:
            advice += "The current stock price is above the recent 30-day average, which can be a positive sign as it indicates an upward trend in the short term.\n"

        if percentage_change > 0:
            advice += "There has been a positive percentage change in the stock price, suggesting recent price growth.\n"

        if volume_today > average_volume:
            advice += "The trading volume today is higher than the 30-day average volume, indicating increased investor interest in the stock.\n"
    else:
        if current_price <= average_price:
            advice += "The current stock price is currently trading below the recent 30-day average, which may indicate a potential downward trend in the short term.\n"

        if percentage_change <= 0:
            advice += "There has been a negative or minimal percentage change in the stock price, suggesting recent stagnation or decline.\n"

        if volume_today <= average_volume:
            advice += "The trading volume today is at or below the 30-day average volume, which may indicate decreased investor interest in the stock.\n"
    return render_template('result.html', stock_symbol=stock_symbol, graph_json=graph_json, advice=advice, average_price=average_price, current_price=current_price, price_change=price_change, percentage_change=percentage_change, volume_today=volume_today, average_volume=average_volume)




if __name__ == '__main__':
    app.run(debug=True)
