# =====================================================================
# [Member 3] 자료구조: 우선순위 큐 (Priority Queue via Max-Heap)
# 선택 이유: 캠퍼스 내 정체나 사고 등 긴급도가 높은 상황을 우선적으로 처리하기 위함.
# =====================================================================
class EmergencyLog:
    def __init__(self, priority, description):
        self.priority = priority  # 숫자가 클수록 긴급도 높음
        self.description = description

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, log):
        # # 자료구조: 우선순위 큐 삽입
        self.heap.append(log)
        self._up_heap(len(self.heap) - 1)

    def pop(self):
        # # 자료구조: 우선순위 큐 추출
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
        if index > 0 and self.heap[index].priority > self.heap[parent].priority:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._up_heap(parent)

    def _down_heap(self, index):
        left = 2 * index + 1
        right = 2 * index + 2
        largest = index

        if left < len(self.heap) and self.heap[left].priority > self.heap[largest].priority:
            largest = left
        if right < len(self.heap) and self.heap[right].priority > self.heap[largest].priority:
            largest = right

        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self._down_heap(largest)


# =====================================================================
# [Member 3] 자료구조: 큐 (FIFO Queue)
# 선택 이유: 셔틀버스 탑승 대기열 등 선입선출 데이터 처리를 위함.
# =====================================================================
class InteractionQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return None

    def is_empty(self):
        return len(self.queue) == 0


# =====================================================================
# [Member 3] 알고리즘: 힙 정렬 (Heap Sort)
# 선택 이유: 내림차순으로 긴급 상황 로그를 정렬하여 최종 보고서를 출력하기 위함.
# =====================================================================
def heap_sort_logs(logs):
    # # 알고리즘: 힙 정렬
    pq = PriorityQueue()
    for log in logs:
        pq.push(log)
    
    sorted_logs = []
    while not pq.is_empty():
        sorted_logs.append(pq.pop())
    return sorted_logs


# =====================================================================
# [Member 3] 보조 자료구조: 서로소 집합 (Disjoint Set / Union-Find)
# 선택 이유: 크루스칼 알고리즘에서 사이클(Cycle) 형성 여부를 O(1)에 가깝게 판별하기 위함.
# =====================================================================
class DisjointSet:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, item):
        if self.parent[item] == item:
            return item
        self.parent[item] = self.find(self.parent[item])  # Path Compression
        return self.parent[item]

    def union(self, set1, set2):
        root1 = self.find(set1)
        root2 = self.find(set2)

        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1
            return True
        return False


# =====================================================================
# [Member 3] 알고리즘: 크루스칼 알고리즘 (Kruskal's MST Algorithm)
# 선택 이유: 순환 셔틀버스가 모든 주요 건물을 최소한의 비용(거리)으로 순회하는 최적 최단 망을 구축하기 위함.
# =====================================================================
def kruskal_mst(campus_graph):
    # # 알고리즘: 크루스칼 알고리즘
    edges = []
    # 중복 간선 제거하며 모든 간선 수집
    visited_edges = set()
    for u in campus_graph.graph:
        for v, weight in campus_graph.get_neighbors(u).items():
            if (v, u) not in visited_edges:
                edges.append((weight, u, v))
                visited_edges.add((u, v))

    # 간선들을 가중치(거리) 기준으로 오름차순 정렬 (Kruskal의 핵심)
    # Python built-in sort sử dụng Timsort (O(N log N))
    edges.sort(key=lambda x: x[0])

    ds = DisjointSet(campus_graph.graph.keys())
    mst = []
    total_cost = 0

    for weight, u, v in edges:
        # 사이클을 만들지 않는 경우에만 선택
        if ds.union(u, v):
            mst.append((u, v, weight))
            total_cost += weight

    return mst, total_cost