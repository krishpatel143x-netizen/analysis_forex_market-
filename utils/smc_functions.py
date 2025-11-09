"""
Smart Money Concepts (SMC) Analysis Functions - COMPLETE SUITE
==============================================================

Comprehensive implementation of ALL major SMC concepts:
- Market Structure (BOS, CHoCH, MSB)
- Liquidity Analysis (Sweeps, Raids, Pools)
- Order Blocks & Fair Value Gaps
- Premium/Discount Zones
- Imbalances & Inefficiencies
- Smart Money Flow & Divergence
- Volume Analysis
- Multi-timeframe Analysis

All functions use mock logic but return realistic data structures.
"""

import random
from datetime import datetime, timedelta

# ============================================================================
# MARKET STRUCTURE FUNCTIONS
# ============================================================================

def detect_bos(data, timeframe):
    """
    Detect Break of Structure - confirms trend direction
    
    BOS occurs when price breaks a previous swing high (bullish) or 
    swing low (bearish), indicating trend continuation.
    """
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    trend = data.get('indicators', {}).get('trend', 'neutral')
    
    if len(candles) < 20:
        return {'detected': False, 'message': 'Insufficient data for BOS detection'}
    
    bos_probability = random.random()
    
    if bos_probability > 0.4:
        direction = 'bullish' if trend == 'bullish' else 'bearish'
        recent_candles = candles[-20:]
        
        if direction == 'bullish':
            bos_level = max([c['high'] for c in recent_candles[:-5]])
            structure_type = 'swing_high'
        else:
            bos_level = min([c['low'] for c in recent_candles[:-5]])
            structure_type = 'swing_low'
        
        price_distance = abs(current_price - bos_level) / bos_level
        confidence = min(95, 60 + (price_distance * 10000))
        bos_candle = candles[-random.randint(1, 5)]
        
        return {
            'detected': True,
            'direction': direction,
            'bos_level': round(bos_level, 4),
            'current_price': current_price,
            'structure_type': structure_type,
            'confidence': round(confidence, 1),
            'timeframe': timeframe,
            'timestamp': bos_candle['timestamp'],
            'interpretation': f"{direction.capitalize()} BOS detected - trend continuation expected",
            'trading_implication': f"Look for pullback to {round(bos_level * (0.998 if direction == 'bullish' else 1.002), 4)} for entry"
        }
    else:
        return {
            'detected': False,
            'reason': 'No clear structure break identified',
            'current_trend': trend,
            'recommendation': 'Wait for clearer structure formation'
        }

def detect_choch(data):
    """
    Detect Change of Character - identifies potential reversals
    
    CHoCH occurs when price fails to make a new high (in uptrend) or 
    new low (in downtrend), signaling potential trend change.
    """
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    trend = data.get('indicators', {}).get('trend', 'neutral')
    rsi = data.get('indicators', {}).get('rsi', 50)
    
    if len(candles) < 30:
        return {'detected': False, 'message': 'Insufficient data for CHoCH detection'}
    
    choch_probability = random.random()
    
    if (trend == 'bullish' and rsi > 70) or (trend == 'bearish' and rsi < 30):
        choch_probability += 0.3
    
    if choch_probability > 0.5:
        reversal_direction = 'bearish' if trend == 'bullish' else 'bullish'
        recent_candles = candles[-15:]
        
        if reversal_direction == 'bearish':
            failure_point = max([c['high'] for c in recent_candles[:10]])
            trigger_level = min([c['low'] for c in recent_candles[10:]])
        else:
            failure_point = min([c['low'] for c in recent_candles[:10]])
            trigger_level = max([c['high'] for c in recent_candles[10:]])
        
        strength_factors = []
        if (reversal_direction == 'bearish' and rsi > 70) or (reversal_direction == 'bullish' and rsi < 30):
            strength_factors.append('rsi_divergence')
        if random.random() > 0.5:
            strength_factors.append('volume_confirmation')
        if random.random() > 0.6:
            strength_factors.append('multiple_rejections')
        
        strength_score = len(strength_factors) * 25 + random.randint(10, 25)
        
        return {
            'detected': True,
            'reversal_direction': reversal_direction,
            'previous_trend': trend,
            'failure_point': round(failure_point, 4),
            'trigger_level': round(trigger_level, 4),
            'current_price': current_price,
            'strength': min(95, strength_score),
            'strength_factors': strength_factors,
            'timestamp': candles[-random.randint(1, 3)]['timestamp'],
            'interpretation': f"CHoCH detected - potential {reversal_direction} reversal from {trend} trend",
            'trading_implication': f"Watch for confirmation below/above {round(trigger_level, 4)} to enter {reversal_direction} positions"
        }
    else:
        return {
            'detected': False,
            'reason': 'Trend structure remains intact',
            'current_trend': trend,
            'recommendation': 'Continue trading with the trend'
        }

