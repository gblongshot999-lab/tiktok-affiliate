"""Content Planner Page — Plan and schedule your TikTok content."""

import streamlit as st
import pandas as pd
from datetime import date, timedelta
from database import (
    get_products, add_content_plan, get_content_plans,
    update_content_status, delete_content_plan,
)
from scraper import get_hashtags, TRENDING_CATEGORIES

st.set_page_config(page_title="Content Planner", page_icon="📅", layout="wide")
st.title("Content Planner")
st.markdown("Plan your TikTok posts, lives, and promotional content.")

# ==================== ADD CONTENT ====================
st.subheader("Schedule New Content")

products = get_products()

with st.form("add_content", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("Content Title *", placeholder="e.g., Morning skincare routine with Product X")
        content_type = st.selectbox("Content Type", ["video", "live", "story", "carousel", "duet", "stitch"])
        platform = st.selectbox("Platform", ["tiktok", "instagram", "youtube_shorts", "pinterest"])

    with col2:
        if products:
            product_options = {"(No product)": None}
            product_options.update({p["name"]: p["id"] for p in products})
            selected = st.selectbox("Link to Product", list(product_options.keys()))
            selected_product_id = product_options[selected]
        else:
            st.info("No products added yet — you can still plan content without linking a product.")
            selected_product_id = None

        scheduled_date = st.date_input("Scheduled Date", value=date.today() + timedelta(days=1))
        notes = st.text_area("Notes / Script Outline", placeholder="Key talking points, hooks, CTA...", height=80)

    # Hashtag helper
    st.markdown("**Hashtag Suggestions:**")
    selected_category = st.selectbox("Pick a category for hashtag ideas:", list(TRENDING_CATEGORIES.keys()))
    suggested_tags = get_hashtags(selected_category)
    hashtag_string = st.text_input("Hashtags (edit as needed)", value=" ".join(suggested_tags))

    if st.form_submit_button("Schedule Content", type="primary"):
        if title:
            add_content_plan(
                selected_product_id, title, content_type, platform,
                str(scheduled_date), hashtag_string, notes
            )
            st.success(f"Scheduled: **{title}** for {scheduled_date}")
            st.rerun()
        else:
            st.error("Title is required.")

st.divider()

# ==================== CONTENT CALENDAR ====================
st.subheader("Content Calendar")

plans = get_content_plans()

if plans:
    # Filter controls
    col1, col2 = st.columns(2)
    status_filter = col1.selectbox("Filter by status", ["all", "planned", "filmed", "edited", "posted", "cancelled"])
    platform_filter = col2.selectbox("Filter by platform", ["all", "tiktok", "instagram", "youtube_shorts", "pinterest"])

    filtered = plans
    if status_filter != "all":
        filtered = [p for p in filtered if p["status"] == status_filter]
    if platform_filter != "all":
        filtered = [p for p in filtered if p["platform"] == platform_filter]

    if filtered:
        for plan in filtered:
            with st.container(border=True):
                col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])

                col1.markdown(f"**{plan['title']}**")
                col2.caption(f"{plan['content_type']} | {plan['platform']} | {plan['scheduled_date']}")
                product_name = plan["product_name"] or "No product"
                col3.caption(f"Product: {product_name}")

                status_options = ["planned", "filmed", "edited", "posted", "cancelled"]
                current_idx = status_options.index(plan["status"]) if plan["status"] in status_options else 0
                new_status = col4.selectbox(
                    "Status", status_options, index=current_idx,
                    key=f"content_status_{plan['id']}", label_visibility="collapsed"
                )
                if new_status != plan["status"]:
                    update_content_status(plan["id"], new_status)
                    st.rerun()

                if col5.button("🗑️", key=f"del_content_{plan['id']}"):
                    delete_content_plan(plan["id"])
                    st.rerun()

                if plan["hashtags"]:
                    st.caption(f"Hashtags: {plan['hashtags']}")
                if plan["notes"]:
                    st.caption(f"Notes: {plan['notes']}")
    else:
        st.info("No content matches your filters.")

    # Summary stats
    st.divider()
    st.subheader("Content Stats")
    df = pd.DataFrame(plans)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Planned", len(df[df["status"] == "planned"]))
    col2.metric("Filmed", len(df[df["status"] == "filmed"]))
    col3.metric("Edited", len(df[df["status"] == "edited"]))
    col4.metric("Posted", len(df[df["status"] == "posted"]))

else:
    st.info("No content scheduled yet. Create your first post above!")

st.divider()

# ==================== CONTENT IDEAS ====================
with st.expander("Content Ideas & Templates"):
    st.markdown("""
    ### High-Performing TikTok Content Formats:

    **1. "TikTok Made Me Buy It" Review**
    - Hook: "I finally tried this viral [product]..."
    - Show unboxing, first impression, demo
    - End with honest verdict + link

    **2. Problem → Solution**
    - Hook: "POV: you've been struggling with [problem]"
    - Show the problem, introduce the product
    - Show the satisfying result

    **3. Get Ready With Me (GRWM)**
    - Natural integration of beauty/fashion products
    - Casual, relatable format
    - High watch time = better algorithm push

    **4. Before & After**
    - Dramatic transformation using the product
    - Works great for skincare, cleaning, organizing
    - Visual wow factor stops the scroll

    **5. Day in My Life**
    - Subtle product placement throughout the day
    - Feels authentic, not salesy
    - Multiple product mentions possible

    **6. Comparison / "Which is better?"**
    - Compare 2-3 similar products
    - Drives engagement through comments
    - Position your affiliate product as the winner

    ### Hooks that work:
    - "Stop scrolling if you..."
    - "I wish I knew about this sooner"
    - "The product that changed my [routine/life/morning]"
    - "Rating viral TikTok products honestly"
    - "3 things I can't live without"
    """)
