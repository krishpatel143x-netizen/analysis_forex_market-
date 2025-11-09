
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
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    
    if len(candles) < 50:
        return {'zones': {}, 'message': 'Insufficient data'}
    
    recent_candles = candles[-50:]
    
    swing_high = max([c['high'] for c in recent_candles])
    swing_low = min([c['low'] for c in recent_candles])
    
    range_size = swing_high - swing_low
    equilibrium = (swing_high + swing_low) / 2
    
    # Fibonacci-like zones
    zones = {
        'swing_high': round(swing_high, 4),
        'premium_zone': {
            'upper': round(swing_high, 4),
            'lower': round(equilibrium + (range_size * 0.236), 4),
            'strength': 'strong_resistance'
        },
        'equilibrium': round(equilibrium, 4),
        'discount_zone': {
            'upper': round(equilibrium - (range_size * 0.236), 4),
            'lower': round(swing_low, 4),
            'strength': 'strong_support'
        },
        'swing_low': round(swing_low, 4),
        'current_price': current_price,
        'current_position': None
    }
    
    # Determine current position
    if current_price > zones['equilibrium']:
        if current_price > zones['premium_zone']['lower']:
            zones['current_position'] = 'premium'
            zones['interpretation'] = 'Price in premium - favor sells'
        else:
            zones['current_position'] = 'equilibrium'
            zones['interpretation'] = 'Price at fair value - watch for direction'
    else:
        if current_price < zones['discount_zone']['upper']:
            zones['current_position'] = 'discount'
            zones['interpretation'] = 'Price in discount - favor buys'
        else:
            zones['current_position'] = 'equilibrium'
            zones['interpretation'] = 'Price at fair value - watch for direction'
    
    return {
        'zones': zones,
        'range_size_pips': round(range_size * 10000, 1),
        'trading_bias': 'Bullish' if zones['current_position'] == 'discount' else 'Bearish' if zones['current_position'] == 'premium' else 'Neutral'
    }

# ============================================================================
# IMBALANCE & INEFFICIENCY DETECTION
# ============================================================================

def detect_imbalances(data):
    """
    Detect Price Imbalances - rapid moves leaving gaps
    
    Imbalances show areas price moved through too quickly.
    """
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    
    if len(candles) < 25:
        return {'imbalances': [], 'message': 'Insufficient data'}
    
    imbalances = []
    
    for i in range(len(candles) - 2, len(candles) - 25, -1):
        if i < 1:
            break
        
        prev_candle = candles[i-1]
        curr_candle = candles[i]
        
        # Check for gap up or gap down
        if random.random() > 0.8:
            if curr_candle['close'] > prev_candle['high']:
                imbalance_type = 'bullish'
                imbalance_low = prev_candle['high']
                imbalance_high = curr_candle['low']
            elif curr_candle['close'] < prev_candle['low']:
                imbalance_type = 'bearish'
                imbalance_high = prev_candle['low']
                imbalance_low = curr_candle['high']
            else:
                continue
            
            imbalance_size = abs(imbalance_high - imbalance_low) * 10000
            
            if imbalance_size > 2:
                imbalances.append({
                    'type': imbalance_type,
                    'imbalance_high': round(imbalance_high, 4),
                    'imbalance_low': round(imbalance_low, 4),
                    'size_pips': round(imbalance_size, 1),
                    'timestamp': curr_candle['timestamp'],
                    'rebalance_probability': random.randint(60, 85),
                    'interpretation': f"{imbalance_type.capitalize()} imbalance - likely rebalance zone"
                })
    
    return {
        'imbalances': imbalances[:3],
        'total_imbalances': len(imbalances),
        'recommendation': 'Imbalances often attract price for rebalancing'
    }

