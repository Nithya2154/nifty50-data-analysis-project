import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
from sqlalchemy import create_engine
import locale
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import math

locale.setlocale(locale.LC_ALL, 'en_IN')

st.set_page_config(page_title="App", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E0E0E;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style='color:white; text-align:center;'>
        Nifty 50 - Market Summary & Top Performers
    </h1>
    """,
    unsafe_allow_html=True
)
engine = create_engine(
    "postgresql+psycopg2://postgres:12345@localhost:5432/Stock_Db"
)
df = pd.read_sql("SELECT * FROM stock_data", engine)


#Total Number of Stocks
total_number_of_Stocks=df['Ticker'].nunique()

# ○ Top 10 Green Stocks: Sort the stocks based on their yearly return and select the top 10.

df_one = df.copy()

df_one['financial_year'] = df_one['date'].apply(
    lambda x: x.year if x.month >= 4 else x.year - 1
)

df_one = (
    df_one.groupby('Ticker')
    .agg(first_close=('close', 'first'),
         last_close=('close', 'last'))
    .reset_index()
)

df_one['yearly_returns'] = (
    (df_one['last_close'] - df_one['first_close']) /
    df_one['first_close']
) * 100

# Split green and red stocks
green = df_one[df_one['yearly_returns'] > 0].sort_values('yearly_returns', ascending=False,ignore_index=True)
red = df_one[df_one['yearly_returns'] <= 0].sort_values('yearly_returns',ignore_index=True)

# Top/Bottom 10
top_10_green = green.head(10)
bottom_10_red = red.head(10)

# Save to PostgreSQL
top_10_green.to_sql('top_10_green', engine, index=False, if_exists='replace', method='multi')
bottom_10_red.to_sql('bottom_10_red', engine, index=False, if_exists='replace', method='multi')


green.to_sql('greenStock', engine, index=False, if_exists='replace', method='multi')
red.to_sql('redStock', engine, index=False, if_exists='replace', method='multi')

# Number of Total Green and Red Stocks
total_no_green_stocks=green['Ticker'].nunique()
total_no_red_stocks=red['Ticker'].nunique()

# Average Close
avg_close = round(df['close'].mean(), 2)

# Average Volumne
avg_volume = df['volume'].mean()
avg_volume_formatted = locale.format_string('%.2f', avg_volume, grouping=True)

# Green Stock Percentages
green_per=(total_no_green_stocks/total_number_of_Stocks)*100

col1, col2, col3, col4,col5,col6 = st.columns(6)

with col1:
    components.html(f"""
    <div style="
        background-color:#0E0E0E;
        padding:20px;
        border-radius:15px;
        text-align:center;
        width:100%;
        box-shadow:0px 0px 10px rgba(0,0,0,0.5);
    ">
        <div style="font-size:30px; font-weight:bold; color:#7C6BE8">{total_number_of_Stocks}</div>
        <div style="font-size:14px; color:#B0B0B0;">Total Stocks</div>
    </div>
    """, height=150)

with col2:
    components.html(f"""
    <div style="
        background-color:#0E0E0E;
        padding:20px;
        border-radius:15px;
        text-align:center;
        width:100%;
        box-shadow:0px 0px 10px rgba(0,0,0,0.5);
    ">
        <div style="font-size:30px; font-weight:bold; color:#00E676;">{total_no_green_stocks}</div>
        <div style="font-size:14px; color:#B0B0B0;">Green Stocks</div>
    </div>
    """, height=150)

with col3:
    components.html(f"""
    <div style="
        background-color:#0E0E0E;
        padding:20px;
        border-radius:15px;
        text-align:center;
        width:100%;
        box-shadow:0px 0px 10px rgba(0,0,0,0.5);
    ">
        <div style="font-size:30px; font-weight:bold; color:#FF5252;">{total_no_red_stocks}</div>
        <div style="font-size:14px; color:#B0B0B0;">Red Stocks</div>
    </div>
    """, height=150)

with col4:
    components.html(f"""
    <div style="
        background-color:#0E0E0E;
        padding:20px;
        border-radius:15px;
        text-align:center;
        width:100%;
        box-shadow:0px 0px 10px rgba(0,0,0,0.5);
    ">
        <div style="font-size:30px; font-weight:bold; color:#FFD740;">₹ {avg_close}</div>
        <div style="font-size:14px; color:#B0B0B0;">Avg Close</div>
    </div>
    """, height=150)

with col5:
    components.html(f"""
    <div style="
        background-color:#0E0E0E;
        padding:22px;
        border-radius:15px;
        text-align:center;
        width:100%;
        box-shadow:0px 0px 10px rgba(0,0,0,0.5);
    ">
        <div style="font-size:30px; font-weight:bold; color:#3FC1FB;">{avg_volume_formatted}</div>
        <div style="font-size:14px; color:#B0B0B0;">Avg Volume</div>
    </div>
    """, height=150)

with col6:
    components.html(f"""
    <div style="
        background-color:#0E0E0E;
        padding:20px;
        border-radius:15px;
        text-align:center;
        width:100%;
        box-shadow:0px 0px 10px rgba(0,0,0,0.5);
    ">
        <div style="font-size:30px; font-weight:bold; color:#00E274;">{green_per}%</div>
        <div style="font-size:14px; color:#B0B0B0;">Green %</div>
    </div>
    """, height=150)


col7,col8=st.columns(2)
with col7:
    st.markdown(
    """
    <h6 style='color:white; text-align:center;'>
        Top 10 Best Performing Stocks (Yearly Returns)
    </h6>
    """,
    unsafe_allow_html=True
)
        # Plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Dark background
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')

    bars = ax.barh(top_10_green["Ticker"], top_10_green["yearly_returns"], color='green')

    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 5, bar.get_y() + bar.get_height()/2,
                f"+{width:.2f}%", va='center', color='#00ffae', fontsize=10)

    # Styling
    ax.set_xlabel("Returns (%)", color='white')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')

    # Remove top/right borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    st.pyplot(fig)

with col8:

    st.markdown(
    """
    <h6 style='color:white; text-align:center;'>
        Top 10 Worst Performing Stocks (Yearly Returns)
    </h6>
    """,
    unsafe_allow_html=True
    )
    fig, ax = plt.subplots(figsize=(10, 6))

    # Dark background
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')

    bars = ax.barh(
        bottom_10_red["Ticker"],
        bottom_10_red["yearly_returns"],
        color='#ff4d4d'
    )

    # Add value labels (correct for negative values)
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width - 5,  # move left for negative bars
            bar.get_y() + bar.get_height()/2,
            f"{width:.2f}%",  # no '+' sign
            va='center',
            ha='right',
            color='#ff3700',
            fontsize=10
        )

    # Styling
    ax.set_xlabel("Returns (%)", color='white')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')

    # Remove extra borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    st.pyplot(fig)


st.markdown(
    """
    <h2 style='color:white; text-align:center;'>
        Volatility Analysis - Top 10 Most Volatile Nifty 50 Stocks
    </h2>
    """,
    unsafe_allow_html=True
    )
volatility_df = df.copy()

volatility_df['daily_returns'] = volatility_df['close'].pct_change()

# Drop NaN
volatility_df = volatility_df.dropna(subset=['daily_returns'])

# ✅ Group by stock
volatility_summary = (
    volatility_df.groupby('Ticker')['daily_returns']
    .std() * np.sqrt(252)
).reset_index(name='volatility')

# Top 10
Top_10_Most_Volatile = volatility_summary.sort_values(
    by='volatility', ascending=False,ignore_index=True
).head(10)
Top_10_Most_Volatile.columns = ['Ticker', 'Cumulative_Return']


Top_10_Most_Volatile.to_sql(
    name="top10_volatility_data",   # table name
    con=engine,
    if_exists="replace",      # 'replace', 'append', 'fail'
    index=False
)

 # 🔹 Sort ascending
df_plot = Top_10_Most_Volatile.sort_values(by="Cumulative_Return", ascending=False)

# 🎨 Color category
def get_color(val):
    if val > 50:
        return "High"
    elif val > 20:
        return "Medium"
    else:
        return "Low"

df_plot["Category"] = df_plot["Cumulative_Return"].apply(get_color)

# Plot
fig = px.bar(
    df_plot,
    x="Ticker",
    y="Cumulative_Return",
    color="Category",
    text="Cumulative_Return",
    color_discrete_map={
        "High": "#00ffae",
        "Medium": "#f4c542",
        "Low": "#ff4d4d"
    }
)

# ✨ Style
fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

fig.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font=dict(color="white"),
    xaxis_title="Stock",
    yaxis_title="Returns (%)"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
    <h2 style='color:white; text-align:center;'>
        Cumulative Return Over Time — Top 5 Performing Stocks
    </h2>
    """,
    unsafe_allow_html=True
    )
