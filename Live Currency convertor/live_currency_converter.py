import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="💱 Professional Currency Converter",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    session_defaults = {
        "from_currency": "USD",
        "to_currency": "INR",
        "conversion_history": [],
        "favorite_pairs": [],
        "last_update": None,
        "cached_rates": {},
        "show_chart": False
    }
    
    for key, default_value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

initialize_session_state()

def load_custom_css():
    """Load custom CSS styling"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .main {
            font-family: 'Inter', sans-serif;
        }
        
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white !important;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: white !important;
        }
        
        .main-subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
            font-weight: 300;
            color: white !important;
        }
        
        .conversion-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            border: 1px solid #e1e5e9;
            margin-bottom: 2rem;
            backdrop-filter: blur(10px);
        }
        
        @media (prefers-color-scheme: dark) {
            .conversion-card {
                background: rgba(40, 44, 52, 0.95);
                border: 1px solid #4a5568;
                color: #e2e8f0;
            }
        }
        
        .result-card {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white !important;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 8px 25px rgba(79, 172, 254, 0.3);
        }
        
        .result-amount {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: white !important;
        }
        
        .result-rate {
            font-size: 1.1rem;
            opacity: 0.9;
            color: white !important;
        }
        
        .metric-card {
            background: rgba(255, 255, 255, 0.9);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 3px 15px rgba(0,0,0,0.08);
            border: 1px solid #e1e5e9;
            text-align: center;
            backdrop-filter: blur(5px);
        }
        
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #2c3e50;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #7f8c8d;
            margin-top: 0.5rem;
        }
        
        @media (prefers-color-scheme: dark) {
            .metric-card {
                background: rgba(45, 55, 72, 0.9);
                border: 1px solid #4a5568;
            }
            
            .metric-value {
                color: #e2e8f0;
            }
            
            .metric-label {
                color: #a0aec0;
            }
        }
        
        .developer-section {
            background: linear-gradient(135deg, #2C3E50, #34495E);
            color: white !important;
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            text-align: center;
            border: 2px solid #3498DB;
        }
        
        .developer-name {
            font-size: 2rem;
            font-weight: 700;
            color: #3498DB !important;
            margin-bottom: 10px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        
        .linkedin-button {
            display: inline-block;
            background: linear-gradient(45deg, #0077B5, #005885);
            color: white !important;
            padding: 12px 25px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            font-size: 16px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,119,181,0.3);
        }
        
        .linkedin-button:hover {
            background: linear-gradient(45deg, #005885, #0077B5);
            color: white !important;
            text-decoration: none;
            box-shadow: 0 6px 20px rgba(0,119,181,0.4);
            transform: translateY(-2px);
        }
        
        .stSelectbox > div > div {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 8px !important;
        }
        
        .stNumberInput > div > div {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 8px !important;
        }
        
        @media (prefers-color-scheme: dark) {
            .stSelectbox > div > div {
                background-color: rgba(45, 55, 72, 0.9) !important;
                border: 2px solid #4a5568 !important;
                color: #e2e8f0 !important;
            }
            
            .stNumberInput > div > div {
                background-color: rgba(45, 55, 72, 0.9) !important;
                border: 2px solid #4a5568 !important;
                color: #e2e8f0 !important;
            }
        }
        
        @media (max-width: 768px) {
            .main-title {
                font-size: 2rem;
            }
            .result-amount {
                font-size: 2rem;
            }
            .developer-name {
                font-size: 1.5rem;
            }
            .conversion-card, .result-card, .developer-section {
                padding: 1.5rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

load_custom_css()

# Currency data with symbols and flags
CURRENCY_DATA = {
    "USD": {"name": "US Dollar", "symbol": "$", "flag": "🇺🇸"},
    "EUR": {"name": "Euro", "symbol": "€", "flag": "🇪🇺"},
    "GBP": {"name": "British Pound", "symbol": "£", "flag": "🇬🇧"},
    "JPY": {"name": "Japanese Yen", "symbol": "¥", "flag": "🇯🇵"},
    "INR": {"name": "Indian Rupee", "symbol": "₹", "flag": "🇮🇳"},
    "AUD": {"name": "Australian Dollar", "symbol": "A$", "flag": "🇦🇺"},
    "CAD": {"name": "Canadian Dollar", "symbol": "C$", "flag": "🇨🇦"},
    "CHF": {"name": "Swiss Franc", "symbol": "Fr", "flag": "🇨🇭"},
    "CNY": {"name": "Chinese Yuan", "symbol": "¥", "flag": "🇨🇳"},
    "SGD": {"name": "Singapore Dollar", "symbol": "S$", "flag": "🇸🇬"},
    "AED": {"name": "UAE Dirham", "symbol": "د.إ", "flag": "🇦🇪"},
    "SAR": {"name": "Saudi Riyal", "symbol": "﷼", "flag": "🇸🇦"},
    "KRW": {"name": "South Korean Won", "symbol": "₩", "flag": "🇰🇷"},
    "BRL": {"name": "Brazilian Real", "symbol": "R$", "flag": "🇧🇷"},
    "RUB": {"name": "Russian Ruble", "symbol": "₽", "flag": "🇷🇺"}
}

def get_currency_display_name(currency_code):
    """Get formatted currency display name"""
    currency_info = CURRENCY_DATA.get(currency_code, {"name": currency_code, "flag": ""})
    return f"{currency_info['flag']} {currency_code} - {currency_info['name']}"

def format_currency(amount, currency_code):
    """Format currency amount with proper symbol"""
    currency_info = CURRENCY_DATA.get(currency_code, {"symbol": currency_code})
    symbol = currency_info["symbol"]
    
    if currency_code in ["JPY", "KRW"]:
        return f"{symbol}{amount:,.0f}"
    else:
        return f"{symbol}{amount:,.2f}"

def add_to_history(from_currency, to_currency, amount, converted_amount, rate):
    """Add conversion to history"""
    conversion = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount,
        "converted_amount": converted_amount,
        "rate": rate
    }
    
    st.session_state.conversion_history.insert(0, conversion)
    
    if len(st.session_state.conversion_history) > 50:
        st.session_state.conversion_history = st.session_state.conversion_history[:50]

@st.cache_data(ttl=300, show_spinner=False)
def fetch_exchange_rates(base_currency):
    """Fetch exchange rates with fallback"""
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        st.session_state.last_update = datetime.now()
        return data
    except requests.exceptions.RequestException as e:
        st.warning(f"API request failed. Using fallback data.")
        
        # Fallback mock rates
        mock_rates = {
            "USD": 1.0, "EUR": 0.85, "GBP": 0.73, "JPY": 110.0,
            "INR": 83.5, "AUD": 1.35, "CAD": 1.25, "CHF": 0.92,
            "CNY": 6.45, "SGD": 1.35, "AED": 3.67, "SAR": 3.75,
            "KRW": 1200.0, "BRL": 5.2, "RUB": 75.0
        }
        
        if base_currency != "USD":
            base_rate = mock_rates.get(base_currency, 1.0)
            adjusted_rates = {k: v / base_rate for k, v in mock_rates.items()}
            return {"rates": adjusted_rates}
        
        return {"rates": mock_rates}
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return {"rates": {}}

@st.cache_data(ttl=3600, show_spinner=False)
def get_historical_data(from_currency, to_currency, days=30):
    """Generate historical data for visualization"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        np.random.seed(42)
        
        # Base rates for common currency pairs
        base_rates = {
            ("USD", "INR"): 83.5,
            ("EUR", "USD"): 1.18,
            ("GBP", "USD"): 1.37,
            ("USD", "JPY"): 110.0,
            ("USD", "EUR"): 0.85,
            ("USD", "GBP"): 0.73
        }
        
        base_rate = base_rates.get((from_currency, to_currency), 1.0)
        
        # Generate realistic rate fluctuations
        daily_changes = np.random.normal(0, 0.015, size=len(dates))
        cumulative_changes = np.cumsum(daily_changes)
        rates = base_rate * (1 + cumulative_changes * 0.08)
        
        # Add trend and seasonal components
        trend = np.linspace(-0.02, 0.03, len(dates))
        seasonal = 0.008 * np.sin(np.arange(len(dates)) * 2 * np.pi / 7)
        rates = rates + base_rate * (trend + seasonal)
        
        return pd.DataFrame({
            'date': dates,
            'rate': rates,
            'volume': np.random.randint(800000, 4000000, size=len(dates)),
            'high': rates * (1 + np.random.uniform(0.002, 0.012, size=len(dates))),
            'low': rates * (1 - np.random.uniform(0.002, 0.012, size=len(dates))),
            'change_pct': np.concatenate([[0], np.diff(rates) / rates[:-1] * 100])
        })
    except Exception as e:
        st.error(f"Error generating historical data: {e}")
        return pd.DataFrame()

