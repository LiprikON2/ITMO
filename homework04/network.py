from igraph import Graph, plot, drawing, summary
import numpy as np
import itertools
import random
import argparse

from api import get_friends, get_user, get_ids, get_name
from bcolors import bcolors


def process_friends(users_ids: int, vertices: list = None) -> (list, list):
    """ Creates list of dictionaries that contains friends info """
    
    users = []
    
    for user_id in users_ids:
        
        # Get user friends
        friends_json = get_friends(user_id, fields='lists')
        
        # Skip user if his profile is not avalible
        if 'error' in friends_json:
            name = get_name(str(user_id))
            print(f"{bcolors.FAIL}{name}'s profile is private{bcolors.ENDC}")
            continue
        
        # Create user friend list
        user_friends = []
        for friend in friends_json['response']['items']:
            # Check if friend profile is deleted
            if not 'deactivated' in friend:
                name = friend['first_name'] + ' ' + friend['last_name']
                
                # Add (1) to the end of a name if needed
                unique_name = resolve_duplicate(name, user_friends)            
                
                user_friends.append({
                    'name': unique_name,
                    'id': friend['id'],
                })
        
        users.append({
            'user_name': get_name(str(user_id)),
            'user_id': user_id,
            'user_friends': user_friends,
            'index': ''
        })
        
    # In case users have DIFFERENT friends with the SAME NAME, assign them unique name
    for user_a, user_b in itertools.combinations(users, 2):
        
        for friend_a in user_a['user_friends']:
            for friend_b in user_b['user_friends']:
                
                if friend_a['name'] == friend_b['name'] and friend_a['id'] != friend_b['id']:
                    friend_a['name'] = resolve_duplicate(friend_a['name'], [friend_b])
            
            
    vertices = create_vertices(users)
        
    # Get users index in vertices list
    for user in users:
        while True:
            # In case getting network of one user
            try:
                user['index'] = vertices.index(user['user_name'])
            # Add him to friend list
            except ValueError:
                vertices.append(str(user['user_name']))
                continue
            break
        
    return users, vertices


def resolve_duplicate(name: str, user_friends: list, recurr_lvl = 0) -> str:
    """ 
    Compares name with list of names
    If duplicate found, add (1) to dupicate
    """
    
    # Recursive check if there is already friend with the same name
    for user_friend in user_friends:
        if user_friend['name'] == name:
            recurr_lvl += 1
            
            if not '(' in name:
                name += f' ({recurr_lvl})'
            else:
                index = name.index('(') - 1
                name = name[0:index] + f' ({recurr_lvl})'
            
            name = resolve_duplicate(name, user_friends, recurr_lvl)
            
    return name
            



def create_vertices(users: list) -> list:
    """ Creates vertices (points) that represent friends """
    
    vertices = set()
    
    for user in users:
        for friend in user['user_friends']:
            vertices.add(friend['name'])
        
    vertices = list(vertices)
    
    return vertices


def connect_mutuals(users: list, vertices: list) -> (list, list):
    """ Creates connectionas between mutual friends """
    
    edges = []
    mutual_indexes = []
    
    # Makes program work in case only one user id is passed to it
    if len(users) == 1:
        users.append(users[0])
    
    for user_a, user_b in itertools.combinations(users, 2):
        
        for friend_a in user_a['user_friends']:
            for friend_b in user_b['user_friends']:
                
                # Connect friends and users
                edges.append((vertices.index(friend_a['name']), user_a['index']))
                edges.append((vertices.index(friend_b['name']), user_b['index']))
                
                # Check if users have mutual friends
                if friend_a['id'] == friend_b['id']:
                    
                    friend_index = vertices.index(friend_a['name'])
                    
                    # Connect mutual friends
                    edges.append((friend_index, user_a['index']))
                    edges.append((friend_index, user_b['index']))
                    
                    # Add friend to mutual friends index list
                    mutual_indexes.append(friend_index)
        
    return edges, mutual_indexes



def get_network(users_ids: list) -> None:
    """ Building a friend graph for an arbitrary list of users """
    
    users, vertices = process_friends(users_ids)
    
    edges, mutual_indexes = connect_mutuals(users, vertices)
    
    plot_graph(vertices, edges, mutual_indexes=mutual_indexes, users=users)
    
    
    

def plot_graph(vertices: list, edges: list, mutual_indexes: list = None, users: list = None) -> None:
    """ Create image of VK friends connections """
    
    # Создание графа
    g = Graph(vertex_attrs={"label":vertices},
        edges=edges, directed=False)

    # Задаем стиль отображения графа
    N = len(vertices)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N**3,
        repulserad=N**3)
    # Image size
    visual_style["bbox"] = (1600, 900)
    # Line size
    visual_style["edge_width"] = 0.5
    # Dot size
    visual_style["vertex_size"] = 25
    # Font size
    visual_style["vertex_label_size"] = 12
    # Distance between dot and label
    visual_style["vertex_label_dist"] = 1.5
    
    visual_style["margin"] = 100
    visual_style["vertex_label_color"] = "black"
    visual_style["edge_color"] = 'grey'

    
    # Теперь удалим из графа петли и повторяющиеся ребра
    g.simplify(multiple=True, loops=True)
    
    communities = g.community_edge_betweenness(directed=True)
    clusters = communities.as_clustering()
    
    pal = drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    
    
    # Optional individual style
    
    if mutual_indexes:
        # Paint mutual friends
        for mutual in mutual_indexes:
            # g.vs[mutual]['color'] = '#5e9955'
            connections = mutual_indexes.count(mutual)
            # Generate unique color for certain level of mutuality
            random.seed(connections*123456)
            g.vs[mutual]['color'] = "#%06x" % random.randint(0, 0xFFFFFF)

    # Paint mutual friends
    if users:
        # Paint given users
        for user in users:
            g.vs[user['index']]['color'] = 'white'
        
    # Отрисовываем граф
    plot(g, **visual_style)
    


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("ids", type=str, help="Comma separated list of VK users ids or screen names")
    
    args = parser.parse_args()
    
    ids = get_ids(args.ids.split(','))
    get_network(ids)
    
    # ids = get_ids(['liprikon2', 'trycha2305', '74171270', '146783872'])