def detect_inefficiencies(data):
    """
    Detect Market Inefficiencies - poorly traded zones
    
    Areas with low volume or quick passage indicating poor price discovery.
    """
    
    candles = data.get('candles', [])
    
    if len(candles) < 30:
        return {'inefficiencies': [], 'message': 'Insufficient data'}
    
    inefficiencies = []
    
    # Look for consecutive candles with small bodies and low volume
    for i in range(len(candles) - 5, len(candles) - 30, -1):
        if i < 5:
            break
        
        if random.random() > 0.85:
            window = candles[i:i+5]
            
            zone_high = max([c['high'] for c in window])
            zone_low = min([c['low'] for c in window])
            
            inefficiency_score = random.randint(65, 90)
            
            inefficiencies.append({
                'zone_high': round(zone_high, 4),
                'zone_low': round(zone_low, 4),
                'zone_midpoint': round((zone_high + zone_low) / 2, 4),
                'timestamp_start': window[0]['timestamp'],
                'timestamp_end': window[-1]['timestamp'],
                'inefficiency_score': inefficiency_score,
                'interpretation': 'Inefficient zone - expect revisit and better price discovery'
            })
    
    return {
        'inefficiencies': inefficiencies[:2],
        'total_inefficiencies': len(inefficiencies),
        'concept': 'Inefficient zones show poor trading and often get revisited'
    }

# ============================================================================
# VOLUME & FLOW ANALYSIS
# ============================================================================

def analyze_volume_profile(data):
    """
    Analyze Volume Profile - where most trading occurred
    
    High volume nodes act as support/resistance.
    """
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    
    if len(candles) < 40:
        return {'profile': {}, 'message': 'Insufficient data'}
    
    recent_candles = candles[-40:]
    
    # Calculate price levels and volumes
    volumes = [c['volume'] for c in recent_candles]
    total_volume = sum(volumes)
    
    # High volume node (POC - Point of Control)
    poc_index = volumes.index(max(volumes))
    poc_price = round((recent_candles[poc_index]['high'] + recent_candles[poc_index]['low']) / 2, 4)
    
    # Value area (70% of volume)
    sorted_volumes = sorted(enumerate(volumes), key=lambda x: x[1], reverse=True)
    value_area_volume = 0
    value_area_indices = []
    
    for idx, vol in sorted_volumes:
        value_area_volume += vol
        value_area_indices.append(idx)
        if value_area_volume >= total_volume * 0.7:
            break
    
    value_area_high = max([recent_candles[i]['high'] for i in value_area_indices])
    value_area_low = min([recent_candles[i]['low'] for i in value_area_indices])
    
    return {
        'profile': {
            'poc': poc_price,
            'poc_volume': max(volumes),
            'value_area_high': round(value_area_high, 4),
            'value_area_low': round(value_area_low, 4),
            'current_price': current_price,
            'position_relative_to_poc': 'above' if current_price > poc_price else 'below'
        },
        'interpretation': f"POC at {poc_price} - strong {'support' if current_price > poc_price else 'resistance'}",
        'trading_implication': 'Price tends to gravitate toward high volume areas (POC)'
    }

def detect_smart_money_divergence(data):
    """
    Detect Smart Money Divergence - price vs accumulation/distribution
    
    When price makes new highs/lows but smart money isn't participating.
    """
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    trend = data.get('indicators', {}).get('trend', 'neutral')
    
    if len(candles) < 40:
        return {'divergence': None, 'message': 'Insufficient data'}
    
    if random.random() > 0.6:
        # Mock divergence detection
        divergence_type = random.choice(['bullish', 'bearish', 'hidden_bullish', 'hidden_bearish'])
        
        if 'bullish' in divergence_type:
            interpretation = 'Price making lower lows but smart money accumulating'
            signal = 'potential_reversal_up'
            strength = random.randint(65, 90)
        else:
            interpretation = 'Price making higher highs but smart money distributing'
            signal = 'potential_reversal_down'
            strength = random.randint(65, 90)
        
        return {
            'divergence': {
                'type': divergence_type,
                'strength': strength,
                'signal': signal,
                'interpretation': interpretation,
                'confirmation_needed': random.choice([True, False])
            },
            'recommendation': f"Watch for {signal.replace('_', ' ')} confirmation"
        }
    
    return {'divergence': None, 'reason': 'No smart money divergence detected'}

