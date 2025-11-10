"""
Real Polygon.io API Integration for Forex Data
===============================================

This module uses real Polygon.io API to fetch forex market data.
Requires API key from polygon.io

Get your FREE API key: https://polygon.io/dashboard/signup
"""

import streamlit as st
from polygon import RESTClient
from datetime import datetime, timedelta
import pandas as pd

def get_forex_data(pair, timeframe):
    """
    Fetch real forex data from Polygon.io
    
    Args:
        pair (str): Forex pair (e.g., 'EURUSD', 'GBPUSD')
        timeframe (str): Chart timeframe ('1m', '5m', '15m', '30m', '1h', '4h', '1d')
    
    Returns:
        dict: Market data with OHLCV, indicators, and context
    """
    
    try:
        # Get API key from Streamlit secrets
        api_key = st.secrets.get("POLYGON_API_KEY")
        
        if not api_key:
            # Fallback to mock data if no API key
            st.warning("⚠️ No Polygon API key found. Using mock data. Add POLYGON_API_KEY to secrets for real data.")
            from utils.polygon_mock import get_forex_data as mock_data
            return mock_data(pair, timeframe)
        
        # Initialize Polygon client
        client = RESTClient(api_key)
        
        # Convert pair format for Polygon (e.g., EURUSD -> C:EURUSD)
        ticker = f"C:{pair.upper()}"
        
        # Map timeframe to Polygon format
        timeframe_map = {
            '1m': (1, 'minute'),
            '5m': (5, 'minute'),
            '15m': (15, 'minute'),
            '30m': (30, 'minute'),
            '1h': (1, 'hour'),
            '4h': (4, 'hour'),
            '1d': (1, 'day')
        }
        
        multiplier, timespan = timeframe_map.get(timeframe, (1, 'hour'))
        
        # Calculate date range (last 100 candles)
        to_date = datetime.now()
        
        # Calculate from_date based on timeframe
        minutes_per_candle = {
            '1m': 1, '5m': 5, '15m': 15, '30m': 30,
            '1h': 60, '4h': 240, '1d': 1440
        }
        
        total_minutes = minutes_per_candle.get(timeframe, 60) * 100
        from_date = to_date - timedelta(minutes=total_minutes)
        
        # Format dates for Polygon API
        from_str = from_date.strftime('%Y-%m-%d')
        to_str = to_date.strftime('%Y-%m-%d')
        
        # Fetch data from Polygon
        try:
            aggs = client.get_aggs(
                ticker=ticker,
                multiplier=multiplier,
                timespan=timespan,
                from_=from_str,
                to=to_str,
                limit=100
            )
            
            # Check if we got data
            if not aggs or len(aggs) == 0:
                st.warning(f"⚠️ No data returned from Polygon for {pair}. Using mock data.")
                from utils.polygon_mock import get_forex_data as mock_data
                return mock_data(pair, timeframe)
            
            # Convert to our format
            candles = []
            for agg in aggs:
                candles.append({
                    'timestamp': datetime.fromtimestamp(agg.timestamp / 1000).isoformat(),
                    'open': round(agg.open, 4),
                    'high': round(agg.high, 4),
                    'low': round(agg.low, 4),
                    'close': round(agg.close, 4),
                    'volume': agg.volume
                })
            
            # Calculate indicators
            closes = [c['close'] for c in candles]
            current_price = closes[-1]
            
            # RSI calculation
            rsi = calculate_rsi(closes)
            
            # Trend detection
            recent_closes = closes[-20:]
            trend = "bullish" if recent_closes[-1] > recent_closes[0] else "bearish"
            
            # ATR (Average True Range)
            highs = [c['high'] for c in candles[-14:]]
            lows = [c['low'] for c in candles[-14:]]
            atr = round(sum([h - l for h, l in zip(highs, lows)]) / len(highs), 4)
            
            # Support and Resistance
            recent_highs = sorted([c['high'] for c in candles[-50:]], reverse=True)
            recent_lows = sorted([c['low'] for c in candles[-50:]])
            
            support_level = round(sum(recent_lows[:5]) / 5, 4)
            resistance_level = round(sum(recent_highs[:5]) / 5, 4)
            
            return {
                'pair': pair.upper(),
                'timeframe': timeframe,
                'current_price': current_price,
                'candles': candles,
                'indicators': {
                    'rsi': rsi,
                    'atr': atr,
                    'trend': trend,
                    'support': support_level,
                    'resistance': resistance_level
                },
                'market_context': {
                    'volatility': 'high' if atr > 0.01 else 'normal',
                    'session': get_market_session(),
                    'momentum': 'strong' if abs(rsi - 50) > 20 else 'weak'
                },
                'metadata': {
                    'data_points': len(candles),
                    'timestamp': datetime.now().isoformat(),
                    'source': 'polygon.io'
                }
            }
            
        except Exception as api_error:
            st.error(f"❌ Polygon API Error: {str(api_error)}")
            st.info("Falling back to mock data...")
            from utils.polygon_mock import get_forex_data as mock_data
            return mock_data(pair, timeframe)
    
    except Exception as e:
        st.error(f"❌ Error initializing Polygon client: {str(e)}")
        st.info("Using mock data...")
        from utils.polygon_mock import get_forex_data as mock_data
        return mock_data(pair, timeframe)

def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
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

def get_market_session():
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