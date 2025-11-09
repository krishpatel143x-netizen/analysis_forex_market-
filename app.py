"""
Forex Market Analyzer with Groq LLM and Smart Money Concepts
============================================================

SETUP INSTRUCTIONS:
1. Install requirements: pip install -r requirements.txt
2. Get free Groq API key from: https://console.groq.com
3. Create .streamlit/secrets.toml with: GROQ_API_KEY = "your_key_here"
4. Run: streamlit run app.py

This app uses Groq's function calling to autonomously analyze forex markets
using Smart Money Concepts (SMC) methodology.
"""

import streamlit as st
import json
from groq import Groq

# Import mock data function
from utils.polygon_mock import get_forex_data

# Import all SMC functions
from utils.smc_functions import (
    # Market Structure
    detect_bos, detect_choch, detect_market_structure_break,
    # Liquidity
    detect_liquidity_sweep, identify_liquidity_pools, detect_liquidity_void,
    # Order Blocks & FVG
    identify_order_blocks, identify_fair_value_gaps, identify_breaker_blocks,
    # Premium/Discount
    calculate_premium_discount_zones,
    # Imbalances
    detect_imbalances, detect_inefficiencies,
    # Volume & Flow
    analyze_volume_profile, detect_smart_money_divergence, analyze_order_flow,
    # Multi-Timeframe
    analyze_higher_timeframe_structure, identify_confluences,
    # Session & Time
    analyze_session_characteristics, detect_news_impact_zones,
    # Advanced
    identify_manipulation_patterns, calculate_institutional_levels,
    detect_wyckoff_phases, identify_turtle_soup_setups
)    

# Page configuration
st.set_page_config(
    page_title="Forex Market Analyzer",
    page_icon="📈",
    layout="wide"
)

# Initialize Groq client
@st.cache_resource
def get_groq_client():
    """Initialize Groq client with API key from secrets"""
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Error loading Groq API key: {e}")
        st.info("Please add GROQ_API_KEY to .streamlit/secrets.toml")
        return None

# System prompt for Groq LLM - COMPLETE SMC ANALYST
SYSTEM_PROMPT = """You are an elite forex analyst and expert in Smart Money Concepts (SMC) with access to a comprehensive suite of analysis tools. 
Your role is to analyze forex markets using institutional trading concepts and provide actionable trading recommendations.

ANALYSIS WORKFLOW:
1. ALWAYS call get_forex_data() FIRST to retrieve market data for the requested pair and timeframe
2. Based on the user's query and market conditions, intelligently select from these analysis functions:

MARKET STRUCTURE ANALYSIS:
- detect_bos(): Break of Structure (trend continuation)
- detect_choch(): Change of Character (trend reversal)
- detect_market_structure_break(): Aggressive structure breaks (strong momentum)

LIQUIDITY ANALYSIS:
- detect_liquidity_sweep(): Stop hunts above/below key levels
- identify_liquidity_pools(): Areas with concentrated stop losses
- detect_liquidity_void(): Price gaps that often get filled

ORDER BLOCKS & ZONES:
- identify_order_blocks(): Institutional demand/supply zones
- identify_fair_value_gaps(): 3-candle imbalances (FVG)
- identify_breaker_blocks(): Failed order blocks that flip polarity

PREMIUM/DISCOUNT:
- calculate_premium_discount_zones(): Determine if price is overvalued/undervalued

IMBALANCES:
- detect_imbalances(): Rapid price moves leaving gaps
- detect_inefficiencies(): Poorly traded zones

VOLUME & FLOW:
- analyze_volume_profile(): POC and value area
- detect_smart_money_divergence(): Price vs institution participation
- analyze_order_flow(): Buying vs selling pressure

MULTI-TIMEFRAME:
- analyze_higher_timeframe_structure(): HTF context and bias
- identify_confluences(): Multiple SMC factors aligned

SESSION & TIME:
- analyze_session_characteristics(): Asian/London/NY behaviors
- detect_news_impact_zones(): Fundamental event reactions

ADVANCED CONCEPTS:
- identify_manipulation_patterns(): Stop hunts, traps, false breakouts
- calculate_institutional_levels(): Round numbers and psychological levels
- detect_wyckoff_phases(): Accumulation/distribution patterns
- identify_turtle_soup_setups(): False breakout reversals

SMART MONEY CONCEPTS PRINCIPLES:
- BOS confirms trend, CHoCH signals reversal
- Trade from order blocks (demand = buy, supply = sell)
- Buy in discount zones, sell in premium zones
- Liquidity sweeps often precede reversals
- FVGs and imbalances act as magnets
- Higher timeframe bias increases probability
- Confluences create high-probability setups
- Smart money manipulates retail before true moves

ANALYSIS APPROACH:
- Don't call every function - be selective based on the query
- If user asks for specific analysis (e.g., "find order blocks"), focus on that
- For comprehensive analysis, use 4-6 relevant functions
- Always prioritize higher timeframe context when available
- Look for confluences (multiple factors aligning)

OUTPUT FORMAT:
Provide your analysis in this structure:
1. **Market Context**: Trend, session, volatility, HTF bias
2. **Key SMC Findings**: Most important signals from your analysis
3. **Trade Setup**:
   - Direction: BUY/SELL or NO TRADE
   - Entry: Specific price level with reasoning
   - Stop Loss: Price level with reasoning
   - Take Profit: Price level(s) with reasoning
   - Risk/Reward Ratio
4. **Reasoning**: Explain using SMC principles, mention confluences
5. **Risk Factors**: What could invalidate the setup

Be precise with price levels, always prioritize risk management, and explain your reasoning clearly using SMC terminology."""