def analyze_order_flow(data):
    """
    Analyze Order Flow - buying vs selling pressure
    
    Determines who's in control: buyers or sellers.
    """
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    
    if len(candles) < 20:
        return {'flow': {}, 'message': 'Insufficient data'}
    
    recent_candles = candles[-20:]
    
    # Calculate buying/selling pressure
    buying_pressure = sum([1 for c in recent_candles if c['close'] > c['open']])
    selling_pressure = sum([1 for c in recent_candles if c['close'] < c['open']])
    
    total_candles = len(recent_candles)
    buy_percentage = (buying_pressure / total_candles) * 100
    sell_percentage = (selling_pressure / total_candles) * 100
    
    # Determine dominant flow
    if buy_percentage > 65:
        dominant_flow = 'strong_buying'
        bias = 'bullish'
    elif sell_percentage > 65:
        dominant_flow = 'strong_selling'
        bias = 'bearish'
    elif buy_percentage > 55:
        dominant_flow = 'moderate_buying'
        bias = 'slightly_bullish'
    elif sell_percentage > 55:
        dominant_flow = 'moderate_selling'
        bias = 'slightly_bearish'
    else:
        dominant_flow = 'balanced'
        bias = 'neutral'
    
    # Calculate delta (net buying/selling)
    delta = buying_pressure - selling_pressure
    
    return {
        'flow': {
            'buying_pressure': round(buy_percentage, 1),
            'selling_pressure': round(sell_percentage, 1),
            'delta': delta,
            'dominant_flow': dominant_flow,
            'bias': bias
        },
        'interpretation': f"Order flow shows {dominant_flow.replace('_', ' ')} - {bias} bias",
        'trading_implication': f"Favor {bias} setups in alignment with order flow"
    }

# ============================================================================
# MULTI-TIMEFRAME ANALYSIS
# ============================================================================

def analyze_higher_timeframe_structure(pair, current_timeframe):
    """
    Analyze Higher Timeframe Structure - HTF context
    
    Trading with HTF bias increases probability of success.
    """
    
    # Map to higher timeframes
    timeframe_hierarchy = {
        '1m': '5m',
        '5m': '15m',
        '15m': '1h',
        '30m': '4h',
        '1h': '4h',
        '4h': '1d',
        '1d': '1w'
    }
    
    htf = timeframe_hierarchy.get(current_timeframe, '1d')
    
    # Mock HTF analysis
    htf_trend = random.choice(['bullish', 'bearish', 'ranging'])
    htf_structure_quality = random.randint(65, 95)
    
    htf_bos_present = random.choice([True, False])
    htf_choch_present = random.choice([True, False]) if not htf_bos_present else False
    
    # Key levels on HTF
    key_support = round(random.uniform(1.05, 1.08), 4)
    key_resistance = round(random.uniform(1.09, 1.12), 4)
    
    alignment_with_ltf = random.choice(['aligned', 'conflicting', 'neutral'])
    
    return {
        'htf': htf,
        'htf_trend': htf_trend,
        'structure_quality': htf_structure_quality,
        'htf_bos': htf_bos_present,
        'htf_choch': htf_choch_present,
        'key_support': key_support,
        'key_resistance': key_resistance,
        'alignment': alignment_with_ltf,
        'interpretation': f"HTF ({htf}) shows {htf_trend} bias with {htf_structure_quality}% structure quality",
        'recommendation': f"{'Trade with' if alignment_with_ltf == 'aligned' else 'Caution:'} HTF bias for best probability"
    }

