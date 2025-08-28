import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class MLPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = []
    
    def _prepare_features(self, data):
        """Prepare features for ML model"""
        if data.empty or len(data) < 3:
            return None, None
        
        # Create a copy to avoid modifying original data
        df = data.copy()
        
        # Ensure we have the required columns
        required_columns = ['close', 'volume', 'high', 'low', 'open']
        if not all(col in df.columns for col in required_columns):
            return None, None
        
        # Create features DataFrame
        features = pd.DataFrame(index=df.index)
        
        # Simple price-based features (no rolling windows needed)
        features['high_low_ratio'] = df['high'] / df['low']
        features['close_open_ratio'] = df['close'] / df['open']
        features['range_ratio'] = (df['high'] - df['low']) / df['close']
        features['volume_price_ratio'] = df['volume'] / df['close']
        
        # Price changes
        features['price_change'] = df['close'].pct_change()
        features['volume_change'] = df['volume'].pct_change()
        
        # Simple lag features
        features['close_lag_1'] = df['close'].shift(1)
        features['volume_lag_1'] = df['volume'].shift(1)
        
        # Only add rolling features if we have enough data
        data_len = len(df)
        if data_len >= 5:
            # Small moving averages
            ma_window = min(3, data_len // 2)
            features['ma_short'] = df['close'].rolling(window=ma_window).mean()
            features['close_to_ma'] = df['close'] / features['ma_short']
            
            # Simple volatility
            vol_window = min(3, data_len // 2)
            features['volatility'] = df['close'].rolling(window=vol_window).std()
            
            # Volume moving average
            features['volume_ma'] = df['volume'].rolling(window=ma_window).mean()
            features['volume_ratio'] = df['volume'] / features['volume_ma']
        
        # For very small datasets, add more basic features
        if data_len < 10:
            # Add position in sequence
            features['position'] = range(len(df))
            features['position_normalized'] = features['position'] / len(df)
            
            # Add simple trend indicators
            if len(df) >= 2:
                features['trend_2'] = df['close'].diff(2)
            if len(df) >= 3:
                features['trend_3'] = df['close'].diff(3)
        
        # Target: next day's closing price
        target = df['close'].shift(-1)
        
        # Handle NaN values more carefully
        # Fill NaN values with forward fill first, then backward fill
        features = features.ffill().bfill()
        
        # Remove the last row from features and target (target is NaN for last row)
        features = features.iloc[:-1]
        target = target.iloc[:-1]
        
        # Final check for any remaining NaN values
        features = features.dropna()
        target = target.dropna()
        
        # Align features and target
        common_index = features.index.intersection(target.index)
        features = features.loc[common_index]
        target = target.loc[common_index]
        
        if features.empty or target.empty or len(features) < 1:
            return None, None
        
        self.feature_names = features.columns.tolist()
        
        return features, target
    
    def train_model(self, features, target):
        """Train the ML model"""
        if features is None or target is None or len(features) < 2:
            return False
        
        try:
            # For small datasets, use all data for training
            if len(features) < 10:
                X_train = features
                y_train = target
                X_test = features
                y_test = target
            else:
                # Split data for larger datasets
                X_train, X_test, y_train, y_test = train_test_split(
                    features, target, test_size=0.2, random_state=42, shuffle=False
                )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.model.fit(X_train_scaled, y_train)
            
            # Calculate metrics
            train_pred = self.model.predict(X_train_scaled)
            test_pred = self.model.predict(X_test_scaled)
            
            self.train_score = r2_score(y_train, train_pred) if len(y_train) > 1 else 0.5
            self.test_score = r2_score(y_test, test_pred) if len(y_test) > 1 else 0.5
            self.mse = mean_squared_error(y_test, test_pred) if len(y_test) > 1 else 0
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"Error training model: {str(e)}")
            return False
    
    def predict_prices(self, data):
        """Generate price predictions"""
        if data is None or data.empty:
            return {'error': 'No data provided'}
        
        try:
            # Prepare features
            features, target = self._prepare_features(data)
            
            if features is None or target is None:
                return {'error': 'Unable to prepare features'}
            
            # Train model
            if not self.train_model(features, target):
                return {'error': 'Model training failed'}
            
            # Make predictions
            latest_features = features.iloc[-1:].values
            latest_features_scaled = self.scaler.transform(latest_features)
            
            next_day_pred = self.model.predict(latest_features_scaled)[0]
            
            # Generate prediction interval - more conservative approach
            if len(features) > 1:
                # Use historical volatility for confidence intervals
                recent_prices = data['close'].tail(10).values
                if len(recent_prices) >= 2:
                    price_std = np.std(recent_prices)
                    # Use 2 standard deviations for 95% confidence interval
                    confidence_interval = 2 * price_std
                else:
                    confidence_interval = next_day_pred * 0.05  # 5% default
                
                lower_bound = next_day_pred - confidence_interval
                upper_bound = next_day_pred + confidence_interval
                
                # Ensure bounds are reasonable
                recent_min = recent_prices.min() if len(recent_prices) > 0 else next_day_pred * 0.9
                recent_max = recent_prices.max() if len(recent_prices) > 0 else next_day_pred * 1.1
                
                lower_bound = max(lower_bound, recent_min * 0.9)
                upper_bound = min(upper_bound, recent_max * 1.1)
            else:
                lower_bound = next_day_pred * 0.95
                upper_bound = next_day_pred * 1.05
            
            # Generate future predictions (next 7 days) - more conservative approach
            future_predictions = []
            
            # Use a more conservative approach for future predictions
            # Apply a simple trend based on recent price movements
            recent_prices = data['close'].tail(5).values
            if len(recent_prices) >= 2:
                # Calculate average daily change
                daily_changes = np.diff(recent_prices)
                avg_daily_change = np.mean(daily_changes)
                # Limit the daily change to be reasonable (max 5% per day)
                max_daily_change = recent_prices[-1] * 0.05
                avg_daily_change = np.clip(avg_daily_change, -max_daily_change, max_daily_change)
            else:
                avg_daily_change = 0
            
            # Generate predictions with dampening effect
            current_price = next_day_pred
            for i in range(7):
                if i == 0:
                    pred = next_day_pred
                else:
                    # Apply dampening to prevent extreme predictions
                    trend_factor = 0.7 ** i  # Exponential dampening
                    pred = current_price + (avg_daily_change * trend_factor)
                    
                    # Ensure prediction stays within reasonable bounds
                    min_price = recent_prices.min() * 0.8
                    max_price = recent_prices.max() * 1.2
                    pred = np.clip(pred, min_price, max_price)
                    
                    current_price = pred
                
                future_predictions.append(pred)
            
            # Calculate model confidence based on R² score
            confidence = max(0, min(1, self.test_score)) if hasattr(self, 'test_score') else 0.5
            accuracy = confidence
            
            return {
                'next_day': next_day_pred,
                'confidence': confidence,
                'accuracy': accuracy,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'future_predictions': future_predictions,
                'train_score': getattr(self, 'train_score', 0),
                'test_score': getattr(self, 'test_score', 0),
                'mse': getattr(self, 'mse', 0)
            }
            
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}
    
    def get_feature_importance(self):
        """Get feature importance from the trained model"""
        if not self.is_trained or not hasattr(self.model, 'coef_'):
            return None
        
        try:
            importance = pd.DataFrame({
                'feature': self.feature_names,
                'importance': np.abs(self.model.coef_)
            }).sort_values('importance', ascending=False)
            
            return importance
        except Exception:
            return None
