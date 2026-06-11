import math
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

class MinHeap:
    """
    [Member 1] 우선순위 큐(Priority Queue) 작업을 위한 커스텀 최소 힙(Min-Heap) 구현.
    다익스트라 및 A* 알고리즘에서 최솟값(최중 비용 노드)을 O(log N)의 시간 복잡도로 추출하기 위해 사용.
    """
    def __init__(self):
        self.heap = []

    def push(self, element):
        """힙에 새로운 원소 (비용, 노드)를 추가"""
        self.heap.append(element)
        self._up_heap(len(self.heap) - 1)

    def pop(self):
        """힙에서 최솟값(루트 노드)을 제거하고 반환"""
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop() # 가장 마지막 원소를 루트로 이동 후 down-heap 수행
        self._down_heap(0)
        return root

    def is_empty(self):
        """힙이 비어있는지 확인"""
        return len(self.heap) == 0

    def _up_heap(self, index):
        """새로운 원소가 삽입되었을 때, 부모 노드와 비교하며 위로 재정렬 (Heapify-up)"""
        parent = (index - 1) // 2
        if index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._up_heap(parent)

    def _down_heap(self, index):
        """루트 원소가 삭제되었을 때, 자식 노드들과 비교하며 아래로 재정렬 (Heapify-down)"""
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
    [Member 1] 캠퍼스 맵을 표현하는 인접 리스트(Adjacency List) 기반 그래프 클래스.
    캠퍼스 맵처럼 노드 대비 간선 수가 적은 희소 그래프(Sparse Graph)에서 메모리 효율성을 극대화하기 위해 선택.
    """
    def __init__(self, json_data):
        self.graph = {}
        self.coordinates = {}
        self._load_data(json_data)

    def _load_data(self, json_data):
        """JSON 데이터로부터 건물(노드) 정보와 이웃 건물(간선 및 가중치), 좌표 데이터를 파싱"""
        for node, info in json_data["buildings"].items():
            self.graph[node] = info["neighbors"]
            self.coordinates[node] = info["coordinates"]

    def get_neighbors(self, node):
        """특정 건물과 연결된 이웃 건물 및 가중치(거리) 딕셔너리를 반환"""
        return self.graph.get(node, {})

    def get_coordinates(self, node):
        """특정 건물의 (X, Y) 절대 좌표를 반환 (A* 휴리스틱 계산용)"""
        return self.coordinates.get(node, [0, 0])


def dijkstra_search(campus_graph, start, end):
    """
    [Member 1] 다익스트라(Dijkstra) 최단 경로 탐색 알고리즘.
    가중치가 음수가 없는 그래프에서 출발지로부터 모든 노드까지의 최단 거리를 보장함.
    """
    # 모든 노드의 최단 거리를 무한대로 초기화
    distances = {node: float('inf') for node in campus_graph.graph}
    distances[start] = 0
    
    # 경로 역추적을 위한 이전 노드(부모 노드) 기록 테이블
    precursors = {node: None for node in campus_graph.graph}
    
    # 커스텀 최소 힙 가동 및 출발 노드 삽입
    pq = MinHeap()
    pq.push((0, start))

    while not pq.is_empty():
        current_distance, current_node = pq.pop()

        # 목적지에 도달한 경우 조기 종료 (탐색 최적화)
        if current_node == end:
            break

        # 힙에서 꺼낸 비용이 기존에 기록된 최단 거리보다 크다면 무시 (가져온 rác 처리)
        if current_distance > distances[current_node]:
            continue

        # 이웃 노드들을 순회하며 완화(Relaxation) 작업 수행
        for neighbor, weight in campus_graph.get_neighbors(current_node).items():
            distance = current_distance + weight
            # 더 짧은 경로를 발견한 경우 테이블 갱신 후 힙에 푸시
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                precursors[neighbor] = current_node
                pq.push((distance, neighbor))

    return _reconstruct_path(precursors, start, end), distances[end]


def a_star_search(campus_graph, start, end):
    """
    [Member 1] A* 탐색 알고리즘.
    실제 비용(G)과 목적지까지의 남은 예상 거리(H, 휴리스틱)를 결합한 총 예상 비용(F = G + H)을 사용하여
    목적지 방향으로 탐색을 집중시켜 다익스트라보다 빠른 속도로 최단 경로를 찾아냄.
    """
    def heuristic(node1, node2):
        """두 건물 간의 직선 거리를 계산하는 유클리드 거리(Euclidean Distance) 휴리스틱 함수"""
        c1 = campus_graph.get_coordinates(node1)
        c2 = campus_graph.get_coordinates(node2)
        return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

    # g_score: 출발지로부터 해당 노드까지의 실제 측정된 최단 거리
    g_score = {node: float('inf') for node in campus_graph.graph}
    g_score[start] = 0

    # f_score: 해당 노드를 거쳐 목적지까지 갈 때의 총 예상 비용 (F = G + H)
    f_score = {node: float('inf') for node in campus_graph.graph}
    f_score[start] = heuristic(start, end)

    precursors = {node: None for node in campus_graph.graph}

    pq = MinHeap()
    pq.push((f_score[start], start)) # A*는 f_score를 기준으로 우선순위 큐를 정렬함

    while not pq.is_empty():
        _, current_node = pq.pop()

        if current_node == end:
            break

        for neighbor, weight in campus_graph.get_neighbors(current_node).items():
            tentative_g_score = g_score[current_node] + weight
            
            # 더 인접한 탐색 경로를 발견한 경우 수치들 갱신
            if tentative_g_score < g_score[neighbor]:
                precursors[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                # F(n) = G(n) + H(n) 업데이트
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                pq.push((f_score[neighbor], neighbor))

    return _reconstruct_path(precursors, start, end), g_score[end]


def _reconstruct_path(precursors, start, end):
    """경로 역추적 헬퍼 함수: 목적지에서부터 출발지까지 부모 노드를 추적해 올라간 뒤 뒤집어서 정방향 경로 반환"""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = precursors[current]
    path.reverse()
    return path if path and path[0] == start else []

def render_navigation_tab(campus_graph):
    """
    [Member 1] streamlit-agraph 기반의 네비게이션 프리미엄 대시보드 화면 렌더링 함수.
    2컬럼 레이아웃을 채택하여 좌측에는 제어판(입력/결과 안내), 우측에는 인터랙티브 그래프 UI를 시각화.
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
                
                # 메트릭 대시보드 출력 섹션
                m1, m2 = st.columns(2)
                total_dist = cost * 80  # 가중치 단위를 도보 속도로 환산하는 도메인 로직 가중 처리
                m1.metric("Total Distance", f"{total_dist}m")
                m2.metric("Estimated Time", f"{cost} min")
                
                # 텍스트 형태의 Step-by-Step 턴바이턴 경로 가이드 제공
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
        # Agraph 네트워크 시각화 데이터 바인딩 파트
        nodes = []
        edges = []
        
        path_nodes = set(path)
        path_edges_set = set()
        if path:
            for i in range(len(path) - 1):
                path_edges_set.add(tuple(sorted((path[i], path[i+1]))))
        
        for node in campus_graph.graph:
            # --- 동적 스타일링 로직 (Dynamic Styling Logic) ---
            # 최단 경로 계산 결과에 포함된 노드들의 색상과 크기를 동적으로 변경하여 뷰포트에 하이라이트
            color = "#334155" # 기본 노드 색상: Slate Grey
            size = 18
            
            if path:
                if node == start_node:
                    color = "#F59E0B" # 출발지 노드: Amber Gold
                    size = 28
                elif node == end_node:
                    color = "#EF4444" # 목적지 노드: Red
                    size = 28
                elif node in path_nodes:
                    color = "#10B981" # 경로 상의 경유 노드: Emerald Green
                    size = 22
            
            nodes.append(Node(id=node, label=node, color=color, size=size))
            
        visited_edges = set()
        for u in campus_graph.graph:
            for v, w in campus_graph.get_neighbors(u).items():
                edge_key = tuple(sorted((u, v)))
                if edge_key not in visited_edges:
                    color = "#E2E8F0" # 기본 간선 색상
                    width = 2
                    
                    # 최단 경로 상에 존재하는 간선(Edge)을 굵은 녹색 선으로 변환
                    if edge_key in path_edges_set:
                        color = "#10B981" # 경로 간선: Emerald Green
                        width = 5
                    
                    edges.append(Edge(source=u, target=v, label=f"{w}m", color=color, width=width))
                    visited_edges.add(edge_key)

        config = Config(
            width="100%", 
            height=650, 
            directed=False, 
            physics=True, # 물리 시뮬레이션 기반 물리 배치 가동
            hierarchical=False,
            nodeHighlightBehavior=True,
            highlightColor="#F59E0B",
            collapsible=False
        )
        
        agraph(nodes=nodes, edges=edges, config=config)