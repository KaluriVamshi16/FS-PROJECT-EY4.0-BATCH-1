import re

def detect_category(text: str) -> str:
    """
    Detects expense category from text using keyword matching.
    """
    text = text.lower()
    
    categories = {
        'Food': ['food', 'eat', 'lunch', 'dinner', 'breakfast', 'restaurant', 'swiggy', 'zomato', 'grocery', 'snack', 'coffee', 'tea'],
        'Travel': ['bus', 'train', 'cab', 'uber', 'ola', 'petrol', 'fuel', 'flight', 'metro', 'ticket', 'transport'],
        'Rent': ['rent', 'house', 'pg', 'hostel', 'accommodation', 'maintenance'],
        'Shopping': ['amazon', 'flipkart', 'clothes', 'shirt', 'shoes', 'mall', 'buy', 'jeans', 'dress'],
        'Healthcare': ['medicine', 'doctor', 'hospital', 'pharmacy', 'clinic', 'health', 'checkup'],
        'Entertainment': ['movie', 'netflix', 'spotify', 'game', 'concert', 'cinema', 'subscription'],
        'Utilities': ['electricity', 'water', 'wifi', 'internet', 'bill', 'recharge', 'gas', 'phone'],
        'Other': []
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in text:
                return category
                
    return 'Other'
