import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pykalman import KalmanFilter

# Load data
df_resampled_midprice = pd.read_csv('df_resampled_midprice.csv')
estimated_midprice = pd.read_csv('estimated_midprice.csv')
estimated_error = pd.read_csv('estimated_error.csv')
resampled_trades = pd.read_csv('resampled_trades.csv')
df_resampled_midprice= pd.read_csv('df_resampled_midprice.csv')
df1= pd.read_csv('df1.csv')

# Convert index to DatetimeIndex
df_resampled_midprice['Time'] = pd.to_datetime(df_resampled_midprice['Time'])
df_resampled_midprice.set_index('Time', inplace=True)

estimated_midprice['Time'] = pd.to_datetime(estimated_midprice['Time'])
estimated_midprice.set_index('Time', inplace=True)

estimated_error['Time'] = pd.to_datetime(estimated_error['Time'])
estimated_error.set_index('Time', inplace=True)

resampled_trades['Time'] = pd.to_datetime(resampled_trades['Time'])
resampled_trades.set_index('Time', inplace=True)

df1['Time'] = pd.to_datetime(df1['Time'])
df1.set_index('Time', inplace=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Midprice and Spread Comparison", "Kalman Midprice and Error", "Market Maker Profitability"])

# Sidebar for user inputs
st.sidebar.header('User Input Parameters')

# Time selection for the period to analyze
start_time = st.sidebar.time_input("Start time", value=pd.to_datetime('1970-01-01 09:30:00').time())
end_time = st.sidebar.time_input("End time", value=pd.to_datetime('1970-01-01 09:31:00').time())
deviation_multiplier = st.sidebar.slider("Deviation Multiplier", min_value=0.1, max_value=5.0, step=0.1, value=1.0)

if page == "Midprice and Spread Comparison":
    # Filter data based on the selected time period
    subset_df_resampled_midprice = df_resampled_midprice.between_time(start_time, end_time)
    subset_estimated_midprice = estimated_midprice.between_time(start_time, end_time)
    subset_estimated_error = estimated_error.between_time(start_time, end_time)
    subset_df1= df1.between_time(start_time, end_time)

    # Calculate bid and ask prices based on Kalman filter mid price and estimated error
    kalman_mid_price = subset_estimated_midprice['0']
    spread = subset_estimated_error['0']
    bid_prices = kalman_mid_price - spread
    ask_prices = kalman_mid_price + spread

    # Plotting
    st.title('Midprice Comparison: Order Book vs Kalman Filter')

    plt.figure(figsize=(14, 7))
    plt.plot(subset_df_resampled_midprice.index, subset_df_resampled_midprice['Mid_Price'], label='Midprice from Order Book', color='blue')
    plt.plot(subset_estimated_midprice.index, subset_estimated_midprice['0'], label='Estimated Midprice from Kalman Filter', color='red')
    plt.plot(bid_prices.index, bid_prices, label='Bid Prices (Kalman - Error)', color='green', linestyle='--')
    plt.plot(ask_prices.index, ask_prices, label='Ask Prices (Kalman + Error)', color='orange', linestyle='--')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt.gcf())

    st.write("The market maker uses the Kalman filter mid price and the estimated error to set dynamic bid and ask prices. The estimated error represents the uncertainty in the mid price estimate and is used as the spread, adjusting the bid and ask prices accordingly.")
    st.title("Spread Comparison over time: Order Book vs Kalman Filter")
    plt.figure(figsize=(14, 7))
    plt.plot(subset_df1.index, subset_df1['Spread'], label='Spread from Order Book', color='blue')
    plt.plot(subset_df1.index, subset_df1['Kalman_error'], label='Estimated Spread from Kalman Filter', color='red')
    plt.xlabel('Time')
    plt.ylabel('Spread')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt.gcf())
    st.write(' Through its state estimation process, the Kalman filter dynamically adjusts the estimated state of the system based on the observed data. This adaptive nature enables the filter to track changes in the underlying process more effectively, leading to a more precise estimation of the mid price and consequently narrower prediction errors.')


