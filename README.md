# 📈 Forex Market Analyzer - Complete SMC Suite

An AI-powered forex analysis system using **Groq LLM** and **Smart Money Concepts** (SMC) with 24+ institutional trading tools.

## 🚀 Features

### **Autonomous AI Analysis**
- Natural language queries interpreted by Groq LLM
- AI decides which analysis functions to call
- Complete execution trace visible
- Multi-model support (Llama 3.3, Mixtral, Gemma)

### **24 Smart Money Concept Functions**

#### 📊 Market Structure (3)
1. **detect_bos()** - Break of Structure
   - Confirms trend continuation
   - Identifies swing high/low breaks
   - Provides confidence levels and entry points

2. **detect_choch()** - Change of Character
   - Signals potential reversals
   - Detects failure to make new high/low
   - Includes strength factors and confirmation

3. **detect_market_structure_break()** - MSB
   - Aggressive structure breaks
   - Strong momentum indicators
   - Extension targets

#### 💧 Liquidity Analysis (3)
4. **detect_liquidity_sweep()** - Stop Hunts
   - Buy-side and sell-side sweeps
   - Reaction analysis (reversal vs continuation)
   - Distance from current price

5. **identify_liquidity_pools()** - Stop Clusters
   - Equal highs/lows identification
   - Density and magnetism scores
   - Price attraction zones

6. **detect_liquidity_void()** - Price Gaps
   - Unfilled price gaps
   - Fill probability calculations
   - Void size and midpoint

#### 📦 Order Blocks & Zones (3)
7. **identify_order_blocks()** - Institutional Zones
   - Demand and supply blocks
   - Strength, validity, freshness ratings
   - Complete trade setups (entry/SL/TP)

8. **identify_fair_value_gaps()** - FVG
   - 3-candle imbalances
   - Bullish and bearish gaps
   - Fill percentage tracking
   - Retest zones

9. **identify_breaker_blocks()** - Flipped Polarity
   - Failed order blocks
   - Demand→Supply, Supply→Demand flips
   - Flip timestamps and strength

#### 💰 Premium/Discount (1)
10. **calculate_premium_discount_zones()** - Value Zones
    - Equilibrium calculations
    - Fibonacci-like zones
    - Current price position
    - Trading bias (buy discount, sell premium)

#### ⚡ Imbalances (2)
11. **detect_imbalances()** - Price Imbalances
    - Rapid price moves
    - Gap identification
    - Rebalance probability

12. **detect_inefficiencies()** - Market Inefficiencies
    - Poorly traded zones
    - Low volume areas
    - Inefficiency scores

#### 📊 Volume & Flow (3)
13. **analyze_volume_profile()** - Volume Analysis
    - Point of Control (POC)
    - Value Area High/Low
    - Volume nodes
    - Position relative to POC

14. **detect_smart_money_divergence()** - Divergence
    - Price vs institution participation
    - Bullish and bearish divergence
    - Hidden divergences
    - Reversal signals

15. **analyze_order_flow()** - Buying/Selling Pressure
    - Order flow delta
    - Dominant flow detection
    - Trading bias calculation
    - Pressure percentages

#### 🔄 Multi-Timeframe (2)
16. **analyze_higher_timeframe_structure()** - HTF Context
    - Higher timeframe trend
    - HTF BOS/CHoCH
    - Key support/resistance
    - Alignment with lower timeframe

17. **identify_confluences()** - Multi-Factor Zones
    - 3-5 SMC factors aligned
    - Confluence strength scoring
    - High-probability setups
    - Stacked probabilities

#### ⏰ Session & Time (2)
18. **analyze_session_characteristics()** - Session Analysis
    - Asian, London, NY behaviors
    - Volatility patterns
    - Best strategies per session
    - Session overlap identification

19. **detect_news_impact_zones()** - News Levels
    - Fundamental event reactions
    - Impact levels
    - News type classification
    - Support/resistance from news

#### 🎯 Advanced Concepts (5)
20. **identify_manipulation_patterns()** - Market Manipulation
    - Bull/bear traps
    - Stop hunts
    - False breakouts
    - Wyckoff springs/upthrusts

21. **calculate_institutional_levels()** - Round Numbers
    - Major round numbers (00)
    - Half numbers (50)
    - Psychological levels
    - Institutional order clustering

22. **detect_wyckoff_phases()** - Wyckoff Method
    - Accumulation/distribution
    - Sub-phase identification (A, B, C, D, E)
    - Expected moves
    - Institutional positioning

23. **identify_turtle_soup_setups()** - False Breakouts
    - Stop hunt reversals
    - Entry/SL/TP levels
    - 3:1 risk/reward setups
    - Setup quality scores

24. **get_forex_data()** - Market Data
    - OHLCV data (100 candles)
    - RSI, ATR indicators
    - Trend detection
    - Support/resistance
    - Market context (session, volatility)

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- Free Groq API key

### Setup Steps

