import streamlit as st
import json
import os
from modules.navigation import CampusGraph, dijkstra_search, a_star_search
from modules.booking import RoomHashTable, BookingBST, quick_sort_rooms, binary_search_by_capacity, filter_rooms_by_capacity
from modules.traffic import PriorityQueue, EmergencyLog, heap_sort_logs, kruskal_mst

# Môi trường chạy Web UI: Streamlit (요구사항 4번 - 실행 환경 명시)
st.set_page_config(page_title="Gachon Campus Finder", page_icon="🏫", layout="wide")

# 데이터 로드
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'data', 'campus_map.json'), 'r', encoding='utf-8') as f:
    map_data = json.load(f)
with open(os.path.join(BASE_DIR, 'data', 'facilities.json'), 'r', encoding='utf-8') as f:
    facility_data = json.load(f)

gachon_graph = CampusGraph(map_data)

# 해시 테이블 및 BST 전역 세션 유지 (Streamlit 특성 대응)
if 'room_handler' not in st.session_state:
    st.session_state.room_handler = RoomHashTable(size=10)
    for room in facility_data["rooms"]:
        st.session_state.room_handler.insert(room["room_id"], room)

if 'booking_tree' not in st.session_state:
    st.session_state.booking_tree = BookingBST()

if 'emergency_records' not in st.session_state:
    st.session_state.emergency_records = []

# Title
st.title("🏫 Gachon Campus Path & Resource Finder Pro")
st.caption("2026 알고리즘 기말 프로젝트 결과물 - 각 멤버별 독립 모듈화 구현")

tab1, tab2, tab3 = st.tabs([
    "📍 [Member 1] 내비게이션 (Graph/Dijkstra/A*)", 
    "🔑 [Member 2] 강의실 관리 (Hash/BST/Sort)", 
    "🚨 [Member 3] 관제 시스템 (PQ/HeapSort/Kruskal)"
])

