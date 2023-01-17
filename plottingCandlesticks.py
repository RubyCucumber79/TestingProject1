import plotly.graph_objects as go

def plot_candlesticks(df):
    # Create the trace for the candlesticks
    trace = go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing_line=dict(color='green'),
        decreasing_line=dict(color='red'),
    )

    # Create the layout for the plot
    layout = go.Layout(
        xaxis=dict(rangeslider=dict(visible=True),
                   fixedrange=False),
        yaxis=dict(fixedrange=False,
                   scaleanchor="x",
                   scaleratio=1,
                   range=[min(df.Low), max(df.High)],
                   hoverformat='.2f')
    )

    # Create the figure
    fig = go.Figure(data=[trace], layout=layout)

    # Show the plot
    fig.show()
