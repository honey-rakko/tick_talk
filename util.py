# 기술적 및 기업가치 지표 계산 통합
def analyze_stock(data, fundamentals):
    # 기술적 지표 계산
    data['RSI'] = calculate_rsi(data)
    data['Rolling Mean'], data['Upper Band'], data['Lower Band'] = calculate_bollinger_bands(data)
    data['MACD'], data['Signal'] = calculate_macd(data)
    data['Volatility'] = calculate_volatility(data)
    data['Volume Change'] = calculate_volume_change(data)

    # 기업가치 지표 계산
    fundamentals['PER'] = calculate_per(fundamentals['Price'], fundamentals['EPS'])
    fundamentals['PBR'] = calculate_pbr(fundamentals['Price'], fundamentals['Book Value'])
    fundamentals['ROE'] = calculate_roe(fundamentals['Net Income'], fundamentals['Shareholders Equity'])
    fundamentals['Revenue Growth'] = calculate_revenue_growth(
        fundamentals['Revenue Current'], fundamentals['Revenue Previous']
    )

    return data, fundamentals

# 거래량 변화율 계산 함수
def calculate_volume_change(data, window=14):
    return data['Volume'].pct_change().rolling(window=window).mean() * 100

# 변동성 계산 함수
def calculate_volatility(data, window=14):
    return data['Close'].pct_change().rolling(window=window).std() * 100


# 매출 성장률 계산 함수
def calculate_revenue_growth(revenue_current, revenue_previous):
    return ((revenue_current - revenue_previous) / revenue_previous) * 100

# EPS 계산 함수
def calculate_eps(net_income, total_shares):
    return net_income / total_shares

# ROE 계산 함수
def calculate_roe(net_income, shareholders_equity):
    return (net_income / shareholders_equity) * 100

# PBR 계산 함수
def calculate_pbr(price, book_value_per_share):
    return price / book_value_per_share

# PER 계산 함수
def calculate_per(price, earnings_per_share):
    return price / earnings_per_share

# MACD 계산 함수
def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

# Bollinger Bands 계산 함수
def calculate_bollinger_bands(data, window=20):
    rolling_mean = data['Close'].rolling(window=window).mean()
    rolling_std = data['Close'].rolling(window=window).std()
    upper_band = rolling_mean + (2 * rolling_std)
    lower_band = rolling_mean - (2 * rolling_std)
    return rolling_mean, upper_band, lower_band

import pandas as pd

# RSI 계산 함수
def calculate_rsi(data, period=14):
    delta = data['Close'].diff(1)  # 종가 차이
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
