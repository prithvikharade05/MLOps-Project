import talib
import numpy as np
import pandas as pd
from typing import Dict, Any

def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate all technical indicators from OHLCV data"""
    high = df['high'].values
    low = df['low'].values
    close = df['close'].values
    volume = df['volume'].values
    open_ = df['open'].values
    
    # RSI
    df['rsi'] = talib.RSI(close, timeperiod=14)
    
    # MACD
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    df['macd'] = macd
    df['macd_signal'] = macdsignal
    
    # Bollinger Bands
    upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
    df['bollinger_upper'] = upper
    df['bollinger_middle'] = middle
    df['bollinger_lower'] = lower
    
    # Moving Averages
    df['ma7'] = talib.SMA(close, timeperiod=7)
    df['ma21'] = talib.SMA(close, timeperiod=21)
    df['ma50'] = talib.SMA(close, timeperiod=50)
    
    # ATR
    df['atr'] = talib.ATR(high, low, close, timeperiod=14)
    
    # VWAP
    df['vwap'] = talib.WMA((high + low + close) / 3 * volume, timeperiod=14) / talib.WMA(volume, timeperiod=14)
    
    return df

def calculate_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate lag features"""
    df['lag1_close'] = df['close'].shift(1)
    df['lag3_close'] = df['close'].shift(3)
    df['lag6_close'] = df['close'].shift(6)
    df['lag12_close'] = df['close'].shift(12)
    df['lag24_close'] = df['close'].shift(24)
    return df

def calculate_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate rolling statistics"""
    df['rolling_mean_20'] = df['close'].rolling(window=20).mean()
    df['rolling_std_20'] = df['close'].rolling(window=20).std()
    df['volatility'] = df['rolling_std_20'] / df['rolling_mean_20']
    return df

def calculate_target(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate log return target"""
    df['log_return'] = np.log(df['close'] / df['close'].shift(1))
    return df

