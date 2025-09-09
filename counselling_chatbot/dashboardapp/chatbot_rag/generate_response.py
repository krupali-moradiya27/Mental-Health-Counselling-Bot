import groq
from .retriever import retrieve_similar
from langdetect import detect
from dashboardapp.models import SubscriptionModel
from django.conf import settings
from llama_cpp import Llama
import os
from django.conf import settings

# MODEL_PATH = os.path.join(settings.BASE_DIR, "dashboardapp", "chatbot_rag", "intern_model.gguf")

# # Initialize once globally (lazy load in production)
# llm = Llama(
#     model_path=MODEL_PATH,
#     n_ctx=2048,           # reduce context if 4096 is too large for your RAM
#     n_threads=4,          # or match your CPU core count
#     n_batch=64,           # default is 512 — tuning this helps on slower CPUs
#     temperature=0.3,
#     top_p=0.8,
#     repeat_penalty=1.1
# )

# Initialize Groq client
client = os.getenv("GROQ_API_KEY")

def generate_response(user_id, user_query, user_health_data):
    """Generate a short and accurate LLM response based on user's subscription and query language."""

    # Step 1: Detect language
    detected_lang = detect(user_query)
    print("Detected Language:", detected_lang)

    # Step 2: Get subscription info
    try:
        subscription = SubscriptionModel.objects.get(
            user_id=user_id,
            counselling_chatbot_subscription_is_active=True
        )
        plan_id = subscription.plan.id
    except SubscriptionModel.DoesNotExist:
        return " No active subscription found. Please subscribe to a plan to use the chatbot."

    # Step 3: Restrict languages by plan ID
    if plan_id == 1 and detected_lang != "en":
        return detected_lang  # free → English only
    elif plan_id == 2 and detected_lang not in ["en", "hi"]:
        return detected_lang  # basic → English + Hindi
    elif plan_id == 3 and detected_lang not in ["en", "hi", "ur"]:
        return detected_lang  # premium → English + Hindi + Urdu
        
    # Step 4: Retrieve relevant knowledge
    retrieved_context = retrieve_similar(user_query, top_k=3)

    # Step 5: Format health data
    user_health_info = "\n".join(
        [f"{key}: {value}" for key, value in user_health_data.items() if value]
    )

    # Step 6: Set language instruction
    if detected_lang == "hi":
        language_instruction = "उत्तर केवल हिंदी में दीजिए।"
    elif detected_lang == "ur":
        language_instruction = "جواب صرف اردو میں دیں۔"
    else:
        language_instruction = "Respond only in English."

    # Step 7: Construct prompt
    prompt = f"""
You are a helpful and professional mental health assistant.

Use ONLY the 'Retrieved Knowledge' and 'User Health Data' provided below to answer the user's query.
Be short (2–4 sentences), clear, and supportive.

{language_instruction}

---
User Query:
{user_query}

User Health Data:
{user_health_info}

Retrieved Knowledge:
{retrieved_context}
"""
    # Step 8: Run LLM
    # response = llm(prompt, max_tokens=300, stop=["User Query:", "Retrieved Knowledge:"])

    # return response["choices"][0]["text"].strip()

    #Step 8: Generate response using Groq LLM
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # Or any other supported model
        messages=[
            {"role": "system", "content": "You are a multilingual mental health counseling assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=300,
        top_p=0.8,
    )

    return response.choices[0].message.content.strip()