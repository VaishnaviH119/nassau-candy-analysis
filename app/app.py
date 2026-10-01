import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page-level settings — must be the first Streamlit command
st.set_page_config(page_title="Nassau Candy Profitability", page_icon="🍬", layout="wide")

# Build the CSV path relative to this script's own location, not the launch folder
# (fixes local vs. deployed-server path mismatches)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, "..", "data", "kpi_data.csv"))
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%Y-%m-%d')  # CSV always loses datetime typing, so reconvert every load

theme_colors = ["#7B3F61", "#C97B84", "#E8A0A0", "#F5C6C6", "#2E2E2E"]  # matches .streamlit/config.toml theme

st.title("Nassau Candy Distributor - Profitability Dashboard")

# ---- Sidebar filters ----
st.sidebar.header("Filters")

# "All" option added so the dropdown can mean "no filter", not just a specific division
divisions = ["All"] + sorted(df['Division'].unique().tolist())
selected_division = st.sidebar.selectbox("Select a Division", divisions)

regions = ["All"] + sorted(df['Region'].unique().tolist())
selected_region = st.sidebar.selectbox("Select a Region", regions)

margin_threshold = st.sidebar.slider("Minimum Gross Margin", min_value=0.0, max_value=1.0, value=0.0)

search_term = st.sidebar.text_input("Search for a product")

