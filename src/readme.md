 # Welcome to my Binance futures project

1. Take care , trading is with high risk potentiaalways adjust your trading base on your knowleage and your personal research.
2. Always DYOR(Do your own research)
3. This bot is not a financial advice it is just for educational purpose


## Create a valid account on binance

``` log in to Binance.com create a api keys```

https://www.binance.com/en-BH/support/faq/how-to-create-api-360002502072


## Trading strategy

```The trading strategy used is the one that switches between long and short positions based on moving averages (MA) and relative strength index (RSI) indicators. ``` 

## Logic behind

```
The quantity for the orders are set manually at 10.
Example : quantity=1,# Set your desired quantity 
If you want you can change the quantity manual.
Based on the strategy the bot is opening positons based on indicator.
The BOT is not capable to close the position only when the trigger is pressed base on RSI indicator
 ```




## Installation 

``` 
pip instal poetry
poetry install
poetry run python .\src\ROBOTFUTURES.py

``` 

## Process flow

![flow.JPG](..%2F..%2F..%2FDesktop%2Fsoftware%20developer%2Fflow.JPG)


## Arhitecture Diagram 


![binance futures.JPG](..%2F..%2F..%2FDesktop%2Fsoftware%20developer%2Fbinance%20futures.JPG)





