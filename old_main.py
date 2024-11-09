# Zeyn Schweyk

import numpy
import datetime
import yfinance as yf

#################### Input ####################

ticker = "MSFT"
start_date = "1984-01-01"
end_date = "2024-11-08"
percent_drop_min = .05
percent_gain_min = .05

#############################################




data = yf.download(ticker, start_date, end_date)
close_list = list(data["Close"][ticker])
dates_list = list(data.index.values)

prev_price = close_list[0]
buy_dates = []
buy_prices = []
for price, date in zip(close_list, dates_list):
    if len(buy_prices) != 0:
        average_buy_price = numpy.mean(buy_prices)
        percent_gain = (price - average_buy_price) / average_buy_price
        if percent_gain >= percent_gain_min:
            num_days = numpy.timedelta64(date - buy_dates[0], 'D').astype(int)
            annualized_return = (1 + percent_gain) ** (365/num_days) - 1
            print(f"Investment gained {round(percent_gain * 100, 2)}% on {str(date)[:10]}. Span of {num_days} days. Sold {len(buy_prices)} shares at ${round(price, 2)}")
            print(f"Annualized return: {round(annualized_return * 100, 2)}%\n")
            buy_prices = []
            buy_dates = []

    percent_drop = (price - prev_price) / prev_price
    if percent_drop <= -percent_drop_min:
        buy_prices.append(price)
        buy_dates.append(date)
        print(f"{ticker} dropped {round(percent_drop * 100, 2)}% on {str(date)[:10]}. Bought 1 share at ${round(buy_prices[-1], 2)}. Average price at ${round(numpy.mean(buy_prices), 2)}.")

    prev_price = price


