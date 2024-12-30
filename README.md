# **Crypto Auto-Trading Bot**

## **Overview**  
This project is a cryptocurrency auto-trading bot developed using Python. The bot leverages the Upbit API for trading and the Telegram API for user interaction. It analyzes market trends, places buy and sell orders automatically based on preset conditions, and notifies users via Telegram about executed trades and account balances.

---

## **Features**  
- **Automated Trading**: Trades cryptocurrencies based on predefined market trends and thresholds.  
- **Trend Analysis**: Uses price data to identify upward and downward trends.  
- **Telegram Integration**:  
  - Start, stop, and configure the bot via Telegram commands.  
  - Receive notifications about executed trades and account balances.  
- **Customizable Settings**: Set the trading coin, price unit, and investment percentage dynamically through Telegram.  
- **Portfolio Overview**: Provides a detailed summary of account balances and holdings.  

---

## **Setup Instructions**  

### **1. Prerequisites**  
- Python 3.x installed on your system.  
- The following Python libraries:  
  - `pyupbit`  
  - `telebot`  
  - `numpy`  
  - `requests`  
  - `threading`  

To install these libraries, run:  
```bash
pip install pyupbit pytelegrambotapi numpy
```

---

### **2. Upbit API Keys**  
1. Log in to your [Upbit account](https://upbit.com).  
2. Generate an **API Key** and **Secret Key** under the API Management section.  
3. Replace `"access-key"` and `"secret-key"` in the script with your keys.

---

### **3. Telegram Bot Token**  
1. Create a Telegram bot via [BotFather](https://core.telegram.org/bots#botfather).  
2. Obtain the **bot token** and replace `"telegram-token"` in the script.  
3. Replace `"chat-id"` with your Telegram chat ID. You can find this by messaging your bot and checking updates via the Telegram API.

---

### **4. Configure the Script**  
- **Ticker**: Set the cryptocurrency you want to trade (e.g., `KRW-BTC`).  
- **Price Unit**: Define the minimum price adjustment unit for the chosen cryptocurrency.  
- Use the `/setcoin` command in Telegram to configure these dynamically.  

---

### **5. Run the Script**  
Run the script using:  
```bash
python trading_bot.py
```

---

## **Usage Instructions**  
The bot can be controlled through Telegram using the following commands:  

| **Command**       | **Description**                                                                 |
|--------------------|---------------------------------------------------------------------------------|
| `/start`           | Starts the auto-trading bot and prompts for investment percentage input.        |
| `/setcoin COIN UNIT` | Sets the trading coin and price unit (e.g., `/setcoin KRW-BTC 1000`).          |
| `/balance`         | Displays the current account balance and holdings.                              |
| `/stop`            | Stops the bot from trading.                                                     |

---

## **How It Works**  
1. **Trend Analysis**:  
   - The bot collects price data for the configured cryptocurrency.  
   - Analyzes the trend using rolling averages and log returns.  
   - Identifies upward or downward trends to determine buy/sell actions.

2. **Automated Trading**:  
   - Places buy orders during upward trends using a portion of the available balance.  
   - Places sell orders during downward trends for held assets.  
   - Ensures orders meet the minimum transaction requirement (`5001 KRW`).  

3. **Notifications**:  
   - Sends real-time updates to Telegram on executed trades and balance summaries.

---

## **Key Parameters**  

| **Parameter**       | **Description**                                                                 |
|----------------------|---------------------------------------------------------------------------------|
| `buy_threshold`      | Percentage increase in price to trigger a buy order (default: 0.005 or 0.5%).   |
| `sell_threshold`     | Percentage decrease in price to trigger a sell order (default: -0.005 or -0.5%).|
| `price_unit`         | Minimum price adjustment unit for the selected coin.                           |
| `invest_percent`     | Percentage of balance to invest per trade (set via Telegram).                  |

---

## **Disclaimer**  
This bot is for educational purposes only. Cryptocurrency trading involves significant risk, and past performance is not indicative of future results. Use this bot at your own risk.  

---

## **Future Enhancements**  
- Add support for multiple coins in parallel.  
- Implement advanced trading strategies (e.g., RSI, MACD).  
- Improve error handling and logging.  
- Add a web dashboard for easier configuration and monitoring.  

---

By using this bot, you acknowledge and accept all associated risks. Have fun trading responsibly! 