def detect_market_structure_break(data):
    """
    Detect Market Structure Break (MSB) - similar to BOS but more aggressive
    
    MSB is a strong break of recent market structure indicating powerful momentum.
    """
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    trend = data.get('indicators', {}).get('trend', 'neutral')
    
    if len(candles) < 25:
        return {'detected': False, 'message': 'Insufficient data for MSB detection'}
    
    if random.random() > 0.6:
        direction = 'bullish' if trend == 'bullish' else 'bearish'
        recent_candles = candles[-25:]
        
        if direction == 'bullish':
            msb_level = max([c['high'] for c in recent_candles[:15]])
            break_distance = current_price - msb_level
        else:
            msb_level = min([c['low'] for c in recent_candles[:15]])
            break_distance = msb_level - current_price
        
        momentum_strength = random.randint(70, 95)
        
        return {
            'detected': True,
            'direction': direction,
            'msb_level': round(msb_level, 4),
            'break_distance_pips': round(abs(break_distance) * 10000, 1),
            'momentum_strength': momentum_strength,
            'interpretation': f"Strong {direction} MSB - aggressive continuation expected",
            'entry_suggestion': f"Enter on minimal pullback, target extension beyond {round(msb_level * (1.002 if direction == 'bullish' else 0.998), 4)}"
        }
    
    return {'detected': False, 'reason': 'No significant market structure break'}

# ============================================================================
# LIQUIDITY ANALYSIS FUNCTIONS
# ============================================================================

def detect_liquidity_sweep(data):
    """
    Detect Liquidity Sweep - when price hunts stops above/below key levels
    
    Smart money often sweeps liquidity (stop losses) before reversing.
    """
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    
    if len(candles) < 30:
        return {'sweeps': [], 'message': 'Insufficient data'}
    
    sweeps = []
    num_sweeps = random.randint(0, 2)
    
    for i in range(num_sweeps):
        sweep_type = random.choice(['buy_side', 'sell_side'])
        lookback = 30 + (i * 10)
        relevant_candles = candles[-lookback:-lookback+15]
        
        if sweep_type == 'buy_side':
            liquidity_level = max([c['high'] for c in relevant_candles])
            sweep_candle = candles[-random.randint(5, 15)]
            reaction = 'bearish_reversal' if random.random() > 0.4 else 'continuation'
        else:
            liquidity_level = min([c['low'] for c in relevant_candles])
            sweep_candle = candles[-random.randint(5, 15)]
            reaction = 'bullish_reversal' if random.random() > 0.4 else 'continuation'
        
        sweeps.append({
            'type': sweep_type,
            'liquidity_level': round(liquidity_level, 4),
            'sweep_time': sweep_candle['timestamp'],
            'reaction': reaction,
            'distance_from_current': round(abs(current_price - liquidity_level) * 10000, 1),
            'interpretation': f"{sweep_type.replace('_', ' ').title()} liquidity swept - watch for {reaction.replace('_', ' ')}"
        })
    
    return {
        'sweeps': sweeps,
        'total_sweeps': len(sweeps),
        'trading_context': 'Liquidity sweeps often precede reversals' if sweeps else 'No recent liquidity sweeps'
    }

def identify_liquidity_pools(data):
    """
    Identify Liquidity Pools - areas with concentrated stop losses
    
    These are common reversal points where smart money enters.
    """
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    
    if len(candles) < 40:
        return {'pools': [], 'message': 'Insufficient data'}
    
    pools = []
    num_pools = random.randint(1, 3)
    
    for i in range(num_pools):
        pool_type = random.choice(['above_highs', 'below_lows', 'equal_highs', 'equal_lows'])
        
        lookback_start = 15 + (i * 15)
        lookback_end = lookback_start + 20
        relevant_candles = candles[-lookback_end:-lookback_start]
        
        if 'high' in pool_type:
            highs = [c['high'] for c in relevant_candles]
            pool_level = max(highs)
            density = len([h for h in highs if abs(h - pool_level) / pool_level < 0.0003])
        else:
            lows = [c['low'] for c in relevant_candles]
            pool_level = min(lows)
            density = len([l for l in lows if abs(l - pool_level) / pool_level < 0.0003])
        
        magnetism = random.randint(60, 90)
        
        pools.append({
            'type': pool_type,
            'level': round(pool_level, 4),
            'density': density,
            'magnetism': magnetism,
            'distance_pips': round(abs(current_price - pool_level) * 10000, 1),
            'interpretation': f"Liquidity pool {pool_type.replace('_', ' ')} - expect price attraction"
        })
    
    pools.sort(key=lambda x: x['distance_pips'])
    
    return {
        'pools': pools,
        'nearest_pool': pools[0] if pools else None,
        'recommendation': 'Watch for price to reach and react at these liquidity levels'
    }

