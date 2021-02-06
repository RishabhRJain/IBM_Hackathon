#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pandas as pd
import numpy as np
from datetime import date
from ics import Calendar, Event
import csv
import requests 


# ### Filter data based on days to expire

# In[2]:


df = pd.read_csv('./data.csv')
df.head()


# In[3]:


today = pd.to_datetime("today")
today


# In[4]:


df['Manufacturing Date'] = pd.to_datetime(df['Manufacturing Date'])
df['Expiry Date'] = pd.to_datetime(df['Expiry Date'])


# In[5]:


df.dtypes


# In[6]:


type(today)


# In[7]:


df['days to expire'] = (df['Expiry Date'] - today).dt.days


# In[8]:


df.dtypes


# In[9]:


df.head()


# In[16]:


# find all the products which are expiring in the next week
expiring_df = df[df['days to expire'] <= 6]
expiring_df.head()


# In[17]:


expiring_df = expiring_df.sort_values(by='days to expire')
expiring_df.head()


# In[18]:


expiring_df.to_csv('./expiring_items.csv', index=False)


# ### Get recipes based on expiring items
# 

# In[39]:


ingredients = expiring_df['Name'].tolist()
ingredients


# In[25]:



  
# api-endpoint 
URL = "https://api.spoonacular.com/recipes/complexSearch"
  
# defining a params dict for the parameters to be sent to the API 
PARAMS = {'includeIngredients': ingredients, 'apiKey': 'c20293f2ec134849b0fe9263ff12f060'} 
  
# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 
  
# extracting data in json format 
data = r.json() 


# In[26]:


print(data)


# In[42]:


# sort recommendations based on least missing ingredients and return top 3
recommended_recipes = []
for d in data['results']:
    recommended_recipes.append([d['title'], d['missedIngredientCount']])

recommended_recipes = sorted(recommended_recipes, key=lambda x: x[1])

recommended_recipes = [items[0] for items in recommended_recipes][:3]
print(recommended_recipes)


# ### create calendar file

# In[46]:


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
e.begin = today
c.events.add(e)
c.events

with open('my.ics', 'w') as my_file:
    my_file.writelines(c)


# In[ ]:




