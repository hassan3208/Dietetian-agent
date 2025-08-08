from typing import Literal, Union

from typing_extensions import TypedDict 

import os
from langchain.chat_models import init_chat_model

from pydantic import Field
import json
import re
from markdown2 import markdown
from jinja2 import Template
import pdfkit
import io



os.environ["GOOGLE_API_KEY"] = "API_KEY"
llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")



class Dietplan_State(TypedDict):
    
    #user input fields
    name: str= Field( default="Patient", description="Name of the patient", examples=["John Doe", "Jane Smith"])
    age: int = Field(default=30, description="Age of the patient", examples=[25, 40],gt=0, lt=90)
    gender: Literal['MALE', 'FEMALE','BISEXUAL','OTHER'] = Field(default='MALE', description='gender of the patient', examples=['MALE', 'FEMALE','BISEXUAL','OTHER'])
    height_m: float = Field(default=1.70, description="Height of the patient in meters", examples=[1.60, 1.80], gt=0.6, lt=2.00)
    weight_kg: int = Field(default=70, description="Weight of the patient in kg", examples=[50, 100], gt=30, lt=200)
    bmi: float = Field(default=None, description="Body Mass Index of the patient", examples=[22.5, 27.0], gt=10.0, lt=50.0)
    primary_goal: str = Field(default='LOSE_WEIGHT', description="Goal of the patient", examples=['LOSE_WEIGHT', 'GAIN_WEIGHT', 'MAINTAIN_WEIGHT'])
    diet_type: Literal['VEGETARIAN', 'NON_VEGETARIAN', 'VEGAN'] = Field(default='NON_VEGETARIAN', description="Type of diet", examples=['VEGETARIAN', 'NON_VEGETARIAN', 'VEGAN'])
    allergies: list[str] = Field(default_factory=list, description="List of allergies", examples=["nuts","gluten", "dairy"])
    medical_conditions: list[str] = Field(default_factory=list, description="List of medical conditions", examples=[["diabetes"], ["hypertension", "high cholesterol"]])
    activity_level_description : str = Field(default='MODERATE', description="Activity level of the patient")
    wake_time: str = Field(default="7:00 AM", description="Wake time of the patient", examples=["6:00 AM", "8:00 AM"])
    sleep_time: str = Field(default="11:00 PM", description="Sleep time of the patient", examples=["10:00 PM", "12:00 AM"])
    meal_frequency: int = Field(default=3, description="Number of meals per day", examples=[2, 5], gt=1, lt=10)
    supper_snacks: Union[Literal['No'],list[str]] = Field(default=None, description="Whether the patient has supper or snacks", examples=['No', ['fruits', 'nuts']])
    breakfast: Union[Literal['No'],list[str]] = Field(default=None, description="Whether the patient has breakfast", examples=['No', ['eggs', 'toast']])
    lunch: Union[Literal['No'],list[str]] = Field(default=None, description="Whether the patient has lunch", examples=['No', ['rice', 'chicken']])
    dinner: Union[Literal['No'],list[str]] = Field(default=None, description="Whether the patient has dinner", examples=['No', ['pasta', 'salad']])
    likes: list[str] = Field(default_factory=list, description="List of liked foods", examples=[["chicken", "fish"], ["fruits", "vegetables"]])
    dislikes: list[str] = Field(default_factory=list, description="List of disliked foods", examples=[["spinach"], ["broccoli", "cauliflower"]])
    water_intake: float = Field(default=4, description="Daily water intake in number of glasses", examples=[1, 3], gt=0, lt=6)
    
    #output fields
    goal_class: Literal['WEIGHT_LOSS', 'WEIGHT_GAIN', 'MAINTENANCE','CLINICAL_DIET','CHILD_DIET'] = Field(default=None, description="Classified goal of the patient", examples=['WEIGHT_LOSS', 'WEIGHT_GAIN', 'MAINTENANCE', 'CLINICAL_DIET', 'CHILD_DIET'])
    target_calories: int = Field(default=2000, description="Target calories for the patient", examples=[1500, 2500], gt=1000, lt=5000)
    restrictions: list[str] = Field(default_factory=list, description="List of dietary restrictions", examples=["gluten-free","low-carb", "low-sugar"])
    warnings: list[str] = Field(default_factory=list, description="List of warnings", examples=["high cholesterol","diabetes management", "low iron levels"])  
    preferences: list[str] = Field(default_factory=list, description="List of dietary preferences", examples=["low-fat","high-protein", "low-carb"])
    avoid: list[str] = Field(default_factory=list, description="List of foods to avoid", examples=["sugar","processed foods", "high sodium foods"])  
    activity_level: Literal['SEDENTARY', 'LIGHT', 'MODERATE', 'ACTIVE', 'VERY_ACTIVE'] = Field(default=None, description="Classified activity level of the patient", examples=['SEDENTARY', 'LIGHT', 'MODERATE', 'ACTIVE', 'VERY_ACTIVE'])
    protein_multiplier: float = Field(default=1.0, description="Protein multiplier based on activity level", examples=[0.8, 1.2, 1.5])
    meal_schedule: dict[str, str] = Field(default_factory=dict, description="Meal schedule for the patient", examples=[{"breakfast": ["eggs", "toast"], "lunch": ["rice", "chicken"], "dinner": ["pasta", "salad"]}])
    macros_target: dict[str, str] = Field(default_factory=dict, description="Macronutrient targets for the patient", examples=[{"protein": 150.0, "carbs": 200.0, "fats": 70.0}])
    micros_needed: list[str] = Field(default_factory=list, description="List of micronutrients needed", examples=["vitamin D","calcium", "iron"])
    allowed_meals: list[str] = Field(default_factory=list, description="List of allowed meals", examples=["grilled chicken salad","vegetable stir-fry", "quinoa bowl"])
    diet_plan_pdf: bytes = Field(default=None,description="The generated proposal PDF in bytes format.")
    
    
    meals: dict[str, dict[str, Union[str, list[str], int]]] = Field(
        default_factory=dict,
        description="Meal plan for the patient with time, items, and calories",
        examples=[
            {
                "breakfast": {"time": "8:00 AM", "items": ["eggs", "toast"], "calories": 300},
                "lunch": {"time": "12:00 PM", "items": ["rice", "chicken"], "calories": 500},
                "dinner": {"time": "7:00 PM", "items": ["pasta", "salad"], "calories": 400},
                "snacks": {"items": ["fruits", "nuts"], "calories": 200}
            }
        ]
    )
    
    total_calories: int = Field(default=2000, description="Total daily calories for the patient",examples=[1500, 2500],gt=1000,lt=5000)
    actual_macros: dict[str, str] = Field(default_factory=dict, description="Actual macronutrient intake for the patient", examples=[{"protein": "150g", "carbs": "200g", "fat": "70g"}])
    recommendation: str = Field(default="", description="Dietary recommendation for the patient", examples=["Increase protein intake","Reduce sugar consumption","Include more vegetables in meals"])
    supplements: list[str] = Field(default_factory=list, description="List of recommended supplements", examples=["vitamin D","omega-3 fatty acids", "multivitamins"])
    notes: str = Field(default="", description="Additional notes for the patient", examples=["Monitor blood sugar levels","Follow up in 2 weeks","Consider a nutritionist consultation"])
    water_intake: str
    tips : list[str]



