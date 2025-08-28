import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

class PortfolioManager:
    def __init__(self):
        self.portfolio_data = {}
    
    def get_portfolio_performance(self, symbols, data_fetcher):
        """Get performance data for a list of symbols"""
        performance_data = []
        
        for symbol in symbols:
            try:
                # Get current price data
                current_data = data_fetcher.get_current_price(symbol)
                
                if current_data:
                    performance_data.append({
                        'symbol': symbol,
                        'current_price': current_data['price'],
                        'change': current_data['change'],
                        'change_percent': current_data['change_percent'],
                        'volume': current_data['volume']
                    })
                else:
                    # Add placeholder data if fetch fails
                    performance_data.append({
                        'symbol': symbol,
                        'current_price': 0,
                        'change': 0,
                        'change_percent': 0,
                        'volume': 0
                    })
                    
            except Exception as e:
                st.error(f"Error fetching data for {symbol}: {str(e)}")
                continue
        
        return performance_data
    
    def calculate_portfolio_metrics(self, portfolio_data):
        """Calculate portfolio-level metrics"""
        if not portfolio_data:
            return {}
        
        try:
            df = pd.DataFrame(portfolio_data)
            
            # Calculate metrics
            total_value = df['current_price'].sum()
            total_change = df['change'].sum()
            average_change_percent = df['change_percent'].mean()
            
            # Calculate volatility (simplified)
            volatility = df['change_percent'].std()
            
            # Best and worst performers
            best_performer = df.loc[df['change_percent'].idxmax()]
            worst_performer = df.loc[df['change_percent'].idxmin()]
            
            return {
                'total_value': total_value,
                'total_change': total_change,
                'average_change_percent': average_change_percent,
                'volatility': volatility,
                'best_performer': best_performer.to_dict(),
                'worst_performer': worst_performer.to_dict(),
                'num_stocks': len(df)
            }
            
        except Exception as e:
            st.error(f"Error calculating portfolio metrics: {str(e)}")
            return {}
    
    def get_diversification_metrics(self, symbols, data_fetcher):
        """Calculate portfolio diversification metrics"""
        if len(symbols) < 2:
            return {'diversification_score': 0, 'message': 'Need at least 2 stocks for diversification analysis'}
        
        try:
            # Get historical data for correlation analysis
            historical_data = {}
            for symbol in symbols:
                data = data_fetcher.get_historical_data(symbol, '3M')
                if data is not None and not data.empty:
                    historical_data[symbol] = data['close']
            
            if len(historical_data) < 2:
                return {'diversification_score': 0, 'message': 'Insufficient historical data for analysis'}
            
            # Create correlation matrix
            df = pd.DataFrame(historical_data)
            correlation_matrix = df.corr()
            
            # Calculate average correlation (excluding diagonal)
            mask = np.triu(np.ones_like(correlation_matrix), k=1).astype(bool)
            avg_correlation = correlation_matrix.values[mask].mean()
            
            # Diversification score (lower correlation = better diversification)
            diversification_score = max(0, 1 - abs(avg_correlation))
            
            return {
                'diversification_score': diversification_score,
                'average_correlation': avg_correlation,
                'correlation_matrix': correlation_matrix.to_dict(),
                'message': f'Average correlation: {avg_correlation:.2f}'
            }
            
        except Exception as e:
            return {'diversification_score': 0, 'message': f'Error calculating diversification: {str(e)}'}
    
    def suggest_rebalancing(self, portfolio_data):
        """Suggest portfolio rebalancing based on simple rules"""
        if not portfolio_data or len(portfolio_data) < 2:
            return {'suggestions': [], 'message': 'Need at least 2 stocks for rebalancing suggestions'}
        
        try:
            df = pd.DataFrame(portfolio_data)
            
            # Calculate weights (assuming equal dollar amounts initially)
            total_value = df['current_price'].sum()
            df['weight'] = df['current_price'] / total_value
            
            suggestions = []
            
            # Check for overweight positions (>30% of portfolio)
            overweight = df[df['weight'] > 0.3]
            for _, stock in overweight.iterrows():
                suggestions.append({
                    'type': 'reduce',
                    'symbol': stock['symbol'],
                    'reason': f'Overweight position ({stock["weight"]:.1%})',
                    'action': 'Consider reducing position'
                })
            
            # Check for underweight positions (<5% of portfolio)
            underweight = df[df['weight'] < 0.05]
            for _, stock in underweight.iterrows():
                suggestions.append({
                    'type': 'increase',
                    'symbol': stock['symbol'],
                    'reason': f'Underweight position ({stock["weight"]:.1%})',
                    'action': 'Consider increasing position'
                })
            
            # Check for poorly performing stocks
            poor_performers = df[df['change_percent'] < -10]
            for _, stock in poor_performers.iterrows():
                suggestions.append({
                    'type': 'review',
                    'symbol': stock['symbol'],
                    'reason': f'Poor performance ({stock["change_percent"]:.1%})',
                    'action': 'Review fundamentals'
                })
            
            return {
                'suggestions': suggestions,
                'message': f'Generated {len(suggestions)} rebalancing suggestions'
            }
            
        except Exception as e:
            return {'suggestions': [], 'message': f'Error generating suggestions: {str(e)}'}
    
    def export_portfolio_data(self, portfolio_data):
        """Export portfolio data to CSV format"""
        if not portfolio_data:
            return None
        
        try:
            df = pd.DataFrame(portfolio_data)
            df['timestamp'] = datetime.now()
            
            # Add calculated fields
            total_value = df['current_price'].sum()
            df['weight'] = df['current_price'] / total_value
            df['total_value'] = total_value
            
            return df.to_csv(index=False)
            
        except Exception as e:
            st.error(f"Error exporting portfolio data: {str(e)}")
            return None