# Define available functions for Groq - ALL SMC FUNCTIONS
AVAILABLE_FUNCTIONS = {
    # Data
    "get_forex_data": get_forex_data,
    # Market Structure
    "detect_bos": detect_bos,
    "detect_choch": detect_choch,
    "detect_market_structure_break": detect_market_structure_break,
    # Liquidity
    "detect_liquidity_sweep": detect_liquidity_sweep,
    "identify_liquidity_pools": identify_liquidity_pools,
    "detect_liquidity_void": detect_liquidity_void,
    # Order Blocks & FVG
    "identify_order_blocks": identify_order_blocks,
    "identify_fair_value_gaps": identify_fair_value_gaps,
    "identify_breaker_blocks": identify_breaker_blocks,
    # Premium/Discount
    "calculate_premium_discount_zones": calculate_premium_discount_zones,
    # Imbalances
    "detect_imbalances": detect_imbalances,
    "detect_inefficiencies": detect_inefficiencies,
    # Volume & Flow
    "analyze_volume_profile": analyze_volume_profile,
    "detect_smart_money_divergence": detect_smart_money_divergence,
    "analyze_order_flow": analyze_order_flow,
    # Multi-Timeframe
    "analyze_higher_timeframe_structure": analyze_higher_timeframe_structure,
    "identify_confluences": identify_confluences,
    # Session & Time
    "analyze_session_characteristics": analyze_session_characteristics,
    "detect_news_impact_zones": detect_news_impact_zones,
    # Advanced
    "identify_manipulation_patterns": identify_manipulation_patterns,
    "calculate_institutional_levels": calculate_institutional_levels,
    "detect_wyckoff_phases": detect_wyckoff_phases,
    "identify_turtle_soup_setups": identify_turtle_soup_setups
}

