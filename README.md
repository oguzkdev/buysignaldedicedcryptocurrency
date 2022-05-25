# buysignaldedicedcryptocurrency
Creating a crytocurrency purchase decision with python

You can read the description of the code in my medium article in detail. Link is below:

https://medium.com/@oguzk.dev/how-to-decide-to-buy-cryptocurrency-using-python-3fb6d3765d43

How to decide to buy cryptocurrency using Python?

In the first step, I defined a few rules. We see the buying frequency of a crypto currency that we choose according to these rules.

The rules I define as catalysts are as follows:
Select last 24 hours data from Binance
RSI ≥20 && RSI ≤80. However, it should be RSI≥50 for buying signal 
MACD ≥ 0
SMA(50) > SMA(200)
Close Value > SMA(50) && Close Value > SMA(200)



Install Libraries

Then we have to install some libraries:

pip install pandas

pip install numpy

pip install python-binance

pip install ta

