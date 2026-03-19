"""Product research helpers for TikTok affiliate marketing."""

import requests
from bs4 import BeautifulSoup

# Trending TikTok product categories with typical commission ranges
TRENDING_CATEGORIES = {
    "Beauty & Skincare": {"avg_commission": "10-20%", "price_range": "$10-$50", "demand": "Very High"},
    "Health & Wellness": {"avg_commission": "10-25%", "price_range": "$15-$60", "demand": "High"},
    "Phone Accessories": {"avg_commission": "5-15%", "price_range": "$5-$30", "demand": "High"},
    "Home & Kitchen Gadgets": {"avg_commission": "8-20%", "price_range": "$10-$40", "demand": "Very High"},
    "Fashion & Accessories": {"avg_commission": "10-20%", "price_range": "$15-$80", "demand": "High"},
    "Fitness & Sports": {"avg_commission": "8-18%", "price_range": "$10-$50", "demand": "Medium-High"},
    "Pet Products": {"avg_commission": "8-15%", "price_range": "$10-$40", "demand": "Medium-High"},
    "Tech Gadgets": {"avg_commission": "5-15%", "price_range": "$15-$100", "demand": "High"},
    "Baby & Kids": {"avg_commission": "8-18%", "price_range": "$10-$50", "demand": "Medium"},
    "Car Accessories": {"avg_commission": "8-15%", "price_range": "$10-$50", "demand": "Medium"},
}

# Popular hashtags by category for content creation
HASHTAGS = {
    "Beauty & Skincare": ["#skincare", "#beautytok", "#skintok", "#glowup", "#skincareroutine", "#tiktokmademebuyit", "#beautyhacks"],
    "Health & Wellness": ["#wellness", "#healthtok", "#supplement", "#selfcare", "#healthylifestyle", "#wellnesstok"],
    "Phone Accessories": ["#phonecase", "#techtok", "#phonehacks", "#phoneaccessories", "#gadgets"],
    "Home & Kitchen Gadgets": ["#homehacks", "#kitchentok", "#homefinds", "#amazonfinds", "#tiktokmademebuyit", "#cleantok"],
    "Fashion & Accessories": ["#fashion", "#ootd", "#fashiontok", "#styleinspo", "#fashionfinds", "#grwm"],
    "Fitness & Sports": ["#fitnesstok", "#gymtok", "#workout", "#fitnessgear", "#homegym"],
    "Pet Products": ["#pettok", "#dogtok", "#cattok", "#petfinds", "#petessentials"],
    "Tech Gadgets": ["#techtok", "#gadgets", "#techfinds", "#techhacks", "#techreview"],
    "Baby & Kids": ["#momtok", "#babytok", "#momfinds", "#parentinghacks", "#babyessentials"],
    "Car Accessories": ["#cartok", "#caraccessories", "#carfinds", "#carhacks", "#autotok"],
}

# Product evaluation criteria
EVALUATION_CRITERIA = [
    ("Video-Friendly", "Can the product be easily demonstrated in a short video?"),
    ("Problem-Solving", "Does it solve a clear pain point?"),
    ("Impulse Buy Price", "Is it priced under $50 for easy impulse purchases?"),
    ("Wow Factor", "Does it have a visual wow factor that stops the scroll?"),
    ("Repeat Purchase", "Will customers come back for refills or accessories?"),
    ("Low Return Rate", "Is it unlikely to be returned?"),
    ("Commission Worth It", "Is the commission rate worth the effort?"),
]


def score_product(name, price, commission_rate, is_video_friendly, is_problem_solving,
                  is_impulse_buy, has_wow_factor, is_repeat_purchase, low_return_rate):
    """Score a product from 0-100 based on affiliate marketing criteria."""
    score = 0

    # Price sweet spot (15-50 is ideal)
    if 15 <= price <= 50:
        score += 20
    elif 10 <= price <= 60:
        score += 12
    elif price < 10:
        score += 5
    else:
        score += 8

    # Commission rate
    if commission_rate >= 20:
        score += 20
    elif commission_rate >= 15:
        score += 15
    elif commission_rate >= 10:
        score += 10
    else:
        score += 5

    # Boolean criteria (10 points each)
    if is_video_friendly:
        score += 12
    if is_problem_solving:
        score += 12
    if is_impulse_buy:
        score += 10
    if has_wow_factor:
        score += 12
    if is_repeat_purchase:
        score += 8
    if low_return_rate:
        score += 6

    return min(score, 100)


def get_category_info(category):
    """Get info about a product category."""
    return TRENDING_CATEGORIES.get(category, {})


def get_hashtags(category):
    """Get recommended hashtags for a category."""
    return HASHTAGS.get(category, ["#tiktokmademebuyit", "#tiktokshop", "#affiliate"])


def estimate_earnings(price, commission_rate, estimated_monthly_sales):
    """Estimate monthly affiliate earnings."""
    commission_per_sale = price * (commission_rate / 100)
    monthly_earnings = commission_per_sale * estimated_monthly_sales
    return {
        "commission_per_sale": round(commission_per_sale, 2),
        "monthly_earnings": round(monthly_earnings, 2),
        "yearly_projection": round(monthly_earnings * 12, 2),
    }
