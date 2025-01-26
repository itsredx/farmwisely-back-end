from groq import Groq
from django.conf import settings
import json


def get_crop_recommendations(farm_data, weather_data, user_notes=None):
    """Fetches crop recommendations from Groq based on farm data and weather data."""
    client = Groq(api_key=settings.GROQ_API_KEY)
    system_prompt = f"""You are an AI farm advisor. A user has provided details about their farm and current weather, including soil type, pH level, climate, water availability, current temperature, humidity, and other relevant data. Your task is to analyze this information and recommend three main crops and two alternative crops suited to the farm's conditions. 
    Each main crop recommendation should include the following details:
    Crop name.
    Sustainability rating (e.g., "Highly Sustainable").
    Benefits (7–10 words).
    Tips for cultivation (7–10 words).
    A brief description or explanation for the recommendation.
    Each alternative crop recommendation should include the following details:
        Crop name.
       Sustainability rating (e.g., "Highly Sustainable").
       Reason for consideration (7-10 words)
    Example Input:
    Farm Information:  
    - Soil Type: Loamy.  
    - pH Level: 6.5.  
    - Climate: Temperate.  
    - Water Availability: Moderate.  
    - Farm Size: 5 acres.  
    - Current Temperature: 25 c
    - Humidity: 60%
    - Other Notes: Interested in crops with high market demand.  
    Output Format:
    {{
    "Main Crop Recommendations":[
         {{
            "Crop Name": "Wheat",  
              "Sustainability Rating": "Highly Sustainable",  
             "Benefits": "Thrives in temperate climates, high market demand.",  
            "Tips": "Plant in spring, ensure moderate soil moisture.",  
              "Description": "Wheat is an ideal crop for temperate climates with loamy soil and moderate water availability. It has a steady market demand and is highly adaptable to varying environmental conditions."
         }},
          {{
              "Crop Name": "Barley",  
               "Sustainability Rating": "Moderately Sustainable",  
               "Benefits": "Grows quickly, tolerates drought, good for soil.",  
               "Tips": "Avoid waterlogged soil, harvest promptly.",
               "Description": "Barley grows well in loamy soil with moderate water and is known for its drought tolerance. It improves soil quality and has various applications in food and beverages."
        }},
          {{
               "Crop Name": "Carrot",  
               "Sustainability Rating": "Highly Sustainable",  
                "Benefits": "High yield, nutrient-rich, suitable for loamy soil.",  
                "Tips": "Ensure consistent watering, thin seedlings early.",  
              "Description": "Carrots are a profitable crop with high nutritional value. They grow well in loose loamy soil and require consistent watering for optimal growth."
            }}
       ],
     "Alternative Crop Recommendations": [
           {{
              "Crop Name": "Millet",
               "Sustainability Rating": "Highly Sustainable",
               "Reason for Consideration": "Highly drought resistant, good source of nutrients."
              }},
            {{
              "Crop Name": "Sorghum",
               "Sustainability Rating": "Highly Sustainable",
               "Reason for Consideration": "Grows well in dry areas, great animal feed."
             }}
       ]
    }}"""
    user_prompt = f"""Based on the following farm information and current weather conditions, recommend three main crops with detailed reasoning. Each main crop recommendation must include the crop name, sustainability rating, benefits, tips, and description. Also recommend two alternative crops, each alternative recommendation must include the crop name, sustainability rating, and reason for consideration. Ensure the response is structured json, concise, and easy to parse.

    Farm Information:

    Soil Type: {farm_data['soilType']}.
    pH Level: {farm_data['pHValue']}.
    Climate: Tropical.
    Water Availability: Adequate.
    Farm Size: {farm_data['farmSize']}.
    Current Temperature: {weather_data['currentConditions']['temp']}c.
    Humidity: {weather_data['currentConditions']['humidity']}.
    Other Notes: {user_notes if user_notes else "Not specified"}."""
    try:
        completion = client.chat.completions.create(
           model="llama-3.3-70b-versatile",
           messages=[
              {"role": "system", "content": system_prompt},
              {"role": "user", "content": user_prompt}
           ],
           temperature=1,
           max_completion_tokens=1024,
           top_p=1,
           stream=False,
           response_format={"type": "json_object"},
           stop=None,
      )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error fetching Groq response: {e}")
        return None