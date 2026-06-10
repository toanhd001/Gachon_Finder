import streamlit as st
import json
import os
from modules.navigation import CampusGraph, render_navigation_tab
from modules.booking import RoomHashTable, BookingBST, quick_sort_rooms, binary_search_by_capacity, \
    filter_rooms_by_capacity
from modules.book_exchange import render_barter_ui

# 실행 환경: Streamlit 웹 UI (요구사항 4번 - 실행 환경 명시)
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

# Title
st.title("🏫 Gachon Campus Path & Resource Finder Pro")
st.caption("2026 알고리즘 기말 프로젝트 결과물 - 각 멤버별 독립 모듈화 구현")

# 멤버 3의 알고리즘 명칭을 실제 구현된 KMP로 수정
tab1, tab2, tab3 = st.tabs([
    "📍 [Member 1] 내비게이션 (Graph/Dijkstra/A*)",
    "🔑 [Member 2] 강의실 관리 (Hash/BST/Sort)",
    "🚨 [Member 3] 스마트 교재 물물교환 에코시스템 (DFS/Greedy/KMP)"
])

# =====================================================================
# TAB 1: Member 1 Logic
# =====================================================================
with tab1:
    render_navigation_tab(gachon_graph)

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
# TAB 3: Member 3 Logic (독립 모듈화 완료)
# =====================================================================
with tab3:
    render_barter_ui()