# =====================================================================
# TAB 1: Member 1 Logic 
# =====================================================================
with tab1:
    st.header("캠퍼스 최단 경로 탐색 및 시각화 시스템")
    buildings = list(gachon_graph.graph.keys())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        start = st.selectbox("출발지 선택", buildings, key="start")
    with col2:
        end = st.selectbox("목적지 선택", buildings, key="end")
    with col3:
        algo = st.radio("알고리즘 선택", ["Dijkstra", "A* Search"])

    path, cost = [], 0
    if st.button("경로 탐색 및 그래프 시각화 실행", type="primary"):
        if start == end:
            st.warning("출발지와 목적지가 같습니다.")
        else:
            # # 최단경로탐색 알고리즘 호출
            if algo == "Dijkstra":
                path, cost = dijkstra_search(gachon_graph, start, end)
            else:
                path, cost = a_star_search(gachon_graph, start, end)
            
            st.success(f"🏁 탐색 완료! 총 소요시간: **{cost}분**")
            st.info(f"🛣️ **추천 경로:** {' ➔ '.join(path)}")

    st.markdown("---")
    st.subheader("📊 가천대학교 캠퍼스 맵 토폴로지 시각화")
    st.caption("레드 라인: 알고리즘이 연산한 최적 최단 경로 (Green: 출발지, Orange: 도착지)")

    # Graphviz를 이용한 동적 DOT 스크립트 생성 (정적 라이브러리 미사용)
    dot_src = "digraph G {\n"
    dot_src += '  graph [rankdir=LR, bgcolor="#F9F9F9"];\n'
    dot_src += '  node [fontname="Malgun Gothic", shape=circle, style="filled", width=1.2, fixedsize=true];\n'
    dot_src += '  edge [fontname="Malgun Gothic", fontsize=10, len=2.0];\n'

    path_set = set(path) if path else set()
    
    # 1. 노드 스타일링 (출발/도착/경로/일반 구분)
    for node in gachon_graph.graph:
        if path and node == start:
            dot_src += f'  "{node}" [fillcolor="#2ECC71", fontcolor="white", color="#27AE60", penwidth=3];\n'
        elif path and node == end:
            dot_src += f'  "{node}" [fillcolor="#E67E22", fontcolor="white", color="#D35400", penwidth=3];\n'
        elif node in path_set:
            dot_src += f'  "{node}" [fillcolor="#F1C40F", fontcolor="black", color="#F39C12", penwidth=2];\n'
        else:
            dot_src += f'  "{node}" [fillcolor="#ECF0F1", fontcolor="#2C3E50", color="#BDC3C7"];\n'

    # 2. 간선 스타일링 및 가중치 표시 (최단 경로 무방향 연동 그래프 생성)
    visited_edges = set()
    for u in gachon_graph.graph:
        for v, w in gachon_graph.get_neighbors(u).items():
            if (v, u) not in visited_edges:
                # 현재 간선이 최단 경로 내에 포함되는지 검증
                is_path_edge = False
                if path:
                    for i in range(len(path) - 1):
                        if (path[i] == u and path[i+1] == v) or (path[i] == v and path[i+1] == u):
                            is_path_edge = True
                            break
                
                if is_path_edge:
                    dot_src += f'  "{u}" -> "{v}" [label="{w}분", color="#E74C3C", penwidth=4, dir=none];\n'
                else:
                    dot_src += f'  "{u}" -> "{v}" [label="{w}분", color="#BDC3C7", style="dashed", dir=none];\n'
                visited_edges.add((u, v))

    dot_src += "}"
    
    # 렌더링 엔진 구동
    st.graphviz_chart(dot_src)

    # =====================================================================
    # [Member 1 New Feature] 상세 길찾기 가이드 (Step-by-Step Table)
    # =====================================================================
    if path:
        st.markdown("---")
        st.subheader("📋 상세 경로 안내 (Step-by-Step Guide)")
        
        directions = []
        total_time = 0
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            weight = gachon_graph.get_neighbors(u).get(v, 0)
            total_time += weight
            directions.append({
                "순서": i + 1,
                "출발": u,
                "도착": v,
                "소요 시간": f"{weight}분",
                "누적 시간": f"{total_time}분"
            })
        
        st.table(directions)
        st.info(f"💡 **팁:** {start}에서 {end}까지 총 {len(path)}개의 지점을 거쳐 이동하며, 예상 소요 시간은 {cost}분입니다.")

