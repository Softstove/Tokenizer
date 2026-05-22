# Indicator-Shoppe 🎯

**Professional Trading Indicators Library**

A comprehensive collection of 12+ algorithmic trading indicators for technical analysis, backtesting, and signal generation.

## Quick Start

```python
from indicator_shoppe import SMA, RSI, MACD, BollingerBands
import pandas as pd

# Load your data
df = pd.read_csv('price_data.csv')

# Calculate indicators
df['SMA_20'] = SMA(df['Close'], period=20)
df['RSI_14'] = RSI(df['Close'], period=14)
df['MACD'], df['Signal'], df['Histogram'] = MACD(df['Close'])
df['BB_Upper'], df['BB_Mid'], df['BB_Lower'] = BollingerBands(df['Close'])

print(df.head())
```

## Installation

```bash
pip install -e .
```

## Available Indicators

### Trend
- **SMA** - Simple Moving Average
- **EMA** - Exponential Moving Average
- **MACD** - Moving Average Convergence Divergence
- **ADX** - Average Directional Index

### Momentum
- **RSI** - Relative Strength Index
- **Stochastic** - Stochastic Oscillator
- **CCI** - Commodity Channel Index

### Volatility
- **Bollinger Bands** - Volatility Measurement
- **ATR** - Average True Range
- **Keltner Channels** - Advanced Volatility

### Volume
- **OBV** - On-Balance Volume
- **VWAP** - Volume Weighted Average Price
- **CMF** - Chaikin Money Flow

## Utilities

- **Backtester** - Test strategies against historical data
- **Signal Detection** - Identify buy/sell signals
- **Performance Analytics** - Calculate returns, drawdowns, Sharpe ratio
- **IndicatorPipeline** - Chain multiple indicators

## Documentation

See [INDICATORS.md](INDICATORS.md) for detailed indicator reference.

## License

MIT License - See LICENSE file

## Author

Softstove - Trading Indicators Library
