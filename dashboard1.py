import pandas as pd
import panel as pn
import matplotlib.pyplot as plt
from panel.pane import Matplotlib

from BacktestN import *

# Assuming "stat" is an instance of backtesting._stats._Stats
# Replace "backtesting._stats._Stats" with the actual import path if needed

# Extract the data from the _Stats object
stat = provStat()
#print(dir(stat))
data = {
    'Start': stat.Start,
    'End': stat.End,
    'Duration': stat.Duration,
    'Equity Final [$]': stat['Equity Final [$]'],
    'Equity Peak [$]': stat['Equity Peak [$]'],
    'Return [%]': stat['Return [%]'],
    'Buy & Hold Return [%]': stat['Buy & Hold Return [%]'],
    'Return (Ann.) [%]': stat['Return (Ann.) [%]'],
    'Volatility (Ann.) [%]': stat['Volatility (Ann.) [%]'],
    'Sharpe Ratio': stat['Sharpe Ratio'],
    'Sortino Ratio': stat['Sortino Ratio'],
    'Calmar Ratio': stat['Calmar Ratio'],
    'Max. Drawdown [%]': stat['Max. Drawdown [%]'],
    'Avg. Drawdown [%]': stat['Avg. Drawdown [%]'],
    'Max. Drawdown Duration': stat['Max. Drawdown Duration'],
    'Avg. Drawdown Duration': stat['Avg. Drawdown Duration'],
    '# Trades': stat['# Trades'],
    'Win Rate [%]': stat['Win Rate [%]'],
    'Best Trade [%]': stat['Best Trade [%]'],
    'Worst Trade [%]': stat['Worst Trade [%]'],
    'Avg. Trade [%]': stat['Avg. Trade [%]'],
    'Max. Trade Duration': stat['Max. Trade Duration'],
    'Avg. Trade Duration': stat['Avg. Trade Duration'],
    'Profit Factor': stat['Profit Factor'],
    'Expectancy [%]': stat['Expectancy [%]'],
    'SQN': stat.SQN,
}

# Create a pandas Series from the extracted data
stat_series = pd.Series(data)

# Convert the Series to a DataFrame
stat_df = pd.DataFrame(stat_series).transpose()

# Create the dashboard layout (similar to the previous example)
section1 = pn.Column(
    pn.pane.Markdown("### Backtest Summary"),
    pn.widgets.DataFrame(stat_df[['Start', 'End', 'Duration', 'Equity Final [$]', 'Equity Peak [$]', 'Return [%]', 'Buy & Hold Return [%]', 'Return (Ann.) [%]']])
)
# Create the bar graph for Equity Final and Equity Peak
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(['Equity Final', 'Equity Peak'], [stat_df['Equity Final [$]'].values[0], stat_df['Equity Peak [$]'].values[0]])
ax.set_ylabel('Equity [$]')
ax.set_title('Backtest Summary - Equity Final and Equity Peak')
plot_bar = pn.pane.Matplotlib(fig, tight=True)

# Create the pie chart for Return Percentage (green if positive, red if negative)
return_percentage = stat_df['Return [%]'].values[0]
if return_percentage >= 0:
    colors = ['green']
else:
    colors = ['red']

fig_pie, ax_pie = plt.subplots(figsize=(4, 4))
ax_pie.pie([abs(return_percentage), 100 - abs(return_percentage)], labels=['Return [%]', ''], colors=colors)
ax_pie.set_title('Backtest Summary - Return Percentage')
plot_pie = pn.pane.Matplotlib(fig_pie, tight=True)

# Create the Panel components for buy and hold value and the plots
buy_and_hold_value = pn.pane.Str(f"Buy & Hold Value: {stat_df['Buy & Hold Return [%]'].values[0]}%", styles={'font-weight': 'bold'})

# Create the Backtest Summary tab with two rows and two columns
backtest_summary_tab = pn.Column(
    pn.Row(pn.Spacer(width=20), plot_bar, pn.Spacer(width=20), pn.Column(buy_and_hold_value, plot_pie, align='center')),
    pn.Row(pn.Spacer(height=20), align='center'),
    align='center'
)


section2 = pn.Column(
    pn.pane.Markdown("### Performance Metrics"),
    pn.widgets.DataFrame(stat_df[['Volatility (Ann.) [%]', 'Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio', 'Max. Drawdown [%]', 'Avg. Drawdown [%]', 'Max. Drawdown Duration', 'Avg. Drawdown Duration', 'SQN']])
)

section3 = pn.Column(
    pn.pane.Markdown("### Trade Statistics"),
    pn.widgets.DataFrame(stat_df[['# Trades', 'Win Rate [%]', 'Best Trade [%]', 'Worst Trade [%]', 'Avg. Trade [%]', 'Max. Trade Duration', 'Avg. Trade Duration', 'Profit Factor', 'Expectancy [%]']])
)

# Create the overall dashboard layout
dashboard = pn.Tabs(
    ("Backtest Summary", section1),
    ("Performance Metrics", section2),
    ("Trade Statistics", section3),
)

# Display the dashboard
dashboard.show()