def detect_liquidity_void(data):
    """
    Detect Liquidity Voids - price gaps with no trading activity
    
    Voids often get filled as price revisits these areas.
    """
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    
    if len(candles) < 30:
        return {'voids': [], 'message': 'Insufficient data'}
    
    voids = []
    
    for i in range(len(candles) - 5, len(candles) - 25, -1):
        if random.random() > 0.85:  # 15% chance of void
            void_high = candles[i-1]['low']
            void_low = candles[i]['high']
            
            if void_high > void_low:  # Valid void
                void_size_pips = (void_high - void_low) * 10000
                
                if void_size_pips > 5:  # Significant void
                    fill_probability = random.randint(70, 95)
                    
                    voids.append({
                        'void_high': round(void_high, 4),
                        'void_low': round(void_low, 4),
                        'void_midpoint': round((void_high + void_low) / 2, 4),
                        'size_pips': round(void_size_pips, 1),
                        'timestamp': candles[i]['timestamp'],
                        'fill_probability': fill_probability,
                        'status': 'unfilled',
                        'interpretation': f"Liquidity void of {round(void_size_pips, 1)} pips - likely to be filled"
                    })
    
    return {
        'voids': voids[:3],  # Return top 3
        'total_voids': len(voids),
        'recommendation': 'Voids act as magnets - expect price to fill these gaps'
    }

# ============================================================================
# ORDER BLOCKS & FAIR VALUE GAPS
# ============================================================================

def identify_order_blocks(data):
    """
    Identify institutional order blocks (demand/supply zones)
    
    Order blocks are areas where institutions placed large orders.
    """
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    trend = data.get('indicators', {}).get('trend', 'neutral')
    
    if len(candles) < 50:
        return {'order_blocks': [], 'message': 'Insufficient data'}
    
    num_blocks = random.randint(2, 4)
    order_blocks = []
    
    for i in range(num_blocks):
        if trend == 'bullish':
            block_type = 'demand' if random.random() > 0.3 else 'supply'
        else:
            block_type = 'supply' if random.random() > 0.3 else 'demand'
        
        lookback_start = 10 + (i * 15)
        lookback_end = lookback_start + 15
        relevant_candles = candles[-lookback_end:-lookback_start] if lookback_start < len(candles) else candles[-lookback_end:]
        
        if not relevant_candles:
            continue
        
        base_candle = relevant_candles[random.randint(0, len(relevant_candles)-1)]
        
        if block_type == 'demand':
            zone_high = base_candle['high']
            zone_low = base_candle['low'] * 0.9995
            price_level = round((zone_high + zone_low) / 2, 4)
        else:
            zone_high = base_candle['high'] * 1.0005
            zone_low = base_candle['low']
            price_level = round((zone_high + zone_low) / 2, 4)
        
        strength_score = random.randint(60, 95)
        distance_pips = abs(current_price - price_level) * 10000
        is_tested = random.random() > 0.6
        validity = 'untested' if not is_tested else 'tested_once'
        
        candle_index = candles.index(base_candle)
        age_candles = len(candles) - candle_index
        freshness = 'fresh' if age_candles < 20 else 'aged'
        
        order_blocks.append({
            'type': block_type,
            'zone_high': round(zone_high, 4),
            'zone_low': round(zone_low, 4),
            'price_level': price_level,
            'strength': strength_score,
            'validity': validity,
            'freshness': freshness,
            'distance_pips': round(distance_pips, 1),
            'timestamp': base_candle['timestamp'],
            'interpretation': f"{block_type.capitalize()} zone - expect {'buying' if block_type == 'demand' else 'selling'} pressure",
            'trading_setup': _generate_order_block_setup(block_type, zone_high, zone_low, current_price)
        })
    
    order_blocks.sort(key=lambda x: x['distance_pips'])
    
    return {
        'order_blocks': order_blocks,
        'total_identified': len(order_blocks),
        'current_price': current_price,
        'nearest_block': order_blocks[0] if order_blocks else None,
        'recommendation': _generate_ob_recommendation(order_blocks, current_price, trend)
    }

