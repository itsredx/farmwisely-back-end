from groq import Groq
from django.conf import settings

def get_ai_response(system_prompt, user_message):
    """Fetches a response from Groq using provided prompts."""
    client = Groq(api_key=settings.GROQ_API_KEY)
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # use this model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        # return only the response
        return completion.choices[0].message.content
    except Exception as e:
       print(f"Error fetching Groq response: {e}")  # Print the error for debugging
       return None