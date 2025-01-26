from groq import Groq
from django.conf import settings
import json


def get_farm_analytics(farm_data, weather_data, user_notes=None):
     """Fetches crop recommendations from Groq based on farm data and weather data."""
     client = Groq(api_key=settings.GROQ_API_KEY)
     system_prompt =  """You are an AI farm analytics advisor. You will be given farm data and weather conditions and your task is to generate the following insights:
     1.  Monthly Yield Increase Prediction: Provide a predicted percentage increase in yield for each month (July - October) based on historical data.
     2.  Cost-Profit Breakdown: Provide the cost-profit breakdown with ROI, Profit, operational expenses, and capital data (in percentage).
     3.  Water Usage and Carbon Footprint: Provide values for water usage percentage and carbon footprint in kg CO2 per hectare and description of what happened this season for each of those (keep it short and concise around 7-10 words each).
     4. Personalized Recommendations: Provide two to three personalized recommendations (keep it short and concise around 7-10 words each), based on the farm data.

     The response must be structured as a JSON object and must be concise, easy to parse, structured as below:

     {
      "yield_increase": [
            {
             "month": "Month 1",
             "increase": 10
            },
            {
               "month": "Month 2",
              "increase": 15
             },
            {
               "month": "Month 3",
                "increase": 12
            },
          {
              "month": "Month 4",
                "increase": 8
            }
          ],
     "cost_profit_breakdown": [
          {
           "metric": "ROI",
             "value": 60,
             "description": "Describes the percentage of returns on investment."
          },
         {
             "metric": "Profit",
              "value": 25,
             "description": "Highlights the percentage of profit made."
         },
         {
              "metric": "Operational Expenses",
               "value": 15,
              "description": "Highlights the percentage of operational expenses."
          },
          {
               "metric": "Capital",
                "value": 40,
                "description": "Highlights the percentage of capital used."
           }
         ],
     "water_usage": {
          "value": 78,
          "description": "Water use has decreased by 20% this season."
         },
       "carbon_footprint":{
            "value": "120kg CO₂/ha",
            "description": "Carbon footprint remains consistent with last season."
           },
     "personalized_recommendations":[
         "Consider switching to drip irrigation for higher water efficiency.",
         "Monitor soil pH to improve crop yield.",
         "Try crop rotation for soil health."
      ]
     }
     """
     user_prompt = f"""Based on the provided farm data and weather conditions, generate detailed analytics for the farm, following the required JSON output format:

     Farm Information:
     - Soil Type: {farm_data['soilType']}.
     - pH Level: {farm_data['pHValue']}.
     - Climate: Tropical.
     - Water Availability: Adequate.
     - Farm Size: {farm_data['farmSize']}.
     - Current Crop: {farm_data['currentCrop']}.
     - Current Temperature: {weather_data['currentConditions']['temp']}c.
     - Humidity: {weather_data['currentConditions']['humidity']}.
     - Other Notes: {user_notes if user_notes else "Not specified"}.
     """
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