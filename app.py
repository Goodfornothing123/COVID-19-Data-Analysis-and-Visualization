import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="COVID-19 Global Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background-color: #0e1117;
    }
    
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #ff4b4b;
    }
    
    .title-text {
        font-size: 3rem;
        font-weight: 600;
        background: -webkit-linear-gradient(#ff4b4b, #ff8a8a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    
    .subtitle-text {
        color: #888;
        font-size: 1.1rem;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(14, 17, 23, 0.95);
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 0.9rem;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Data Loading Function
@st.cache_data(ttl=3600)  # Cache data for 1 hour
def load_data():
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    df['date'] = pd.to_datetime(df['date'])
    return df

try:
    with st.spinner('Fetching latest COVID-19 data...'):
        df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar
st.sidebar.image("https://img.icons8.com/fluent/100/000000/coronavirus.png", width=100)
st.sidebar.title("Dashboard Controls")

# Filtering Data
locations = sorted(df['location'].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries to Compare",
    options=locations,
    default=["World", "India", "United States", "Brazil"]
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['date'].min().to_pydatetime(), df['date'].max().to_pydatetime()),
    min_value=df['date'].min().to_pydatetime(),
    max_value=df['date'].max().to_pydatetime()
)

# Filter Dataset
mask = (df['location'].isin(selected_countries)) & \
       (df['date'] >= pd.Timestamp(date_range[0])) & \
       (df['date'] <= pd.Timestamp(date_range[1]))
filtered_df = df.loc[mask]

# Latest Global Stats (for metrics)
latest_date = df['date'].max()
global_data = df[df['location'] == 'World'].iloc[-1]

# Header Area
st.image("banner.png", use_container_width=True)
st.markdown('<p class="title-text">COVID-19 Global Insights</p>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle-text">Real-time data visualization & trend analysis | Last Updated: {latest_date.strftime("%B %d, %Y")}</p>', unsafe_allow_html=True)

# Main Dashboard Layout
m1, m2, m3, m4 = st.columns(4)

def format_num(num):
    if num >= 1_000_000_000: return f"{num/1_000_000_000:.2f}B"
    if num >= 1_000_000: return f"{num/1_000_000:.2f}M"
    return f"{num:,.0f}"

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <h3 style='margin:0; color:#ff4b4b;'>Total Cases</h3>
        <h1 style='margin:0;'>{format_num(global_data['total_cases'])}</h1>
        <p style='color:#888;'>+{format_num(global_data['new_cases'])} today</p>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <h3 style='margin:0; color:#ff8a8a;'>Total Deaths</h3>
        <h1 style='margin:0;'>{format_num(global_data['total_deaths'])}</h1>
        <p style='color:#888;'>+{format_num(global_data['new_deaths'])} today</p>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <h3 style='margin:0; color:#4BFF8A;'>Vaccinations</h3>
        <h1 style='margin:0;'>{format_num(global_data['total_vaccinations'])}</h1>
        <p style='color:#888;'>Global Administered</p>
    </div>
    """, unsafe_allow_html=True)

with m4:
    mortality = (global_data['total_deaths'] / global_data['total_cases']) * 100
    st.markdown(f"""
    <div class="metric-card">
        <h3 style='margin:0; color:#4bbdff;'>Mortality Rate</h3>
        <h1 style='margin:0;'>{mortality:.2f}%</h1>
        <p style='color:#888;'>Case Fatality</p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# Row 2: Charts
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### 📈 Daily New Cases Trend")
    fig_cases = px.line(
        filtered_df, 
        x='date', 
        y='new_cases_smoothed', 
        color='location',
        template='plotly_dark',
        labels={'new_cases_smoothed': 'New Cases (7-day avg)', 'date': 'Date'},
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig_cases.update_layout(
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig_cases, use_container_width=True)

with c2:
    st.markdown("### 🗺️ Global Distribution")
    # Map for latest data
    map_df = df[df['date'] == latest_date].copy()
    fig_map = px.choropleth(
        map_df,
        locations="iso_code",
        color="total_cases",
        hover_name="location",
        color_continuous_scale=px.colors.sequential.Reds,
        template='plotly_dark'
    )
    fig_map.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_map, use_container_width=True)

# Row 3: Vaccinations and Testing
st.write("---")
c3, c4 = st.columns(2)

with c3:
    st.markdown("### 💉 Vaccination Progress")
    # Bar chart for selected countries
    latest_selection = df[(df['location'].isin(selected_countries)) & (df['date'] == latest_date)]
    fig_vac = px.bar(
        latest_selection,
        x='location',
        y='people_fully_vaccinated_per_hundred',
        color='location',
        template='plotly_dark',
        labels={'people_fully_vaccinated_per_hundred': '% Fully Vaccinated'},
        title="Fully Vaccinated % by Country"
    )
    st.plotly_chart(fig_vac, use_container_width=True)

with c4:
    st.markdown("### 🔍 Testing vs Positivity")
    fig_test = px.scatter(
        filtered_df.dropna(subset=['new_tests_per_thousand', 'positive_rate']),
        x='new_tests_per_thousand',
        y='positive_rate',
        color='location',
        size='total_cases',
        hover_name='date',
        template='plotly_dark',
        labels={'new_tests_per_thousand': 'New Tests (per 1k)', 'positive_rate': 'Positivity Rate'},
        log_x=True
    )
    st.plotly_chart(fig_test, use_container_width=True)

# Footer/Credit
st.markdown(f"""
    <div class="footer">
        🚀 Developed with ❤️ by <b>Md Shamshad Shamim</b> | Created for Academic Submission
    </div>
""", unsafe_allow_html=True)