def identify_confluences(pair, timeframe):
    """
    Identify Multi-Factor Confluences - stacked probabilities
    
    Areas where multiple SMC concepts align create high-probability setups.
    """
    
    # Mock confluence zones
    confluences = []
    num_confluences = random.randint(1, 2)
    
    for i in range(num_confluences):
        confluence_price = round(random.uniform(1.06, 1.10), 4)
        
        # Multiple factors at this level
        possible_factors = [
            'order_block',
            'fvg',
            'liquidity_pool',
            'premium_zone',
            'discount_zone',
            'old_high',
            'old_low',
            'poc',
            'imbalance'
        ]
        
        num_factors = random.randint(3, 5)
        factors = random.sample(possible_factors, num_factors)
        
        confluence_strength = len(factors) * 15 + random.randint(10, 25)
        
        setup_type = 'buy' if 'discount_zone' in factors or 'order_block' in factors else 'sell'
        
        confluences.append({
            'price_level': confluence_price,
            'factors': factors,
            'confluence_strength': min(100, confluence_strength),
            'setup_type': setup_type,
            'interpretation': f"{len(factors)} SMC factors align at {confluence_price}",
            'recommendation': f"High-probability {setup_type} zone - wait for confirmation"
        })
    
    return {
        'confluences': confluences,
        'total_confluences': len(confluences),
        'concept': 'Confluences occur when multiple SMC factors align, creating high-probability zones'
    }

# ============================================================================
# SESSION & TIME-BASED ANALYSIS
# ============================================================================

def analyze_session_characteristics(data):
    """
    Analyze Trading Session Characteristics
    
    Different sessions (Asian, London, NY) have different behaviors.
    """
    
    current_hour = datetime.utcnow().hour
    
    # Determine session
    if 0 <= current_hour < 8:
        session = 'asian'
        characteristics = {
            'volatility': 'low',
            'typical_range_pips': '20-40',
            'best_strategy': 'range_trading',
            'liquidity': 'low'
        }
    elif 8 <= current_hour < 16:
        session = 'london'
        characteristics = {
            'volatility': 'high',
            'typical_range_pips': '60-100',
            'best_strategy': 'breakout_continuation',
            'liquidity': 'high'
        }
    else:
        session = 'newyork'
        characteristics = {
            'volatility': 'very_high',
            'typical_range_pips': '80-120',
            'best_strategy': 'trend_following',
            'liquidity': 'very_high'
        }
    
    # Session overlap bonus
    session_overlap = None
    if 12 <= current_hour < 16:
        session_overlap = 'london_newyork'
        characteristics['note'] = 'High volatility overlap - expect big moves'
    
    return {
        'current_session': session,
        'characteristics': characteristics,
        'session_overlap': session_overlap,
        'recommendation': f"Trade {characteristics['best_strategy']} during {session} session"
    }

def detect_news_impact_zones(pair):
    """
    Detect potential News Impact Zones
    
    Areas where price reacted to fundamental news releases.
    """
    
    # Mock news impact detection
    news_zones = []
    num_zones = random.randint(0, 2)
    
    for i in range(num_zones):
        event_time = datetime.now() - timedelta(hours=random.randint(1, 48))
        impact_level = round(random.uniform(1.07, 1.10), 4)
        
        news_type = random.choice(['central_bank', 'employment', 'inflation', 'gdp'])
        reaction = random.choice(['spike_up', 'spike_down', 'range_expansion'])
        
        news_zones.append({
            'event_time': event_time.isoformat(),
            'news_type': news_type,
            'impact_level': impact_level,
            'reaction': reaction,
            'interpretation': f"{news_type.replace('_', ' ').title()} news caused {reaction.replace('_', ' ')}",
            'trading_note': 'News reaction levels often become support/resistance'
        })
    
    return {
        'news_zones': news_zones,
        'total_zones': len(news_zones),
        'recommendation': 'Be cautious around news impact levels'
    }

# ============================================================================
# ADVANCED CONCEPTS
# ============================================================================

