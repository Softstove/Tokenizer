"""Trading Indicators Implementation"""

import numpy as np
import pandas as pd


class SMA:
    """Simple Moving Average"""
    def __init__(self, prices, period=20):
        self.prices = prices
        self.period = period
    
    def calculate(self):
        return pd.Series(self.prices).rolling(window=self.period).mean()


class EMA:
    """Exponential Moving Average"""
    def __init__(self, prices, period=20):
        self.prices = prices
        self.period = period
    
    def calculate(self):
        return pd.Series(self.prices).ewm(span=self.period, adjust=False).mean()


class MACD:
    """Moving Average Convergence Divergence"""
    def __init__(self, prices, fast=12, slow=26, smooth=9):
        self.prices = prices
        self.fast = fast
        self.slow = slow
        self.smooth = smooth
    
    def calculate(self):
        prices_series = pd.Series(self.prices)
        ema_fast = prices_series.ewm(span=self.fast, adjust=False).mean()
        ema_slow = prices_series.ewm(span=self.slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal = macd.ewm(span=self.smooth, adjust=False).mean()
        histogram = macd - signal
        return macd, signal, histogram


class RSI:
    """Relative Strength Index"""
    def __init__(self, prices, period=14):
        self.prices = prices
        self.period = period
    
    def calculate(self):
        prices_series = pd.Series(self.prices)
        delta = prices_series.diff()
        gains = np.where(delta > 0, delta, 0)
        losses = np.where(delta < 0, -delta, 0)
        
        avg_gains = pd.Series(gains).rolling(window=self.period).mean()
        avg_losses = pd.Series(losses).rolling(window=self.period).mean()
        
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        return rsi


class ADX:
    """Average Directional Index"""
    def __init__(self, high, low, close, period=14):
        self.high = high
        self.low = low
        self.close = close
        self.period = period
    
    def calculate(self):
        high_series = pd.Series(self.high)
        low_series = pd.Series(self.low)
        close_series = pd.Series(self.close)
        
        plus_dm = high_series.diff()
        minus_dm = -low_series.diff()
        
        tr = np.maximum(high_series - low_series, 
                       np.maximum(abs(high_series - close_series.shift()),
                                abs(low_series - close_series.shift())))
        
        atr = pd.Series(tr).rolling(window=self.period).mean()
        plus_di = 100 * (pd.Series(np.where(plus_dm > 0, plus_dm, 0)).rolling(self.period).mean() / atr)
        minus_di = 100 * (pd.Series(np.where(minus_dm > 0, minus_dm, 0)).rolling(self.period).mean() / atr)
        
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = pd.Series(dx).rolling(window=self.period).mean()
        
        return adx


class Stochastic:
    """Stochastic Oscillator"""
    def __init__(self, high, low, close, period=14, smooth_k=3, smooth_d=3):
        self.high = high
        self.low = low
        self.close = close
        self.period = period
        self.smooth_k = smooth_k
        self.smooth_d = smooth_d
    
    def calculate(self):
        high_series = pd.Series(self.high)
        low_series = pd.Series(self.low)
        close_series = pd.Series(self.close)
        
        lowest_low = low_series.rolling(window=self.period).min()
        highest_high = high_series.rolling(window=self.period).max()
        
        k_percent = 100 * (close_series - lowest_low) / (highest_high - lowest_low)
        k_line = k_percent.rolling(window=self.smooth_k).mean()
        d_line = k_line.rolling(window=self.smooth_d).mean()
        
        return k_line, d_line


class CCI:
    """Commodity Channel Index"""
    def __init__(self, high, low, close, period=20):
        self.high = high
        self.low = low
        self.close = close
        self.period = period
    
    def calculate(self):
        high_series = pd.Series(self.high)
        low_series = pd.Series(self.low)
        close_series = pd.Series(self.close)
        
        typical_price = (high_series + low_series + close_series) / 3
        sma = typical_price.rolling(window=self.period).mean()
        mad = typical_price.rolling(window=self.period).apply(lambda x: abs(x - x.mean()).mean())
        
        cci = (typical_price - sma) / (0.015 * mad)
        return cci


class BollingerBands:
    """Bollinger Bands"""
    def __init__(self, prices, period=20, std_dev=2):
        self.prices = prices
        self.period = period
        self.std_dev = std_dev
    
    def calculate(self):
        prices_series = pd.Series(self.prices)
        middle = prices_series.rolling(window=self.period).mean()
        std = prices_series.rolling(window=self.period).std()
        upper = middle + (std * self.std_dev)
        lower = middle - (std * self.std_dev)
        return upper, middle, lower


class ATR:
    """Average True Range"""
    def __init__(self, high, low, close, period=14):
        self.high = high
        self.low = low
        self.close = close
        self.period = period
    
    def calculate(self):
        high_series = pd.Series(self.high)
        low_series = pd.Series(self.low)
        close_series = pd.Series(self.close)
        
        tr1 = high_series - low_series
        tr2 = abs(high_series - close_series.shift())
        tr3 = abs(low_series - close_series.shift())
        tr = np.maximum(tr1, np.maximum(tr2, tr3))
        
        atr = pd.Series(tr).rolling(window=self.period).mean()
        return atr


class KeltnerChannels:
    """Keltner Channels"""
    def __init__(self, high, low, close, period=20, atr_period=10):
        self.high = high
        self.low = low
        self.close = close
        self.period = period
        self.atr_period = atr_period
    
    def calculate(self):
        close_series = pd.Series(self.close)
        middle = close_series.ewm(span=self.period, adjust=False).mean()
        
        atr_calc = ATR(self.high, self.low, self.close, self.atr_period)
        atr = atr_calc.calculate()
        
        upper = middle + (atr * 2)
        lower = middle - (atr * 2)
        return upper, middle, lower


class OBV:
    """On-Balance Volume"""
    def __init__(self, close, volume):
        self.close = close
        self.volume = volume
    
    def calculate(self):
        close_series = pd.Series(self.close)
        volume_series = pd.Series(self.volume)
        
        obv = np.where(close_series > close_series.shift(), volume_series, 
                      np.where(close_series < close_series.shift(), -volume_series, 0))
        return pd.Series(obv).cumsum()


class VWAP:
    """Volume Weighted Average Price"""
    def __init__(self, high, low, close, volume):
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
    
    def calculate(self):
        high_series = pd.Series(self.high)
        low_series = pd.Series(self.low)
        close_series = pd.Series(self.close)
        volume_series = pd.Series(self.volume)
        
        typical_price = (high_series + low_series + close_series) / 3
        vwap = (typical_price * volume_series).cumsum() / volume_series.cumsum()
        return vwap


class CMF:
    """Chaikin Money Flow"""
    def __init__(self, high, low, close, volume, period=20):
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.period = period
    
    def calculate(self):
        high_series = pd.Series(self.high)
        low_series = pd.Series(self.low)
        close_series = pd.Series(self.close)
        volume_series = pd.Series(self.volume)
        
        mfv = ((close_series - low_series) - (high_series - close_series)) / (high_series - low_series) * volume_series
        cmf = mfv.rolling(window=self.period).sum() / volume_series.rolling(window=self.period).sum()
        return cmf
