import time
import pyupbit
import telebot
import numpy as np
import threading
import requests

# 업비트 API 키 설정
access_key = "access-key"
secret_key = "secret-key"
upbit = pyupbit.Upbit(access_key, secret_key)

# 텔레그램 봇 설정
telegram_token = "telegram-token"
telegram_chat_id = "chat-id"
bot = telebot.TeleBot(telegram_token)

# 자동 매매 실행 여부 변수
is_auto_trading = False
invest_percent = None

# 매매할 코인의 티커
ticker = None
price_unit = None

# 자산 초기값 설정
initial_balance = 0.0

# 가격 단위 조정
def adjust_price(price):
    global price_unit
    return round(price / price_unit) * price_unit

# 주문 생성 및 실행
def execute_order(ticker, side, price, volume):
    try:
        if side == "buy":
            response = upbit.buy_limit_order(ticker, price, volume)
        elif side == "sell":
            response = upbit.sell_limit_order(ticker, price, volume)

        if "error" in response:
            print(f"주문 실행 실패: {response['error']['message']}")
            return False

        print("주문 실행 완료")
        return True
    except Exception as e:
        print(f"주문 실행 중 에러 발생: {str(e)}")
        return False

# 전체 자산 계산
def get_total_balance():
    total_balance = 0
    balances = upbit.get_balances()

    for balance in balances:
        ticker = balance['currency']
        if ticker == "KRW":
            total_balance += float(balance['balance'])
        else:
            try:
                current_price = pyupbit.get_current_price("KRW-" + ticker)
                if current_price is not None:
                    total_balance += current_price * float(balance['balance'])
            except Exception as e:
                print(f"Error occurred with {ticker}: {e}")

    return total_balance

# 가격 데이터 수집
def get_price_data(ticker, interval, count):
    return pyupbit.get_ohlcv(ticker, interval=interval, count=count)

# 추세 분석
def analyze_trend(data):
    returns = np.diff(np.log(data['close'].values))
    ma = data['close'].rolling(window=10).mean()

    if returns[-1] > 0 and data['close'].values[-1] > ma.values[-1]:
        return '상승 추세'
    elif returns[-1] < 0 and data['close'].values[-1] < ma.values[-1]:
        return '하락 추세'
    else:
        return '보합'

# 텔레그램 메시지 전송
def send_telegram_message(message):
    try:
        bot.send_message(telegram_chat_id, message)
    except Exception as e:
        print(f"텔레그램 메시지 전송 실패: {str(e)}")

# 메인 함수
def main():
    global is_auto_trading, invest_percent, ticker, price_unit

    interval = "minute1"
    count = 100
    buy_threshold = 0.005
    sell_threshold = -0.005

    while True:
        if is_auto_trading and ticker is not None:
            data = get_price_data(ticker, interval, count)
            trend = analyze_trend(data)

            if trend == '상승 추세':
                current_price = pyupbit.get_current_price(ticker)
                buy_price = adjust_price(current_price * (1 + buy_threshold))

                balance = upbit.get_balances()
                krw_balance = float(next((b['balance'] for b in balance if b['currency'] == 'KRW'), 0))
                invest_amount = min(krw_balance * invest_percent, krw_balance - 5001)
                if invest_amount < 5001:
                    continue

                buy_volume = invest_amount / buy_price
                if execute_order(ticker, "buy", buy_price, buy_volume):
                    send_telegram_message(f"매수 주문 실행 - 가격: {buy_price}, 수량: {buy_volume}")

            elif trend == '하락 추세':
                current_price = pyupbit.get_current_price(ticker)
                sell_price = adjust_price(current_price * (1 + sell_threshold))

                balance = upbit.get_balances()
                coin_balance = float(next((b['balance'] for b in balance if b['currency'] == ticker.split('-')[1]), 0))
                sell_amount = coin_balance * sell_price
                if sell_amount < 5001:
                    continue

                sell_volume = coin_balance
                if execute_order(ticker, "sell", sell_price, sell_volume):
                    send_telegram_message(f"매도 주문 실행 - 가격: {sell_price}, 수량: {sell_volume}")

        time.sleep(3)

# 텔레그램 메시지 처리
@bot.message_handler(commands=['start'])
def handle_start(message):
    global is_auto_trading, initial_balance
    is_auto_trading = True
    initial_balance = get_total_balance()
    msg = bot.reply_to(message, "자동 매매를 시작합니다. 투자 비율을 입력해주세요 (예: 30).")
    bot.register_next_step_handler(msg, handle_invest_percent)

def handle_invest_percent(message):
    global invest_percent
    try:
        invest_percent = float(message.text) / 100
        bot.reply_to(message, f"투자 비율이 {invest_percent * 100}%로 설정되었습니다. 매매할 코인을 설정해주세요. (예: /setcoin KRW-BTC 1000)")
    except ValueError:
        bot.reply_to(message, "잘못된 입력입니다. 숫자로 입력해주세요.")

@bot.message_handler(commands=['setcoin'])
def handle_setcoin(message):
    global ticker, price_unit
    try:
        _, coin, unit = message.text.split()
        ticker = coin.upper()
        price_unit = float(unit)
        bot.reply_to(message, f"매매 코인이 {ticker}, 가격 단위는 {price_unit}으로 설정되었습니다.")
    except ValueError:
        bot.reply_to(message, "명령어 형식이 잘못되었습니다. (예: /setcoin KRW-BTC 1000)")

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    global is_auto_trading
    is_auto_trading = False
    bot.reply_to(message, "자동 매매를 중지합니다.")

@bot.message_handler(commands=['balance'])
def handle_balance(message):
    balances = upbit.get_balances()
    response = "현재 보유 자산:\n"
    total_balance = 0
    for balance in balances:
        ticker = balance['currency']
        if ticker == "KRW":
            total_balance += float(balance['balance'])
            response += f"KRW: {balance['balance']} KRW\n"
        else:
            current_price = pyupbit.get_current_price(f"KRW-{ticker}")
            if current_price:
                total_balance += float(balance['balance']) * current_price
                response += f"{ticker}: {balance['balance']} coins, {float(balance['balance']) * current_price} KRW\n"
    response += f"총 자산: {total_balance} KRW"
    bot.send_message(message.chat.id, response)

# 스레드로 메인 함수 실행
main_thread = threading.Thread(target=main)
main_thread.start()
bot.polling()