def identify_manipulation_patterns(data):
    """
    Identify Market Manipulation Patterns - stop hunts and traps
    
    Smart money often manipulates retail traders before true moves.
    """
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    
    if len(candles) < 30:
        return {'manipulations': [], 'message': 'Insufficient data'}
    
    manipulations = []
    
    if random.random() > 0.6:
        manipulation_type = random.choice([
            'bull_trap',
            'bear_trap',
            'stop_hunt',
            'false_breakout',
            'wyckoff_spring',
            'wyckoff_upthrust'
        ])
        
        recent_candles = candles[-15:]
        manipulation_candle = recent_candles[random.randint(0, len(recent_candles)-1)]
        
        if 'bull' in manipulation_type or 'spring' in manipulation_type:
            fake_move_direction = 'down'
            true_direction = 'up'
            level = manipulation_candle['low']
        else:
            fake_move_direction = 'up'
            true_direction = 'down'
            level = manipulation_candle['high']
        
        confidence = random.randint(70, 90)
        
        manipulations.append({
            'type': manipulation_type,
            'manipulation_level': round(level, 4),
            'fake_move': fake_move_direction,
            'true_direction': true_direction,
            'confidence': confidence,
            'timestamp': manipulation_candle['timestamp'],
            'interpretation': f"{manipulation_type.replace('_', ' ').title()} - expect move {true_direction}",
            'trading_implication': f"Wait for price to reverse {true_direction} from {round(level, 4)}"
        })
    
    return {
        'manipulations': manipulations,
        'total_manipulations': len(manipulations),
        'concept': 'Smart money manipulates retail stops before true directional moves'
    }

def calculate_institutional_levels(data):
    """
    Calculate Institutional Price Levels - round numbers and psychological levels
    
    Institutions often place orders at round numbers (00, 50 levels).
    """
    
    current_price = data.get('current_price', 0)
    
    # Find nearby round numbers
    price_str = str(current_price)
    base_price = float(price_str[:4])  # e.g., 1.09 from 1.0934
    
    institutional_levels = []
    
    # Major round numbers (00)
    for i in range(-2, 3):
        level = round(base_price + (i * 0.01), 4)
        if level > 0:
            distance_pips = abs(current_price - level) * 10000
            level_type = 'major_round_number'
            strength = random.randint(75, 95)
            
            institutional_levels.append({
                'level': level,
                'type': level_type,
                'strength': strength,
                'distance_pips': round(distance_pips, 1),
                'psychological_impact': 'high'
            })
    
    # Half numbers (50)
    for i in range(-2, 3):
        level = round(base_price + (i * 0.01) + 0.005, 4)
        if level > 0:
            distance_pips = abs(current_price - level) * 10000
            level_type = 'half_round_number'
            strength = random.randint(60, 80)
            
            institutional_levels.append({
                'level': level,
                'type': level_type,
                'strength': strength,
                'distance_pips': round(distance_pips, 1),
                'psychological_impact': 'medium'
            })
    
    # Sort by distance
    institutional_levels.sort(key=lambda x: x['distance_pips'])
    
    return {
        'institutional_levels': institutional_levels[:5],
        'nearest_level': institutional_levels[0] if institutional_levels else None,
        'recommendation': 'Institutions cluster orders at round numbers - expect reactions'
    }

def detect_wyckoff_phases(data):
    """
    Detect Wyckoff Market Phases - accumulation/distribution
    
    Identifies institutional accumulation/distribution patterns.
    """
    
    candles = data.get('candles', [])
    trend = data.get('indicators', {}).get('trend', 'neutral')
    
    if len(candles) < 50:
        return {'phase': None, 'message': 'Insufficient data'}
    
    # Mock Wyckoff phase detection
    if random.random() > 0.5:
        phase_type = random.choice([
            'accumulation',
            'markup',
            'distribution',
            'markdown'
        ])
        
        sub_phase = None
        if phase_type == 'accumulation':
            sub_phase = random.choice(['Phase A', 'Phase B', 'Phase C - Spring', 'Phase D', 'Phase E'])
        elif phase_type == 'distribution':
            sub_phase = random.choice(['Phase A', 'Phase B', 'Phase C - Upthrust', 'Phase D', 'Phase E'])
        
        phase_confidence = random.randint(65, 90)
        
        if phase_type in ['accumulation', 'markup']:
            expected_move = 'bullish'
        else:
            expected_move = 'bearish'
        
        return {
            'phase': {
                'type': phase_type,
                'sub_phase': sub_phase,
                'confidence': phase_confidence,
                'expected_move': expected_move
            },
            'interpretation': f"Wyckoff {phase_type} phase detected - {sub_phase}",
            'trading_implication': f"Position for {expected_move} move from {phase_type}"
        }
    
    return {'phase': None, 'reason': 'No clear Wyckoff phase identified'}

