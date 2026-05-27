import math

# =====================================================================
# [Member 1] 자료구조: 최소 힙 (Min-Heap)
# 선택 이유: 다익스트라 알고리즘에서 최단 거리 정점을 O(log N)만에 추출하기 위함.
# =====================================================================
class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, element):
        # element format: (cost, node)
        self.heap.append(element)
        self._up_heap(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._down_heap(0)
        return root

    def is_empty(self):
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


# =====================================================================
# [Member 1] 자료구조: 인접 리스트 그래프 (Adjacency List Graph)
# 선택 이유: 캠퍼스 맵은 간선이 적은 희소 그래프이므로 메모리 절약을 위해 인접 리스트 채택.
# =====================================================================
class CampusGraph:
    def __init__(self, json_data):
        self.graph = {}
        self.coordinates = {}
        self._load_data(json_data)

    def _load_data(self, json_data):
        for node, info in json_data["buildings"].items():
            self.graph[node] = info["neighbors"]
            self.coordinates[node] = info["coordinates"]

    def get_neighbors(self, node):
        return self.graph.get(node, {})

    def get_coordinates(self, node):
        return self.coordinates.get(node, [0, 0])


# =====================================================================
# [Member 1] 알고리즘: 다익스트라 최단 경로 탐색 (Dijkstra Algorithm)
# =====================================================================
def dijkstra_search(campus_graph, start, end):
    # # 최단경로탐색: 다익스트라 알고리즘
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


# =====================================================================
# [Member 1] 알고리즘: A* 탐색 알고리즘 (A* Search Algorithm)
# 선택 이유: 휴리스틱(유클리드 거리)을 도입하여 목적지 방향의 노드를 우선 탐색, 속도 최적화.
# =====================================================================
def a_star_search(campus_graph, start, end):
    # # 최단경로탐색: A* 알고리즘
    def heuristic(node1, node2):
        # 유클리드 거리 계산 수식: $h(n) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$
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
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = precursors[current]
    path.reverse()
    return path if path[0] == start else []