cumulative_df=volatility_df.copy()
cumulative_df['cumulative_return']=(1 + cumulative_df['daily_returns']).groupby(cumulative_df['Ticker']).cumprod() - 1
top_5_performing=cumulative_df.groupby('Ticker')['cumulative_return'].last()
top_5_performing=top_5_performing.sort_values(ascending=False).head(5)

top_5_performing = (
    cumulative_df.groupby('Ticker')['cumulative_return']
      .last()
      .sort_values(ascending=False)
      .head(5)
      .index
)

top5_tick = []

for ticker in top_5_performing:
    top5_tick.append(cumulative_df[cumulative_df['Ticker'] == ticker])

top_5_performing = pd.concat(top5_tick, ignore_index=True)

top5_pivot = top_5_performing.pivot(
    index='date',
    columns='Ticker',
    values='cumulative_return'
)

fig = px.line(
    top_5_performing,
    x="date",
    y="cumulative_return",
    color="Ticker"
)

# 🌙 Dark theme
fig.update_layout(
    plot_bgcolor="#0e1117",
    font=dict(color="white"),
    xaxis_title="Date",
    yaxis_title="Cumulative Return (%)",
    legend_title=""
)

# Smooth lines
fig.update_traces(mode="lines", line=dict(width=3))

# ➖ Zero baseline
fig.add_hline(y=0, line_dash="dash", line_color="gray")

