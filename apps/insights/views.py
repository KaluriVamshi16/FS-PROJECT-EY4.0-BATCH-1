from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.core.utils import get_financial_context
import json
from apps.chatbot.groq_utils import get_groq_client

@login_required
def insights_view(request):
    user = request.user
    
    # Get Full Context
    context_data = get_financial_context(user)
    
    # Generate Insights via Groq (Simulation for now or real call if key exists)
    insights = []
    client = get_groq_client()
    if client:
        try:
            prompt = f"""
            You are FinSight AI. Analyze this user data:
            {context_data}
            
            Provide 5 specific, actionable insights in this EXACT format:
            1. [Category] Insight text here.
            2. [Category] Insight text here.
            ...
            
            Keep strictly to this format.
            """
            
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7,
                max_tokens=500,
            )
            raw_text = completion.choices[0].message.content
            
            # Parse lines
            lines = raw_text.strip().split('\n')
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # Try to extract [Category] Text or just Text
                if ']' in line:
                    parts = line.split(']', 1)
                    category = parts[0].replace('[', '').lstrip('0123456789.- ')
                    text = parts[1].strip()
                    insights.append({'category': category or 'General', 'text': text})
                else:
                    # Fallback for plain lines
                    clean_text = line.lstrip('0123456789.- ')
                    insights.append({'category': 'General', 'text': clean_text})
                        
        except Exception as e:
            insights.append({'category': 'Error', 'text': f"Could not generate insights: {str(e)}"})
    else:
        insights.append({'category': 'Setup', 'text': 'Please configure GROQ_API_KEY in .env to see AI insights.'})

    insights.append({'category': 'SYSTEM', 'text': 'AI Insights logic is active.'})
    return render(request, 'insights/index.html', {'insights': insights})
