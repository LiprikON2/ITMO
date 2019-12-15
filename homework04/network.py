from api import get_friends, get_mutual, get_user
from igraph import Graph, plot, drawing, summary
import numpy as np
import itertools

def get_network(users_ids, as_edgelist=True):
    """ Building a friend graph for an arbitrary list of users """
    
    users = []
    
    # Creating list of dictionaries that contain friends info
    for user_id in users_ids:
        
        friends_json = get_friends(user_id, fields='lists')
        
        user_friends = []
        for friend in friends_json['response']['items']:
            if not 'deactivated' in friend:
                user_friends.append({'name': friend['first_name'] + ' ' + friend['last_name'], 'id': friend['id']})    
        
        # Get user info
        user_info = get_user(user_id)['response'][0]
        # Format name from user info
        user_name = user_info['first_name'] + ' ' + user_info['last_name']
        
        users.append({
            'user_name': user_name,
            'user_id': user_id,
            'user_friends': user_friends,
            'index': ''
        })
    
    
    # Create friend-points
    vertices = set()
    
    for user in users:
        
        for friend in user['user_friends']:
            vertices.add(friend['name'])
        
    vertices = list(vertices)
    
    # Give users index in vertices list
    for user in users:
        user['index'] = vertices.index(user['user_name'])
    
    # print(vertices)
    
    
    
    # Get mutual friends
    edges = []
    mutuals_index = []
    for user_a, user_b in itertools.combinations(users, 2):
        
        for friend_a in user_a['user_friends']:
            for friend_b in user_b['user_friends']:
                
                edges.append((vertices.index(friend_a['name']), user_a['index']))
                edges.append((vertices.index(friend_b['name']), user_b['index']))
                
                # Check if users have mutual friend
                if friend_a['id'] == friend_b['id']:
                    
                    friend_index = vertices.index(friend_a['name'])
                    
                    # Connect them with users
                    edges.append((friend_index, user_a['index']))
                    edges.append((friend_index, user_b['index']))
                    
                    # Add friend to mutual friends index list
                    mutuals_index.append(friend_index)
    
    print(mutuals_index)
    
    # Создание вершин и ребер
    # vertices = [i for i in range(7)]
    
    # edges = [
    #     (0,2),(0,1),(0,3),
    #     (1,0),(1,2),(1,3),
    #     (2,0),(2,1),(2,3),(2,4),
    #     (3,0),(3,1),(3,2),
    #     (4,5),(4,6),
    #     (5,4),(5,6),
    #     (6,4),(6,5)
    # ]
    

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
    # visual_style['vertex_label'] = users['user_friends']
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
    
    # visual_style["vertex_shape"] = 'rectangle'

    
    
    # summary(g)
    
    # Теперь удалим из графа петли и повторяющиеся ребра
    g.simplify(multiple=True, loops=True)
    
    communities = g.community_edge_betweenness(directed=True)
    clusters = communities.as_clustering()
    
    pal = drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    
    
    # Individual style
    
    # Paint mutual friends
    for mutual in mutuals_index:
        g.vs[mutual]['color'] = 'grey'

    # Paint given users
    for user in users:
        g.vs[user['index']]['color'] = 'white'
        
    # for e in g.es:
    #     s= e.tuple
    #     print(s)
    # for v in g.vs:
    #     v["weight"] = 100
    
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