min_date = df['Order Date'].min()
max_date = df['Order Date'].max()
date_range = st.sidebar.date_input("Select Order Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)


# ---- Apply all filters together onto one shared dataframe ----
# Every tab below reads from filtered_df, so one filter change updates the whole dashboard at once
filtered_df = df.copy()

if selected_division != "All":
    filtered_df = filtered_df[filtered_df['Division'] == selected_division]

if selected_region != "All":
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

filtered_df = filtered_df[filtered_df['Gross Margin'] >= margin_threshold]

if search_term:
    filtered_df = filtered_df[filtered_df['Product Name'].str.contains(search_term, case=False)]

if len(date_range) == 2:  # guards against the moment only one date is picked mid-click
    start_date, end_date = date_range
    filtered_df = filtered_df[(filtered_df['Order Date'] >= pd.to_datetime(start_date)) &
                               (filtered_df['Order Date'] <= pd.to_datetime(end_date))]

st.sidebar.metric("Orders Matching Filters", len(filtered_df))

# Lets the user export exactly what they're currently looking at
st.sidebar.download_button("⬇️ Download filtered data (CSV)", filtered_df.to_csv(index=False), "filtered_data.csv")

# ---- No-results guard ----
# Prevents crashes if the filter combination matches zero rows (e.g. a search term + narrow margin)
if filtered_df.empty:
    st.warning("⚠️ No data matches the current filters. Try widening your selection.")
    st.stop()  # halts the script here — nothing below runs on empty data

# ---- KPI summary cards ----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered_df['Gross Profit'].sum():,.0f}")
col3.metric("Avg Margin", f"{filtered_df['Gross Margin'].mean()*100:.1f}%")
col4.metric("Total Orders", f"{len(filtered_df):,}")

# ---- Product lookup (for browsing without knowing product names) ----
st.markdown("#### 🔍 Quick Product Stats")

product_list = ["-- Select a product --"] + sorted(df['Product Name'].unique().tolist())
selected_product = st.selectbox("Choose a product", product_list)

if selected_product != "-- Select a product --":
    product_data = df[df['Product Name'] == selected_product]

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Total Sales", f"${product_data['Sales'].sum():,.2f}")
    p2.metric("Total Profit", f"${product_data['Gross Profit'].sum():,.2f}")
    p3.metric("Total Units", f"{product_data['Units'].sum():,}")
    p4.metric("Total Orders", f"{len(product_data):,}")

# ---- Product lookup — narrows the tabs below to one product, if selected ----
st.markdown("#### 🔍 Filter Tabs by Product")

product_list = ["-- All Products --"] + sorted(filtered_df['Product Name'].unique().tolist())
selected_product = st.selectbox("Choose a product to focus the tabs below on", product_list)

if selected_product != "-- All Products --":
    filtered_df = filtered_df[filtered_df['Product Name'] == selected_product]


# ---- Tabs ----
tab1, tab2, tab3, tab4 = st.tabs(["📦 Product Overview", "🏭 Division Performance", "💰 Cost Diagnostics", "📊 Pareto Analysis"])

with tab1:
    st.subheader("Product Profitability Overview")
    product_summary = filtered_df.groupby('Product Name').agg({
        'Sales': 'sum', 'Cost': 'sum', 'Gross Profit': 'sum', 'Gross Margin': 'mean', 'Units': 'sum'
    }).sort_values('Gross Profit', ascending=False)
    st.dataframe(product_summary)

    # Dynamically flags any product currently in view with margin below 20% —
    # reflects the Kazookles-style risk finding from the analysis, recalculated live as filters change
    risky = product_summary[product_summary['Gross Margin'] < 0.20]
    if not risky.empty:
        st.error(f"⚠️ Margin risk: {', '.join(risky.index)} — below 20% gross margin. Recommend pricing/cost review.")

    margin_leaderboard = product_summary.sort_values('Gross Margin', ascending=True)  # ascending so best margin lands at top of horizontal bar
    fig = px.bar(margin_leaderboard, x='Gross Margin', y=margin_leaderboard.index, orientation='h',
                title='Product Margin Leaderboard', color_discrete_sequence=theme_colors)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Division Performance")
    division_summary = filtered_df.groupby('Division').agg({'Sales': 'sum', 'Gross Profit': 'sum', 'Gross Margin': 'mean'})
    st.dataframe(division_summary)

    col1, col2 = st.columns(2)  # side-by-side charts instead of stacked
    with col1:
        fig1 = px.bar(division_summary, x=division_summary.index, y=['Sales', 'Gross Profit'], barmode='group',
                      title='Revenue vs Profit by Division', color_discrete_sequence=theme_colors)
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.bar(division_summary, x=division_summary.index, y='Gross Margin', title='Average Margin by Division',
                      color_discrete_sequence=theme_colors)
        st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Cost vs Margin Diagnostics")
    product_summary_full = filtered_df.groupby('Product Name').agg({'Sales': 'sum', 'Cost': 'sum', 'Gross Margin': 'mean'}).reset_index()
    # color = margin (continuous gradient), size = sales — encodes three variables in one 2D chart
    fig3 = px.scatter(product_summary_full, x='Cost', y='Sales', hover_name='Product Name',
                    color='Gross Margin', size='Sales', title='Cost vs Sales (colored by Margin, sized by Sales)',
                    color_continuous_scale=["#F5C6C6", "#7B3F61"])
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.subheader("Profit Concentration (Pareto Analysis)")
    pareto = filtered_df.groupby('Product Name')['Gross Profit'].sum().sort_values(ascending=False).reset_index()
    pareto['Cumulative %'] = pareto['Gross Profit'].cumsum() / pareto['Gross Profit'].sum() * 100

    fig4 = px.bar(pareto, x='Product Name', y='Gross Profit', title='Pareto Chart - Profit Concentration',
                  color_discrete_sequence=theme_colors)
    # Cumulative % line needs its own y-axis (y2) since dollars and percentages are on totally different scales
    fig4.add_scatter(x=pareto['Product Name'], y=pareto['Cumulative %'], mode='lines+markers',
                      name='Cumulative %', yaxis='y2', line=dict(color="#2E2E2E"))
    fig4.update_layout(yaxis2=dict(title='Cumulative %', overlaying='y', side='right', range=[0, 105]))
    st.plotly_chart(fig4, use_container_width=True)

# Collapsed by default via checkbox — keeps the page clean, still available for anyone who wants raw stats
if st.checkbox("**Show Summary Statistics**"):
    st.write(filtered_df.describe())