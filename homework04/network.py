from api import get_friends, get_user, get_mutual
from igraph import Graph, plot, drawing, summary
import numpy as np
import itertools
import random

def process_friends(users_ids: int, vertices: list = None) -> (list, list):
    """ Creates list of dictionaries that contains friends info """
    
    users = []
    
    for user_id in users_ids:
        
        # Get user friends
        friends_json = get_friends(user_id, fields='lists')
        
        
        if 'error' in friends_json:
            print(friends_json['error'])
            continue
        
        # Create user friend list
        user_friends = []
        for friend in friends_json['response']['items']:
            # Check if friend profile is deleted
            if not 'deactivated' in friend:
                name = friend['first_name'] + ' ' + friend['last_name']
                
                user_friends.append({
                    'name': name,
                    'id': friend['id'],
                })
        
        users.append({
            'user_name': get_name(user_id),
            'user_id': user_id,
            'user_friends': user_friends,
            'index': ''
        })
        
    
    if not vertices:
        vertices = create_vertices(users)
        
    # Get users index in vertices list
    for user in users:
        print('user', user['user_name'])
        
        while True:
            # In case getting network of one user
            try:
                print('trying', user['user_name'])
                user['index'] = vertices.index(user['user_name'])
            # Add him to friend list
            except ValueError:
                vertices.append(str(user['user_name']))
                print(user['user_name'], 'ValueError in process_friends; continuing')
                continue
            break
        
    print(vertices)
    return users, vertices

def get_name(id: int) -> str:
    """ Retrives name from id """
    
    # Get user info
    user_info = get_user(id)['response'][0]
    # Retrive user name from user info
    user_name = user_info['first_name'] + ' ' + user_info['last_name']
    
    return user_name


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
    if len(users) == 1:
        users.append(users[0])
    for user_a, user_b in itertools.combinations(users, 2):
        # for friend_a, friend_b in itertools.combinations(user_a['user_friends'], 2):
        for friend_a in user_a['user_friends']:
            for friend_b in user_b['user_friends']:
                
                # mutals_json = get_mutual(int(friend_a['id']), int(friend_b['id']))
                
                # for mutual_id in mutals_json['response']:
                #     mutual_name = get_name(mutual_id)
                #     try:
                #         edges.append((vertices.index(friend_a['name']), (vertices.index(mutual_name))))
                #         edges.append((vertices.index(friend_b['name']), (vertices.index(mutual_name))))
                #     except ValueError:
                #         print('ValueError')
                #         continue
                # Connect friends and users
                try:
                    edges.append((vertices.index(friend_a['name']), user_a['index']))
                    edges.append((vertices.index(friend_b['name']), user_b['index']))
                except ValueError:
                    print('ValueError')
                    continue
                
                # Check if users have mutual friends
                if friend_a['id'] == friend_b['id']:
                    
                    friend_index = vertices.index(friend_a['name'])
                    
                    # Connect mutual friends
                    edges.append((friend_index, user_a['index']))
                    edges.append((friend_index, user_b['index']))
                    
                    # Add friend to mutual friends index list
                    mutual_indexes.append(friend_index)
        print(users.index(user_a), 'and',users.index(user_b) ,'/', len(users))
    # edges = list(set(edges))
    return edges, mutual_indexes



def get_network(users_ids, as_edgelist=True):
    """ Building a friend graph for an arbitrary list of users """
    
    users, vertices = process_friends(users_ids)
    
    edges, mutual_indexes = connect_mutuals(users, vertices)
    
    # all_friends = []
    # for user in users:
    #     for friend in user['user_friends']:
    #         all_friends.append(friend['id'])
            
    # users2, _ = process_friends(all_friends, vertices=vertices)
    
    # print('users2 len', len(users2))
    # edges, mutual_indexes = connect_mutuals(users2, vertices)
    # print('EDGY', edges)
    
    # print(vertices)

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
        
        random.seed(connections*123456)
        g.vs[mutual]['color'] = "#%06x" % random.randint(0, 0xFFFFFF)

    # Paint given users
    for user in users:
        print(user['index'], len(g.vs))
        g.vs[user['index']]['color'] = 'white'
        
    # Отрисовываем граф
    plot(g, **visual_style)
    

def plot_graph(graph):
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    # get_network([87393116])
    get_network([74171270, 87393116, 146783872])
    s = get_mutual(74171270, 87393116)
    print(s)
    # get_network([87393116, 74171270])
    pass