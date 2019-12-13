from igraph import Graph, plot, drawing


g = Graph()
g.add_vertices(3)
g.add_edges([(0,2),(0,2), (2,0),])

plot(g)
    