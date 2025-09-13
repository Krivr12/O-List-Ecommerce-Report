import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Olist E-commerce Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    """
    Load processed data from CSV files with caching for performance.
    This function runs only once when the app starts or when data changes.
    """
    try:
        customers = pd.read_csv('data/processed/customers_processed.csv')
        orders = pd.read_csv('data/processed/orders_processed.csv')
        
        date_columns = ['order_purchase_dt', 'order_approved_dt', 
                       'order_delivered_carrier_dt', 'order_delivered_customer_dt', 
                       'order_estimated_delivery_dt']
        
        
        for col in date_columns:
            if col in orders.columns:
                orders[col] = pd.to_datetime(orders[col], errors='coerce')
        
        orders['order_month'] = orders['order_purchase_dt'].dt.to_period('M').astype(str)
        
        return customers, orders
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

@st.cache_data
def get_filter_options(customers, orders):
    """
    Extract unique values for filter dropdowns
    """
    states = ['All States'] + sorted(customers['customer_state'].unique().tolist())
    months = ['All Months'] + sorted(orders['order_month'].dropna().unique().tolist())
    return states, months

def filter_data(customers, orders, selected_state, selected_month):
    """
    Apply filters to the datasets based on user selections
    """
    if selected_state != 'All States':
        filtered_customers = customers[customers['customer_state'] == selected_state]
        customer_ids = filtered_customers['customer_id'].unique()
        filtered_orders = orders[orders['customer_id'].isin(customer_ids)]
    else:
        filtered_customers = customers.copy()
        filtered_orders = orders.copy()
    
    if selected_month != 'All Months':
        filtered_orders = filtered_orders[filtered_orders['order_month'] == selected_month]
    
    return filtered_customers, filtered_orders

def calculate_kpis(customers, orders):
    """
    Calculate key performance indicators for the dashboard
    """
    total_orders = len(orders)
    total_customers = len(customers)
    
    delivered_orders = orders[orders['order_status'] == 'delivered'].copy()
    if not delivered_orders.empty:
        delivered_orders['delivery_days'] = (
            delivered_orders['order_delivered_customer_dt'] - 
            delivered_orders['order_purchase_dt']
        ).dt.days
        avg_delivery_days = delivered_orders['delivery_days'].mean()
    else:
        avg_delivery_days = 0
    
    most_common_status = orders['order_status'].mode().iloc[0] if not orders.empty else 'N/A'
    
    return total_orders, total_customers, avg_delivery_days, most_common_status

def create_orders_timeline(orders):
    """
    Create monthly orders trend line chart
    """
    if orders.empty:
        return go.Figure().add_annotation(text="No data available", showarrow=False)
    
    monthly_orders = orders.groupby('order_month').size().reset_index(name='order_count')
    
    fig = px.line(
        monthly_orders, 
        x='order_month', 
        y='order_count',
        title='Orders Over Time (Monthly Trend)',
        markers=True
    )
    
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Number of Orders',
        hovermode='x unified'
    )
    
    return fig

def create_brazil_map(customers):
    """
    Create Brazil choropleth map showing customer density by state
    """
    if customers.empty:
        return go.Figure().add_annotation(text="No data available", showarrow=False)
    
    state_counts = customers['customer_state'].value_counts().reset_index()
    state_counts.columns = ['state', 'customer_count']
    
    fig = px.choropleth(
        state_counts,
        locations='state',
        color='customer_count',
        locationmode='geojson-id',
        title='Customer Distribution by State',
        color_continuous_scale='Blues',
        labels={'customer_count': 'Number of Customers'}
    )
    
    fig.update_geos(
        visible=False,
        projection_type='natural earth',
        showlakes=True,
        showcountries=True
    )
    
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
        )
    )
    
    return fig

def create_order_status_chart(orders):
    """
    Create order status distribution donut chart
    """
    if orders.empty:
        return go.Figure().add_annotation(text="No data available", showarrow=False)
    
    status_counts = orders['order_status'].value_counts()
    
    fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title='Order Status Distribution',
        hole=0.4  
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig

def create_delivery_time_chart(orders):
    """
    Create delivery time distribution histogram
    """
    delivered_orders = orders[orders['order_status'] == 'delivered'].copy()
    
    if delivered_orders.empty:
        return go.Figure().add_annotation(text="No delivered orders data available", showarrow=False)
    
    delivered_orders['delivery_days'] = (
        delivered_orders['order_delivered_customer_dt'] - 
        delivered_orders['order_purchase_dt']
    ).dt.days
    
    delivered_orders = delivered_orders[delivered_orders['delivery_days'] <= 100]
    
    fig = px.histogram(
        delivered_orders,
        x='delivery_days',
        nbins=30,
        title='Delivery Time Distribution (Days)',
        labels={'delivery_days': 'Delivery Days', 'count': 'Number of Orders'}
    )
    
    avg_delivery = delivered_orders['delivery_days'].mean()
    fig.add_vline(x=avg_delivery, line_dash="dash", line_color="red",
                  annotation_text=f"Avg: {avg_delivery:.1f} days")
    
    return fig