# Function schemas for Groq - COMPLETE SMC TOOLKIT
FUNCTION_SCHEMAS = [
    # ========== DATA RETRIEVAL ==========
    {
        "type": "function",
        "function": {
            "name": "get_forex_data",
            "description": "Retrieves forex market data including OHLCV, indicators, and market context. ALWAYS call this first before any analysis.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pair": {"type": "string", "description": "Forex pair symbol (e.g., 'EURUSD', 'GBPUSD', 'USDJPY')"},
                    "timeframe": {"type": "string", "description": "Chart timeframe", "enum": ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]}
                },
                "required": ["pair", "timeframe"]
            }
        }
    },
    
    # ========== MARKET STRUCTURE ==========
    {
        "type": "function",
        "function": {
            "name": "detect_bos",
            "description": "Detects Break of Structure - confirms trend direction and continuation signals. Shows when price breaks previous swing high/low.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"},
                    "timeframe": {"type": "string", "description": "Timeframe being analyzed"}
                },
                "required": ["data", "timeframe"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "detect_choch",
            "description": "Detects Change of Character - identifies potential trend reversals. Shows when trend structure fails.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "detect_market_structure_break",
            "description": "Detects Market Structure Break (MSB) - aggressive break of structure indicating strong momentum.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    
    # ========== LIQUIDITY ANALYSIS ==========
    {
        "type": "function",
        "function": {
            "name": "detect_liquidity_sweep",
            "description": "Detects liquidity sweeps - when smart money hunts stops above/below key levels before reversing.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "identify_liquidity_pools",
            "description": "Identifies liquidity pools - areas with concentrated stop losses where price often reverses.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "detect_liquidity_void",
            "description": "Detects liquidity voids - price gaps with no trading activity that often get filled.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    
    # ========== ORDER BLOCKS & FVG ==========
    {
        "type": "function",
        "function": {
            "name": "identify_order_blocks",
            "description": "Identifies institutional order blocks (demand/supply zones) where institutions placed large orders.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "identify_fair_value_gaps",
            "description": "Identifies Fair Value Gaps (FVG) - 3-candle imbalances showing inefficient price movement.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "identify_breaker_blocks",
            "description": "Identifies breaker blocks - failed order blocks that flip polarity (demand becomes supply, vice versa).",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    
    # ========== PREMIUM/DISCOUNT ==========
    {
        "type": "function",
        "function": {
            "name": "calculate_premium_discount_zones",
            "description": "Calculates premium/discount zones using equilibrium - determines if price is overvalued or undervalued.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    
    # ========== IMBALANCES ==========
    {
        "type": "function",
        "function": {
            "name": "detect_imbalances",
            "description": "Detects price imbalances - rapid moves leaving gaps that price often revisits.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "detect_inefficiencies",
            "description": "Detects market inefficiencies - poorly traded zones with low volume that get revisited.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    
    # ========== VOLUME & FLOW ==========
    {
        "type": "function",
        "function": {
            "name": "analyze_volume_profile",
            "description": "Analyzes volume profile - identifies where most trading occurred (POC, value area).",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "detect_smart_money_divergence",
            "description": "Detects smart money divergence - when price makes new highs/lows but institutions aren't participating.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_order_flow",
            "description": "Analyzes order flow - determines buying vs selling pressure and who's in control.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    
    # ========== MULTI-TIMEFRAME ==========
    {
        "type": "function",
        "function": {
            "name": "analyze_higher_timeframe_structure",
            "description": "Analyzes higher timeframe structure - provides HTF context and bias for better trade probability.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pair": {"type": "string", "description": "Forex pair being analyzed"},
                    "current_timeframe": {"type": "string", "description": "Current timeframe to get HTF context"}
                },
                "required": ["pair", "current_timeframe"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "identify_confluences",
            "description": "Identifies multi-factor confluences - areas where multiple SMC concepts align for high-probability setups.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pair": {"type": "string", "description": "Forex pair being analyzed"},
                    "timeframe": {"type": "string", "description": "Timeframe being analyzed"}
                },
                "required": ["pair", "timeframe"]
            }
        }
    },
    
    # ========== SESSION & TIME ==========
    {
        "type": "function",
        "function": {
            "name": "analyze_session_characteristics",
            "description": "Analyzes trading session characteristics - different behaviors for Asian, London, NY sessions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "detect_news_impact_zones",
            "description": "Detects news impact zones - price levels where fundamental news caused reactions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pair": {"type": "string", "description": "Forex pair being analyzed"}
                },
                "required": ["pair"]
            }
        }
    },
    
    # ========== ADVANCED CONCEPTS ==========
    {
        "type": "function",
        "function": {
            "name": "identify_manipulation_patterns",
            "description": "Identifies market manipulation patterns - stop hunts, traps, and false breakouts before true moves.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_institutional_levels",
            "description": "Calculates institutional price levels - round numbers and psychological levels where institutions place orders.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "detect_wyckoff_phases",
            "description": "Detects Wyckoff market phases - accumulation, markup, distribution, markdown patterns.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "identify_turtle_soup_setups",
            "description": "Identifies Turtle Soup patterns - false breakout reversals when stops are hunted.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Market data from get_forex_data()"}
                },
                "required": ["data"]
            }
        }
    }
]

def execute_function_call(function_name, function_args):
    """Execute a function call and return the result"""
    if function_name not in AVAILABLE_FUNCTIONS:
        return {"error": f"Function {function_name} not found"}
    
    try:
        function = AVAILABLE_FUNCTIONS[function_name]
        result = function(**function_args)
        return result
    except Exception as e:
        return {"error": str(e)}

def run_analysis(query, model, client):
    """Run the complete analysis using Groq function calling"""
    
    # Initialize conversation
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query}
    ]
    
    execution_log = []
    max_iterations = 10  # Prevent infinite loops
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        try:
            # Call Groq API
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=FUNCTION_SCHEMAS,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=4000
            )
            
            response_message = response.choices[0].message
            
            # Check if we're done (no tool calls)
            if not response_message.tool_calls:
                # Final response from LLM
                execution_log.append({
                    "type": "final_response",
                    "content": response_message.content
                })
                return execution_log, response_message.content
            
            # Process tool calls
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Log the function call
                execution_log.append({
                    "type": "function_call",
                    "function": function_name,
                    "arguments": function_args
                })
                
                # Execute the function
                function_result = execute_function_call(function_name, function_args)
                
                # Log the result
                execution_log.append({
                    "type": "function_result",
                    "function": function_name,
                    "result": function_result
                })
                
                # Add result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(function_result)
                })
        
        except Exception as e:
            error_msg = f"Error in iteration {iteration}: {str(e)}"
            execution_log.append({
                "type": "error",
                "message": error_msg
            })
            return execution_log, f"Analysis error: {error_msg}"
    
    # If we hit max iterations
    return execution_log, "Analysis exceeded maximum iterations. Please try again with a simpler query."

