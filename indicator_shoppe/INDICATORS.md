# Indicator Reference Guide

## Trend Indicators

### SMA (Simple Moving Average)
**Purpose:** Identify trends by averaging prices over a period

```python
from indicator_shoppe import SMA

sma_20 = SMA(prices, period=20)
```

### EMA (Exponential Moving Average)
**Purpose:** Weighted moving average giving more importance to recent prices

```python
from indicator_shoppe import EMA

ema_12 = EMA(prices, period=12)
```

### MACD (Moving Average Convergence Divergence)
**Purpose:** Detect momentum and trend changes

```python
from indicator_shoppe import MACD

macd, signal, histogram = MACD(prices, fast=12, slow=26, smooth=9)
```

### ADX (Average Directional Index)
**Purpose:** Measure trend strength (0-100)

```python
from indicator_shoppe import ADX

adx = ADX(high, low, close, period=14)
```

## Momentum Indicators

### RSI (Relative Strength Index)
**Purpose:** Identify overbought/oversold conditions (0-100)

```python
from indicator_shoppe import RSI

rsi = RSI(prices, period=14)
# < 30 = Oversold (potential buy)
# > 70 = Overbought (potential sell)
```

### Stochastic Oscillator
**Purpose:** Momentum confirmation indicator

```python
from indicator_shoppe import Stochastic

k_line, d_line = Stochastic(high, low, close, period=14)
```

### CCI (Commodity Channel Index)
**Purpose:** Identify cyclical trends and mean reversion

```python
from indicator_shoppe import CCI

cci = CCI(high, low, close, period=20)
```

## Volatility Indicators

### Bollinger Bands
**Purpose:** Measure volatility and price levels

```python
from indicator_shoppe import BollingerBands

upper, middle, lower = BollingerBands(prices, period=20, std_dev=2)
```

### ATR (Average True Range)
**Purpose:** Measure volatility in absolute terms

```python
from indicator_shoppe import ATR

atr = ATR(high, low, close, period=14)
```

### Keltner Channels
**Purpose:** Advanced volatility bands using EMA and ATR

```python
from indicator_shoppe import KeltnerChannels

upper, middle, lower = KeltnerChannels(high, low, close, period=20)
```

## Volume Indicators

### OBV (On-Balance Volume)
**Purpose:** Measure cumulative buying/selling pressure

```python
from indicator_shoppe import OBV

obv = OBV(close, volume)
```

### VWAP (Volume Weighted Average Price)
**Purpose:** Fair value price weighted by volume

```python
from indicator_shoppe import VWAP

vwap = VWAP(high, low, close, volume)
```

### CMF (Chaikin Money Flow)
**Purpose:** Accumulation/distribution indicator

```python
from indicator_shoppe import CMF

cmf = CMF(high, low, close, volume, period=20)
```

## Utilities

### Backtester
**Purpose:** Test trading strategies against historical data

```python
from indicator_shoppe.utilities import Backtester

bt = Backtester(initial_capital=10000)
returns = bt.backtest(signals, prices)
```

### Signal Detection
**Purpose:** Identify buy/sell signals from indicators

```python
from indicator_shoppe.utilities import detect_signals

buy_signals, sell_signals = detect_signals(rsi, threshold_buy=30, threshold_sell=70)
```

### Performance Analytics
**Purpose:** Calculate performance metrics

```python
from indicator_shoppe.utilities import calculate_performance

metrics = calculate_performance(returns)
# Returns: Sharpe ratio, max drawdown, win rate, etc.
```

### IndicatorPipeline
**Purpose:** Chain multiple indicators together

```python
from indicator_shoppe.utilities import IndicatorPipeline

pipeline = IndicatorPipeline()
pipeline.add(SMA, {'period': 20})
pipeline.add(RSI, {'period': 14})
pipeline.add(MACD)
results = pipeline.execute(prices)
```