def create_customer_segments_chart(customers, orders):
    """
    Create customer segmentation chart (new vs repeat customers)
    """
    if orders.empty:
        return go.Figure().add_annotation(text="No data available", showarrow=False)
    
    customer_order_counts = orders['customer_id'].value_counts()
    
    segments = []
    for count in customer_order_counts.values:
        if count == 1:
            segments.append('One-time Customer')
        elif count <= 3:
            segments.append('Repeat Customer (2-3 orders)')
        else:
            segments.append('Loyal Customer (4+ orders)')
    
    segment_df = pd.DataFrame({'segment': segments})
    segment_counts = segment_df['segment'].value_counts()
    
    fig = px.bar(
        x=segment_counts.index,
        y=segment_counts.values,
        title='Customer Segmentation',
        labels={'x': 'Customer Type', 'y': 'Number of Customers'}
    )
    
    fig.update_layout(showlegend=False)
    
    return fig

def create_top_states_chart(customers):
    """
    Create top 10 states by customer count
    """
    if customers.empty:
        return go.Figure().add_annotation(text="No data available", showarrow=False)
    
    top_states = customers['customer_state'].value_counts().head(10)
    
    fig = px.bar(
        x=top_states.values,
        y=top_states.index,
        orientation='h',
        title='Top 10 States by Customer Count',
        labels={'x': 'Number of Customers', 'y': 'State'}
    )
    
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    
    return fig

def main():
    st.title("Olist E-commerce Dashboard")
    st.markdown("**Data analytics report for Olist**")
    st.markdown("---")
    

    customers, orders = load_data()
    
    if customers is None or orders is None:
        st.error("Failed to load data. Please check your data files.")
        return
  
    st.sidebar.header("Filters")
    
    states, months = get_filter_options(customers, orders)
    
    selected_state = st.sidebar.selectbox("Select State:", states)
    selected_month = st.sidebar.selectbox("Select Month:", months)
    
    filtered_customers, filtered_orders = filter_data(customers, orders, selected_state, selected_month)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Filtered Results:**")
    st.sidebar.markdown(f"• Customers: {len(filtered_customers):,}")
    st.sidebar.markdown(f"• Orders: {len(filtered_orders):,}")
    
    st.subheader("Key Performance Indicators")
    
    total_orders, total_customers, avg_delivery_days, most_common_status = calculate_kpis(filtered_customers, filtered_orders)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Orders", f"{total_orders:,}")
    
    with col2:
        st.metric("Total Customers", f"{total_customers:,}")
    
    with col3:
        st.metric("Avg Delivery Time", f"{avg_delivery_days:.1f} days")
    
    with col4:
        st.metric("Most Common Status", most_common_status.title())
    
    st.markdown("---")
    
    st.subheader("Trends & Geographic Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        timeline_fig = create_orders_timeline(filtered_orders)
        st.plotly_chart(timeline_fig, use_container_width=True)
    
    with col2:
        top_states_fig = create_top_states_chart(filtered_customers)
        st.plotly_chart(top_states_fig, use_container_width=True)
    
    st.subheader("Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        status_fig = create_order_status_chart(filtered_orders)
        st.plotly_chart(status_fig, use_container_width=True)
    
    with col2:
        delivery_fig = create_delivery_time_chart(filtered_orders)
        st.plotly_chart(delivery_fig, use_container_width=True)
    
    st.subheader("Customer Insights")
    
    segments_fig = create_customer_segments_chart(filtered_customers, filtered_orders)
    st.plotly_chart(segments_fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Data Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Dataset Overview:**")
        st.write(f"• Total unique customers: {len(customers):,}")
        st.write(f"• Total orders: {len(orders):,}")
        st.write(f"• Date range: {orders['order_purchase_dt'].min().strftime('%Y-%m-%d')} to {orders['order_purchase_dt'].max().strftime('%Y-%m-%d')}")
        st.write(f"• States covered: {customers['customer_state'].nunique()}")
    
    with col2:
        if not filtered_orders.empty:
            st.markdown("**Current Filter Results:**")
            st.write(f"• Filtered customers: {len(filtered_customers):,}")
            st.write(f"• Filtered orders: {len(filtered_orders):,}")
            st.write(f"• State filter: {selected_state}")
            st.write(f"• Month filter: {selected_month}")

if __name__ == "__main__":
    main()