import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import os

# Import custom modules
from data_fetcher import DataFetcher
from ml_predictor import MLPredictor
from chart_generator import ChartGenerator
from portfolio_manager import PortfolioManager
from technical_indicators import TechnicalIndicators
from utils import format_currency, format_percentage, get_market_status
from stock_tickers import search_tickers, get_popular_tickers, get_micro_stocks

# Configure page
st.set_page_config(
    page_title="AI Stock Market Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []
if 'selected_stock' not in st.session_state:
    st.session_state.selected_stock = 'AAPL'
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'search_input' not in st.session_state:
    st.session_state.search_input = 'AAPL'
if 'show_suggestions' not in st.session_state:
    st.session_state.show_suggestions = False
if 'last_selected_stock' not in st.session_state:
    st.session_state.last_selected_stock = 'AAPL'

# Initialize components
@st.cache_resource
def initialize_components():
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
    data_fetcher = DataFetcher(api_key)
    ml_predictor = MLPredictor()
    chart_generator = ChartGenerator()
    portfolio_manager = PortfolioManager()
    technical_indicators = TechnicalIndicators()
    return data_fetcher, ml_predictor, chart_generator, portfolio_manager, technical_indicators

data_fetcher, ml_predictor, chart_generator, portfolio_manager, technical_indicators = initialize_components()

# Main app
def main():
    st.title("🚀 AI-Driven Stock Market Dashboard")
    
    # Add API status indicator
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
    if api_key == "demo":
        st.warning("⚠️ Using demo API key - limited functionality available")
    else:
        st.success("✅ Alpha Vantage API connected")
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Navigation")
        
        # Stock selection with autocomplete
        st.subheader("Stock Selection")
        
        # Track the last selected stock for reference
        if 'last_selected_stock' not in st.session_state:
            st.session_state.last_selected_stock = st.session_state.selected_stock
        
        # Search input
        search_input = st.text_input(
            "Search for stocks", 
            value=st.session_state.search_input,
            placeholder="Type company name or ticker (e.g., 'micro', 'apple', 'AAPL')",
            help="Start typing to see suggestions - press Enter to search",
            key="stock_search"
        )
        
        # Update search state and handle immediate ticker selection
        if search_input != st.session_state.search_input:
            st.session_state.search_input = search_input
            st.session_state.show_suggestions = len(search_input) > 0
            
            # Check if input is a valid ticker (3-5 uppercase letters)
            if len(search_input) >= 3 and search_input.isalpha() and search_input.isupper():
                # Auto-select if it's a potential ticker
                potential_matches = search_tickers(search_input, limit=1)
                if potential_matches and potential_matches[0]['ticker'] == search_input:
                    st.session_state.selected_stock = search_input
                    st.session_state.show_suggestions = False
        
        # Show suggestions when user is typing
        if st.session_state.show_suggestions and len(search_input) > 0:
            suggestions = search_tickers(search_input, limit=8)
            
            if suggestions:
                st.markdown("**💡 Suggestions:**")
                
                # Create a container for suggestions with custom styling
                with st.container():
                    for i, suggestion in enumerate(suggestions):
                        # Format the suggestion text
                        company_name = suggestion['company']
                        ticker = suggestion['ticker']
                        
                        # Truncate long company names
                        if len(company_name) > 25:
                            company_name = company_name[:22] + "..."
                        
                        suggestion_text = f"{company_name} ({ticker})"
                        
                        # Create button with better styling
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            if st.button(
                                suggestion_text,
                                key=f"suggest_{ticker}_{i}",
                                help=f"Select {suggestion['company']} - {ticker}",
                                use_container_width=True
                            ):
                                st.session_state.selected_stock = ticker
                                st.session_state.search_input = ""  # Clear search instead of setting to ticker
                                st.session_state.show_suggestions = False
                                st.session_state.last_selected_stock = ticker
                                st.rerun()
                        with col2:
                            # Show match type indicator
                            match_icon = "🎯" if suggestion['match_type'] == 'ticker' else "🏢"
                            st.write(match_icon)
                
                # Add control buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Hide", key="hide_suggestions"):
                        st.session_state.show_suggestions = False
                        st.rerun()
                with col2:
                    if st.button("Clear", key="clear_search"):
                        st.session_state.search_input = ""
                        st.session_state.show_suggestions = False
                        st.rerun()
            else:
                st.markdown("*🔍 No matching stocks found*")
                st.markdown("*Try searching for: 'apple', 'microsoft', 'tesla', or any ticker symbol*")
        
        # Manual ticker input with better handling
        st.write("**Or enter ticker directly:**")
        
        # Use a different key to avoid conflicts
        direct_ticker_input = st.text_input(
            "Ticker Symbol", 
            value="",
            max_chars=10,
            placeholder="e.g., TSLA, GOOGL, AMZN",
            key="direct_ticker_input"
        ).upper()
        
        # Handle direct ticker submission
        if direct_ticker_input and st.button("Go", key="direct_ticker_submit"):
            st.session_state.selected_stock = direct_ticker_input
            st.session_state.search_input = ""  # Clear search after selection
            st.session_state.show_suggestions = False
            st.session_state.last_selected_stock = direct_ticker_input
            st.rerun()
        
        # Quick access to popular stocks
        st.write("**Popular Stocks:**")
        popular_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX']
        
        cols = st.columns(2)
        for i, ticker in enumerate(popular_stocks):
            with cols[i % 2]:
                if st.button(ticker, key=f"popular_{ticker}"):
                    st.session_state.selected_stock = ticker
                    st.session_state.search_input = ticker
                    st.session_state.show_suggestions = False
                    st.rerun()
        
        # Demo section for "micro" search
        st.markdown("---")
        st.markdown("**🔍 Try searching for:**")
        demo_searches = [
            ("micro", "Find micro-related stocks"),
            ("apple", "Find Apple Inc."),
            ("tesla", "Find Tesla Inc."),
            ("MSFT", "Find by ticker symbol")
        ]
        
        cols = st.columns(2)
        for i, (search_term, description) in enumerate(demo_searches):
            with cols[i % 2]:
                if st.button(f'"{search_term}"', key=f"demo_{search_term}", help=description):
                    st.session_state.search_input = search_term
                    st.session_state.show_suggestions = True
                    st.rerun()
        
        stock_symbol = st.session_state.selected_stock
        
        # Show currently selected stock clearly
        if stock_symbol:
            st.success(f"📈 **Currently analyzing: {stock_symbol}**")
        else:
            st.info("👆 Please select a stock to analyze")
        
        # Time period selection
        st.subheader("Time Period")
        time_period = st.selectbox(
            "Select Period",
            ["1D", "1W", "1M", "3M", "1Y"],
            index=2
        )
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox("Auto Refresh (30s)", value=False)
        
        # Portfolio section
        st.subheader("Portfolio")
        if st.button("Add to Portfolio"):
            if stock_symbol and stock_symbol not in st.session_state.portfolio:
                st.session_state.portfolio.append(stock_symbol)
                st.success(f"Added {stock_symbol} to portfolio")
                st.rerun()
        
        # Display portfolio
        if st.session_state.portfolio:
            st.write("Current Portfolio:")
            for i, symbol in enumerate(st.session_state.portfolio):
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button(symbol, key=f"portfolio_{i}"):
                        st.session_state.selected_stock = symbol
                        st.rerun()
                with col2:
                    if st.button("❌", key=f"remove_{i}"):
                        st.session_state.portfolio.remove(symbol)
                        st.rerun()
        
        # Market status
        st.subheader("Market Status")
        market_status = get_market_status()
        st.write(f"Status: {market_status}")
        
        # Last update time
        if st.session_state.last_update:
            st.write(f"Last Update: {st.session_state.last_update.strftime('%H:%M:%S')}")
    
    # Main content
    if not stock_symbol:
        st.warning("Please select a stock symbol from the sidebar to get started.")
        st.info("💡 Try searching for 'micro', 'apple', 'tesla', or any company name in the sidebar!")
        return
    
    # Auto-refresh logic
    if auto_refresh:
        placeholder = st.empty()
        time.sleep(30)
        st.rerun()
    
    # Fetch data
    with st.spinner(f"Fetching data for {stock_symbol}..."):
        try:
            # Get current price and basic info
            current_data = data_fetcher.get_current_price(stock_symbol)
            if not current_data:
                st.error(f"Unable to fetch data for {stock_symbol}.")
                st.info("🔄 This might be due to:")
                st.markdown("""
                - **API Rate Limit**: Alpha Vantage free tier allows 25 requests/day
                - **Invalid Symbol**: Please check the stock symbol is correct
                - **Network Issues**: Try refreshing the page
                
                💡 **Solutions:**
                - Wait for API limit to reset (resets daily)
                - Try a different stock symbol
                - Check if the symbol exists on major exchanges
                """)
                return
            
            # Get historical data
            historical_data = data_fetcher.get_historical_data(stock_symbol, time_period)
            if historical_data is None or historical_data.empty:
                st.error(f"No historical data available for {stock_symbol}.")
                return
            
            st.session_state.last_update = datetime.now()
            
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            return
    
    # Display current price info
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_price = current_data.get('price', 0)
        st.metric("Current Price", format_currency(current_price))
    
    with col2:
        change = current_data.get('change', 0)
        change_percent = current_data.get('change_percent', 0)
        st.metric("Change", format_currency(change), delta=format_percentage(change_percent))
    
    with col3:
        volume = current_data.get('volume', 0)
        st.metric("Volume", f"{volume:,}")
    
    with col4:
        market_cap = current_data.get('market_cap', 'N/A')
        st.metric("Market Cap", market_cap if market_cap != 'N/A' else "N/A")
    
    # Technical indicators
    with st.spinner("Calculating technical indicators..."):
        indicators = technical_indicators.calculate_indicators(historical_data)
        historical_data = pd.concat([historical_data, indicators], axis=1)
    
    # ML Predictions
    st.subheader("🤖 AI Price Predictions")
    
    with st.spinner("Training ML model and generating predictions..."):
        try:
            predictions = ml_predictor.predict_prices(historical_data)
            
            if 'error' in predictions:
                st.error(f"Prediction Error: {predictions['error']}")
            else:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    next_day_pred = predictions.get('next_day', 0)
                    st.metric("Next Day Prediction", f"${next_day_pred:.2f}")
                
                with col2:
                    confidence = predictions.get('confidence', 0)
                    st.metric("Model Confidence", f"{confidence:.1%}")
                
                with col3:
                    accuracy = predictions.get('accuracy', 0)
                    st.metric("Model Accuracy", f"{accuracy:.1%}")
                
                # Additional prediction info
                if 'lower_bound' in predictions and 'upper_bound' in predictions:
                    st.info(f"📊 **Price Range Prediction:** ${predictions['lower_bound']:.2f} - ${predictions['upper_bound']:.2f}")
                
                # Prediction chart
                pred_fig = chart_generator.create_prediction_chart(
                    historical_data, predictions, stock_symbol
                )
                st.plotly_chart(pred_fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error generating predictions: {str(e)}")
    
    # Main charts
    st.subheader(f"📈 {stock_symbol} Price Analysis")
    
    # Create tabs for different chart types
    tab1, tab2, tab3 = st.tabs(["Candlestick Chart", "Technical Analysis", "Volume Analysis"])
    
    with tab1:
        candlestick_fig = chart_generator.create_candlestick_chart(historical_data, stock_symbol)
        st.plotly_chart(candlestick_fig, use_container_width=True)
    
    with tab2:
        technical_fig = chart_generator.create_technical_chart(historical_data, stock_symbol)
        st.plotly_chart(technical_fig, use_container_width=True)
    
    with tab3:
        volume_fig = chart_generator.create_volume_chart(historical_data, stock_symbol)
        st.plotly_chart(volume_fig, use_container_width=True)
    
    # Portfolio performance
    if st.session_state.portfolio:
        st.subheader("📊 Portfolio Performance")
        
        with st.spinner("Loading portfolio data..."):
            portfolio_data = portfolio_manager.get_portfolio_performance(
                st.session_state.portfolio, data_fetcher
            )
            
            if portfolio_data:
                # Portfolio summary
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    total_value = sum(stock['current_price'] for stock in portfolio_data)
                    st.metric("Total Portfolio Value", format_currency(total_value))
                
                with col2:
                    total_change = sum(stock['change'] for stock in portfolio_data)
                    st.metric("Total Change", format_currency(total_change))
                
                with col3:
                    avg_change_percent = np.mean([stock['change_percent'] for stock in portfolio_data])
                    st.metric("Average Change %", format_percentage(avg_change_percent))
                
                # Portfolio table
                portfolio_df = pd.DataFrame(portfolio_data)
                st.dataframe(
                    portfolio_df[['symbol', 'current_price', 'change', 'change_percent', 'volume']],
                    use_container_width=True
                )
    
    # Data table
    with st.expander("📋 Raw Data"):
        st.dataframe(historical_data.tail(50), use_container_width=True)

if __name__ == "__main__":
    main()