def calculate_bmi(weight_kg, height_m) -> float:
    """
    Calculates the Body Mass Index (BMI).

    Args:
        weight_kg (float): The individual's weight in kilograms.
        height_m (float): The individual's height in meters.

    Returns:
        float: The calculated BMI value.
    """
    if height_m <= 0:
        raise ValueError("Height cannot be zero or negative.")
    bmi = weight_kg / (height_m ** 2)
    return bmi


def get_response(Prompt: str) -> str:
    """
    Gets a response from the language model based on the provided prompt.
    
    Args:
        Prompt (str): The input prompt for the language model.
        
    Returns:
        str: The response content from the language model.
    """
    response = llm.invoke(Prompt)
    return response.content
    


def get_JSON(response: str) -> dict:
    """
    Parses a JSON string into a Python dictionary.
    
    Args:
        response (str): The JSON string to parse.
        
    Returns:
        dict: The parsed JSON data.
    """
    try:
        match = re.search(r'\{[\s\S]*\}', response)
        if match:
            response_json = match.group(0)
            response_json = json.loads(response_json)
            return response_json
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return {}





def goal_class(state: Dietplan_State) -> Dietplan_State:
    """
    Classifies the user's fitness/diet goal (e.g., weight loss, muscle gain).
    """
    print('goal class')
    
    bmi=calculate_bmi(state['weight_kg'], state['height_m'])
    
    
    prompt = f"""Given the following patient data, classify the primary health goal as one of the following: 
             - weight_loss
             - muscle_gain
             - maintenance
             - child_diet
             - clinical_diet
             
             Also estimate a daily target calorie intake.
             
             Patient Info:
             Age: {state['age']}
             Gender: {state['gender']}
             Height: {bmi}
             Stated Goal(by user): {state["primary_goal"]}
             
             Respond in json format: {{"goal_class": "...", "target_calories": ...}}
             """
    try:
        response = get_response(prompt)
        response_json = get_JSON(response)
        
        state['goal_class'] = response_json.get('goal_class', 'MAINTENANCE')  # Default to MAINTENANCE if not provided
        state['target_calories'] = response_json.get('target_calories', 2000)  # Default to 2000 if not provided
        return {'goal_class': state['goal_class'], 'target_calories': state['target_calories'], 'bmi': bmi}
    except Exception as e:
        print(f"Error in goal_class: {e}")
    
    

