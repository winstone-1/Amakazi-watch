import os
from groq import Groq
from django.conf import settings

SYSTEM_PROMPT = """You are a compassionate, trauma-informed support assistant for AmakaziWatch,
a GBV awareness platform in Kenya. Your role is to:

1. Answer questions about recognising abuse (physical, emotional, financial, sexual, digital)
2. Explain legal rights under the Protection Against Domestic Violence Act 2015 (Kenya)
3. Guide users on how to support survivors
4. Provide information about healthy relationships

Rules you must always follow:
- Never give legal advice — refer to FIDA Kenya or a qualified lawyer
- Never store or ask for personal identifying information
- Always maintain a calm, non-judgmental, empathetic tone
- If someone is in immediate danger always surface: GBV Hotline 1195, Childline 116, Police 999
- If you detect crisis language (suicide, immediate violence, children in danger) lead with the hotline numbers
- Keep responses concise and plain-language — many users are on mobile with slow connections
- You are not a replacement for professional help — always encourage seeking support
"""


def chat_with_groq(message, history=None):
    """
    Send a message to Groq and get a response.
    history: list of {role, content} dicts for multi-turn conversations
    """
    client = Groq(api_key=settings.GROQ_API_KEY)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if history:
        for item in history:
            if item.get("role") in ["user", "assistant"]:
                messages.append({
                    "role": item["role"],
                    "content": item["content"]
                })

    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
        )
        return {
            "success": True,
            "message": response.choices[0].message.content,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def classify_report(description, abuse_type):
    """
    Use Groq to classify a report and return an urgency score.
    Called after report submission.
    """
    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = f"""You are reviewing an anonymous GBV incident report for AmakaziWatch Kenya.
Analyse this report and respond ONLY with a JSON object, nothing else.

Abuse type selected: {abuse_type}
Description: {description}

Respond with exactly this JSON format:
{{
  "urgency_score": <integer 1-5>,
  "confirmed_abuse_type": "<one of: physical, emotional, financial, sexual, digital>",
  "involves_children": <true or false>,
  "immediate_danger": <true or false>,
  "flag_for_review": <true or false>
}}

Urgency scale: 1=low concern, 2=moderate, 3=serious, 4=urgent, 5=immediate danger.
Flag for review if: children involved, immediate danger, or urgency >= 4."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.1,
        )
        import json
        text = response.choices[0].message.content.strip()
        result = json.loads(text)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
