from langgraph.graph import StateGraph, START, END
from methods import *



def Get_workflow():
    """
    This function returns the workflow of the graph.
    """

    graph= StateGraph(Dietplan_State, start=START, end=END)
    
    # adding the nodes
    graph.add_node('goal_class', goal_class)
    graph.add_node('medical_conditions', medical_conditions)
    graph.add_node('habits', habits)
    graph.add_node('activity_level', activity_level)
    graph.add_node('routine_time', routine_time)
    graph.add_node('nutrient_need', nutrient_need)
    graph.add_node('meal_filter', meal_filter)
    graph.add_node('personalized_meals', personalized_meals)
    graph.add_node('calorie_macro_ai', calorie_macro_ai)
    graph.add_node('supplement_advisor', supplement_advisor)
    graph.add_node('hydration_tips', hydration_tips)
    graph.add_node('pdf_generator', pdf_generator)
    
    
    # add the edges
    graph.add_edge(START, 'goal_class')
    graph.add_edge(START, 'medical_conditions')
    graph.add_edge(START, 'habits')
    graph.add_edge(START, 'activity_level')
    graph.add_edge(START, 'routine_time')
    
    # Parallel preprocessors → Nutrient Need and Meal Filter
    graph.add_edge('goal_class', 'nutrient_need')
    graph.add_edge('medical_conditions', 'meal_filter')
    graph.add_edge('habits', 'meal_filter')
    graph.add_edge('activity_level', 'nutrient_need')
    graph.add_edge('routine_time', 'meal_filter')
    
    # Nutrient Need → Personalized Meals
    graph.add_edge('nutrient_need', 'personalized_meals')
    
    # Meal Filter → Personalized Meals
    graph.add_edge('meal_filter', 'personalized_meals')
    
    # Personalized Meals → Calorie & Macro AI
    graph.add_edge('personalized_meals', 'calorie_macro_ai')
    
    # Calorie & Macro AI → Supplement Advisor
    graph.add_edge('calorie_macro_ai', 'supplement_advisor')
    
    # Supplement Advisor → Hydration & Tips
    graph.add_edge('supplement_advisor', 'hydration_tips')
    
    # Hydration & Tips → PDF Generator
    graph.add_edge('hydration_tips', 'pdf_generator')
    
    # PDF Generator → Final Output
    graph.add_edge('pdf_generator', END)

        

    return graph.compile()



