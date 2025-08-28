import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import streamlit as st

class DataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
    
    def _make_request(self, params):
        """Make API request with error handling"""
        try:
            params['apikey'] = self.api_key
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Check for API-specific errors
            if 'Error Message' in data:
                st.error(f"API Error: {data['Error Message']}")
                return None
            elif 'Note' in data:
                st.error(f"API Rate Limit: {data['Note']}")
                return None
            elif 'Information' in data:
                st.error(f"API Limit Reached: {data['Information']}")
                return None
                
            return data
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    def _is_cache_valid(self, cache_key):
        """Check if cached data is still valid"""
        if cache_key not in self.cache:
            return False
        
        cached_time = self.cache[cache_key].get('timestamp', 0)
        return time.time() - cached_time < self.cache_timeout
    
    def get_current_price(self, symbol):
        """Get current price and basic info for a stock"""
        cache_key = f"current_{symbol}"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
        
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol
        }
        
        data = self._make_request(params)
        if not data:
            return None
            
        if 'Global Quote' not in data:
            # Try to provide more specific error information
            if 'Error Message' in data:
                st.warning(f"Symbol '{symbol}' not found: {data['Error Message']}")
            else:
                st.warning(f"No data available for symbol '{symbol}'. Please check the symbol and try again.")
            return None
        
        quote = data['Global Quote']
        
        try:
            result = {
                'symbol': quote.get('01. symbol', symbol),
                'price': float(quote.get('05. price', 0)),
                'change': float(quote.get('09. change', 0)),
                'change_percent': float(quote.get('10. change percent', '0%').replace('%', '')),
                'volume': int(quote.get('06. volume', 0)),
                'market_cap': 'N/A'  # Not available in this endpoint
            }
            
            # Cache the result
            self.cache[cache_key] = {
                'data': result,
                'timestamp': time.time()
            }
            
            return result
        except (ValueError, KeyError) as e:
            st.error(f"Error parsing current price data: {str(e)}")
            return None
    
    def get_historical_data(self, symbol, period='1M'):
        """Get historical price data"""
        cache_key = f"historical_{symbol}_{period}"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
        
        # Determine the function based on period
        if period == '1D':
            function = 'TIME_SERIES_INTRADAY'
            params = {
                'function': function,
                'symbol': symbol,
                'interval': '5min',
                'outputsize': 'compact'
            }
        else:
            function = 'TIME_SERIES_DAILY'
            params = {
                'function': function,
                'symbol': symbol,
                'outputsize': 'full'
            }
        
        data = self._make_request(params)
        if not data:
            return None
        
        # Extract time series data
        time_series_key = None
        for key in data.keys():
            if 'Time Series' in key:
                time_series_key = key
                break
        
        if not time_series_key or time_series_key not in data:
            if 'Error Message' in data:
                st.error(f"API Error: {data['Error Message']}")
            elif 'Note' in data:
                st.warning(f"API Note: {data['Note']}")
            return None
        
        time_series = data[time_series_key]
        
        # Convert to DataFrame
        df_data = []
        for date_str, values in time_series.items():
            try:
                df_data.append({
                    'date': pd.to_datetime(date_str),
                    'open': float(values.get('1. open', 0)),
                    'high': float(values.get('2. high', 0)),
                    'low': float(values.get('3. low', 0)),
                    'close': float(values.get('4. close', 0)),
                    'volume': int(values.get('5. volume', 0))
                })
            except (ValueError, KeyError):
                continue
        
        if not df_data:
            return None
        
        df = pd.DataFrame(df_data)
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)
        
        # Filter data based on period
        if period != '1D':
            end_date = datetime.now()
            if period == '1W':
                start_date = end_date - timedelta(weeks=1)
            elif period == '1M':
                start_date = end_date - timedelta(days=30)
            elif period == '3M':
                start_date = end_date - timedelta(days=90)
            elif period == '1Y':
                start_date = end_date - timedelta(days=365)
            else:
                start_date = end_date - timedelta(days=30)
            
            df = df[df.index >= start_date]
        
        # Cache the result
        self.cache[cache_key] = {
            'data': df,
            'timestamp': time.time()
        }
        
        return df
    
    def get_company_info(self, symbol):
        """Get company overview information"""
        cache_key = f"company_{symbol}"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
        
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol
        }
        
        data = self._make_request(params)
        if not data:
            return None
        
        try:
            result = {
                'name': data.get('Name', 'N/A'),
                'description': data.get('Description', 'N/A'),
                'sector': data.get('Sector', 'N/A'),
                'industry': data.get('Industry', 'N/A'),
                'market_cap': data.get('MarketCapitalization', 'N/A'),
                'pe_ratio': data.get('PERatio', 'N/A'),
                'dividend_yield': data.get('DividendYield', 'N/A')
            }
            
            # Cache the result
            self.cache[cache_key] = {
                'data': result,
                'timestamp': time.time()
            }
            
            return result
        except Exception as e:
            st.error(f"Error parsing company info: {str(e)}")
            return None
