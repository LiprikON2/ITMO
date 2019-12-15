from api import get_friends, get_mutual, get_user
from igraph import Graph, plot, drawing
import numpy as np
import itertools

users_ids = [74171270, 87393116]

    
users = []

# Creating list of dictionaries that contain friends info
for user_id in users_ids:
    json2 = get_user(user_id)
    
    
    
    print(json2)