def create_line_chart(data, from_currency, to_currency):
    """Create line chart for exchange rates"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['rate'],
        mode='lines+markers',
        name=f'{from_currency}/{to_currency}',
        line=dict(color='#667eea', width=3, shape='spline'),
        marker=dict(size=6, color='#667eea', symbol='circle', line=dict(width=2, color='white')),
        hovertemplate=(
            '<b>%{fullData.name}</b><br>'
            'Date: %{x|%B %d, %Y}<br>'
            'Rate: %{y:.4f}<br>'
            'Change: %{customdata:.2f}%<br>'
            '<extra></extra>'
        ),
        customdata=data['change_pct']
    ))
    
    # Add trend line
    z = np.polyfit(range(len(data)), data['rate'], 1)
    trend_line = np.poly1d(z)(range(len(data)))
    
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=trend_line,
        mode='lines',
        name='Trend',
        line=dict(color='rgba(255, 99, 132, 0.6)', width=2, dash='dash'),
        hovertemplate='Trend: %{y:.4f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=f'{from_currency} to {to_currency} Exchange Rate Trend', x=0.5, font=dict(size=20, color='#2c3e50')),
        xaxis=dict(title='Date', showgrid=True, gridcolor='rgba(128, 128, 128, 0.2)', showline=True, linecolor='#2c3e50', tickformat='%b %d'),
        yaxis=dict(title=f'Exchange Rate ({from_currency} to {to_currency})', showgrid=True, gridcolor='rgba(128, 128, 128, 0.2)', showline=True, linecolor='#2c3e50', tickformat='.4f'),
        template='plotly_white',
        height=500,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig

def create_area_chart(data, from_currency, to_currency):
    """Create area chart for exchange rates"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['rate'],
        mode='lines',
        name=f'{from_currency}/{to_currency}',
        line=dict(color='#667eea', width=2),
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.3)',
        hovertemplate='<b>Rate:</b> %{y:.4f}<br><b>Date:</b> %{x}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'{from_currency} to {to_currency} Exchange Rate Area Chart',
        xaxis_title='Date',
        yaxis_title='Exchange Rate',
        template='plotly_white',
        height=500,
        hovermode='x unified'
    )
    
    return fig

