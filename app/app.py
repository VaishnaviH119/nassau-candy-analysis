import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Nassau Candy Profitability", page_icon="🍬", layout="wide")

st.title("Nassau Candy Distributor - Profitability Dashboard")

tab1, tab2, tab3, tab4 = st.tabs(["📦 Product Overview", "🏭 Division Performance", "💰 Cost Diagnostics", "📊 Pareto Analysis"])

df = pd.read_csv("../data/kpi_data.csv")
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%Y-%m-%d')

with tab1:
    st.subheader("Product Profitability Overview")

    product_summary = df.groupby('Product Name').agg({
        'Sales': 'sum',
        'Cost': 'sum',
        'Gross Profit': 'sum',
        'Gross Margin': 'mean',
        'Units': 'sum'
    }).sort_values('Gross Profit', ascending=False)

    st.dataframe(product_summary)
    

    margin_leaderboard = product_summary.sort_values('Gross Margin', ascending=True)

    fig = px.bar(margin_leaderboard, x='Gross Margin', y=margin_leaderboard.index, orientation='h', 
                title='Product Margin Leaderboard')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Division Performance")

    division_summary = df.groupby('Division').agg({
        'Sales': 'sum',
        'Gross Profit': 'sum',
        'Gross Margin': 'mean'
    })

    st.dataframe(division_summary)

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(division_summary, x=division_summary.index, y=['Sales', 'Gross Profit'], barmode='group', title='Revenue vs Profit by Division')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(division_summary, x=division_summary.index, y='Gross Margin', title='Average Margin by Division')
        st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.write("Cost vs Margin Diagnostics")

    product_summary_full = df.groupby('Product Name').agg({
        'Sales': 'sum',
        'Cost': 'sum', 
        'Gross Margin': 'mean'
    }).reset_index()

    fig3 = px.scatter(product_summary_full, x='Cost', y='Sales', hover_name='Product Name',
                    color='Gross Margin', size='Sales',
                    title='Cost vs Sales (colored by Margin, sized by Sales)')
    st.plotly_chart(fig3, use_container_width=True)
    
with tab4:
    st.subheader("Profit Concentration (Pareto Analysis)")

    pareto = df.groupby('Product Name')['Gross Profit'].sum().sort_values(ascending=False).reset_index()
    pareto['Cumulative %'] = pareto['Gross Profit'].cumsum() / pareto['Gross Profit'].sum() * 100

    fig4 = px.bar(pareto, x='Product Name', y='Gross Profit', title='Pareto Chart - Profit Concentration')
    fig4.add_scatter(x=pareto['Product Name'], y=pareto['Cumulative %'], mode='lines+markers', name='Cumulative %', yaxis='y2')
    fig4.update_layout(yaxis2=dict(title='Cumulative %', overlaying='y', side='right', range=[0, 105]))

    st.plotly_chart(fig4, use_container_width=True)

    st.write("5 of 15 products (33%) account for 95.1% of total Gross Profit - all 5 are Wonka Bar variants.")




st.write("Here's a preview of the data:")
st.dataframe(df)

# Get the list of unique divisions
divisions = df['Division'].unique()

# Add a selectbox for the user to choose a division
selected_division = st.selectbox("Select a Division", divisions)

# Filter the dataframe based on the selected division
filtered_df = df[df['Division'] == selected_division]

st.write(f"Data for Division: {selected_division}")
st.metric("Number of Orders", len(filtered_df))
st.dataframe(filtered_df)

# Add the slider
margin_threshold = st.slider("Minimum Gross Margin", min_value=0.0, max_value=1.0, value=0.5)

# Filter based on the selected division and margin threshold
filtered_by_margin = df[df['Gross Margin'] >= margin_threshold]

# Show the count and the table 
st.metric("Orders Meeting Margin Threshold", len(filtered_by_margin))
st.dataframe(filtered_by_margin)

# Add the search box for product search
search_term = st.text_input("Search for a product")

# Filter the dataframe based on the search term
if search_term:
    filtered_by_product = df[df['Product Name'].str.contains(search_term, case=False)]
    st.dataframe(filtered_by_product)

# Figure out the actual min/max dates in the data
min_date = df['Order Date'].min()
max_date = df['Order Date'].max()

# Add the date range widget
date_range = st.date_input("Select Order Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

# Filter using the selected date range
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_by_date = df[(df['Order Date'] >= pd.to_datetime(start_date)) & (df['Order Date'] <= pd.to_datetime(end_date))]
    st.metric("Orders in Date Range", len(filtered_by_date))
    st.dataframe(filtered_by_date)
    

# Add a checkbox to show/hide the summary statistics
if st.checkbox("Show Summary Statistics"):
    st.write("Summary Statistics:")
    st.write(df.describe()) 