from collections import deque
from heapq import heappush, heappop 

def shortest_shortest_path(graph, source):
    """
    Params: 
      graph.....a graph represented as a dict where each key is a vertex
                and the value is a set of (vertex, weight) tuples (as in the test case)
      source....the source node
      
    Returns:
      a dict where each key is a vertex and the value is a tuple of
      (shortest path weight, shortest path number of edges). See test case for example.
    """
  
    def shortest_shortest_path_helper(visited, frontier):
        if len(frontier) == 0:
            return visited
        else:
            # Pick next closest node from heap
            distance, edges, node = heappop(frontier)
            print('visiting', node)
            if node in visited:
                # Same distance but smaller amount of edges
                if distance == visited[node][0] and edges < visited[node][1]:
                    visited[node] = (distance, edges)
                # Already visited, so ignore this longer path
                return shortest_shortest_path_helper(visited, frontier)
            else:
                # We now know the shortest path from source to node.
                # insert into visited dict.
                visited[node] = (distance, edges)
                print('...distance=', distance)
                # Visit each neighbor of node and insert into heap.
                # We may add same node more than once, heap
                # will keep shortest distance prioritized.
                for neighbor, weight in graph[node]:
                    heappush(frontier, (distance + weight, edges + 1, neighbor))
                return shortest_shortest_path_helper(visited, frontier)
  
    frontier = []
    heappush(frontier, (0, 0, source))
    visited = dict()  # store the final shortest paths for each node.
    return shortest_shortest_path_helper(visited, frontier)
    
    
def test_shortest_shortest_path():

    graph = {
                's': {('a', 1), ('c', 4)},
                'a': {('b', 2)}, # 'a': {'b'},
                'b': {('c', 1), ('d', 4)}, 
                'c': {('d', 3)},
                'd': {},
                'e': {('d', 0)}
            }
    result = shortest_shortest_path(graph, 's')
    # result has both the weight and number of edges in the shortest shortest path
    assert result['s'] == (0,0)
    assert result['a'] == (1,1)
    assert result['b'] == (3,2)
    assert result['c'] == (4,1)
    assert result['d'] == (7,2)
    
    
def bfs_path(graph, source):
    """
    Returns:
      a dict where each key is a vertex and the value is the parent of 
      that vertex in the shortest path tree.
    """
    def bfs_path_helper(visited, frontier):
        if len(frontier) == 0:
            return visited
        else:
            ## pick a node
            node = frontier.popleft()
            print('visiting', node)
            
            ## update visited set
            visited.add(node)
            
            ## update frontier set
            for n in graph[node]:
                if n not in visited:
                    frontier.extend(n)
                if n not in parents.keys():
                    parents[n] = node
            
            return bfs_path_helper(visited, frontier)
        
    frontier = deque()
    frontier.append(source)
    visited = set()
    parents = dict()
    bfs_path_helper(visited, frontier)
    return parents


def get_sample_graph():
     return {'s': {'a', 'b'},
            'a': {'b'},
            'b': {'c'},
            'c': {'a', 'd'},
            'd': {}
            }

def test_bfs_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert parents['a'] == 's'
    assert parents['b'] == 's'    
    assert parents['c'] == 'b'
    assert parents['d'] == 'c'
    
def get_path(parents, destination):
    """
    Returns:
      The shortest path from the source node to this destination node 
      (excluding the destination node itself). See test_get_path for an example.
    """
    path = []
    parent = parents[destination]
    while (parent in parents):
      path.append(parent)
      parent = parents[parent]
    path.append(parent)
    path.reverse()

    path_string = ""
    for node in path:
        path_string += node
      
    return path_string

def test_get_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert get_path(parents, 'd') == 'sbc'


# Extra tests
graph1 = {
                's': {('a', 1), ('c', 4)},
                'a': {('b', 2)}, # 'a': {'b'},
                'b': {('c', 1), ('d', 4)}, 
                'c': {('d', 3)},
                'd': {},
                'e': {('d', 0)}
            }
print(shortest_shortest_path(graph1, 's'))

graph2 = {'s': {'a', 'b'},
            'a': {'b'},
            'b': {'c'},
            'c': {'a', 'd'},
            'd': {}
            }

print(bfs_path(graph2, 's'))

parents = {'a': 's', 'b': 's', 'c': 'b', 'd': 'c'}
print(get_path(parents, 'd'))