# 🏷️ Final labels (right side)
for ticker in top_5_performing["Ticker"].unique():
    last_point = top_5_performing[
        top_5_performing["Ticker"] == ticker
    ].iloc[-1]

    fig.add_annotation(
        x=last_point["date"],
        y=last_point["cumulative_return"],
        text=f"{ticker} +{last_point['cumulative_return']:.1f}%",
        showarrow=False,
        font=dict(size=12),
        xanchor="left"
    )

# Grid styling
fig.update_xaxes(showgrid=True, gridcolor="#2a2a2a")
fig.update_yaxes(showgrid=True, gridcolor="#2a2a2a")

# 🚀 Show chart
st.plotly_chart(fig, use_container_width=True)

top_5_performing.to_sql(
    name="top5_cumulative_data",   # table name
    con=engine,
    if_exists="replace",      # 'replace', 'append', 'fail'
    index=False
)

# sector_df=pd.read_csv("Sector_df.csv")

# sector_df.to_sql(
#     name="sector_df_data",   # table name
#     con=engine,
#     if_exists="replace",      # 'replace', 'append', 'fail'
#     index=False
# )
st.markdown(
    """
    <h2 style='color:white; text-align:center;'>
        Sector-wise Average Yearly Return (%)
    </h2>
    """,
    unsafe_allow_html=True
    )
sector_df = pd.read_sql("SELECT * FROM sector_df_data", engine)
sector_performance = (
    sector_df
    .groupby('sector', as_index=False)['Daily_Return']
    .mean()
)
sector_performance.to_sql(
    name="sector_performance",   # table name
    con=engine,
    if_exists="replace",      # 'replace', 'append', 'fail'
    index=False
)
# 🔹 Sort ascending (small → big like your image)
df_plot = sector_performance.sort_values(by="Daily_Return", ascending=True)

# 🎨 Color logic (positive = green, negative = red)
df_plot["Category"] = df_plot["Daily_Return"].apply(
    lambda x: "Positive" if x >= 0 else "Negative"
)

fig = px.bar(
    df_plot,
    x="Daily_Return",
    y="sector",
    orientation='h',
    color="Category",
    text="Daily_Return",
    color_discrete_map={
        "Positive": "#00ffae",
        "Negative": "#ff4d4d"
    }
)

# ✨ Value labels
fig.update_traces(
    texttemplate='%{text:.10f}%',
    textposition='outside'
)

# 🌙 Dark theme
fig.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font=dict(color="white"),
    xaxis_title="Average Yearly Return (%)",
    yaxis_title="",
    legend_title=""
)

# Grid styling
fig.update_xaxes(showgrid=True, gridcolor="#2a2a2a")
fig.update_yaxes(showgrid=False)

st.plotly_chart(fig, use_container_width=True)



returns_pivot = cumulative_df.pivot(
    index='date',
    columns='Ticker',
    values='daily_returns'
)

