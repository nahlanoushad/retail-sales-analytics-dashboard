import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the sales data
df = pd.read_csv("cleaned_retail_sales.csv")

df['OrderDate'] = pd.to_datetime(df['OrderDate'])

# Set the page title
st.set_page_config(
    page_title="Retail Sales Dashboard",
    layout="wide"
)
st.markdown("""
<style>
[data-testid="stMetric"] {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #334155;
    text-align: center;
}

[data-testid="stMetricLabel"] {
    font-size: 16px;
    font-weight: bold;
}

[data-testid="stMetricValue"] {
    font-size: 28px;
}
</style>
""", unsafe_allow_html=True)
st.title("Retail Sales Dashboard")

st.markdown("Business Performance Analysis Dashboard")

#creating sidebar filters
st.sidebar.title("Dashboard Filters")
st.sidebar.header("Filters")
# Region
select_all_region = st.sidebar.checkbox(
    "Select All Regions",
    value=True
)

if select_all_region:
    selected_region = df['Region'].unique().tolist()
else:
    selected_region = st.sidebar.multiselect(
        "Region",
        df['Region'].unique()
    )

# Category
select_all_category = st.sidebar.checkbox(
    "Select All Categories",
    value=True
)

if select_all_category:
    selected_category = df['Category'].unique().tolist()
else:
    selected_category = st.sidebar.multiselect(
        "Category",
        df['Category'].unique()
    )

# Segment
select_all_segment = st.sidebar.checkbox(
    "Select All Segments",
    value=True
)

if select_all_segment:
    selected_segment = df['Segment'].unique().tolist()
else:
    selected_segment = st.sidebar.multiselect(
        "Segment",
        df['Segment'].unique()
    )
#date range filter

st.sidebar.markdown("---")

st.sidebar.subheader("📅 Date Filter")

date_range = st.sidebar.date_input(
    "Date Range",
    [
        df['OrderDate'].min(),
        df['OrderDate'].max()
    ]
)
st.info(
    f"Showing data from {date_range[0]} to {date_range[1]}")
#apply filters to the dataframe
filtered_df = df.copy()

# Region Filter
if selected_region:
    filtered_df = filtered_df[
        filtered_df['Region'].isin(selected_region)
    ]

# Category Filter
if selected_category:
    filtered_df = filtered_df[
        filtered_df['Category'].isin(selected_category)
    ]

# Segment Filter
if selected_segment:
    filtered_df = filtered_df[
        filtered_df['Segment'].isin(selected_segment)
    ]
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])
filtered_df = filtered_df[
    (filtered_df['OrderDate'] >= start_date)
    &
    (filtered_df['OrderDate'] <= end_date)
]

st.subheader("📊 Business Performance Overview")
#calculate total sales,profit,orders
revenue = filtered_df['Sales'].sum()

profit = filtered_df['Profit'].sum()

orders = filtered_df['OrderID'].nunique()

aov = revenue / orders if orders > 0 else 0

profit_margin = (
    profit / revenue * 100
    if revenue > 0
    else 0
)
#creating KPI cards
col1,col2,col3,col4,col5 = st.columns(5)

with col1:
    st.metric(
        label="💰 Revenue",
        value=f"${revenue:,.0f}"
    )

with col2:
    st.metric(
        label="📈 Profit",
        value=f"${profit:,.0f}"
    )

with col3:
    st.metric(
        label="🛒 Orders",
        value=f"{orders:,}"
    )

with col4:
    st.metric(
        label="💳 AOV",
        value=f"${aov:.2f}"
    )

with col5:
    st.metric(
        label="📊 Margin",
        value=f"{profit_margin:.1f}%"
    )

# Monthly Sales Trend(seasonality)

filtered_df['YearMonth'] = (
    filtered_df['OrderDate']
    .dt.to_period('M')
    .astype(str)
)

monthly_sales = (
    filtered_df
    .groupby('YearMonth')['Sales']
    .sum()
    .reset_index()
)

fig_monthly_sales = px.line(
    monthly_sales,
    x='YearMonth',
    y='Sales',
    title='Monthly Sales Trend (Seasonality)',
    markers=True
)


# Sales by Category

category_sales = (
    filtered_df
    .groupby('Category')['Sales']
    .sum()
    .reset_index()
)

fig_category_sales = px.bar(
    category_sales,
    x='Category',
    y='Sales',
    title='Sales by Category'
)

# Top 10 Customers

top_customers = (
    filtered_df
    .groupby('CustomerName')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_top_customers = px.bar(
    top_customers,
    x='Sales',
    y='CustomerName',
    orientation='h',
    title='Top 10 Customers by Sales',
    text_auto='.2s'
)

fig_top_customers.update_layout(
    yaxis={'categoryorder': 'total ascending'}
)

# Region Comparison

region_data = (
    filtered_df
    .groupby('Region')[['Sales','Profit']]
    .sum()
    .reset_index()
)

fig_region = px.bar(
    region_data,
    x='Region',
    y=['Sales','Profit'],
    barmode='group',
    title='Sales vs Profit by Region'
)
st.subheader("📈 Sales Analysis")

revenue = filtered_df['Sales'].sum()

profit = filtered_df['Profit'].sum()

orders = filtered_df['OrderID'].nunique()

aov = revenue / orders if orders > 0 else 0

profit_margin = (
    profit / revenue * 100
    if revenue > 0
    else 0
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig_monthly_sales,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fig_category_sales,
        use_container_width=True
    )

st.subheader("🌍 Customer & Region Analysis")

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(
        fig_top_customers,
        use_container_width=True
    )

with col4:
    st.plotly_chart(
        fig_region,
        use_container_width=True
    )
st.subheader("Filtered Sales Data")

st.write(f"Showing {len(filtered_df):,} records")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)
#footer
st.markdown("_ _ _")
st.caption(
    "created by Fathima Nahla Noushad EV| retail Sales Dashboard " 
)
