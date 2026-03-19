"""TikTok Affiliate Marketing Suite — Main Dashboard."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import get_dashboard_stats, get_affiliate_links, get_content_plans

st.set_page_config(
    page_title="TikTok Affiliate Suite",
    page_icon="🛍️",
    layout="wide",
)

# Mobile-friendly responsive CSS
st.markdown("""
<style>
    @media (max-width: 768px) {
        .stMainBlockContainer { padding-left: 1rem !important; padding-right: 1rem !important; }
        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > div { width: 100% !important; flex: 1 1 100% !important; min-width: 100% !important; }
        [data-testid="stMetric"] { padding: 0.5rem !important; }
        .stTabs [data-baseweb="tab-list"] { flex-wrap: wrap !important; gap: 0.25rem !important; }
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.25rem !important; }
        h3 { font-size: 1.1rem !important; }
        .stButton > button { min-height: 48px !important; font-size: 1rem !important; }
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div { min-height: 44px !important; font-size: 1rem !important; }
        .stTextArea > div > div > textarea { font-size: 1rem !important; }
        [data-testid="stTable"], .stDataFrame { overflow-x: auto !important; }
        [data-testid="stSidebar"] { min-width: 250px !important; max-width: 250px !important; }
    }
</style>
""", unsafe_allow_html=True)

st.title("TikTok Affiliate Marketing Suite")
st.markdown("Your all-in-one dashboard for product research, link tracking, and content planning.")

# --- Key Metrics ---
stats = get_dashboard_stats()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Products Tracked", stats["total_products"])
col2.metric("Active Links", stats["active_links"])
col3.metric("Total Clicks", f"{stats['total_clicks']:,}")
col4.metric("Total Revenue", f"${stats['total_revenue']:,.2f}")

st.divider()

# --- Revenue & Performance Charts ---
left, right = st.columns(2)

with left:
    st.subheader("Link Performance")
    links = get_affiliate_links()
    if links:
        df = pd.DataFrame(links)
        fig = px.bar(
            df,
            x="product_name",
            y=["clicks", "conversions"],
            barmode="group",
            title="Clicks vs Conversions by Product",
            color_discrete_sequence=["#00f2ea", "#ff0050"],
        )
        fig.update_layout(xaxis_title="", yaxis_title="Count", legend_title="")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add affiliate links in the **Affiliate Tracker** page to see performance data here.")

with right:
    st.subheader("Revenue by Product")
    if links:
        df = pd.DataFrame(links)
        revenue_df = df[df["revenue"] > 0]
        if not revenue_df.empty:
            fig = px.pie(
                revenue_df,
                values="revenue",
                names="product_name",
                title="Revenue Distribution",
                color_discrete_sequence=px.colors.sequential.Teal,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Update revenue data in the **Affiliate Tracker** to see charts.")
    else:
        st.info("No revenue data yet.")

st.divider()

# --- Upcoming Content ---
st.subheader("Upcoming Content")
plans = get_content_plans()
planned = [p for p in plans if p["status"] == "planned"]

if planned:
    for plan in planned[:5]:
        product_name = plan["product_name"] or "No product"
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        col1.write(f"**{plan['title']}**")
        col2.write(f"Product: {product_name}")
        col3.write(f"Date: {plan['scheduled_date']}")
        col4.write(f"`{plan['platform']}`")
else:
    st.info("No upcoming content planned. Head to the **Content Planner** to schedule posts.")

st.divider()

# --- Quick Start Guide ---
with st.expander("Quick Start Guide (click to expand)"):
    st.markdown("""
    ### How to use this suite:

    **1. Product Research** (sidebar menu)
    - Browse trending categories and their commission rates
    - Score products to find winners worth promoting
    - Calculate potential earnings before committing

    **2. Affiliate Tracker** (sidebar menu)
    - Add products you want to promote
    - Track your affiliate links across platforms
    - Monitor clicks, conversions, and revenue

    **3. Content Planner** (sidebar menu)
    - Plan your TikTok videos and lives
    - Get hashtag suggestions for each category
    - Track your posting schedule

    ### Tips for success:
    - Start with **1-3 products** in a single niche
    - Post **1-3 times daily** for growth
    - Use trending sounds and hashtags
    - Focus on products in the **$15-$50** range
    - Products that **solve a problem** or have a **wow factor** perform best
    """)