# =====================================================================
# TAB 2: Member 2 Logic
# =====================================================================
with tab2:
    st.header("강의실 실시간 상태 및 예약 시스템")
    
    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs(["해시 테이블 조회", "BST 학번 예약", "정렬 및 이진 탐색", "Classroom Filter"])
    
    with sub_tab1:
        room_id = st.text_input("조회할 강의실 ID 입력 (예: AI-401, GH-101)").strip()
        if st.button("실시간 상태 조회 (O(1))"):
            # # 자료구조: 해시 테이블 검색
            room = st.session_state.room_handler.search(room_id)
            if room:
                st.json(room)
            else:
                st.error("등록되지 않은 강의실입니다.")
                
    with sub_tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("예약 등록")
            st_id_in = st.number_input("학번 입력 (등록)", step=1, value=202000000)
            r_id_in = st.text_input("예약할 강의실 ID")
            if st.button("예약 확정"):
                st.session_state.booking_tree.insert(st_id_in, r_id_in)
                st.success("BST에 예약 노드가 삽입되었습니다.")
        with c2:
            st.subheader("예약 조회")
            st_id_out = st.number_input("조회할 학번 입력", step=1, value=202000000)
            if st.button("조회 실행"):
                # # 자료구조: 이진 탐색 트리 검색
                res = st.session_state.booking_tree.search(st_id_out)
                if res:
                    st.info(f"🔍 학번 {st_id_out}님은 현재 **{res.room_id}** 강의실 예약 상태입니다.")
                else:
                    st.error("예약 내역이 없습니다.")

    with sub_tab3:
        if st.button("수용 인원 기준 퀵 정렬(Quick Sort) 실행"):
            # # 알고리즘: 퀵 정렬
            sorted_rooms = quick_sort_rooms(facility_data["rooms"])
            st.write("📊 정렬 결과 (오름차순):")
            st.dataframe(sorted_rooms)
            
        target_cap = st.number_input("이진 탐색(Binary Search)할 정확한 수용 인원 설정", step=10, value=60)
        if st.button("이진 탐색 시작"):
            sorted_rooms = quick_sort_rooms(facility_data["rooms"])
            # # 알고리즘: 이진 탐색
            match = binary_search_by_capacity(sorted_rooms, target_cap)
            if match:
                st.success(f"🎯 매칭 성공: {match['room_id']} (수용인원: {match['capacity']}명)")
            else:
                st.error("해당 수용 인원을 가진 강의실이 없습니다.")

    with sub_tab4:
        st.subheader("Interactive Classroom Data Table")
        sorted_rooms = quick_sort_rooms(facility_data["rooms"])
        capacities = [room["capacity"] for room in sorted_rooms]
        min_capacity = min(capacities)
        max_capacity = max(capacities)
        selected_capacity = st.slider(
            "Capacity range",
            min_value=min_capacity,
            max_value=max_capacity,
            value=(min_capacity, max_capacity),
            step=10,
        )
        filtered_rooms = filter_rooms_by_capacity(
            sorted_rooms,
            selected_capacity[0],
            selected_capacity[1],
        )

        available_only = st.checkbox("Show available rooms only")
        if available_only:
            filtered_rooms = [
                room for room in filtered_rooms
                if room["status"] == "Available"
            ]

        st.metric("Matching rooms", len(filtered_rooms))
        st.dataframe(filtered_rooms, use_container_width=True)

# =====================================================================
# TAB 3: Member 3 Logic
# =====================================================================
with tab3:
    st.header("캠퍼스 교통 제어 및 셔틀 노선 최적화")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("실시간 긴급 제보 (우선순위 큐 작동)")
        if st.button("의사 데이터 시뮬레이션 삽입"):
            pq = PriorityQueue()
            pq.push(EmergencyLog(3, "AI관 앞 셔틀버스 대기 정체 심화"))
            pq.push(EmergencyLog(5, "가천관 내부 엘리베이터 고장 고립 사고"))
            pq.push(EmergencyLog(1, "운동장 물품 분실 신고"))
            
            st.session_state.emergency_records = []
            st.write("📥 **우선순위 큐(Max-Heap)로부터 순차적 추출 결과:**")
            while not pq.is_empty():
                log = pq.pop()
                st.warning(f"🚨 [위험도 {log.priority}] {log.description}")
                st.session_state.emergency_records.append(log)
                
    with c2:
        st.subheader("위험도 순 정렬 보고서 (Heap Sort)")
        if st.button("힙 정렬 실행"):
            if not st.session_state.emergency_records:
                st.error("왼쪽 메뉴에서 시뮬레이션 데이터를 먼저 삽입하세요.")
            else:
                # # 알고리즘: 힙 정렬
                sorted_logs = heap_sort_logs(st.session_state.emergency_records)
                for log in sorted_logs:
                    st.code(f"[위험도 {log.priority}] {log.description}")

    st.markdown("---")
    st.subheader("🚌 크루스칼(Kruskal) 알고리즘 기반 순환 셔틀버스 최적 노선망 설계")
    if st.button("MST(최소 신장 트리) 계산"):
        # # 알고리즘: 크루스칼 알고리즘
        mst, total_cost = kruskal_mst(gachon_graph)
        st.success(f"📊 캠퍼스 전체 순회 최소 가중치: **{total_cost}분**")
        for edge in mst:
            st.write(f"🔗 연결 노선: `{edge[0]}` ➔ `{edge[1]}` (구간 소요: {edge[2]}분)")
