import pandas as pd
import numpy as np
from datetime import date
from ics import Calendar, Event
import csv
import requests 
from ics import Calendar, Event
import csv
from datetime import timedelta

def get_expiring_items_and_recipes():
    '''
    Returns all items expiring in a week and recommends recipes based on that. 
    '''
    df = pd.read_csv('./barcodes.csv')
    # df = pd.read_csv('./data.csv')
    today = pd.to_datetime("today")
    df['Manufacturing Date'] = pd.to_datetime(df['Manufacturing Date'])
    df['Expiry Date'] = pd.to_datetime(df['Expiry Date'])
    df['days to expire'] = (df['Expiry Date'] - today).dt.days
    expiring_df = df[df['days to expire'] <= 6]
    expiring_df = expiring_df.sort_values(by='days to expire')
    expiring_df.to_csv('./expiring_items.csv', index=False)
    ingredients = expiring_df['Name'].tolist()

    URL = "https://api.spoonacular.com/recipes/complexSearch" 
    PARAMS = {'includeIngredients': ingredients, 'apiKey': 'c20293f2ec134849b0fe9263ff12f060'} 
    r = requests.get(url = URL, params = PARAMS) 
    data = r.json()

    recommended_recipes = []
    for d in data['results']:
        recommended_recipes.append([d['title'], d['missedIngredientCount']])

    recommended_recipes = sorted(recommended_recipes, key=lambda x: x[1])

    recommended_recipes = [items[0] for items in recommended_recipes][:3]

    return recommended_recipes, ingredients


def generate_ics():
    '''
    creates a calendar file which can be synced to GMAIL, Outlook, etc and returns list of expiring items
    '''

    recommended_recipes, ingredients = get_expiring_items_and_recipes()

    event_description = ""
    expired_items = pd.read_csv('expiring_items.csv')

    for index, row in expired_items.iterrows():
        event_description = event_description + str(row['Name']) + " in " + str(row['days to expire']) + " days\n" 


    event_description = event_description + "\n" + "Suggested Recipes: \n" 
    for recipe in recommended_recipes:
        event_description = event_description + recipe + "\n"

        
    c = Calendar()
    e = Event()
    e.name = "Items expiring this week"
    e.description = event_description
    today = pd.to_datetime("today")
    e.begin = today + timedelta(days = 6)
    c.events.add(e)
    c.events

    with open('expiry_reminder.ics', 'w') as my_file:
        my_file.writelines(c)

    return ingredients