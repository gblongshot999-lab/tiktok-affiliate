"""Affiliate Tracker Page — Manage products and track link performance."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
from database import (
    add_product, get_products, update_product_status, delete_product,
    add_affiliate_link, get_affiliate_links, update_link_stats, delete_affiliate_link,
)

st.set_page_config(page_title="Affiliate Tracker", page_icon="📊", layout="wide")
st.title("Affiliate Tracker")
st.markdown("Track your products, affiliate links, and performance metrics.")

tab1, tab2 = st.tabs(["Products", "Affiliate Links"])

# ==================== PRODUCTS TAB ====================
with tab1:
    st.subheader("Add New Product")
    with st.form("add_product", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Product Name *", placeholder="e.g., Portable Blender")
            category = st.selectbox("Category", [
                "Beauty & Skincare", "Health & Wellness", "Phone Accessories",
                "Home & Kitchen Gadgets", "Fashion & Accessories", "Fitness & Sports",
                "Pet Products", "Tech Gadgets", "Baby & Kids", "Car Accessories", "Other"
            ])
            price = st.number_input("Price ($)", min_value=0.0, value=0.0, step=1.0)
        with col2:
            commission_rate = st.number_input("Commission Rate (%)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
            source_url = st.text_input("Product URL", placeholder="https://...")
            notes = st.text_area("Notes", placeholder="Why this product? Target audience?", height=80)

        if st.form_submit_button("Add Product", type="primary"):
            if name:
                add_product(name, category, price, commission_rate, source_url, notes)
                st.success(f"Added **{name}**!")
                st.rerun()
            else:
                st.error("Product name is required.")

    st.divider()
    st.subheader("Your Products")

    products = get_products()
    if products:
        for product in products:
            with st.container(border=True):
                col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])
                col1.markdown(f"**{product['name']}**")
                col2.caption(f"{product['category']} | ${product['price']:.2f} | {product['commission_rate']}%")

                status_options = ["researching", "active", "paused", "dropped"]
                current_idx = status_options.index(product["status"]) if product["status"] in status_options else 0
                new_status = col3.selectbox(
                    "Status", status_options, index=current_idx,
                    key=f"status_{product['id']}", label_visibility="collapsed"
                )
                if new_status != product["status"]:
                    update_product_status(product["id"], new_status)
                    st.rerun()

                if col4.button("🗑️", key=f"del_prod_{product['id']}"):
                    delete_product(product["id"])
                    st.rerun()

                if product["notes"]:
                    st.caption(product["notes"])
    else:
        st.info("No products yet. Add your first product above!")

# ==================== AFFILIATE LINKS TAB ====================
with tab2:
    st.subheader("Add Affiliate Link")
    products = get_products()

    if not products:
        st.warning("Add a product first in the Products tab.")
    else:
        with st.form("add_link", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                product_options = {p["name"]: p["id"] for p in products}
                selected_product = st.selectbox("Product", list(product_options.keys()))
            with col2:
                link_url = st.text_input("Affiliate Link URL", placeholder="https://...")
            with col3:
                platform = st.selectbox("Platform", ["tiktok", "instagram", "youtube", "pinterest", "other"])

            if st.form_submit_button("Add Link", type="primary"):
                if link_url:
                    add_affiliate_link(product_options[selected_product], link_url, platform)
                    st.success("Link added!")
                    st.rerun()
                else:
                    st.error("URL is required.")

    st.divider()
    st.subheader("Your Affiliate Links")

    links = get_affiliate_links()
    if links:
        for link in links:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                col1.markdown(f"**{link['product_name'] or 'Unknown'}** — `{link['platform']}`")
                col2.caption(f"[{link['url'][:40]}...]({link['url']})" if len(link['url']) > 40 else link['url'])

                # Editable stats
                with col3:
                    c1, c2, c3 = st.columns(3)
                    new_clicks = c1.number_input("Clicks", value=link["clicks"], min_value=0, key=f"clicks_{link['id']}", label_visibility="collapsed")
                    new_conv = c2.number_input("Conv", value=link["conversions"], min_value=0, key=f"conv_{link['id']}", label_visibility="collapsed")
                    new_rev = c3.number_input("Rev $", value=float(link["revenue"]), min_value=0.0, step=1.0, key=f"rev_{link['id']}", label_visibility="collapsed")

                    if (new_clicks != link["clicks"] or new_conv != link["conversions"]
                            or new_rev != link["revenue"]):
                        if st.button("Save", key=f"save_{link['id']}"):
                            update_link_stats(link["id"], new_clicks, new_conv, new_rev)
                            st.rerun()

                if col4.button("🗑️", key=f"del_link_{link['id']}"):
                    delete_affiliate_link(link["id"])
                    st.rerun()

        # Summary
        st.divider()
        df = pd.DataFrame(links)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Clicks", f"{df['clicks'].sum():,}")
        col2.metric("Total Conversions", f"{df['conversions'].sum():,}")
        col3.metric("Total Revenue", f"${df['revenue'].sum():,.2f}")

        if df["clicks"].sum() > 0:
            conv_rate = (df["conversions"].sum() / df["clicks"].sum()) * 100
            st.metric("Overall Conversion Rate", f"{conv_rate:.1f}%")
    else:
        st.info("No affiliate links yet. Add one above!")
