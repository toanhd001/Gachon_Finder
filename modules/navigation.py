import math
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

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

def render_navigation_tab(campus_graph):
    """
    [Member 1] Premium Navigation Dashboard using streamlit-agraph.
    Implements a 2-column layout with interactive graph visualization.
    """
    st.header("📍 캠퍼스 최단 경로 탐색 Pro")
    buildings = list(campus_graph.graph.keys())
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.subheader("탐색 설정")
        start_node = st.selectbox("출발지 선택", buildings, key="nav_start")
        end_node = st.selectbox("목적지 선택", buildings, key="nav_end")
        algo = st.radio("알고리즘 선택", ["Dijkstra", "A* Search"], horizontal=True)
        
        execute = st.button("🚀 경로 탐색 실행", type="primary", use_container_width=True)
        
        path, cost = [], 0
        if execute:
            if start_node == end_node:
                st.warning("⚠️ 출발지와 목적지가 같습니다.")
            else:
                if algo == "Dijkstra":
                    path, cost = dijkstra_search(campus_graph, start_node, end_node)
                else:
                    path, cost = a_star_search(campus_graph, start_node, end_node)
                
                # Metrics Section
                m1, m2 = st.columns(2)
                total_dist = cost * 80  # Assume 80m per minute walking speed
                m1.metric("Total Distance", f"{total_dist}m")
                m2.metric("Estimated Time", f"{cost} min")
                
                # Step-by-Step Guide
                st.markdown("---")
                with st.container():
                    st.markdown("### 🗺️ Route Guide")
                    with st.expander("상세 경로 안내 (Step-by-Step)", expanded=True):
                        for i in range(len(path) - 1):
                            u, v = path[i], path[i+1]
                            w = campus_graph.get_neighbors(u).get(v, 0)
                            st.write(f"🚶 **{u}** ➔ **{v}** ({w}m)")
                        st.success(f"🏁 **{end_node}** 도착 완료!")

    with col2:
        # Agraph Visualization
        nodes = []
        edges = []
        
        path_nodes = set(path)
        path_edges_set = set()
        if path:
            for i in range(len(path) - 1):
                path_edges_set.add(tuple(sorted((path[i], path[i+1]))))
        
        for node in campus_graph.graph:
            # Dynamic Styling Logic
            color = "#334155" # Default: Slate Grey
            size = 18
            
            if path:
                if node == start_node:
                    color = "#F59E0B" # Start: Amber Gold
                    size = 28
                elif node == end_node:
                    color = "#EF4444" # Destination: Red
                    size = 28
                elif node in path_nodes:
                    color = "#10B981" # Path nodes: Emerald Green
                    size = 22
            
            nodes.append(Node(id=node, label=node, color=color, size=size))
            
        visited_edges = set()
        for u in campus_graph.graph:
            for v, w in campus_graph.get_neighbors(u).items():
                edge_key = tuple(sorted((u, v)))
                if edge_key not in visited_edges:
                    color = "#E2E8F0" # Default Edge
                    width = 2
                    
                    if edge_key in path_edges_set:
                        color = "#10B981" # Path Edge: Emerald Green
                        width = 5
                    
                    edges.append(Edge(source=u, target=v, label=f"{w}m", color=color, width=width))
                    visited_edges.add(edge_key)

        config = Config(
            width="100%", 
            height=650, 
            directed=False, 
            physics=True, 
            hierarchical=False,
            nodeHighlightBehavior=True,
            highlightColor="#F59E0B",
            collapsible=False
        )
        
        agraph(nodes=nodes, edges=edges, config=config)
