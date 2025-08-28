import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ChartGenerator:
    def __init__(self):
        self.colors = {
            'bullish': '#00ff88',
            'bearish': '#ff4444',
            'neutral': '#888888',
            'volume': '#666666',
            'prediction': '#ff9900',
            'confidence': '#ffcc00'
        }
    
    def create_candlestick_chart(self, data, symbol):
        """Create candlestick chart with volume"""
        if data.empty:
            return self._create_empty_chart("No data available")
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=[f'{symbol} Price', 'Volume'],
            row_width=[0.2, 0.7]
        )
        
        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                name='Price',
                increasing_line_color=self.colors['bullish'],
                decreasing_line_color=self.colors['bearish']
            ),
            row=1, col=1
        )
        
        # Volume chart
        colors = ['red' if data['close'].iloc[i] < data['open'].iloc[i] else 'green' 
                 for i in range(len(data))]
        
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.7
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            title=f'{symbol} Candlestick Chart',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            template='plotly_dark',
            showlegend=True,
            height=600,
            xaxis_rangeslider_visible=False
        )
        
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        
        return fig
    
    def create_technical_chart(self, data, symbol):
        """Create technical analysis chart with indicators"""
        if data.empty:
            return self._create_empty_chart("No data available")
        
        fig = go.Figure()
        
        # Price line
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['close'],
                mode='lines',
                name='Close Price',
                line=dict(color='white', width=2)
            )
        )
        
        # Moving averages if available
        if 'ma_5' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['ma_5'],
                    mode='lines',
                    name='MA 5',
                    line=dict(color='yellow', width=1)
                )
            )
        
        if 'ma_10' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['ma_10'],
                    mode='lines',
                    name='MA 10',
                    line=dict(color='orange', width=1)
                )
            )
        
        if 'ma_20' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['ma_20'],
                    mode='lines',
                    name='MA 20',
                    line=dict(color='red', width=1)
                )
            )
        
        # Bollinger Bands if available
        if 'bb_upper' in data.columns and 'bb_lower' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['bb_upper'],
                    mode='lines',
                    name='BB Upper',
                    line=dict(color='gray', width=1, dash='dash')
                )
            )
            
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['bb_lower'],
                    mode='lines',
                    name='BB Lower',
                    line=dict(color='gray', width=1, dash='dash'),
                    fill='tonexty',
                    fillcolor='rgba(128,128,128,0.1)'
                )
            )
        
        # Update layout
        fig.update_layout(
            title=f'{symbol} Technical Analysis',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            template='plotly_dark',
            showlegend=True,
            height=500
        )
        
        return fig
    
    def create_volume_chart(self, data, symbol):
        """Create volume analysis chart"""
        if data.empty:
            return self._create_empty_chart("No data available")
        
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=[f'{symbol} Volume', 'Volume Moving Average'],
            row_width=[0.7, 0.3]
        )
        
        # Volume bars
        colors = ['red' if data['close'].iloc[i] < data['open'].iloc[i] else 'green' 
                 for i in range(len(data))]
        
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.7
            ),
            row=1, col=1
        )
        
        # Volume moving average
        if 'volume_ma' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['volume_ma'],
                    mode='lines',
                    name='Volume MA',
                    line=dict(color='yellow', width=2)
                ),
                row=2, col=1
            )
        
        # Update layout
        fig.update_layout(
            title=f'{symbol} Volume Analysis',
            template='plotly_dark',
            showlegend=True,
            height=500
        )
        
        fig.update_yaxes(title_text="Volume", row=1, col=1)
        fig.update_yaxes(title_text="Volume MA", row=2, col=1)
        
        return fig
    
    def create_prediction_chart(self, data, predictions, symbol):
        """Create prediction chart with confidence intervals"""
        if data.empty or 'error' in predictions:
            return self._create_empty_chart("No predictions available")
        
        fig = go.Figure()
        
        # Historical prices
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['close'],
                mode='lines',
                name='Historical Price',
                line=dict(color='white', width=2),
                hovertemplate='<b>%{x}</b><br>Price: $%{y:.2f}<extra></extra>'
            )
        )
        
        # Prediction point
        last_date = data.index[-1]
        next_date = last_date + timedelta(days=1)
        
        fig.add_trace(
            go.Scatter(
                x=[next_date],
                y=[predictions['next_day']],
                mode='markers',
                name='Next Day Prediction',
                marker=dict(
                    color=self.colors['prediction'],
                    size=12,
                    symbol='star'
                ),
                hovertemplate='<b>%{x}</b><br>Predicted Price: $%{y:.2f}<extra></extra>'
            )
        )
        
        # Confidence interval as filled area
        if 'lower_bound' in predictions and 'upper_bound' in predictions:
            # Upper bound line
            fig.add_trace(
                go.Scatter(
                    x=[next_date],
                    y=[predictions['upper_bound']],
                    mode='lines',
                    name='Upper Confidence',
                    line=dict(color=self.colors['confidence'], width=0),
                    showlegend=False,
                    hovertemplate='<b>%{x}</b><br>Upper Bound: $%{y:.2f}<extra></extra>'
                )
            )
            
            # Lower bound line with fill
            fig.add_trace(
                go.Scatter(
                    x=[next_date],
                    y=[predictions['lower_bound']],
                    mode='lines',
                    name='Confidence Interval',
                    line=dict(color=self.colors['confidence'], width=0),
                    fill='tonexty',
                    fillcolor='rgba(255, 204, 0, 0.2)',
                    hovertemplate='<b>%{x}</b><br>Lower Bound: $%{y:.2f}<extra></extra>'
                )
            )
        
        # Future predictions
        if 'future_predictions' in predictions:
            future_dates = [last_date + timedelta(days=i+1) for i in range(len(predictions['future_predictions']))]
            fig.add_trace(
                go.Scatter(
                    x=future_dates,
                    y=predictions['future_predictions'],
                    mode='lines+markers',
                    name='7-Day Forecast',
                    line=dict(color=self.colors['prediction'], width=2, dash='dash'),
                    marker=dict(size=6),
                    hovertemplate='<b>%{x}</b><br>Predicted Price: $%{y:.2f}<extra></extra>'
                )
            )
        
        # Calculate appropriate y-axis range
        all_prices = list(data['close'])
        if 'next_day' in predictions:
            all_prices.append(predictions['next_day'])
        if 'future_predictions' in predictions:
            all_prices.extend(predictions['future_predictions'])
        if 'lower_bound' in predictions:
            all_prices.append(predictions['lower_bound'])
        if 'upper_bound' in predictions:
            all_prices.append(predictions['upper_bound'])
        
        min_price = min(all_prices)
        max_price = max(all_prices)
        price_range = max_price - min_price
        padding = price_range * 0.1  # 10% padding
        
        # Update layout with proper scaling
        fig.update_layout(
            title=f'{symbol} AI Price Predictions',
            xaxis_title='Date',
            yaxis_title='Price (USD per Share)',
            template='plotly_dark',
            showlegend=True,
            height=500,
            yaxis=dict(
                range=[min_price - padding, max_price + padding],
                tickformat='$,.2f'
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(128,128,128,0.2)'
            )
        )
        
        # Add price format buttons
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    direction="left",
                    buttons=list([
                        dict(
                            args=[{"yaxis.tickformat": "$,.2f"}],
                            label="USD",
                            method="relayout"
                        ),
                        dict(
                            args=[{"yaxis.tickformat": "$,.0f"}],
                            label="Rounded",
                            method="relayout"
                        )
                    ]),
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.01,
                    xanchor="left",
                    y=1.02,
                    yanchor="top"
                ),
            ]
        )
        
        return fig
    
    def create_correlation_matrix(self, data):
        """Create correlation matrix heatmap"""
        if data.empty:
            return self._create_empty_chart("No data available")
        
        # Select numeric columns
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return self._create_empty_chart("Insufficient numeric data")
        
        # Calculate correlation matrix
        corr_matrix = data[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Feature Correlation Matrix',
            template='plotly_dark',
            height=500
        )
        
        return fig
    
    def _create_empty_chart(self, message):
        """Create empty chart with message"""
        fig = go.Figure()
        fig.add_annotation(
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            text=message,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            template='plotly_dark',
            height=400,
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
        return fig
