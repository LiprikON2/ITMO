from api import get_friends, get_group
from igraph import Graph, plot, drawing
import numpy as np

def get_network(users_ids, as_edgelist=True):
    """ Building a friend graph for an arbitrary list of users """
    
    
    
    group_ids = []
    for user_id in users_ids:
        json = get_friends(user_id, vk_command='groups.get')
        
        for group_id in json['response']['items']:
            group_ids.append(group_id)
    
    
    json = get_group(group_ids)
    
    groups = []
    for group in json['response']:
        # groups.append((group['name'], group['id']))
        groups.append(group['name'])
        
    print(groups)
    
    
            
    
    
    
    # Создание вершин и ребер
    vertices = [i for i in range(7)]
    # vertices = ['lol', 'kek', 'lol', 'kek', 'lol', 'kek', 'cheburek']
    
    edges = [
        (0,2),(0,1),(0,3),
        (1,0),(1,2),(1,3),
        (2,0),(2,1),(2,3),(2,4),
        (3,0),(3,1),(3,2),
        (4,5),(4,6),
        (5,4),(5,6),
        (6,4),(6,5)
    ]

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
    visual_style['vertex_label'] = groups
    visual_style["bbox"] = (1200, 900)
    visual_style["edge_width"] = min(2, 20)
    visual_style["vertex_size"] = 30
    # visual_style["vertex_shape"] = 'rectangle'
    visual_style["vertex_label_dist"] = 1.5
    
    
    # Теперь удалим из графа петли и повторяющиеся ребра
    # g.simplify(multiple=True, loops=True)
    
    # communities = g.community_edge_betweenness(directed=False)
    # clusters = communities.as_clustering()
    # print(clusters)
    
    # pal = drawing.colors.ClusterColoringPalette(len(clusters))
    # g.vs['color'] = pal.get_many(clusters.membership)
    
    # Отрисовываем граф
    plot(g, **visual_style)
    

def plot_graph(graph):
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    get_network([74171270, 87393116])
    pass