def identify_turtle_soup_setups(data):
    """
    Identify Turtle Soup Patterns - false breakout reversals
    
    When price breaks a level then immediately reverses (stop hunt).
    """
    
    candles = data.get('candles', [])
    current_price = data.get('current_price', 0)
    
    if len(candles) < 30:
        return {'setups': [], 'message': 'Insufficient data'}
    
    setups = []
    
    if random.random() > 0.7:
        setup_type = random.choice(['long', 'short'])
        
        recent_candles = candles[-20:]
        
        if setup_type == 'long':
            # Price broke below support then reversed
            false_break_level = min([c['low'] for c in recent_candles[:10]])
            entry_level = round(false_break_level * 1.0005, 4)
            stop_level = round(false_break_level * 0.9995, 4)
            target_level = round(entry_level + (entry_level - stop_level) * 3, 4)
        else:
            # Price broke above resistance then reversed
            false_break_level = max([c['high'] for c in recent_candles[:10]])
            entry_level = round(false_break_level * 0.9995, 4)
            stop_level = round(false_break_level * 1.0005, 4)
            target_level = round(entry_level - (stop_level - entry_level) * 3, 4)
        
        setup_quality = random.randint(70, 90)
        
        setups.append({
            'type': setup_type,
            'false_break_level': round(false_break_level, 4),
            'entry': entry_level,
            'stop_loss': stop_level,
            'target': target_level,
            'quality': setup_quality,
            'interpretation': f"Turtle Soup {setup_type} - false breakout reversal",
            'risk_reward': 3.0
        })
    
    return {
        'setups': setups,
        'total_setups': len(setups),
        'concept': 'Turtle Soup exploits false breakouts when stops are hunted'
    }

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _generate_order_block_setup(block_type, zone_high, zone_low, current_price):
    """Generate trading setup for an order block"""
    
    if block_type == 'demand':
        entry = round((zone_high + zone_low) / 2, 4)
        stop_loss = round(zone_low * 0.9998, 4)
        take_profit = round(entry + (entry - stop_loss) * 2.5, 4)
        
        return {
            'direction': 'BUY',
            'entry_zone': f"{round(zone_low, 4)} - {round(zone_high, 4)}",
            'entry_price': entry,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'risk_reward': 2.5
        }
    else:
        entry = round((zone_high + zone_low) / 2, 4)
        stop_loss = round(zone_high * 1.0002, 4)
        take_profit = round(entry - (stop_loss - entry) * 2.5, 4)
        
        return {
            'direction': 'SELL',
            'entry_zone': f"{round(zone_low, 4)} - {round(zone_high, 4)}",
            'entry_price': entry,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'risk_reward': 2.5
        }

def _generate_ob_recommendation(order_blocks, current_price, trend):
    """Generate recommendation based on order blocks"""
    
    if not order_blocks:
        return "No clear order blocks identified. Wait for structure formation."
    
    nearest = order_blocks[0]
    
    if nearest['distance_pips'] < 10:
        return f"Price near {nearest['type']} zone at {nearest['price_level']} - watch for reaction"
    elif nearest['type'] == 'demand' and trend == 'bullish':
        return f"Bullish trend with demand zone at {nearest['price_level']} - wait for pullback"
    elif nearest['type'] == 'supply' and trend == 'bearish':
        return f"Bearish trend with supply zone at {nearest['price_level']} - wait for retest"
    else:
        return f"Monitor {nearest['type']} zone at {nearest['price_level']} for potential reversal"