def medical_conditions(state: Dietplan_State) -> Dietplan_State:
    """
    Filters meals or suggestions based on medical conditions.
    """
    print('medical condition')
        
    
    prompt = f"""Analyze the following medical conditions and allergies. Provide a list of dietary restrictions and medical cautions that must be considered while creating a meal plan.

             Medical Conditions: {state['medical_conditions']}
             Allergies: {state["allergies"]}
             Respond in JSON: {{ "restrictions": [...], "warnings": [...] }}
             """

    try:
        response = get_response(prompt)
        response_json = get_JSON(response)
        
        state['restrictions'] = response_json.get('restrictions', None)  # Default to MAINTENANCE if not provided
        state['warnings'] = response_json.get('warnings', None)  # Default to 2000 if not provided
        return {'restrictions': state['restrictions'], 'warnings': state['warnings']}
    except Exception as e:
        print(f"Error in medical conditions: {e}")
        
        
        

def habits(state: Dietplan_State) -> Dietplan_State:
    """
    Analyzes user habits like meal preferences, allergies, etc.
    """
    
    print('habbits')
        
    prompt = f"""Given the patient’s eating habits and preferences, generate a list of food preferences, cultural restrictions, and foods to avoid to achieve his goal.
              
              Patient Goal: {state['primary_goal']}
              Diet Type: {state['diet_type']}
              Likes: {state['likes']}
              Dislikes: {state['dislikes']}
              Snacks at supper: {state['supper_snacks']}
              Breakfast: {state['breakfast']}
              Lunch: {state['lunch']}
              Dinner: {state['dinner']}
                
              
              Respond in JSON: {{ "preferences": [...], "avoid": [...] }}
              """


    try:
        response = get_response(prompt)
        response_json = get_JSON(response)
        
        state['preferences'] = response_json.get('preferences', None)  # Default to MAINTENANCE if not provided
        state['avoid'] = response_json.get('avoid', None)  # Default to 2000 if not provided
        return {'preferences': state['preferences'], 'avoid': state['avoid']}
    except Exception as e:
        print(f"Error in habits: {e}")
        
        
        
        
        
        

def activity_level(state: Dietplan_State) -> Dietplan_State:
    """
    Adjusts nutrition based on the patient's activity level.
    """
    
    print('activity level')
        
    prompt = f"""Classify the patient’s physical activity level as one of:
             - sedentary
             - moderate
             - light
             - active
             - very_active
             
             Also suggest a protein intake multiplier (between 1.0–2.0) based on activity.
             
             Activity Description: {state['activity_level_description']}
             
             Respond in JSON: {{ "activity_level": "...", "protein_multiplier": ... }}
             """



    try:
        response = get_response(prompt)
        response_json = get_JSON(response)
        
        state['activity_level'] = response_json.get('activity_level', None)  # Default to MAINTENANCE if not provided
        state['protein_multiplier'] = response_json.get('protein_multiplier', None)  # Default to 2000 if not provided
        return {'activity_level': state['activity_level'], 'protein_multiplier': state['protein_multiplier']}
    except Exception as e:
        print(f"Error in habits: {e}")
        
        
        
        
        

