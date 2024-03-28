import plotly.graph_objs as go

def visualize_data(transformed_data):
    
    for stock, df in transformed_data.items():
        fig = go.Figure()

        # Add Close Price trace
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price', line=dict(color='blue')))

        # Add Open Price trace
        fig.add_trace(go.Scatter(x=df.index, y=df['Open'], mode='lines', name='Open Price', line=dict(color='orange')))

        # Add 50-Day SMA trace
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], mode='lines', name='50-Day SMA', line=dict(color='red', dash='dash')))

        # Add 200-Day SMA trace
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_200'], mode='lines', name='200-Day SMA', line=dict(color='green', dash='dash')))

        # Add Bollinger Bands
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_upper'], mode='lines', name='Upper Bollinger Band', line=dict(color='gray')))
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_lower'], mode='lines', name='Lower Bollinger Band', line=dict(color='gray')))

        # Update layout
        fig.update_layout(title=f'OHLC Data Visualization for {stock}',
                          xaxis_title='Date',
                          yaxis_title='Price',
                          legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                          margin=dict(l=50, r=50, t=50, b=50),
                          hovermode='x unified')

        # Show plot
        fig.show()