elif page == "Kalman Midprice and Error":
    # Filter data based on the selected time period
    subset_start = pd.Timestamp.combine(pd.to_datetime('1970-01-01'), start_time)
    subset_end = pd.Timestamp.combine(pd.to_datetime('1970-01-01'), end_time)
    
    subset_midprice = estimated_midprice[subset_start:subset_end]
    subset_error = estimated_error[subset_start:subset_end]
    subset_trades = resampled_trades[subset_start:subset_end]

    # Calculate deviation threshold based on user-selected multiplier
    deviation_threshold = deviation_multiplier * subset_error 

    # Plotting
    st.title('Kalman Midprice and Error Analysis')

    plt.figure(figsize=(14, 7))
    plt.plot(subset_trades.index, subset_trades['Price'], label='Trade Prices', color='blue')
    plt.plot(subset_midprice.index, subset_midprice['0'], label='Estimated Mid Price', color='red')
    plt.fill_between(subset_midprice.index, 
                     subset_midprice['0'] - subset_error['0'], 
                     subset_midprice['0'] + subset_error['0'], 
                     color='red', alpha=0.2, label='Estimation Error')

    # Find deviations and mark them with a sign
    deviations = np.abs(subset_trades['Price'] - subset_midprice['0']) > deviation_threshold['0']
    deviation_times = subset_trades.index[deviations]
    deviation_values = subset_trades[deviations]
    plt.scatter(deviation_times, deviation_values, marker='o', color='black', label='Deviation')

    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt.gcf())

    st.write("This page shows the Kalman filter mid price with the estimation error shaded around it, along with the trade prices. Deviations beyond the threshold (based on the selected multiplier) are marked with black dots.This deviation, of course can be adjusted tking into consideration the risk tolerance of traders and market volatility.")
    st.write("By providing a more reliable estimate of the true value of the security, the filter reduces the likelihood of executing trades at unfavorable prices, thus minimizing potential losses. ")