def create_candlestick_chart(data, from_currency, to_currency):
    """Create candlestick chart for exchange rates"""
    fig = go.Figure(data=go.Candlestick(
        x=data['date'],
        open=data['rate'],
        high=data['high'],
        low=data['low'],
        close=data['rate'],
        name=f'{from_currency}/{to_currency}',
        increasing_line_color='#00ff88',
        decreasing_line_color='#ff4444'
    ))
    
    fig.update_layout(
        title=f'{from_currency} to {to_currency} Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Exchange Rate',
        template='plotly_white',
        height=500,
        xaxis_rangeslider_visible=False
    )
    
    return fig

def create_ohlc_chart(data, from_currency, to_currency):
    """Create OHLC chart for exchange rates"""
    fig = go.Figure(data=go.Ohlc(
        x=data['date'],
        open=data['rate'],
        high=data['high'],
        low=data['low'],
        close=data['rate'],
        name=f'{from_currency}/{to_currency}',
        increasing_line_color='#00ff88',
        decreasing_line_color='#ff4444'
    ))
    
    fig.update_layout(
        title=f'{from_currency} to {to_currency} OHLC Chart',
        xaxis_title='Date',
        yaxis_title='Exchange Rate',
        template='plotly_white',
        height=500,
        xaxis_rangeslider_visible=False
    )
    
    return fig

def render_enhanced_charts(from_currency, to_currency):
    """Render enhanced charts with multiple types"""
    st.markdown("### 📈 Advanced Exchange Rate Analytics")
    
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        period = st.selectbox("📅 Select Time Period", ["7 days", "30 days", "90 days", "180 days"], index=1, key="chart_period")
    
    with col2:
        chart_type = st.selectbox("📊 Chart Type", ["Line Chart", "Area Chart", "Candlestick", "OHLC"], key="chart_type")
    
    with col3:
        show_volume = st.checkbox("📊 Show Volume", value=False, key="show_volume")
    
    days_map = {"7 days": 7, "30 days": 30, "90 days": 90, "180 days": 180}
    days = days_map[period]
    
    historical_data = get_historical_data(from_currency, to_currency, days)
    
    if not historical_data.empty:
        # Create chart based on selected type
        if chart_type == "Line Chart":
            fig = create_line_chart(historical_data, from_currency, to_currency)
        elif chart_type == "Area Chart":
            fig = create_area_chart(historical_data, from_currency, to_currency)
        elif chart_type == "Candlestick":
            fig = create_candlestick_chart(historical_data, from_currency, to_currency)
        elif chart_type == "OHLC":
            fig = create_ohlc_chart(historical_data, from_currency, to_currency)
        else:
            fig = create_line_chart(historical_data, from_currency, to_currency)
        
        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
        })
        
        render_chart_analytics(historical_data, from_currency, to_currency)
    else:
        st.error("Unable to load chart data. Please try again later.")

