# Algo-Trading-KalmanFilter
# Enhancing Market Making with Kalman Filter-Based Mid Price Estimation

## Overview

This project explores the application of the Kalman filter to improve market making strategies by providing a more accurate and responsive measure of an asset's mid price. Traditional mid price calculations derived from the order book can lag or be noisy, whereas the Kalman filter offers a refined estimate that anticipates market movements more effectively.

## Project Highlights

### 1. Data Analysis
- **Data Preparation**: Resampled and cleaned high-frequency market data for analysis.
- **Exploratory Data Analysis**: Analyzed data trends and patterns to understand market behavior.

### 2. Kalman Filter Implementation
- **Mid Price Estimation**: Implemented the Kalman filter to estimate the mid price of a financial asset.
- **Error Calculation**: Calculated the estimation error to understand the uncertainty in the mid price estimates.

### 3. Comparison and Validation
- **Traditional vs. Kalman Mid Price**: Compared the mid prices from the order book and the Kalman filter.
- **Performance Metrics**: Validated the accuracy and responsiveness of the Kalman mid price using various performance metrics.

### 4. Profitability Analysis
- **Trade Simulation**: Simulated trades based on both traditional and Kalman mid prices.
- **Profit Calculation**: Analyzed the profitability of market making strategies using both methods.
- **Risk Assessment**: Evaluated the risk associated with each strategy by considering the estimation error.

## Why It’s Useful for Market Makers

- **Accurate Pricing**: The Kalman filter provides a more precise estimate of the mid price, which reduces the risk of executing trades at unfavorable prices.
- **Better Execution**: By anticipating price movements more effectively, market makers can execute trades with better timing and accuracy.
- **Increased Profitability**: Improved mid price estimates allow market makers to place limit orders more strategically, enhancing profitability.
- **Dynamic Spreads**: The estimation error can be used to set dynamic bid-ask spreads, adapting to market conditions in real-time.

## Tools and Technologies

- **Programming Language**: Python
- **Data Manipulation**: Pandas, NumPy
- **Data Visualization**: Matplotlib
- **Web Application**: Streamlit

## Interactive Streamlit App

Explore the data and results through an interactive Streamlit app. The app allows you to:
- Visualize the mid prices from the order book and the Kalman filter.
- Analyze the estimation error and its impact on pricing.
- Compare the profitability of different market making strategies.

## Conclusion

The Kalman filter stands out for its exceptional precision in trading decisions, surpassing traditional methods. While it may yield fewer successful trades compared to conventional approaches, its knack for achieving a lower average execution price underscores its unmatched ability to pinpoint optimal entry and exit points with remarkable accuracy. This precision translates to maximized returns per trade, as the Kalman filter adeptly identifies the most lucrative opportunities while minimizing risk exposure. By prioritizing precision, the Kalman filter offers traders a strategic advantage, enabling them to navigate volatile markets with confidence and efficiency.

