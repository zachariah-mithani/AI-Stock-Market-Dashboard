import pandas as pd
import numpy as np

class TechnicalIndicators:
    def __init__(self):
        pass
    
    def calculate_indicators(self, data):
        """Calculate various technical indicators"""
        if data.empty:
            return pd.DataFrame()
        
        indicators = pd.DataFrame(index=data.index)
        
        # Moving Averages
        indicators['ma_5'] = data['close'].rolling(window=5).mean()
        indicators['ma_10'] = data['close'].rolling(window=10).mean()
        indicators['ma_20'] = data['close'].rolling(window=20).mean()
        indicators['ma_50'] = data['close'].rolling(window=50).mean()
        
        # Exponential Moving Averages
        indicators['ema_12'] = data['close'].ewm(span=12).mean()
        indicators['ema_26'] = data['close'].ewm(span=26).mean()
        
        # MACD
        indicators['macd'] = indicators['ema_12'] - indicators['ema_26']
        indicators['macd_signal'] = indicators['macd'].ewm(span=9).mean()
        indicators['macd_histogram'] = indicators['macd'] - indicators['macd_signal']
        
        # Bollinger Bands
        indicators['bb_middle'] = indicators['ma_20']
        bb_std = data['close'].rolling(window=20).std()
        indicators['bb_upper'] = indicators['bb_middle'] + (bb_std * 2)
        indicators['bb_lower'] = indicators['bb_middle'] - (bb_std * 2)
        
        # RSI
        indicators['rsi'] = self._calculate_rsi(data['close'])
        
        # Stochastic Oscillator
        stoch_k, stoch_d = self._calculate_stochastic(data)
        indicators['stoch_k'] = stoch_k
        indicators['stoch_d'] = stoch_d
        
        # Volume indicators
        indicators['volume_ma'] = data['volume'].rolling(window=10).mean()
        indicators['volume_ratio'] = data['volume'] / indicators['volume_ma']
        
        # Price momentum
        indicators['momentum'] = data['close'].pct_change(periods=10)
        
        # Volatility
        indicators['volatility'] = data['close'].rolling(window=20).std()
        
        # Average True Range (ATR)
        indicators['atr'] = self._calculate_atr(data)
        
        # Williams %R
        indicators['williams_r'] = self._calculate_williams_r(data)
        
        # Commodity Channel Index (CCI)
        indicators['cci'] = self._calculate_cci(data)
        
        return indicators
    
    def _calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_stochastic(self, data, k_period=14, d_period=3):
        """Calculate Stochastic Oscillator"""
        lowest_low = data['low'].rolling(window=k_period).min()
        highest_high = data['high'].rolling(window=k_period).max()
        k_percent = 100 * ((data['close'] - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_period).mean()
        return k_percent, d_percent
    
    def _calculate_atr(self, data, period=14):
        """Calculate Average True Range"""
        high_low = data['high'] - data['low']
        high_close = np.abs(data['high'] - data['close'].shift())
        low_close = np.abs(data['low'] - data['close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        atr = true_range.rolling(window=period).mean()
        return atr
    
    def _calculate_williams_r(self, data, period=14):
        """Calculate Williams %R"""
        highest_high = data['high'].rolling(window=period).max()
        lowest_low = data['low'].rolling(window=period).min()
        williams_r = -100 * ((highest_high - data['close']) / (highest_high - lowest_low))
        return williams_r
    
    def _calculate_cci(self, data, period=20):
        """Calculate Commodity Channel Index"""
        typical_price = (data['high'] + data['low'] + data['close']) / 3
        sma = typical_price.rolling(window=period).mean()
        mean_deviation = typical_price.rolling(window=period).apply(
            lambda x: np.abs(x - x.mean()).mean()
        )
        cci = (typical_price - sma) / (0.015 * mean_deviation)
        return cci
    
    def get_trading_signals(self, data, indicators):
        """Generate trading signals based on technical indicators"""
        signals = pd.DataFrame(index=data.index)
        
        # RSI signals
        signals['rsi_oversold'] = indicators['rsi'] < 30
        signals['rsi_overbought'] = indicators['rsi'] > 70
        
        # MACD signals
        signals['macd_bullish'] = (indicators['macd'] > indicators['macd_signal']) & \
                                 (indicators['macd'].shift(1) <= indicators['macd_signal'].shift(1))
        signals['macd_bearish'] = (indicators['macd'] < indicators['macd_signal']) & \
                                 (indicators['macd'].shift(1) >= indicators['macd_signal'].shift(1))
        
        # Moving Average signals
        signals['ma_golden_cross'] = (indicators['ma_5'] > indicators['ma_20']) & \
                                    (indicators['ma_5'].shift(1) <= indicators['ma_20'].shift(1))
        signals['ma_death_cross'] = (indicators['ma_5'] < indicators['ma_20']) & \
                                   (indicators['ma_5'].shift(1) >= indicators['ma_20'].shift(1))
        
        # Bollinger Bands signals
        signals['bb_squeeze'] = (data['close'] > indicators['bb_upper']) | \
                               (data['close'] < indicators['bb_lower'])
        
        # Volume signals
        signals['volume_spike'] = indicators['volume_ratio'] > 2
        
        # Stochastic signals
        signals['stoch_oversold'] = indicators['stoch_k'] < 20
        signals['stoch_overbought'] = indicators['stoch_k'] > 80
        
        return signals
    
    def get_support_resistance(self, data, window=20):
        """Calculate support and resistance levels"""
        if len(data) < window:
            return {'support': [], 'resistance': []}
        
        # Find local minima and maxima
        highs = data['high'].rolling(window=window, center=True).max()
        lows = data['low'].rolling(window=window, center=True).min()
        
        # Identify support and resistance levels
        resistance_levels = []
        support_levels = []
        
        for i in range(window, len(data) - window):
            if data['high'].iloc[i] == highs.iloc[i]:
                resistance_levels.append(data['high'].iloc[i])
            if data['low'].iloc[i] == lows.iloc[i]:
                support_levels.append(data['low'].iloc[i])
        
        # Remove duplicates and sort
        resistance_levels = sorted(list(set(resistance_levels)), reverse=True)
        support_levels = sorted(list(set(support_levels)))
        
        return {
            'resistance': resistance_levels[:5],  # Top 5 resistance levels
            'support': support_levels[-5:]       # Top 5 support levels
        }