def render_chart_analytics(data, from_currency, to_currency):
    """Render chart analytics and insights"""
    st.markdown("### 📊 Chart Analytics")
    
    current_rate = data['rate'].iloc[-1]
    previous_rate = data['rate'].iloc[-2] if len(data) > 1 else current_rate
    change = current_rate - previous_rate
    change_pct = (change / previous_rate) * 100 if previous_rate != 0 else 0
    
    volatility = data['rate'].std()
    avg_rate = data['rate'].mean()
    min_rate = data['rate'].min()
    max_rate = data['rate'].max()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Current Rate", value=f"{current_rate:.4f}", delta=f"{change_pct:+.2f}%")
    
    with col2:
        st.metric(label="Average Rate", value=f"{avg_rate:.4f}", delta=f"{((current_rate - avg_rate) / avg_rate * 100):+.2f}%")
    
    with col3:
        st.metric(label="Volatility", value=f"{volatility:.4f}", help="Standard deviation of exchange rates")
    
    with col4:
        st.metric(label="Range", value=f"{min_rate:.4f} - {max_rate:.4f}", help="Minimum and maximum rates in the period")
    
    with st.expander("📈 Market Insights"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Price Movement Analysis:**")
            if change_pct > 0:
                st.success(f"📈 {from_currency} has strengthened against {to_currency} by {change_pct:.2f}%")
            elif change_pct < 0:
                st.error(f"📉 {from_currency} has weakened against {to_currency} by {abs(change_pct):.2f}%")
            else:
                st.info(f"➡️ {from_currency} rate against {to_currency} is unchanged")
        
        with col2:
            st.markdown("**Volatility Assessment:**")
            if volatility < avg_rate * 0.01:
                st.info("🔹 Low volatility - Stable exchange rate")
            elif volatility < avg_rate * 0.03:
                st.warning("🔸 Moderate volatility - Normal fluctuations")
            else:
                st.error("🔺 High volatility - Significant price swings")

def render_header():
    """Render main header"""
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">💱 Professional Currency Converter</h1>
        <p class="main-subtitle">Real-time exchange rates with advanced analytics and interactive charts</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render sidebar with quick tools"""
    with st.sidebar:
        st.markdown("### ⚙️ Quick Tools")
        
        st.markdown("#### 🚀 Popular Pairs")
        popular_pairs = [("USD", "INR"), ("EUR", "USD"), ("GBP", "USD"), ("USD", "JPY"), ("EUR", "INR")]
        
        for from_curr, to_curr in popular_pairs:
            if st.button(f"{from_curr} → {to_curr}", key=f"quick_{from_curr}_{to_curr}", use_container_width=True):
                st.session_state.from_currency = from_curr
                st.session_state.to_currency = to_curr
                st.rerun()
        
        st.markdown("---")
        
        st.markdown("#### 📊 Market Status")
        if st.session_state.last_update:
            st.success(f"✅ Last updated: {st.session_state.last_update.strftime('%H:%M:%S')}")
        else:
            st.info("🔄 Ready to fetch rates")
        
        st.markdown("#### 📈 Today's Highlights")
        st.info("💹 USD/INR: Trending up")
        st.info("💹 EUR/USD: Stable range")
        st.info("💹 GBP/USD: Slight gain")

def render_developer_section():
    """Render developer section"""
    st.markdown("""
    <div class="developer-section">
        <h2 class="developer-name">Naman Agrawal</h2>
        <div style="margin-top: 25px;">
            <a href="https://www.linkedin.com/in/naman-agrawal-8671aa27b/" target="_blank" class="linkedin-button">
                🔗 Connect on LinkedIn
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render footer with developer info"""
    st.markdown("---")
    
    render_developer_section()
    
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; padding: 20px; background: rgba(0,0,0,0.05); border-radius: 10px; margin-top: 20px;">
        <p><strong>Professional Currency Converter</strong> - Real-time exchange rates with advanced analytics</p>
        <p>💡 Featuring interactive charts, multiple currency pairs, and professional-grade financial data visualization</p>
        <p>⚠️ <em>Exchange rates are for informational purposes only. Actual rates may vary.</em></p>
        <p style="margin-top: 15px; font-size: 0.9rem;">
            Developed by <strong>Naman Agrawal</strong> | 
            <a href="https://www.linkedin.com/in/naman-agrawal-8671aa27b/" target="_blank" style="color: #0077B5; text-decoration: none;">
                LinkedIn Profile
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main Application
def main():
    """Main application function"""
    render_header()
    render_sidebar()
    
    # Main conversion interface
    st.markdown('<div class="conversion-card">', unsafe_allow_html=True)
    st.markdown("### 💱 Currency Conversion")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        currency_options = list(CURRENCY_DATA.keys())
        from_currency = st.selectbox(
            "From Currency", 
            currency_options, 
            index=currency_options.index(st.session_state.from_currency), 
            format_func=get_currency_display_name, 
            key="from_select"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Swap", use_container_width=True):
            st.session_state.from_currency, st.session_state.to_currency = st.session_state.to_currency, st.session_state.from_currency
            st.rerun()
    
    with col3:
        to_currency = st.selectbox(
            "To Currency", 
            currency_options, 
            index=currency_options.index(st.session_state.to_currency), 
            format_func=get_currency_display_name, 
            key="to_select"
        )
    
    st.session_state.from_currency = from_currency
    st.session_state.to_currency = to_currency
    
    amount = st.number_input(
        f"💰 Enter amount in {from_currency}", 
        min_value=0.01, 
        value=100.0, 
        format="%.2f", 
        help="Enter the amount you want to convert"
    )
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        convert_button = st.button("✅ Convert Now", use_container_width=True, type="primary")
    
    with col2:
        chart_button = st.button("📊 View Charts", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle conversion
    if convert_button:
        if from_currency == to_currency:
            st.warning("⚠️ Please select different currencies for conversion.")
        else:
            with st.spinner("🔄 Fetching live exchange rates..."):
                try:
                    data = fetch_exchange_rates(from_currency)
                    
                    if to_currency in data["rates"]:
                        rate = data["rates"][to_currency]
                        converted_amount = rate * amount
                        
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="result-amount">{format_currency(converted_amount, to_currency)}</div>
                            <div class="result-rate">1 {from_currency} = {rate:.4f} {to_currency}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        add_to_history(from_currency, to_currency, amount, converted_amount, rate)
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-value">{rate:.4f}</div>
                                <div class="metric-label">Exchange Rate</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            reverse_rate = 1 / rate
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-value">{reverse_rate:.4f}</div>
                                <div class="metric-label">Reverse Rate</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            fee_estimate = converted_amount * 0.02
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-value">{format_currency(fee_estimate, to_currency)}</div>
                                <div class="metric-label">Est. Transfer Fee (2%)</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                    else:
                        st.error(f"❌ Conversion rate for {to_currency} not found.")
                        
                except Exception as e:
                    st.error("🚫 Failed to fetch exchange rate. Please check your internet connection or try again later.")
    
    # Handle chart display
    if chart_button:
        st.session_state.show_chart = True
    
    if st.session_state.get('show_chart', False):
        render_enhanced_charts(from_currency, to_currency)
    
    # Conversion history
    if st.session_state.conversion_history:
        st.markdown("### 📜 Conversion History")
        
        if st.button("🗑️ Clear History"):
            st.session_state.conversion_history = []
            st.success("History cleared!")
            st.rerun()
        
        for i, conversion in enumerate(st.session_state.conversion_history[:5]):
            with st.expander(f"{conversion['from_currency']} → {conversion['to_currency']} | {conversion['timestamp']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Amount:** {format_currency(conversion['amount'], conversion['from_currency'])}")
                    st.write(f"**Converted:** {format_currency(conversion['converted_amount'], conversion['to_currency'])}")
                
                with col2:
                    st.write(f"**Rate:** {conversion['rate']:.4f}")
                    st.write(f"**Time:** {conversion['timestamp']}")
    
    # Live currency rates table
    st.markdown("### 🌍 Live Currency Rates (Base: USD)")
    
    if st.button("🔄 Refresh All Rates"):
        st.cache_data.clear()
        st.success("Rates refreshed!")
    
    try:
        base_currency = "USD"
        data = fetch_exchange_rates(base_currency)
        
        comparison_currencies = ["EUR", "GBP", "JPY", "INR", "AUD", "CAD", "CHF", "CNY", "SGD"]
        comparison_data = []
        
        for currency in comparison_currencies:
            if currency in data["rates"]:
                rate = data["rates"][currency]
                currency_info = CURRENCY_DATA.get(currency, {"flag": "", "name": currency})
                comparison_data.append({
                    "Currency": f"{currency_info['flag']} {currency}",
                    "Name": currency_info['name'],
                    "Rate (1 USD =)": f"{rate:.4f}",
                    "Reverse (1 {currency} =)": f"{1/rate:.4f} USD"
                })
        
        if comparison_data:
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    except Exception as e:
        st.error("Unable to load currency comparison table")
    
    render_footer()

if __name__ == "__main__":
    main()
