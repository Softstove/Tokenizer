"""Indicator-Shoppe: Professional Trading Indicators Library"""

from .indicators import (
    SMA,
    EMA,
    MACD,
    RSI,
    ADX,
    Stochastic,
    CCI,
    BollingerBands,
    ATR,
    KeltnerChannels,
    OBV,
    VWAP,
    CMF
)

from .utilities import (
    Backtester,
    detect_signals,
    calculate_performance,
    IndicatorPipeline
)

__version__ = '1.0.0'
__author__ = 'Softstove'
__all__ = [
    'SMA', 'EMA', 'MACD', 'RSI', 'ADX', 'Stochastic', 'CCI',
    'BollingerBands', 'ATR', 'KeltnerChannels', 'OBV', 'VWAP', 'CMF',
    'Backtester', 'detect_signals', 'calculate_performance', 'IndicatorPipeline'
]