def routine_time(state: Dietplan_State) -> Dietplan_State:
    """
    Uses wake/sleep time and meal frequency to estimate meal timings.
    """
    
    print('routine time')
        
    prompt = f"""Based on the patient's wake and sleep times and number of meals per day, create an ideal daily meal schedule with meal names and suggested times.

             Wake Time: {state['wake_time']}
             Sleep Time: {state['sleep_time']}
             Meal Frequency: {state['meal_frequency']}
             
             Respond in JSON: 
             {{ 
               "meal_schedule": {{ 
                 "breakfast": "...", 
                 "lunch": "...", 
                 "dinner": "...", 
                 "snack_1": "...", 
                 ...
               }}
             }}
             """




    try:
        response = get_response(prompt)
        response_json = get_JSON(response)
        
        state['meal_schedule'] = response_json.get('meal_schedule', None)  
        return {'meal_schedule': state['meal_schedule']}
    except Exception as e:
        print(f"Error in habits: {e}")
        
        
        
        
        
        

def nutrient_need(state: Dietplan_State) -> Dietplan_State:
    """
    Calculates the patient's required calories and macronutrient distribution.
    """
    
    print('nutrient need')
        
    prompt = f"""Estimate daily macro- and micronutrient needs for the patient based on their profile.

             Age: {state['age']}
             Gender: {state['gender']}
             BMI: {state['bmi']} 
             Goal Class: {state['goal_class']}
             Activity Level: {state['activity_level']}
             
             Respond in JSON:
             {{ 
               "macros_target": {{ "protein": "...g", "carbs": "...g", "fat": "...g" }},
               "micros_needed": ["calcium", "iron", "vitamin D", "fiber", ...]
             }}
             """


    try:
        response = get_response(prompt)
        response_json = get_JSON(response)
        
        state['macros_target'] = response_json.get('macros_target', None) 
        state['micros_needed'] = response_json.get('micros_needed', None)  
        return {'macros_target': state['macros_target'], 'micros_needed': state['micros_needed']}
    except Exception as e:
        print(f"Error in habits: {e}")
        
        
        
        
        
        
        

def meal_filter(state: Dietplan_State) -> Dietplan_State:
    """
    Filters meals based on dislikes, allergies, preferences (veg/non-veg).
    """
    
    print('meal filter')
        
    prompt = f"""Filter the allowed meals based on the patient’s dislikes, allergies, preferences and medical restrictions.

             Preferences: {state['preferences']}
             Restrictions: {state['restrictions']}
             Avoid: {state['avoid']}
             Likes: {state['likes']}
             Dislikes: {state['dislikes']}
             
                          
             Respond in JSON: {{ "allowed_meals": [ "grilled chicken", "lentils", ... ] }}
             """



    try:
        response = get_response(prompt)
        response_json = get_JSON(response)
        
        state['allowed_meals'] = response_json.get('allowed_meals', None)
        return {'allowed_meals': state['allowed_meals']}
    except Exception as e:
        print(f"Error in habits: {e}")
        
        
        
        
        
        
        

def personalized_meals(state: Dietplan_State) -> Dietplan_State:
    """
    Selects personalized meal suggestions for breakfast, lunch, dinner, and snacks.
    """
    
    print('personalize meal')
        
    prompt = f"""Create a full-day meal plan using the allowed meals, nutrient needs, and meal timing schedule.

             Goal: {state['goal_class']}
             Target Calories: {state['target_calories']}
             Meal Schedule: {state['meal_schedule']}
             Allowed Meals: {state['allowed_meals']}
             Macros Target: {state['macros_target']}
             Micros Needed: {state['micros_needed']}
                
             
             Respond in JSON:
             {{
               "meals": {{
                 "breakfast": {{
                   "time": "...",
                   "items": [...],
                   "calories": ...
                 }},
                 "lunch": {{...}},
                 "dinner": {{...}},
                 "snacks": [...]
               }}
             }}
             """

    try:
        response = get_response(prompt)
        response_json = get_JSON(response)
        
        
        state['meals'] = response_json.get('meals', None)
        return {'meals': state['meals']}
    except Exception as e:
        print(f"Error in habits: {e}")
        
        
        
        
        
        
        