# Main UI
st.title("📈 Forex Market Analyzer")
st.markdown("**Powered by Groq LLM + Smart Money Concepts**")

# Sidebar with examples and info
with st.sidebar:
    st.header("📚 Example Queries")
    
    st.subheader("🎯 Basic Analysis")
    basic_queries = [
        "Analyze EURUSD on 1H timeframe",
        "What's the trend on GBPUSD 4H?",
        "Give me a trade setup for USDJPY 15m"
    ]
    for example in basic_queries:
        if st.button(example, key=example):
            st.session_state.query = example
    
    st.subheader("🔍 Specific SMC Analysis")
    smc_queries = [
        "Find order blocks on AUDUSD 1H",
        "Detect liquidity sweeps on EURUSD 4H",
        "Show me Fair Value Gaps on GBPJPY 1H",
        "Is there a CHoCH on USDJPY 30m?",
        "Find confluences on EURUSD 1H"
    ]
    for example in smc_queries:
        if st.button(example, key=example):
            st.session_state.query = example
    
    st.subheader("⚡ Advanced Analysis")
    advanced_queries = [
        "Comprehensive SMC analysis EURUSD 1H",
        "Find manipulation patterns GBPUSD 15m",
        "Wyckoff phase analysis USDJPY 4H",
        "Multi-timeframe analysis AUDUSD 1H",
        "Premium/discount zones EURJPY 1H"
    ]
    for example in advanced_queries:
        if st.button(example, key=example):
            st.session_state.query = example
    
    st.divider()
    
    st.header("⚙️ Setup")
    st.markdown("""
    **Get Free Groq API Key:**
    1. Visit [console.groq.com](https://console.groq.com)
    2. Create account (free)
    3. Generate API key
    4. Add to `.streamlit/secrets.toml`:
    ```toml
    GROQ_API_KEY = "your_key_here"
    ```
    """)
    
    st.divider()
    
    st.header("🎯 SMC Concepts Available")
    with st.expander("Market Structure", expanded=False):
        st.markdown("""
        - **BOS**: Break of Structure
        - **CHoCH**: Change of Character
        - **MSB**: Market Structure Break
        """)
    
    with st.expander("Liquidity", expanded=False):
        st.markdown("""
        - **Liquidity Sweeps**: Stop hunts
        - **Liquidity Pools**: Stop clusters
        - **Liquidity Voids**: Price gaps
        """)
    
    with st.expander("Zones & Blocks", expanded=False):
        st.markdown("""
        - **Order Blocks**: Institutional zones
        - **FVG**: Fair Value Gaps
        - **Breaker Blocks**: Flipped polarity
        - **Premium/Discount**: Value zones
        """)
    
    with st.expander("Advanced", expanded=False):
        st.markdown("""
        - **Wyckoff Phases**: Accumulation/Distribution
        - **Manipulation**: Traps & Stop Hunts
        - **Confluences**: Multiple factors
        - **Institutional Levels**: Round numbers
        """)
    
    st.divider()
    
    st.caption(f"📊 Total SMC Functions: **24**")
    st.caption("🤖 Powered by Groq LLM")

# Initialize Groq client
client = get_groq_client()

if client is None:
    st.stop()

# Main input area
col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_area(
        "Enter your analysis query:",
        value=st.session_state.get('query', ''),
        height=100,
        placeholder="Example: Analyze EURUSD on 1H timeframe"
    )

with col2:
    model = st.selectbox(
        "Select Model:",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ]
    )
    
    analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)

# Run analysis
if analyze_button and query:
    with st.spinner("🤖 AI Analyst is working..."):
        try:
            execution_log, final_analysis = run_analysis(query, model, client)
            
            # Display results
            st.success("✅ Analysis Complete!")
            
            # Execution trace
            with st.expander("🔍 Execution Trace (Click to expand)", expanded=False):
                for i, log_entry in enumerate(execution_log):
                    if log_entry["type"] == "function_call":
                        st.markdown(f"**Step {i+1}: Calling `{log_entry['function']}`**")
                        st.json(log_entry["arguments"])
                    
                    elif log_entry["type"] == "function_result":
                        st.markdown(f"**Result from `{log_entry['function']}`:**")
                        st.json(log_entry["result"])
                        st.divider()
                    
                    elif log_entry["type"] == "error":
                        st.error(f"❌ {log_entry['message']}")
            
            # Final analysis
            st.markdown("### 📊 Final Analysis")
            st.markdown(final_analysis)
            
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            st.info("Please check your API key and try again.")

elif analyze_button:
    st.warning("Please enter a query first!")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
Built with Streamlit + Groq | Using Mock Data | Ready for Polygon.io Integration
</div>
""", unsafe_allow_html=True)