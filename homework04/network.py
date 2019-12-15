from api import get_friends, get_user
from igraph import Graph, plot, drawing, summary
import numpy as np
import itertools
import random

def process_friends(users_ids) -> list:
    """ Creates list of dictionaries that contains friends info """
    
    users = []
    
    for user_id in users_ids:
        
        friends_json = get_friends(user_id, fields='lists')
        
        user_friends = []
        for friend in friends_json['response']['items']:
            # Check if profile is deleted
            if not 'deactivated' in friend:
                name = friend['first_name'] + ' ' + friend['last_name']
                user_friends.append({'name': name, 'id': friend['id']})
        
        # Get user info
        user_info = get_user(user_id)['response'][0]
        # Retrive user name from user info
        user_name = user_info['first_name'] + ' ' + user_info['last_name']
        
        users.append({
            'user_name': user_name,
            'user_id': user_id,
            'user_friends': user_friends,
            'index': ''
        })
        
        
    
    vertices = create_vertices(users)    
    
    # Get users index in vertices list
    for user in users:
        user['index'] = vertices.index(user['user_name'])
        
    return users

def create_vertices(users) -> list:
    """ Creates vertices (points) that represent friends """
    vertices = set()
    
    # vertices = []
    
    for user in users:
        for friend in user['user_friends']:
            vertices.add(friend['name'])
        
    vertices = list(vertices)
    
    return vertices

def get_mutual(users, vertices):
    # Get mutual friends
    edges = []
    mutual_indexes = []
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



def get_network(users_ids, as_edgelist=True):
    """ Building a friend graph for an arbitrary list of users """
    
    users = process_friends(users_ids)
    vertices = create_vertices(users)    
    
    edges, mutual_indexes = get_mutual(users, vertices)
    

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
    
    
    # Individual style
    
    # Paint mutual friends
    for mutual in mutual_indexes:
        # g.vs[mutual]['color'] = '#5e9955'
        connections = mutual_indexes.count(mutual)
        
        random.seed(connections*12345)
        g.vs[mutual]['color'] = "#%06x" % random.randint(0, 0xFFFFFF)

    # Paint given users
    for user in users:
        g.vs[user['index']]['color'] = 'white'
        
    # Отрисовываем граф
    plot(g, **visual_style)
    

def plot_graph(graph):
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    # get_network([87393116])
    get_network([74171270, 87393116, 146783872])
    # get_network([87393116, 74171270])
    pass