def identify_fair_value_gaps(data):
    """
    Identify Fair Value Gaps (FVG) - 3-candle imbalances
    
    FVGs show inefficient price movement that often gets filled.
    """
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    
    if len(candles) < 20:
        return {'fvgs': [], 'message': 'Insufficient data'}
    
    fvgs = []
    
    # Look for 3-candle patterns
    for i in range(len(candles) - 3, len(candles) - 30, -1):
        if i < 2:
            break
        
        candle1 = candles[i-2]
        candle2 = candles[i-1]
        candle3 = candles[i]
        
        # Bullish FVG: candle1 high < candle3 low
        if candle1['high'] < candle3['low'] and random.random() > 0.7:
            gap_high = candle3['low']
            gap_low = candle1['high']
            gap_type = 'bullish'
            
        # Bearish FVG: candle1 low > candle3 high
        elif candle1['low'] > candle3['high'] and random.random() > 0.7:
            gap_high = candle1['low']
            gap_low = candle3['high']
            gap_type = 'bearish'
        else:
            continue
        
        gap_size_pips = (gap_high - gap_low) * 10000
        
        if gap_size_pips > 3:  # Significant gap
            distance_pips = abs(current_price - (gap_high + gap_low) / 2) * 10000
            fill_percentage = random.randint(0, 100)
            
            fvgs.append({
                'type': gap_type,
                'gap_high': round(gap_high, 4),
                'gap_low': round(gap_low, 4),
                'gap_midpoint': round((gap_high + gap_low) / 2, 4),
                'size_pips': round(gap_size_pips, 1),
                'fill_percentage': fill_percentage,
                'distance_pips': round(distance_pips, 1),
                'timestamp': candle2['timestamp'],
                'interpretation': f"{gap_type.capitalize()} FVG - expect {100 - fill_percentage}% fill remaining",
                'trading_use': f"Retest zone for {gap_type} continuation"
            })
    
    fvgs.sort(key=lambda x: x['distance_pips'])
    
    return {
        'fvgs': fvgs[:4],  # Return top 4
        'total_fvgs': len(fvgs),
        'nearest_fvg': fvgs[0] if fvgs else None,
        'recommendation': 'FVGs often act as support/resistance and fill zones'
    }

def identify_breaker_blocks(data):
    """
    Identify Breaker Blocks - failed order blocks that flip polarity
    
    When an order block fails, it becomes a breaker (demand becomes supply, vice versa).
    """
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    
    if len(candles) < 40:
        return {'breaker_blocks': [], 'message': 'Insufficient data'}
    
    breakers = []
    num_breakers = random.randint(0, 2)
    
    for i in range(num_breakers):
        original_type = random.choice(['demand', 'supply'])
        breaker_type = 'supply' if original_type == 'demand' else 'demand'
        
        lookback = 20 + (i * 15)
        relevant_candles = candles[-lookback:-lookback+10]
        
        if not relevant_candles:
            continue
        
        base_candle = relevant_candles[random.randint(0, len(relevant_candles)-1)]
        
        zone_high = round(base_candle['high'], 4)
        zone_low = round(base_candle['low'], 4)
        
        strength = random.randint(70, 90)
        
        breakers.append({
            'original_type': original_type,
            'current_type': breaker_type,
            'zone_high': zone_high,
            'zone_low': zone_low,
            'flip_timestamp': base_candle['timestamp'],
            'strength': strength,
            'interpretation': f"Failed {original_type} OB flipped to {breaker_type} breaker",
            'trading_implication': f"Expect strong {breaker_type} reaction at zone"
        })
    
    return {
        'breaker_blocks': breakers,
        'total_breakers': len(breakers),
        'concept': 'Breaker blocks show failed institutional levels that reverse polarity'
    }

# ============================================================================
# PREMIUM/DISCOUNT ZONES
# ============================================================================

def calculate_premium_discount_zones(data):
    """
    Calculate Premium/Discount zones using Equilibrium
    
    Based on recent swing high/low, identifies fair value areas.
    """
    
    