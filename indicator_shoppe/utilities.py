"""Trading Utilities and Helpers"""

import numpy as np
import pandas as pd


class Backtester:
    """Backtest trading strategies"""
    def __init__(self, initial_capital=10000, commission=0.001):
        self.initial_capital = initial_capital
        self.commission = commission
    
    def backtest(self, signals, prices):
        """Backtest strategy signals against prices"""
        positions = np.where(signals > 0, 1, 0)
        returns = np.diff(prices) / prices[:-1]
        strategy_returns = positions[:-1] * returns * (1 - self.commission)
        cumulative_returns = (1 + strategy_returns).cumprod()
        return cumulative_returns * self.initial_capital


def detect_signals(indicator, threshold_buy=30, threshold_sell=70):
    """Detect buy/sell signals from indicators"""
    buy_signals = np.where(indicator < threshold_buy, 1, 0)
    sell_signals = np.where(indicator > threshold_sell, -1, 0)
    return buy_signals, sell_signals


def calculate_performance(returns):
    """Calculate performance metrics"""
    total_return = (returns[-1] / returns[0] - 1) * 100
    annual_return = (returns[-1] / returns[0]) ** (252 / len(returns)) - 1
    
    log_returns = np.log(returns / returns.shift(1))
    sharpe_ratio = log_returns.mean() / log_returns.std() * np.sqrt(252)
    
    cummax = returns.expanding().max()
    drawdown = (returns - cummax) / cummax
    max_drawdown = drawdown.min() * 100
    
    return {
        'total_return': total_return,
        'annual_return': annual_return * 100,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'win_rate': (returns > returns.shift(1)).sum() / len(returns) * 100
    }


class IndicatorPipeline:
    """Chain multiple indicators together"""
    def __init__(self):
        self.indicators = []
    
    def add(self, indicator_class, params=None):
        """Add indicator to pipeline"""
        self.indicators.append((indicator_class, params or {}))
        return self
    
    def execute(self, prices):
        """Execute all indicators in pipeline"""
        results = {}
        for indicator_class, params in self.indicators:
            indicator = indicator_class(prices, **params)
            results[indicator_class.__name__] = indicator.calculate()
        return results
