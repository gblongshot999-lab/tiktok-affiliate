"""Seed the database with beginner-friendly starter products across 3 niches."""

from database import add_product, add_content_plan, get_products
from datetime import date, timedelta

# Check if already seeded
existing = get_products()
if existing:
    print(f"Database already has {len(existing)} products. Skipping seed.")
    exit()

# ============================================================
# NICHE 1: Home & Kitchen Gadgets
# ============================================================
add_product(
    name="Mini Portable Blender",
    category="Home & Kitchen Gadgets",
    price=19.99,
    commission_rate=15.0,
    source_url="",
    notes="Viral product. Easy demo: blend a smoothie in 30 sec. Great wow factor. Search 'portable blender' on TikTok Shop."
)

add_product(
    name="LED Sunset Lamp",
    category="Home & Kitchen Gadgets",
    price=12.99,
    commission_rate=18.0,
    source_url="",
    notes="Aesthetic room decor. Just turn it on and film — instant visual content. Huge on #roomtok and #aesthetictok."
)

add_product(
    name="Electric Spin Scrubber",
    category="Home & Kitchen Gadgets",
    price=24.99,
    commission_rate=12.0,
    source_url="",
    notes="Satisfying before/after cleaning content. #CleanTok is massive. Film a dirty surface → sparkling clean."
)

add_product(
    name="Portable Mini Vacuum (Desktop)",
    category="Home & Kitchen Gadgets",
    price=14.99,
    commission_rate=14.0,
    source_url="",
    notes="Cute, compact, satisfying to watch. Great for desk/car content. Low price = easy impulse buy."
)

# ============================================================
# NICHE 2: Beauty & Skincare
# ============================================================
add_product(
    name="Ice Roller for Face",
    category="Beauty & Skincare",
    price=9.99,
    commission_rate=20.0,
    source_url="",
    notes="Simple GRWM addition. Show puffy face → use roller → instant de-puff. Very visual, high commission."
)

add_product(
    name="Lip Stain / Lip Tint",
    category="Beauty & Skincare",
    price=8.99,
    commission_rate=18.0,
    source_url="",
    notes="Apply on camera, show long-lasting result. 'Water test' videos go viral. Cheap = high conversion."
)

add_product(
    name="LED Face Mask",
    category="Beauty & Skincare",
    price=29.99,
    commission_rate=15.0,
    source_url="",
    notes="Looks futuristic on camera — instant scroll-stopper. Before/after content works great. Higher price but strong wow factor."
)

add_product(
    name="Hair Oil Serum",
    category="Beauty & Skincare",
    price=12.99,
    commission_rate=20.0,
    source_url="",
    notes="Before/after hair transformation. Easy demo: apply to one side, show the difference. #HairTok is huge."
)

# ============================================================
# NICHE 3: Phone / Tech Accessories
# ============================================================
add_product(
    name="3-in-1 Charging Station",
    category="Tech Gadgets",
    price=19.99,
    commission_rate=12.0,
    source_url="",
    notes="Desk setup content. Film your clean desk aesthetic. Appeals to everyone with a phone + watch + earbuds."
)

add_product(
    name="Magnetic Phone Mount (Car)",
    category="Tech Gadgets",
    price=11.99,
    commission_rate=15.0,
    source_url="",
    notes="Quick install demo in car. Problem→solution format: shaky phone → mount → stable. Universal appeal."
)

add_product(
    name="Clip-On Phone Ring Light",
    category="Tech Gadgets",
    price=9.99,
    commission_rate=18.0,
    source_url="",
    notes="Meta product: use it to make better content! Show the lighting difference. Very beginner-friendly."
)

add_product(
    name="Portable Phone Projector",
    category="Tech Gadgets",
    price=27.99,
    commission_rate=10.0,
    source_url="",
    notes="Movie night vibes. Film dark room → turn on projector → wow factor. Great for #roomtok content."
)

print("Seeded 12 products across 3 niches!")

# ============================================================
# SEED CONTENT IDEAS (first week schedule)
# ============================================================
products = get_products()
product_map = {p["name"]: p["id"] for p in products}

today = date.today()

content_schedule = [
    # Day 1
    (product_map.get("Mini Portable Blender"), "Unboxing + smoothie demo", "video", "tiktok",
     today + timedelta(days=0), "#portableblender #tiktokmademebuyit #kitchengadgets #smoothie #homehacks",
     "Hook: 'This tiny blender actually works?!' — unbox, add fruit, blend, taste test. 30 sec max."),

    # Day 1 - second post
    (product_map.get("Ice Roller for Face"), "Morning routine de-puff", "video", "tiktok",
     today + timedelta(days=0), "#skincare #icefacial #grwm #beautytok #morningroutine #glowup",
     "Hook: 'My secret for puffy morning face' — show before, roll for 30 sec, show after. Use trending sound."),

    # Day 2
    (product_map.get("Clip-On Phone Ring Light"), "Lighting difference side by side", "video", "tiktok",
     today + timedelta(days=1), "#ringlight #techtok #contentcreator #tiktokhacks #phonegadgets",
     "Hook: 'Why your videos look amateur' — film face without light, clip it on, show the glow-up."),

    # Day 2
    (product_map.get("Electric Spin Scrubber"), "Bathroom cleaning transformation", "video", "tiktok",
     today + timedelta(days=1), "#cleantok #cleaningmotivation #satisfying #homehacks #tiktokmademebuyit",
     "Hook: 'The most satisfying clean ever' — show dirty grout → scrub → sparkling. Trending audio."),

    # Day 3
    (product_map.get("Lip Stain / Lip Tint"), "Water test challenge", "video", "tiktok",
     today + timedelta(days=2), "#liptint #beautyhacks #lipstain #waterproof #beautytok #grwm",
     "Hook: 'This $9 lip tint survives ANYTHING' — apply, drink water, eat, kiss napkin — still on!"),

    # Day 3
    (product_map.get("3-in-1 Charging Station"), "Desk setup aesthetic", "video", "tiktok",
     today + timedelta(days=2), "#desksetup #techtok #aesthetic #organize #techfinds #gadgets",
     "Hook: 'Upgrade your desk for under $20' — messy cables → place charging station → clean setup."),

    # Day 4
    (product_map.get("LED Sunset Lamp"), "Room transformation at night", "video", "tiktok",
     today + timedelta(days=3), "#sunsetlamp #roomtok #aesthetic #roomdecor #tiktokmademebuyit #vibes",
     "Hook: 'This $13 lamp changed my entire room' — lights off, turn on lamp, pan around room. Cozy vibes."),
]

for product_id, title, ctype, platform, sched_date, hashtags, notes in content_schedule:
    add_content_plan(product_id, title, ctype, platform, str(sched_date), hashtags, notes)

print("Seeded 7 content ideas for your first week!")
print("\nYour first week posting schedule:")
print("  Day 1: Portable Blender unboxing + Ice Roller morning routine")
print("  Day 2: Ring Light comparison + Spin Scrubber cleaning")
print("  Day 3: Lip Tint water test + Charging Station desk setup")
print("  Day 4: Sunset Lamp room transformation")
