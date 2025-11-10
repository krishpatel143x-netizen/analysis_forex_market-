"""
Forex Market Analyzer with Groq LLM and Smart Money Concepts
============================================================
"""

import streamlit as st
import json
from groq import Groq

# Import real Polygon API (with fallback to mock)
try:
    from utils.polygon_api import get_forex_data
    st.sidebar.success("✅ Using Real Polygon.io Data")
except ImportError:
    from utils.polygon_mock import get_forex_data
    st.sidebar.warning("⚠️ Using Mock Data (Install polygon-api-client)")

# Import all SMC functions
from utils.smc_functions import *

# Page configuration
st.set_page_config(page_title="Forex Market Analyzer", page_icon="📈", layout="wide")

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


# ------------------------- SYSTEM PROMPT --------------------------
SYSTEM_PROMPT = """You are an elite forex analyst... (same as before, trimmed for brevity)"""
# keep your original full SYSTEM_PROMPT text here


# ------------------------- FUNCTION SCHEMAS ------------------------
FUNCTION_SCHEMAS = [
    # ... (everything you already had above)

    # ✅ Complete the last unfinished one:
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
            "description": "Identifies Turtle Soup setups - false breakout reversals based on liquidity grab logic.",
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


# ------------------------- STREAMLIT UI ----------------------------

st.title("📈 Forex Market Analyzer (Groq + Smart Money Concepts)")
st.write("Analyze forex pairs using institutional logic (SMC) powered by Groq LLM.")

pair = st.selectbox("Select Forex Pair", ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"])
timeframe = st.selectbox("Select Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d"])
query = st.text_area("Enter your analysis request", 
                     "Analyze today's EURUSD market structure, liquidity, and possible smart money setup.")

if st.button("🔍 Run Analysis"):
    client = get_groq_client()
    if not client:
        st.stop()

    st.info("Fetching market data...")
    try:
        data = get_forex_data(pair=pair, timeframe=timeframe)
        st.success(f"Market data retrieved for {pair} ({timeframe})")
    except Exception as e:
        st.error(f"Data retrieval failed: {e}")
        st.stop()

    st.info("Analyzing with Groq LLM...")

    try:
        # Groq LLM call
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ],
            tools=FUNCTION_SCHEMAS,
            tool_choice="auto"
        )

        # Show raw model output
        st.subheader("🧠 LLM Response")
        st.write(response.choices[0].message.content)

        # Parse and pretty display
        st.json(response.model_dump(), expanded=False)

    except Exception as e:
        st.error(f"Error during Groq LLM call: {e}")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Groq LLM + Streamlit + Smart Money Concepts Toolkit")