elif page == "Market Maker Profitability":
    # Filtering data based on the selected time period
    subset_df_resampled_midprice = df_resampled_midprice.between_time(start_time, end_time)
    subset_estimated_midprice = estimated_midprice.between_time(start_time, end_time)
    subset_estimated_error = estimated_error.between_time(start_time, end_time)
    subset_trades = resampled_trades.between_time(start_time, end_time)

    # Selecting the columns of interest
    market_mid_price = subset_df_resampled_midprice['Mid_Price']
    kalman_mid_price = subset_estimated_midprice['0']
    kalman_error = subset_estimated_error['0']
    spread_kalman = kalman_error.mean() #From Kalman
    spread_order_book= df1['Spread'].mean() #From Order Book


    # Trades based on market mid price
    market_trades = subset_trades[(subset_trades['Price'] >= market_mid_price - spread_order_book) & 
                                  (subset_trades['Price'] <= market_mid_price + spread_order_book)]

    # Trades based on Kalman mid price
    kalman_trades = subset_trades[(subset_trades['Price'] >= kalman_mid_price - spread_kalman) & 
                                  (subset_trades['Price'] <= kalman_mid_price + spread_kalman)]

    st.title('Market Maker Profitability Analysis')

    plt.figure(figsize=(14, 7))
    plt.plot(subset_df_resampled_midprice.index, market_mid_price, label='Market Mid Price', color='blue')
    plt.plot(subset_estimated_midprice.index, kalman_mid_price, label='Kalman Mid Price', color='red')
    plt.fill_between(subset_estimated_midprice.index, 
                     kalman_mid_price - kalman_error, 
                     kalman_mid_price + kalman_error, 
                     color='red', alpha=0.2, label='Kalman Estimation Error')
    plt.scatter(market_trades.index, market_trades['Price'], label='Market Trades', color='blue', marker='x')
    plt.scatter(kalman_trades.index, kalman_trades['Price'], label='Kalman Trades', color='red', marker='x')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt.gcf())
    st.write("By comparing the profitability based on the trades executed around the mid price from the order book and the mid price estimated by the Kalman filter, market makers coul have a <span style='color:red'>Competitive Advantage</span> by assessing the effectiveness of their pricing strategy and making adjustments to improve profitability.", unsafe_allow_html=True)
    st.write("<span style='color:red'>Mean as Central Value</span>: Using the mean error as the central value for spread calculation ensures that the resulting spread reflects the average volatility observed in the market. By basing the spread on the mean error, the spread dynamically adjusts to changes in market conditions.",unsafe_allow_html=True)
    st.write("The different colors of the trade marks (blue and red) represent trades executed based on different mid-price estimations. Blue trade marks indicate trades executed using the market mid-price obtained from the order book data, while red trade marks indicate trades executed using the Kalman mid-price estimation. The distinction in colors helps traders visually differentiate between trades executed under different estimation methods and analyze their effectiveness relative to market conditions.")
    st.write("In other words, if the trade price is within the range (Kalman mid-price−spread,Kalman mid-price+spread), then it is considered a successful execution according to the Kalman approach. Same for the mid-price from the order book.")
    
    st.title('Trade Success Evaluation with Kalman Filter on the entire Dataset: Comparing Execution Strategies in High-Frequency Trading')
    st.write('Now I check the number of successful trades according to kelman and according to the mid-price from order book. In this case I don´t use the mean for the spread but the spread for each trade. I also calculate the average execution price for each method.')
    # Define the success criteria which can be adjusted based on the risk tolerance
    success_margin = df1['Spread']
    success_margin_kelman= df1['Kalman_error']

    # I separate the buy and sell trades
    buy_trades = df1[df1['Direction'] == 1]
    sell_trades = df1[df1['Direction'] == -1]

    # Aligning the indexes
    success_margin_buy = success_margin[buy_trades.index]
    success_margin_sell = success_margin[sell_trades.index]

    success_margin_buy_kelman= success_margin_kelman[buy_trades.index]
    success_margin_sell_kelman= success_margin_kelman[sell_trades.index] 

    # Buy orders are successful if close to bid price
    traditional_buy_successful = buy_trades[np.abs(buy_trades['Trade_Price'] - buy_trades['Mid_Price']) <= success_margin_buy]
    kalman_buy_successful = buy_trades[np.abs(buy_trades['Filtered_Trade_Price'] - buy_trades['Mid_Price']) <= success_margin_buy_kelman]

    # Sell orders are successful if close to ask price
    traditional_sell_successful = sell_trades[np.abs(sell_trades['Trade_Price'] - sell_trades['Mid_Price']) <= success_margin_sell]
    kalman_sell_successful = sell_trades[np.abs(sell_trades['Filtered_Trade_Price'] - sell_trades['Mid_Price']) <= success_margin_sell_kelman]
    traditional_successful_trades = pd.concat([traditional_buy_successful, traditional_sell_successful])
    kalman_successful_trades = pd.concat([kalman_buy_successful, kalman_sell_successful])

    traditional_successful_count = len(traditional_successful_trades)
    traditional_avg_execution_price = traditional_successful_trades['Trade_Price'].mean()

    kalman_successful_count = len(kalman_successful_trades)
    kalman_avg_execution_price = kalman_successful_trades['Filtered_Trade_Price'].mean()

    methods = ['Traditional Mid Price', 'Kalman Mid Price']
    successful_trades = [traditional_successful_count, kalman_successful_count]
    avg_execution_prices = [traditional_avg_execution_price, kalman_avg_execution_price]

    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Method')
    ax1.set_ylabel('Number of Successful Trades', color=color)
    ax1.bar(methods, successful_trades, color=color, alpha=0.6)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Average Execution Price', color=color)
    ax2.plot(methods, avg_execution_prices, color=color, marker='o')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    st.pyplot(fig)
    st.write(f"Traditional Successful Trades: {traditional_successful_count}")
    st.write(f"Traditional Average Execution Price: {traditional_avg_execution_price}")
    st.write(f"Kalman Successful Trades: {kalman_successful_count}")
    st.write(f"Kalman Average Execution Price: {kalman_avg_execution_price}")
    st.write("<span style='color:red'>Trade Execution Analysis Summary:</span> The main success margin for trade execution has been set to the spread value. The traditional method has a higher number of successful trades compared to the Kalman filter. However, the Kalman filter has a lower average execution price, indicating that it is more effective at identifying optimal entry and exit points. The Kalman filter's precision in trade execution is further highlighted by its ability to achieve a lower average execution price, maximizing returns per trade.",unsafe_allow_html=True)
    st.write("<span style='color:red'>Key Findings:</span>",unsafe_allow_html=True)
    st.write("The **Kalman filter** stands out for its exceptional **precision** in trading decisions, surpassing traditional methods. While it may yield **fewer successful trades** compared to conventional approaches, its knack for achieving a lower **average execution price** underscores its unmatched ability to pinpoint optimal entry and exit points with remarkable accuracy. This precision translates to **maximized returns** per trade, as the Kalman filter adeptly identifies the most lucrative opportunities while minimizing risk exposure. By prioritizing precision, the Kalman filter offers traders a strategic advantage, enabling them to navigate volatile markets with confidence and efficiency.")
