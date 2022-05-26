# Crypto-Technical-Analysis-Trading-Bot
A bot that calculates the RSI and MACD momentum indicators of any crypto coin on binance and automatically purchases based off the indicators. The bot sends a text message to the users cell phone when a transaction is made. 

## About  
Being a long time follower of financial markets such as the stock market and the crypto market, I wanted a way to trade on the market without having to always do the analysis, purchases, and selling while I am busy. This project was created to do all that work in the background for the user, and sends the user updates to their cell phone through SMS as soon as a transaction is made. 

The bot uses two momentum indicators:

1. Relative Strength Index ([RSI]([url](https://www.investopedia.com/terms/r/rsi.asp))) 
  - Bot default Buying Condition: RSI < 30
  - Bot default Selling Condition: RSI > 70

2. Average Convergence/Divergence ([MACD]([url](https://www.investopedia.com/terms/m/macd.asp)))
  - Bot default Buying Condition: MACD > 0
  - Bot default Selling Condition:  MACD < 0 

When both RSI and MACD buying conditions are met, the bot will buy. 

When both RSU and MACD selling conditions are met, the bot will sell. 

Through backtesting 2021 ETH USD data, this bot would have given a return of ~6.54% in 2021. 

## Author & Date 
- Author: [@hadisrour6](https://www.github.com/hadisrour6)
- Version: 1.0.0 
- Date: May 4, 2022 

## Technical Documentation   

**To use the bot locally**
  1. Install Python 3.7 or above. Install Python [here]([url](https://www.python.org/)).  

  2. Run ```pip install -r requirements.txt``` to install all dependencies.

  3. Edit all the API crededentials in ```config.py``` to your unique keys. You can get all the keys and numbers from the twilio and binance website after creating        accounts.
 
  4. Run the bot with  ```python CryptoBot.py```
 
**How the Bot Works**





