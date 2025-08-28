import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

def format_currency(value, currency='USD'):
    """Format currency values"""
    if pd.isna(value) or value == 0:
        return "$0.00"
    
    if abs(value) >= 1e9:
        return f"${value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"

def format_percentage(value):
    """Format percentage values"""
    if pd.isna(value):
        return "0.00%"
    return f"{value:.2f}%"

def format_large_number(value):
    """Format large numbers with appropriate suffixes"""
    if pd.isna(value) or value == 0:
        return "0"
    
    if abs(value) >= 1e9:
        return f"{value/1e9:.1f}B"
    elif abs(value) >= 1e6:
        return f"{value/1e6:.1f}M"
    elif abs(value) >= 1e3:
        return f"{value/1e3:.1f}K"
    else:
        return f"{value:.0f}"

def get_market_status():
    """Get current market status"""
    try:
        # Get current time in Eastern Time (NYSE timezone)
        eastern = pytz.timezone('US/Eastern')
        current_time = datetime.now(eastern)
        
        # Check if it's a weekday
        if current_time.weekday() >= 5:  # Saturday = 5, Sunday = 6
            return "🔴 Closed (Weekend)"
        
        # Market hours: 9:30 AM - 4:00 PM ET
        market_open = current_time.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = current_time.replace(hour=16, minute=0, second=0, microsecond=0)
        
        if market_open <= current_time <= market_close:
            return "🟢 Open"
        elif current_time < market_open:
            return "🟡 Pre-Market"
        else:
            return "🟡 After-Hours"
            
    except Exception:
        return "❓ Unknown"

def calculate_returns(prices):
    """Calculate returns from price series"""
    if len(prices) < 2:
        return pd.Series(dtype=float)
    
    returns = prices.pct_change().dropna()
    return returns

def calculate_volatility(returns, annualize=True):
    """Calculate volatility from returns"""
    if len(returns) < 2:
        return 0
    
    vol = returns.std()
    if annualize:
        vol = vol * np.sqrt(252)  # Annualize assuming 252 trading days
    
    return vol

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """Calculate Sharpe ratio"""
    if len(returns) < 2:
        return 0
    
    excess_returns = returns.mean() * 252 - risk_free_rate  # Annualized
    volatility = calculate_volatility(returns, annualize=True)
    
    if volatility == 0:
        return 0
    
    return excess_returns / volatility

def calculate_max_drawdown(prices):
    """Calculate maximum drawdown"""
    if len(prices) < 2:
        return 0
    
    # Calculate cumulative returns
    cum_returns = (1 + prices.pct_change()).cumprod()
    
    # Calculate running maximum
    running_max = cum_returns.expanding().max()
    
    # Calculate drawdown
    drawdown = (cum_returns - running_max) / running_max
    
    return drawdown.min()

def get_trading_days_between(start_date, end_date):
    """Get number of trading days between two dates"""
    # Create date range
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')  # Business days
    
    # Remove holidays (simplified - just removes major US holidays)
    holidays = [
        '2024-01-01',  # New Year's Day
        '2024-01-15',  # Martin Luther King Jr. Day
        '2024-02-19',  # Presidents' Day
        '2024-05-27',  # Memorial Day
        '2024-07-04',  # Independence Day
        '2024-09-02',  # Labor Day
        '2024-11-28',  # Thanksgiving
        '2024-12-25',  # Christmas
    ]
    
    holidays = pd.to_datetime(holidays)
    trading_days = date_range.difference(holidays)
    
    return len(trading_days)

def detect_outliers(data, method='iqr', threshold=1.5):
    """Detect outliers in data"""
    if len(data) < 4:
        return pd.Series([False] * len(data), index=data.index)
    
    if method == 'iqr':
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        outliers = (data < lower_bound) | (data > upper_bound)
        
    elif method == 'zscore':
        z_scores = np.abs((data - data.mean()) / data.std())
        outliers = z_scores > threshold
        
    else:
        outliers = pd.Series([False] * len(data), index=data.index)
    
    return outliers

def smooth_data(data, method='rolling', window=5):
    """Smooth data using various methods"""
    if method == 'rolling':
        return data.rolling(window=window, center=True).mean()
    elif method == 'ewm':
        return data.ewm(span=window).mean()
    else:
        return data

def validate_stock_symbol(symbol):
    """Validate stock symbol format"""
    if not symbol:
        return False
    
    # Basic validation - should be 1-5 characters, letters only
    if len(symbol) < 1 or len(symbol) > 5:
        return False
    
    if not symbol.isalpha():
        return False
    
    return True

def get_time_period_days(period):
    """Convert time period string to number of days"""
    period_map = {
        '1D': 1,
        '1W': 7,
        '1M': 30,
        '3M': 90,
        '6M': 180,
        '1Y': 365,
        '2Y': 730,
        '5Y': 1825
    }
    
    return period_map.get(period, 30)

def calculate_correlation_matrix(data):
    """Calculate correlation matrix for multiple stocks"""
    if data.empty:
        return pd.DataFrame()
    
    # Select only numeric columns
    numeric_data = data.select_dtypes(include=[np.number])
    
    if numeric_data.empty:
        return pd.DataFrame()
    
    correlation_matrix = numeric_data.corr()
    return correlation_matrix

def generate_trading_signals(data, indicators):
    """Generate simple trading signals"""
    signals = []
    
    if 'rsi' in indicators.columns:
        latest_rsi = indicators['rsi'].iloc[-1]
        if latest_rsi < 30:
            signals.append({'type': 'BUY', 'reason': 'RSI oversold', 'strength': 'Medium'})
        elif latest_rsi > 70:
            signals.append({'type': 'SELL', 'reason': 'RSI overbought', 'strength': 'Medium'})
    
    if 'macd' in indicators.columns and 'macd_signal' in indicators.columns:
        latest_macd = indicators['macd'].iloc[-1]
        latest_signal = indicators['macd_signal'].iloc[-1]
        prev_macd = indicators['macd'].iloc[-2] if len(indicators) > 1 else latest_macd
        prev_signal = indicators['macd_signal'].iloc[-2] if len(indicators) > 1 else latest_signal
        
        if latest_macd > latest_signal and prev_macd <= prev_signal:
            signals.append({'type': 'BUY', 'reason': 'MACD bullish crossover', 'strength': 'Strong'})
        elif latest_macd < latest_signal and prev_macd >= prev_signal:
            signals.append({'type': 'SELL', 'reason': 'MACD bearish crossover', 'strength': 'Strong'})
    
    return signals
