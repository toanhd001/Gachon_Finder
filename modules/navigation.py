import math
import heapq

class MinHeap:
    """
    [Member 1] Custom Min-Heap implementation for priority queue operations.
    Used in Dijkstra and A* to extract the node with the minimum cost in O(log N).
    """
    def __init__(self):
        self.heap = []

    def push(self, element):
        """Adds a new element (cost, node) to the heap."""
        self.heap.append(element)
        self._up_heap(len(self.heap) - 1)

    def pop(self):
        """Removes and returns the minimum element from the heap."""
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._down_heap(0)
        return root

    def is_empty(self):
        """Returns True if the heap is empty."""
        return len(self.heap) == 0

    def _up_heap(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._up_heap(parent)

    def _down_heap(self, index):
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index

        if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left
        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._down_heap(smallest)


class CampusGraph:
    """
    [Member 1] Adjacency List Graph representing the campus map.
    Chosen for memory efficiency in sparse graphs like a campus layout.
    """
    def __init__(self, json_data):
        self.graph = {}
        self.coordinates = {}
        self._load_data(json_data)

    def _load_data(self, json_data):
        """Parses building and neighbor data from JSON."""
        for node, info in json_data["buildings"].items():
            self.graph[node] = info["neighbors"]
            self.coordinates[node] = info["coordinates"]

    def get_neighbors(self, node):
        """Returns a dictionary of neighbors and their weights for a given node."""
        return self.graph.get(node, {})

    def get_coordinates(self, node):
        """Returns the (x, y) coordinates of a node."""
        return self.coordinates.get(node, [0, 0])


def dijkstra_search(campus_graph, start, end):
    """
    [Member 1] Dijkstra's algorithm to find the shortest path between two nodes.
    Guarantees the shortest path in a graph with non-negative edge weights.
    """
    distances = {node: float('inf') for node in campus_graph.graph}
    distances[start] = 0
    
    precursors = {node: None for node in campus_graph.graph}
    
    pq = MinHeap()
    pq.push((0, start))

    while not pq.is_empty():
        current_distance, current_node = pq.pop()

        if current_node == end:
            break

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in campus_graph.get_neighbors(current_node).items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                precursors[neighbor] = current_node
                pq.push((distance, neighbor))

    return _reconstruct_path(precursors, start, end), distances[end]


def a_star_search(campus_graph, start, end):
    """
    [Member 1] A* search algorithm for faster pathfinding.
    Uses a heuristic (Euclidean distance) to prioritize exploration towards the goal.
    """
    def heuristic(node1, node2):
        # Euclidean distance formula: sqrt((x1-x2)^2 + (y1-y2)^2)
        c1 = campus_graph.get_coordinates(node1)
        c2 = campus_graph.get_coordinates(node2)
        return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

    g_score = {node: float('inf') for node in campus_graph.graph}
    g_score[start] = 0

    f_score = {node: float('inf') for node in campus_graph.graph}
    f_score[start] = heuristic(start, end)

    precursors = {node: None for node in campus_graph.graph}

    pq = MinHeap()
    pq.push((f_score[start], start))

    while not pq.is_empty():
        _, current_node = pq.pop()

        if current_node == end:
            break

        for neighbor, weight in campus_graph.get_neighbors(current_node).items():
            tentative_g_score = g_score[current_node] + weight
            if tentative_g_score < g_score[neighbor]:
                precursors[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                pq.push((f_score[neighbor], neighbor))

    return _reconstruct_path(precursors, start, end), g_score[end]


def _reconstruct_path(precursors, start, end):
    """Helper function to backtrack and build the path from search results."""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = precursors[current]
    path.reverse()
    return path if path and path[0] == start else []