def calorie_macro_ai(state: Dietplan_State) -> Dietplan_State:
    """
    Finalizes calorie and macronutrient mapping to selected meals.
    """
    
    print('macro calori')
        
    prompt = f"""Calculate the total calorie count and macro breakdown for the provided meals. Compare it with the target and return recommendations.

             Target Calories: {state['target_calories']}
             Macros Target: {state['macros_target']}
             Micros Needed: {state['micros_needed']}
             Meal Schedule: {state['meal_schedule']}
             Meal Plan: {state['meals']}
             
             
             Respond in JSON:
             {{
               "total_calories": ...,
               "actual_macros": {{ "protein": "...g", "carbs": "...g", "fat": "...g" }},
               "recommendation": "..."
             }}
             """


    try:
        response = get_response(prompt)
        response_json = get_JSON(response)
        
        
        state['total_calories'] = response_json.get('total_calories', None)
        state['actual_macros'] = response_json.get('actual_macros', None)
        state['recommendation'] = response_json.get('recommendation', None)
        return {'total_calories': state['total_calories'],'actual_macros': state['actual_macros'],'recommendation': state['recommendation']}
    except Exception as e:
        print(f"Error in habits: {e}")
        
        
        
        
        
        

def supplement_advisor(state: Dietplan_State) -> Dietplan_State:
    """
    Suggests supplements based on deficiencies, goal, and medical conditions.
    """
    
    print("supplement")
        
    prompt = f"""Based on the meal plan and patient profile, recommend any nutritional supplements that may help achieve the goal.

             Medical Conditions: {state['medical_conditions']}
             Diet Type: {state['diet_type']}
             Allergies: {state['allergies']}
             Macros Target: {state['macros_target']}
             Micronutrient Needs: {state['micros_needed']}
             Goal Class: {state['goal_class']}
             Meal Plan: {state['meals']}
             
             Respond in JSON:
             {{ "supplements": [...], "notes": "..." }}
             """



    try:
        response = get_response(prompt)
        response_json = get_JSON(response)
        
        
        state['supplements'] = response_json.get('supplements', None)
        state['notes'] = response_json.get('notes', None)
        return {'supplements': state['supplements'],'notes': state['notes']}
    except Exception as e:
        print(f"Error in habits: {e}")
        
        
        
        
        
        

def hydration_tips(state: Dietplan_State) -> Dietplan_State:
    """
    Provides daily water intake tips based on activity and weather (optional live info).
    """
    
    print('hydration')
        
    prompt = f"""Suggest personalized hydration advice and 2-3 lifestyle tips for wellness.

             BMI: {state['bmi']}
             Climate: 'monson'
             Activity Level: {state['activity_level']}
             
             Respond in JSON:
             {{ 
               "water_intake": "... liters/day", 
               "tips": ["...", "...", "..."] 
             }}
             """




    try:
        response = get_response(prompt)
        response_json = get_JSON(response)
        
        
        state['water_intake'] = response_json.get('water_intake', None)
        state['tips'] = response_json.get('tips', None)
        return {'water_intake': state['water_intake'],'tips': state['tips']}
    except Exception as e:
        print(f"Error in habits: {e}")
        
        
        
        
        

