import os
import json
import re
from groq import Groq
from django.conf import settings
from django.utils import timezone
from dotenv import load_dotenv

def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        load_dotenv(override=True)
        api_key = os.environ.get("GROQ_API_KEY")
    
    if api_key:
        return Groq(api_key=api_key)
    return None

SYSTEM_PROMPTS = {
    "en": "You are FinSight, an expert multilingual financial assistant. Respond in English. Keep answers short and bulleted.",
    "te": "మీరు FinSight, ఒక నిపుణుడైన ఆర్థిక సహాయకుడు. తెలుగులో సమాధానం ఇవ్వండి.",
    "hi": "आप FinSight हैं, एक विशेषज्ञ वित्तीय सहायक। हिंदी में जवाब दें।"
}

def process_message(user, message, language="en"):
    # Local imports to avoid circular dependency
    from apps.expenses.models import Expense, ExpenseCategory
    from apps.expenses.nlp_utils import detect_category
    from apps.core.utils import get_financial_context
    
    client = get_groq_client()
    if not client:
        return "Please configure the Groq API key in the .env file."
    
    # NLP Expense extraction logic
    amount_match = re.search(r'(\d+(?:\.\d{1,2})?)', message)
    
    if "spent" in message.lower() or "pay" in message.lower() or "paid" in message.lower():
        if amount_match:
            amount = float(amount_match.group(1))
            category_name = detect_category(message)
            
            # Create Expense
            category, _ = ExpenseCategory.objects.get_or_create(name=category_name, defaults={'user': user})
            Expense.objects.create(
                user=user,
                amount=amount,
                category=category,
                description=message,
                source='chat'
            )
            return f"✅ Recorded expense: ₹{amount} for {category_name}."

    # Fetch Context
    context = get_financial_context(user)
    
    system_prompt = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS["en"])
    full_prompt = f"{system_prompt}\n\nUSER DATA:\n{context}"

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": full_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=500,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Groq Error: {e}")
        return "Sorry, I am unable to process your request right now."
