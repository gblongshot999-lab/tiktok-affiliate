"""Product Research Page — Find winning products to promote."""

import streamlit as st
from scraper import (
    TRENDING_CATEGORIES,
    EVALUATION_CRITERIA,
    get_hashtags,
    score_product,
    estimate_earnings,
)

st.set_page_config(page_title="Product Research", page_icon="🔍", layout="wide")
st.title("Product Research")
st.markdown("Find and evaluate winning products for TikTok affiliate marketing.")

# --- Trending Categories ---
st.subheader("Trending Product Categories")
st.markdown("These categories are currently performing well on TikTok Shop:")

cols = st.columns(2)
for i, (category, info) in enumerate(TRENDING_CATEGORIES.items()):
    with cols[i % 2]:
        with st.container(border=True):
            st.markdown(f"**{category}**")
            c1, c2, c3 = st.columns(3)
            c1.caption(f"Commission: {info['avg_commission']}")
            c2.caption(f"Price: {info['price_range']}")
            c3.caption(f"Demand: {info['demand']}")

            tags = get_hashtags(category)
            st.caption("Hashtags: " + " ".join(tags[:5]))

st.divider()

# --- Product Scorer ---
st.subheader("Product Scorer")
st.markdown("Evaluate a product to see if it's worth promoting. Score it across key criteria.")

with st.form("product_scorer"):
    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Product Name", placeholder="e.g., LED Face Mask")
        price = st.number_input("Product Price ($)", min_value=0.0, value=25.0, step=1.0)
        commission = st.number_input("Commission Rate (%)", min_value=0.0, max_value=100.0, value=15.0, step=1.0)

    with col2:
        st.markdown("**Rate these criteria:**")
        video_friendly = st.checkbox("Video-Friendly (easy to demo in a short video)")
        problem_solving = st.checkbox("Problem-Solving (solves a clear pain point)")
        impulse_buy = st.checkbox("Impulse Buy (priced for easy purchase)")
        wow_factor = st.checkbox("Wow Factor (stops the scroll)")
        repeat_purchase = st.checkbox("Repeat Purchase (refills, accessories)")
        low_returns = st.checkbox("Low Return Rate")

    submitted = st.form_submit_button("Score This Product", type="primary")

if submitted and product_name:
    score = score_product(
        product_name, price, commission, video_friendly,
        problem_solving, impulse_buy, wow_factor, repeat_purchase, low_returns
    )

    st.divider()

    # Score display
    if score >= 75:
        color = "green"
        verdict = "Excellent — strong candidate for promotion!"
    elif score >= 50:
        color = "orange"
        verdict = "Decent — could work with the right content strategy."
    else:
        color = "red"
        verdict = "Weak — consider a different product."

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Product Score", f"{score}/100")
    with col2:
        st.markdown(f"**Verdict:** :{color}[{verdict}]")

    # Earnings estimate
    st.markdown("---")
    st.markdown("**Earnings Estimates:**")
    for sales_label, monthly_sales in [("Conservative (10 sales/mo)", 10), ("Moderate (50 sales/mo)", 50), ("Aggressive (200 sales/mo)", 200)]:
        earnings = estimate_earnings(price, commission, monthly_sales)
        c1, c2, c3 = st.columns(3)
        c1.write(f"**{sales_label}**")
        c2.write(f"${earnings['monthly_earnings']}/month")
        c3.write(f"${earnings['yearly_projection']}/year")

st.divider()

# --- Evaluation Guide ---
with st.expander("Product Evaluation Guide"):
    st.markdown("Use these criteria when evaluating any product:")
    for name, description in EVALUATION_CRITERIA:
        st.markdown(f"- **{name}**: {description}")

    st.markdown("""
    ### Where to find products:
    1. **TikTok Shop Marketplace** — Browse the affiliate marketplace directly in TikTok
    2. **TikTok Creative Center** — See trending ads and products
    3. **#TikTokMadeMeBuyIt** — Browse viral products
    4. **Amazon Best Sellers** — Cross-reference with TikTok trends
    5. **Competitor Creators** — See what similar creators are promoting
    """)
