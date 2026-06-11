import streamlit as st
import json
import os
from modules.navigation import CampusGraph, render_navigation_tab
from modules.booking import RoomHashTable, BookingBST, quick_sort_rooms, binary_search_by_capacity, \
    filter_rooms_by_capacity, recommend_rooms
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
    st.header("Member 2 Classroom Operations Center")
    st.caption("Hash Table lookup, BST reservations, Quick Sort ranking, Binary Search, and room recommendation.")

    rooms = st.session_state.room_handler.values()
    sorted_rooms = quick_sort_rooms(rooms)
    capacities = [room["capacity"] for room in sorted_rooms]
    available_count = sum(1 for room in rooms if room["status"] == "Available")
    occupied_count = sum(1 for room in rooms if room["status"] == "Occupied")
    maintenance_count = sum(1 for room in rooms if room["status"] == "Maintenance")

    metric_cols = st.columns(4)
    metric_cols[0].metric("Total rooms", len(rooms))
    metric_cols[1].metric("Available", available_count)
    metric_cols[2].metric("Occupied", occupied_count)
    metric_cols[3].metric("Hash load factor", f"{st.session_state.room_handler.load_factor():.2f}")

    if maintenance_count:
        st.warning(f"{maintenance_count} room(s) are under maintenance and excluded from default recommendations.")

    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
        "Hash Lookup",
        "BST Booking",
        "Sort & Search",
        "Smart Filter"
    ])

    with sub_tab1:
        left, right = st.columns([1, 1.2])
        with left:
            st.subheader("O(1) classroom lookup")
            room_options = [room["room_id"] for room in sorted_rooms]
            room_id = st.selectbox("Room ID", room_options, index=0)
            if st.button("Lookup room in hash table", type="primary", use_container_width=True):
                room = st.session_state.room_handler.search(room_id)
                if room:
                    st.success(f"{room_id} found in the chaining hash table.")
                    st.json(room)
                else:
                    st.error("Room not found.")
        with right:
            st.subheader("Hash bucket diagnostics")
            st.caption("Shows how room IDs are distributed across chained buckets.")
            st.dataframe(st.session_state.room_handler.bucket_summary(), use_container_width=True, hide_index=True)

    with sub_tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Create or update reservation")
            st_id_in = st.number_input("Student ID", step=1, value=202000000)
            available_rooms = [room["room_id"] for room in sorted_rooms if room["status"] == "Available"]
            r_id_in = st.selectbox("Available room", available_rooms) if available_rooms else None
            if not available_rooms:
                st.warning("No rooms are currently available for booking.")
            if st.button("Confirm reservation", type="primary", use_container_width=True, disabled=not available_rooms):
                room = st.session_state.room_handler.search(r_id_in)
                if not room:
                    st.error("This room ID is not registered.")
                elif room["status"] != "Available":
                    st.error("This room is not available right now.")
                else:
                    st.session_state.booking_tree.insert(st_id_in, r_id_in)
                    st.session_state.room_handler.update_status(r_id_in, "Occupied")
                    st.success(f"Reservation saved in BST: {st_id_in} -> {r_id_in}")
                    st.rerun()
        with c2:
            st.subheader("Search reservation")
            st_id_out = st.number_input("Student ID to search", step=1, value=202000000)
            if st.button("Search BST", use_container_width=True):
                res = st.session_state.booking_tree.search(st_id_out)
                if res:
                    st.info(f"Student {st_id_out} currently reserved **{res.room_id}**.")
                else:
                    st.error("No reservation found.")

        st.subheader("BST in-order reservation table")
        reservation_rows = st.session_state.booking_tree.inorder()
        if reservation_rows:
            st.dataframe(reservation_rows, use_container_width=True, hide_index=True)
        else:
            st.info("No reservations yet. Add one above to see the BST traversal result.")

    with sub_tab3:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("Quick Sort by capacity")
            if st.button("Run Quick Sort", use_container_width=True):
                st.dataframe(sorted_rooms, use_container_width=True, hide_index=True)
        with c2:
            st.subheader("Binary Search exact capacity")
            target_cap = st.number_input("Capacity to find", step=5, value=60)
            if st.button("Run Binary Search", use_container_width=True):
                match = binary_search_by_capacity(sorted_rooms, target_cap)
                if match:
                    st.success(f"Match: {match['room_id']} ({match['capacity']} seats)")
                    st.json(match)
                else:
                    st.error("No classroom has exactly that capacity.")

        st.subheader("Smart room recommendation")
        buildings = ["Any"] + sorted({room["building"] for room in rooms})
        rec_cols = st.columns(3)
        needed_capacity = rec_cols[0].number_input("Minimum seats", min_value=1, value=45, step=5)
        preferred_building = rec_cols[1].selectbox("Preferred building", buildings)
        available_only = rec_cols[2].checkbox("Available only", value=True)

        recommendations = recommend_rooms(rooms, needed_capacity, preferred_building, available_only)
        if recommendations:
            st.dataframe(recommendations, use_container_width=True, hide_index=True)
            best = recommendations[0]
            st.success(
                f"Best match: {best['room_id']} with {best['capacity']} seats "
                f"({best['capacity_gap']} extra seats)."
            )
        else:
            st.warning("No room matches the selected recommendation filters.")

    with sub_tab4:
        st.subheader("Interactive classroom table")
        selected_capacity = st.slider(
            "Capacity range",
            min_value=min(capacities),
            max_value=max(capacities),
            value=(min(capacities), max(capacities)),
            step=5,
        )
        filtered_rooms = filter_rooms_by_capacity(sorted_rooms, selected_capacity[0], selected_capacity[1])

        status_filter = st.multiselect(
            "Status",
            ["Available", "Occupied", "Maintenance"],
            default=["Available", "Occupied", "Maintenance"],
        )
        filtered_rooms = [room for room in filtered_rooms if room["status"] in status_filter]

        st.metric("Matching rooms", len(filtered_rooms))
        st.dataframe(filtered_rooms, use_container_width=True, hide_index=True)

# =====================================================================
# TAB 3: Member 3 Logic (독립 모듈화 완료)
# =====================================================================
with tab3:
    render_barter_ui()