def pdf_generator(state: Dietplan_State) -> Dietplan_State:
    """
    Compiles the full diet plan into a downloadable or shareable PDF.
    """
    
    print('pdf')
    
    prompt=f"""
             You are a professional assistant creating a comprehensive, friendly, and beautifully formatted **diet plan report** for a patient. The output will be used in a **PDF**, so make it visually structured, rich in details, and warm in tone.
             
             Use:
             - 📌 Headings and subheadings  
             - ✅ Bullet points  
             - 🧠 Quotes and health facts  
             - 🍱 Tables for meal plans  
             - ✨ Emojis for better visual appeal  
             - 📣 Motivational messages  
             - 📋 Final health notes  
             
             Use the following data to construct the report:
             
             ---
             
             👤 **Patient Profile:**
             - Name: {state['name']}
             - Age: {state['age']}
             - Gender: {state['gender']}
             - BLI : {state['bmi']}
             - Activity Level: {state['activity_level']}
             - Diet Type: {state['diet_type']}
             - Health Goal: {state['goal_class']}
             
             🩺 **Medical:**
             - Conditions: {state['medical_conditions']}
             - Allergies: {state['allergies']}
             - Restrictions: {state['restrictions']}
             
             🍽️ **Preferences:**
             - Likes: {state['likes']}
             - Dislikes: {state['dislikes']}
             - Meal Frequency: {state['meal_frequency']}
             
             ⏰ **Meal Timing (Routine):**  
             {state['meal_schedule']}
             
             🔥 **Nutritional Targets:**
             - Calories: {state['target_calories']} kcal/day
             - Macronutrients:
               - Protein: {state['macros_target']['protein']}
               - Carbohydrates: {state['macros_target']['carbs']}
               - Fats: {state['macros_target']['fat']}
             - Micronutrients Focus: {state['micros_needed']}
             
             🥗 **Detailed Daily Meal Plan:**  
             {state['meals']}  # Contains breakfast, lunch, dinner, snacks, time, items, calories
             
             💊 **Supplement Suggestions:**
             - {state['supplements']}
             - Notes: {state['notes']}
             
             💧 **Water Intake Recommendation:** {state['water_intake']}  
             🧘‍♀️ **Lifestyle & Wellness Tips:** {state['tips']}
             
             ---
             
             ### 📘 **Structure of the Report:**
             
             1. ✨ Title Page with Quote  
             2. 📋 Patient Summary  
             3. 🚦 Medical Warnings  
             4. 🔬 Nutrition Targets  
             5. 🍱 Full Meal Plan (Table Format)  
             6. 💊 Supplements & Guidance  
             7. 💡 Water + Lifestyle Advice  
             8. 💬 Final Motivational Quote  
             
             ---
             
             Use markdown-style formatting like:
             
             ### 🍱 Meal Plan Table
             
             | Meal      | Time     | Items                            | Calories |
             |-----------|----------|----------------------------------|----------|
             | Breakfast | 08:00 AM | Boiled eggs, Brown toast, Tea    | 350 kcal |
             
             and motivational messages like:
             
             > 🧠 *“Let food be thy medicine and medicine be thy food.”* — Hippocrates
             
             Now generate the full report using the given data. Use UTF-8 Encoding instead of emogis as i will paste to pdf. Use bullet points.
             """
             
    response=get_response(prompt)
    
    print('get response')
    
    html_body = markdown(response,extras=["tables", "fenced-code-blocks"])
    
    print('get html body')
    
    html_template = Template("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', 'Arial Unicode MS', 'Arial', sans-serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #2C3E50;
            background-color: #FFFFFF;
            margin: 40px;
        }


        h1 {
            color: #1A5276;
            background-color: #D6EAF8;
            padding: 16px;
            border-left: 10px solid #2980B9;
            font-size: 24pt;
            margin-bottom: 30px;
        }

        h2 {
            color: #2471A3;
            border-bottom: 2px solid #D4E6F1;
            padding-bottom: 6px;
            margin-top: 30px;
            font-size: 18pt;
        }

        h3 {
            color: #2980B9;
            font-size: 14pt;
            margin-top: 25px;
            margin-bottom: 10px;
        }

        ul, ol {
            margin-left: 25px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 11pt;
        }

        table, th, td {
            border: 1px solid #BDC3C7;
            padding: 10px;
        }

        th {
            background-color: #3498DB;
            color: white;
        }

        tr:nth-child(even) {
            background-color: #F2F3F4;
        }

        tr:hover {
            background-color: #EBF5FB;
        }

        .section-box {
            border: 2px solid #AED6F1;
            background-color: #F4F6F7;
            padding: 20px;
            margin-top: 30px;
            border-radius: 10px;
        }

        .quote {
            font-style: italic;
            color: #34495E;
            padding: 12px;
            margin-top: 20px;
            border-left: 5px solid #2980B9;
            background-color: #FBFCFC;
        }

        .note {
            font-size: 11pt;
            padding: 10px;
            margin-top: 20px;
            background-color: #FCF3CF;
            border-left: 5px solid #F1C40F;
            color: #7D6608;
        }

        .page-break {
            page-break-after: always;
        }

        .center {
            text-align: center;
        }
    </style>
</head>
<body>
    {{ body }}
</body>
</html>
""")

    
    
    
    final_html = html_template.render(body=html_body)
    final_html.encode('utf-8')
    
    print('set final html')
    
    # Save path to wkhtmltopdf
    try:
        path_to_wkhtmltopdf = r"C:\Users\hassan\Desktop\Dietetian Agent\wkhtmltopdf\bin\wkhtmltopdf.exe"
        if not path_to_wkhtmltopdf:
            print("nammually assign path")
            path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    except Exception as e:
        print("Error setting wkhtmltopdf path:", e)

    pdf_bytes=pdfkit.from_string(final_html, False, configuration=config)
    pdf_buffer = io.BytesIO(pdf_bytes)
    state["diet_plan_pdf"] = pdf_buffer.getvalue()
    
    print('set state')
    

    
    


    print(f"✅ Proposal saved to: output_pdf")
    return state


         


























