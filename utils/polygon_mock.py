"""
Mock Polygon.io API for Forex Data
===================================

This module simulates forex market data that would normally come from Polygon.io.
Replace these functions with real API calls when ready to go live.

To integrate real Polygon.io:
1. Get API key from polygon.io
2. Install: pip install polygon-api-client
3. Replace mock functions with actual API calls
"""

import random
from datetime import datetime, timedelta

def get_forex_data(pair, timeframe):
    """
    Mock forex data retrieval - simulates Polygon.io response
    
    Args:
        pair (str): Forex pair (e.g., 'EURUSD', 'GBPUSD')
        timeframe (str): Chart timeframe ('1m', '5m', '15m', '30m', '1h', '4h', '1d')
    
    Returns:
        dict: Market data with OHLCV, indicators, and context
    
    Real Polygon.io Integration:
        from polygon import RESTClient
        client = RESTClient(api_key)
        aggs = client.get_aggs("C:" + pair, multiplier, timespan, from_, to)
    """
    
    # Simulate realistic price ranges for different pairs
    price_ranges = {
        'EURUSD': (1.0500, 1.1200),
        'GBPUSD': (1.2400, 1.3100),
        'USDJPY': (140.00, 152.00),
        'AUDUSD': (0.6300, 0.6800),
        'USDCHF': (0.8400, 0.9100),
        'GBPJPY': (175.00, 195.00),
        'EURJPY': (150.00, 165.00),
        'AUDJPY': (90.00, 102.00),
    }
    
    # Get base price range or use default
    base_min, base_max = price_ranges.get(pair.upper(), (1.0000, 1.2000))
    
    # Current price somewhere in the range
    current_price = round(random.uniform(base_min, base_max), 4)
    
    # Generate OHLCV data (last 100 candles)
    candles = []
    price = current_price
    
    for i in range(100, 0, -1):
        # Simulate price movement
        change = random.uniform(-0.002, 0.002) * price
        open_price = price
        high_price = price + abs(random.uniform(0, 0.003) * price)
        low_price = price - abs(random.uniform(0, 0.003) * price)
        close_price = price + change
        
        # Volume simulation
        volume = random.randint(50000, 500000)
        
        # Timestamp calculation based on timeframe
        timeframe_minutes = {
            '1m': 1, '5m': 5, '15m': 15, '30m': 30,
            '1h': 60, '4h': 240, '1d': 1440
        }
        minutes = timeframe_minutes.get(timeframe, 60)
        timestamp = datetime.now() - timedelta(minutes=minutes * i)
        
        candles.append({
            'timestamp': timestamp.isoformat(),
            'open': round(open_price, 4),
            'high': round(high_price, 4),
            'low': round(low_price, 4),
            'close': round(close_price, 4),
            'volume': volume
        })
        
        price = close_price
    
    # Calculate indicators
    closes = [c['close'] for c in candles]
    
    # RSI calculation (simplified)
    def calculate_rsi(prices, period=14):
        if len(prices) < period:
            return 50
        gains = []
        losses = []
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            gains.append(max(change, 0))
            losses.append(max(-change, 0))
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)
    
    rsi = calculate_rsi(closes)
    
    # Trend detection (simplified)
    recent_closes = closes[-20:]
    trend = "bullish" if recent_closes[-1] > recent_closes[0] else "bearish"
    
    # Volatility (ATR approximation)
    highs = [c['high'] for c in candles[-14:]]
    lows = [c['low'] for c in candles[-14:]]
    atr = round(sum([h - l for h, l in zip(highs, lows)]) / len(highs), 4)
    
    # Support and Resistance levels
    recent_highs = sorted([c['high'] for c in candles[-50:]], reverse=True)
    recent_lows = sorted([c['low'] for c in candles[-50:]])
    
    support_level = round(sum(recent_lows[:5]) / 5, 4)
    resistance_level = round(sum(recent_highs[:5]) / 5, 4)
    
    return {
        'pair': pair.upper(),
        'timeframe': timeframe,
        'current_price': round(closes[-1], 4),
        'candles': candles,
        'indicators': {
            'rsi': rsi,
            'atr': atr,
            'trend': trend,
            'support': support_level,
            'resistance': resistance_level
        },
        'market_context': {
            'volatility': 'high' if atr > (base_max - base_min) * 0.01 else 'normal',
            'session': _get_market_session(),
            'momentum': 'strong' if abs(rsi - 50) > 20 else 'weak'
        },
        'metadata': {
            'data_points': len(candles),
            'timestamp': datetime.now().isoformat(),
            'source': 'mock_data'
        }
    }

def _get_market_session():
    """Determine current market session based on UTC time"""
    hour = datetime.utcnow().hour
    
    if 0 <= hour < 8:
        return 'asian'
    elif 8 <= hour < 16:
        return 'london'
    elif 16 <= hour < 24:
        return 'newyork'
    else:
        return 'unknown'