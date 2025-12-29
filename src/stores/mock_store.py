"""Mock store for testing the scraper with sample data."""

def adapt_items(html, selectors):
    """Return mock items for testing."""
    return [
        {
            "title": "Casual Cotton Shirt XXL - Blue Sale 40% Off",
            "price": 599.0,
            "original_price": 999.0,
            "sizes": "M, L, XL, XXL",
            "url": "https://example-store.test/shirt-blue-xxl",
        },
        {
            "title": "Formal Business Shirt XXL - White Discount",
            "price": 1199.0,
            "original_price": 1799.0,
            "sizes": "XXL",
            "url": "https://example-store.test/shirt-formal-xxl",
        },
        {
            "title": "Trouser Size 40 - Black Premium Sale",
            "price": 2499.0,
            "original_price": 3999.0,
            "sizes": "38, 40, 42",
            "url": "https://example-store.test/trouser-black-40",
        },
        {
            "title": "Chino Pants Size 40 - Khaki Offer",
            "price": 1899.0,
            "original_price": 2499.0,
            "sizes": "40",
            "url": "https://example-store.test/chino-khaki-40",
        },
    ]