correlation_matrix = returns_pivot.corr()
# st.dataframe(correlation_matrix)

correlation_matrix.to_sql(
    name="correlation_matrix",   # table name
    con=engine,
    if_exists="replace",      # 'replace', 'append', 'fail'
    index=False
)

# correlation_matrix.to_csv(r'C:\Nithyanantham\Mini_Projects\results\question4.csv', index=False)
# 1. Use a large figure size to give the grid more room
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(22, 18))

# 2. Create the heatmap with small internal numbers
sns.heatmap(
    correlation_matrix, 
    annot=True,              # Keep numbers on
    fmt=".2f",               # Two decimal places
    annot_kws={"size": 6},   # LOW FONT SIZE for numbers inside squares
    cmap="RdYlGn", 
    center=0,
    linewidths=0.1,          # Very thin lines for the grid
    linecolor='#222222', 
    cbar_kws={"label": "Correlation Coefficient", "shrink": 0.8},
    ax=ax
)

# 3. Formatting labels
ax.set_title("Stock Price Correlation Heatmap\n", fontsize=25, fontweight='bold')

# Adjust ticker label font size to be readable but compact
plt.xticks(rotation=90, fontsize=9) 
plt.yticks(rotation=0, fontsize=9)

# 4. Display in Streamlit
st.pyplot(fig)

# sector_df.groupby('month')['Daily_Return']
# # monthly_returns = (
# #     sector_df.sort_values(['Ticker', 'date'])
# #       .groupby(['month', 'Ticker'])['Daily_Return']
# #       .apply(lambda x: (1 + x).prod() - 1)
# #       .reset_index(name='monthly_return')
# # )
# st.dataframe(sector_df)

# Clean hidden characters from column names
sector_df.columns = sector_df.columns.str.replace('^\ufeff', '', regex=True)
# 1. Clean the column names (Fixes the KeyError)
sector_df.columns = sector_df.columns.str.replace('^\ufeff', '', regex=True)

# 2. Calculate Monthly Returns
monthly_returns = (
    sector_df.sort_values(['Ticker', 'date'])
      .groupby(['month', 'Ticker'])['Daily_Return']
      .apply(lambda x: (1 + x).prod() - 1)
      .reset_index(name='monthly_return')
)

monthly_returns=monthly_returns.sort_values(by='monthly_return')
monthly_returns.to_sql(
    name="monthly_returns",   # table name
    con=engine,
    if_exists="replace",      # 'replace', 'append', 'fail'
    index=False
)

top5_gainers = (
    monthly_returns
    .sort_values(['month', 'monthly_return'], ascending=[True, False])
    .groupby('month')
    .head(5)
)

top5_losers = (
    monthly_returns
    .sort_values(['month', 'monthly_return'], ascending=[True, True])
    .groupby('month')
    .head(5)
)

# 1. Calculate grid size dynamically
months = sorted(monthly_returns['month'].unique())
n_months = len(months)
cols = 4
rows = math.ceil(n_months / cols)

plt.style.use('dark_background')
fig, axes = plt.subplots(rows, cols, figsize=(20, 5 * rows)) # Height scales with rows
plt.subplots_adjust(hspace=0.5, wspace=0.4)
fig.suptitle("Monthly Top 5 Gainers & Losers", fontsize=22, fontweight='bold', y=0.98)

# 2. Iterate through months
# We use axes.flatten() but handle cases where months < subplots
flat_axes = axes.flatten() if n_months > 1 else [axes]

for i, month in enumerate(months):
    ax = flat_axes[i]
    
    # Filter and combine data
    m_gainers = top5_gainers[top5_gainers['month'] == month].copy()
    m_losers = top5_losers[top5_losers['month'] == month].copy()
    combined = pd.concat([m_losers, m_gainers]).sort_values('monthly_return')
    
    # Plotting logic
    colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in combined['monthly_return']]
    bars = ax.barh(combined['Ticker'], combined['monthly_return'] * 100, color=colors)
    
    # Add labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f}%', va='center', fontsize=8, fontweight='bold')

    # Formatting
    ax.set_title(f"{month}", fontsize=14, fontweight='bold')
    ax.axvline(0, color='white', linewidth=0.8)
    ax.tick_params(labelsize=8)

# 3. Hide any empty subplots (e.g., if you have 13 months, hide the remaining 3 empty boxes)
for j in range(i + 1, len(flat_axes)):
    flat_axes[j].axis('off')

st.pyplot(fig)