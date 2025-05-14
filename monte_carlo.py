from model import black_scholes, implied_volatility
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
today = datetime.today()

"""
    S: Current stock price
    K: Strike price
    T: Time to maturity in years
    r: Risk-free interest rate (annualised)
    sigma: Volatility of the underlying (annualised std dev)
    option_type: 'call' or 'put'
"""

# Choose a ticker (e.g., AAPL)
ticker = yf.Ticker("AAPL")

# List all available option expiry dates
expiry_dates = ticker.options

# Pick one expiry date
opt_chain = ticker.option_chain(expiry_dates[0])

expiry_str = expiry_dates[0]
expiry = datetime.strptime(expiry_str, "%Y-%m-%d")
time = (expiry - today).days / 365

df_puts = opt_chain.puts
put_strike_prices = df_puts['strike']
put_market_prices = df_puts['lastPrice']
put_model_prices = [black_scholes(ticker.info['regularMarketPrice'], put_strike_prices[i], time, 0.0445, df_puts["impliedVolatility"][i], 'put') for i in range(len(put_strike_prices))]

df_calls = opt_chain.calls
call_strike_prices = df_calls['strike']
call_market_prices = df_calls['lastPrice']
call_model_prices = [black_scholes(ticker.info['regularMarketPrice'], call_strike_prices[i], time, 0.0445, df_calls["impliedVolatility"][i], 'call') for i in range(len(call_strike_prices))]

# Plotting the results
plt.figure(figsize=(10,6))
plt.plot(put_strike_prices, put_market_prices, label='Market Price', marker='o', color='red')
plt.plot(put_strike_prices, put_model_prices, label='Model Price (Black-Scholes)', marker='x', color='blue')
plt.xlabel('Strike Price')
plt.ylabel('Price')
plt.title('Market vs Model Put Option Prices for AAPL')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10,6))
plt.plot(call_strike_prices, call_market_prices, label='Market Price', marker='o', color='red')
plt.plot(call_strike_prices, call_model_prices, label='Model Price (Black-Scholes)', marker='x', color='blue')
plt.xlabel('Strike Price')
plt.ylabel('Price')
plt.title('Market vs Model Call Option Prices for AAPL')
plt.legend()
plt.grid(True)
plt.show()