# Zeyn Schweyk

import numpy
import datetime
import yfinance as yf

#################### Input ####################

ticker = "NVDA"
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
    msg = None
    condition_satisfied = False
    if (len(buy_prices) == 0 and percent_drop <= -percent_drop_min):
        msg = f"{ticker} dropped {round(percent_drop * 100, 2)}% on {str(date)[:10]}"
        condition_satisfied = True
    elif len(buy_prices) != 0 and price <= numpy.mean(buy_prices) * (1-percent_drop_min):
        msg = f"{ticker} is below the mean by {round((1 - price/numpy.mean(buy_prices)) * 100, 2)}%>={round(percent_drop_min * 100, 2)}% on {str(date)[:10]}"
        condition_satisfied = True
    
    if condition_satisfied:
        # Ensure that `price` is below the average buy price by percent_drop_min. Don't want a buy to happen too close to the average buy, as that won't average us down very much at all.
        # Of course, buy if the stock hasn't yet dipped at all or if this is a new segment.
        buy_prices.append(price)
        buy_dates.append(date)
        print(f"{msg}. Bought 1 share at ${round(buy_prices[-1], 2)}. Average price at ${round(numpy.mean(buy_prices), 2)}.")

    prev_price = price


