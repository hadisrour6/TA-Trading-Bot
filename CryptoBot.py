import talib, json, numpy, websocket, config
from binance.enums import *
from binance.client import Client
from SMS import send_message

MACD_FREQUENCY = 34
MACD_ZERO_LINE = 0
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
RSI_FREQUENCY = 14

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_" + config.FREQUENCY

client = Client(config.API_KEY, config.API_SECRET, tld='us')

closed_stick_prices = []  # collects filled price of candle stick when it closes

holding_position = False

def on_close(ws):
    print('Connection closed')
    send_message('Connection closed')

def on_open(ws):
    print('Connection opened')
    send_message('Connection opened')

def on_message(ws, message):
    global closed_stick_prices, holding_position

    print("Message Recieved")
    json_message = json.loads(message)  # takes json string and converts it to python data structure we can use

    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("candle closed at {}".format(close))
        closed_stick_prices.append(float(close))
        print("all closes:")
        print(closed_stick_prices)

        if len(closed_stick_prices) > MACD_FREQUENCY:
            close_price_np = numpy.array(closed_stick_prices)

            rsi = talib.RSI(close_price_np, RSI_FREQUENCY)
            recent_rsi = rsi[-1]

            macdhist = talib.MACD(close_price_np, fastperiod=12, slowperiod=26, signalperiod=9)
            recent_macd = macdhist[-1][-1]

            print("the current rsi is {}".format(recent_rsi))
            print("the current MACD is {}".format(recent_macd))

            if recent_macd > MACD_ZERO_LINE and recent_rsi < RSI_OVERSOLD :
                if holding_position:
                    send_message(
                        "Oversold, however you cannot buy as you already have a position, the price is: {}".format(
                            closed_stick_prices[-1]))
                else:
                    print("BUY!!")
                    order_placed = Place_Order(SIDE_BUY, config.TRADE_AMOUNT, config.CRYPTO_SYMBOL)
                    if order_placed:
                        send_message("Successfully bought at {}".format(closed_stick_prices[-1]))
                        print("Successfully bought at {}".format(closed_stick_prices[-1]))
                        holding_position = True

            if recent_macd < MACD_ZERO_LINE and recent_rsi > RSI_OVERBOUGHT:
                if holding_position:
                    print("SELL!!")
                    order_placed = Place_Order(SIDE_SELL, config.TRADE_AMOUNT, config.CRYPTO_SYMBOL)
                    if order_placed:
                        send_message("Successfully sold at {}".format(closed_stick_prices[-1]))
                        print("Successfully sold at {}".format(closed_stick_prices[-1]))
                        holding_position = False
                else:
                    send_message("Overbought, however you cannot sell as you do not hold any positions, the is price: {}".format(closed_stick_prices[-1]))


def Place_Order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print("ORDER HAS BEEN FILLED")
    except:
        print("ERROR HAS OCCURRED")
        return False
    return True


def run_Trade():
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close = on_close, on_message=on_message)  # connects to websocket and collects crypto data
    ws.run_forever()


run_Trade()