1. **Clone/Download the project:**
```bash
git clone <your-repo>
cd forex_analyzer
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Get Groq API Key:**
   - Visit https://console.groq.com
   - Create free account
   - Generate API key

4. **Configure secrets:**
Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

5. **Run the app:**
```bash
streamlit run app.py
```

## 📖 Usage Guide

### Basic Queries
```
"Analyze EURUSD on 1H timeframe"
"What's the trend on GBPUSD 4H?"
"Give me a trade setup for USDJPY 15m"
```

### Specific SMC Analysis
```
"Find order blocks on AUDUSD 1H"
"Detect liquidity sweeps on EURUSD 4H"
"Show me Fair Value Gaps on GBPJPY 1H"
"Is there a CHoCH on USDJPY 30m?"
"Find confluences on EURUSD 1H"
```

### Advanced Analysis
```
"Comprehensive SMC analysis EURUSD 1H"
"Find manipulation patterns GBPUSD 15m"
"Wyckoff phase analysis USDJPY 4H"
"Multi-timeframe analysis AUDUSD 1H"
"Premium/discount zones EURJPY 1H"
```

### How It Works
1. You enter a natural language query
2. Groq LLM interprets your request
3. AI decides which SMC functions to call
4. Functions execute and return results
5. LLM synthesizes all data
6. You receive a complete analysis with trade setup

## 🎯 Smart Money Concepts Explained

### Core Principles
- **BOS (Break of Structure)**: Price breaks previous swing → Trend continues
- **CHoCH (Change of Character)**: Structure fails → Potential reversal
- **Order Blocks**: Where institutions entered → Strong zones
- **Liquidity**: Stop clusters → Price magnets
- **Premium/Discount**: Overvalued vs undervalued areas
- **FVG (Fair Value Gaps)**: Price imbalances → Fill zones
- **Confluences**: Multiple factors align → High probability

### Trading Philosophy
1. Trade with higher timeframe bias
2. Buy in discount zones, sell in premium zones
3. Enter at order blocks with confluence
4. Use liquidity as targets/entry triggers
5. Wait for manipulation before true moves
6. Prioritize risk management (always)

## 🔧 Customization

### Adding Real Polygon.io Data
Replace mock data in `utils/polygon_mock.py`:

```python
from polygon import RESTClient

def get_forex_data(pair, timeframe):
    client = RESTClient(api_key)
    # Convert timeframe to Polygon format
    multiplier, timespan = parse_timeframe(timeframe)
    
    # Fetch real data
    aggs = client.get_aggs(
        f"C:{pair}",
        multiplier,
        timespan,
        from_date,
        to_date
    )
    
    # Process and return
    return process_polygon_data(aggs)
```

### Adding New SMC Functions
1. Add function to `utils/smc_functions.py`
2. Import in `app.py`
3. Add to `AVAILABLE_FUNCTIONS` dict
4. Add schema to `FUNCTION_SCHEMAS` list
5. Update system prompt to mention it

## 📊 Project Structure

```
forex_analyzer/
├── app.py                      # Main Streamlit app
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── secrets.toml           # API keys (create this)
├── utils/
│   ├── polygon_mock.py        # Mock data generator
│   └── smc_functions.py       # 24 SMC analysis functions
└── README.md                   # This file
```

## 🤖 Supported Models

- **llama-3.3-70b-versatile** (Recommended)
- llama-3.1-70b-versatile
- mixtral-8x7b-32768
- gemma2-9b-it

## 🎓 Learning Resources

### Smart Money Concepts
- Break of Structure (BOS)
- Change of Character (CHoCH)
- Order Blocks (OB)
- Fair Value Gaps (FVG)
- Liquidity Pools & Sweeps
- Premium/Discount Zones
- Wyckoff Method
- Market Manipulation

### Recommended Study
1. Understand market structure first
2. Learn liquidity concepts
3. Master order blocks and FVGs
4. Study multi-timeframe analysis
5. Practice identifying confluences

## ⚠️ Disclaimer

**This is an educational tool using MOCK DATA.**
- Not financial advice
- For learning purposes only
- Always practice risk management
- Test strategies on demo accounts first
- Never risk more than you can afford to lose

## 🔮 Future Enhancements

### Planned Features
- [ ] Real-time Polygon.io integration
- [ ] Backtesting engine
- [ ] Chart visualization
- [ ] Trade journal
- [ ] Alert system
- [ ] Performance analytics
- [ ] Machine learning price predictions
- [ ] Multi-pair correlation analysis

### Easy Extensions
- Add more forex pairs
- Include crypto/stocks support
- Custom indicator integration
- Email/SMS alerts
- PDF report generation
- Cloud deployment (Streamlit Cloud)

## 🤝 Contributing

Contributions welcome! Areas to improve:
- More SMC functions
- Better mock data realism
- UI/UX enhancements
- Documentation
- Testing suite

## 📝 License

MIT License - Use freely for learning and development

## 💬 Support

For questions or issues:
1. Check this README
2. Review code comments
3. Test with example queries
4. Consult Groq documentation
5. Study SMC concepts online

## 🎉 Credits

Built with:
- **Streamlit** - Web framework
- **Groq** - LLM inference
- **Smart Money Concepts** - Trading methodology

---

**Happy Trading! 📈**

*Remember: The best trades are the ones you don't take when conditions aren't right.*