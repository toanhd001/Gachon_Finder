import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


# ==========================================
# 0. HÀM CALLBACK (CHUYỂN TRANG MƯỢT MÀ, KHÔNG LỖI)
# ==========================================
def connect_action(book_name):
    # Hàm này chạy NGAY LẬP TỨC khi bấm nút "Kết nối" (Trước khi web load lại)
    st.session_state.target_book = book_name
    st.session_state.run_matching = True
    st.session_state.active_tab = "⚡ 2. Khớp Lệnh Thông Minh (DFS)"


def reset_action():
    # Hàm này chạy khi bấm nút quay lại
    st.session_state.run_matching = False
    st.session_state.active_tab = "🛒 1. Chợ Giáo Trình (KMP Search)"


# ==========================================
# 1. THUẬT TOÁN (CORE ALGORITHMS)
# ==========================================
def find_barter_cycles(data):
    graph = {u: [] for u in data}
    for u in data:
        for v in data:
            if u != v and data[u]["has"] == data[v]["wants"]:
                graph[u].append(v)

    G = nx.DiGraph(graph)
    try:
        cycles = list(nx.simple_cycles(G))
        return [c for c in cycles if len(c) >= 2], graph
    except:
        return [], graph


# ==========================================
# 2. GIAO DIỆN (UI) & KHỞI TẠO DỮ LIỆU
# ==========================================
def render_barter_ui():
    if 'students_data' not in st.session_state:
        st.session_state.students_data = {
            "김민준": {"has": "쉽게 배우는 알고리즘", "wants": "데이터베이스 시스템", "desc": "상태 아주 좋음"},
            "박서윤": {"has": "데이터베이스 시스템", "wants": "컴퓨터 네트워크", "desc": "필기 조금 있음"},
            "이도현": {"has": "컴퓨터 네트워크", "wants": "쉽게 배우는 알고리즘", "desc": "새책 수준"},
            "최하은": {"has": "자료구조와 파이썬", "wants": "포인트 (Point)", "desc": "2025년판"},
            "정지훈": {"has": "포인트 (Point)", "wants": "자료구조와 파이썬", "desc": "즉시 거래 가능"},
            "강수아": {"has": "인공지능 입문", "wants": "운영체제 공룡책", "desc": "상태 보통"},
            "한예은": {"has": "운영체제 공룡책", "wants": "자바 프로그래밍", "desc": "깨끗함"},
            "윤시우": {"has": "자바 프로그래밍", "wants": "인공지능 입문", "desc": "커피 자국 약간 있음"},
            "임서아": {"has": "소프트웨어 공학", "wants": "포인트 (Point)", "desc": "거의 안 봄"},
            "오지훈": {"has": "웹 프로그래밍", "wants": "소프트웨어 공학", "desc": "상태 좋음"},
            "서유빈": {"has": "포인트 (Point)", "wants": "웹 프로그래밍", "desc": "빠른 거래 원함"},
            "김도윤": {"has": "회계원리", "wants": "마케팅의 이해", "desc": "필기 많음"},
            "이채원": {"has": "마케팅의 이해", "wants": "거시경제학", "desc": "상태 좋음"},
            "정우진": {"has": "거시경제학", "wants": "회계원리", "desc": "새책"},
            "조민지": {"has": "경영통계학", "wants": "포인트 (Point)", "desc": "연습문제 풀이 있음"},
            "강태오": {"has": "포인트 (Point)", "wants": "경영통계학", "desc": "상태 좋음"},
            "박하윤": {"has": "해부학 기초", "wants": "간호학 개론", "desc": "상태 좋음"},
            "신지호": {"has": "간호학 개론", "wants": "병리학", "desc": "표지 약간 찢어짐"},
            "권아린": {"has": "병리학", "wants": "해부학 기초", "desc": "새책"},
            "서은우": {"has": "약리학 기초", "wants": "포인트 (Point)", "desc": "2024년판"},
            "문서준": {"has": "포인트 (Point)", "wants": "약리학 기초", "desc": "필기 꼼꼼함"},
            "백예준": {"has": "색채학", "wants": "시각디자인론", "desc": "상태 좋음"},
            "김지안": {"has": "시각디자인론", "wants": "디자인 씽킹", "desc": "사용감 있음"},
            "송도윤": {"has": "디자인 씽킹", "wants": "색채학", "desc": "새책"},
            "장하은": {"has": "기초 조형", "wants": "포인트 (Point)", "desc": "실습 위주"},
            "류건우": {"has": "포인트 (Point)", "wants": "기초 조형", "desc": "상태 좋음"},
            "배수민": {"has": "클라우드 컴퓨팅", "wants": "사이버 보안론", "desc": "새책"},
            "홍준혁": {"has": "사이버 보안론", "wants": "클라우드 컴퓨팅", "desc": "상태 좋음"},
            "최다은": {"has": "데이터 마이닝", "wants": "포인트 (Point)", "desc": "2025 최신판"},
            "강민우": {"has": "포인트 (Point)", "wants": "데이터 마이닝", "desc": "즉시 거래"}
        }
    if 'run_matching' not in st.session_state:
        st.session_state.run_matching = False
    if 'target_book' not in st.session_state:
        st.session_state.target_book = ""
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "🛒 1. Chợ Giáo Trình (KMP Search)"

    st.header("🔄 Gachon Smart Book Ecosystem")
    st.caption("IT 학과 전용 교재 물물교환 시스템 | KMP Search · DFS Cycle Detection")

    # --- MENU ĐIỀU HƯỚNG ---
    st.radio(
        "Menu Điều Hướng",
        ["🛒 1. Chợ Giáo Trình (KMP Search)", "⚡ 2. Khớp Lệnh Thông Minh (DFS)", "💳 3. Ví Điểm / Thanh Khoản"],
        horizontal=True,
        key="active_tab",
        label_visibility="collapsed"
    )

    # ==========================================
    # TAB 1: Tìm kiếm & Đăng ký
    # ==========================================
    if st.session_state.active_tab == "🛒 1. Chợ Giáo Trình (KMP Search)":
        st.subheader("🛒 Chợ Giáo Trình Gachon")

        with st.expander("➕ Đăng ký Sách Mới (Cung cấp sách của bạn để hệ thống nối vòng)", expanded=False):
            with st.form("add_book_form"):
                st.info(
                    "Ví dụ: Bạn cần 'Cấu trúc dữ liệu' nhưng người bán lại cần 'Toán'. Hãy đăng ký cuốn sách bạn đang có để hệ thống tự tìm người thứ 3 ghép nối!")
                user_name = st.text_input("Tên sinh viên")
                col_h, col_w = st.columns(2)
                has_book = col_h.text_input("Sách bạn đang CÓ")
                want_book = col_w.text_input("Sách bạn đang CẦN")
                desc = st.text_area("Tình trạng sách")

                if st.form_submit_button("Đăng lên hệ thống", type="primary"):
                    if user_name and has_book and want_book:
                        st.session_state.students_data[user_name] = {"has": has_book, "wants": want_book, "desc": desc}
                        st.success(f"Đã đăng ký thành công! Hệ thống đã ghi nhận bạn có {has_book}.")
                        st.rerun()

        st.divider()
        search_query = st.text_input("🔍 Nhập tên sách để tìm kiếm (KMP Search):", placeholder="Ví dụ: 운영체제 공룡책")

        df = pd.DataFrame(
            [{"Sinh viên": k, "Có": v["has"], "Cần": v["wants"]} for k, v in st.session_state.students_data.items()])
        if search_query:
            df = df[df["Có"].str.contains(search_query, case=False) | df["Cần"].str.contains(search_query, case=False)]

        for idx, row in df.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                col1.write(f"**📖 {row['Có']}** (Cần: {row['Cần']})")

                # SỬ DỤNG ON_CLICK ĐỂ CHUYỂN TRANG KHÔNG BỊ LỖI
                col2.button("Kết nối ngay", key=f"btn_{idx}", on_click=connect_action, args=(row['Có'],))

    # ==========================================
    # TAB 2: Khớp lệnh
    # ==========================================
    elif st.session_state.active_tab == "⚡ 2. Khớp Lệnh Thông Minh (DFS)":
        st.subheader("⚡ Hệ thống Khớp Lệnh (Smart Match)")
        if st.session_state.run_matching:
            st.info(f"Đang tìm kiếm mạng lưới trao đổi cho sách: **{st.session_state.target_book}**")
            cycles, graph = find_barter_cycles(st.session_state.students_data)

            # Lọc các chu trình có chứa cuốn sách mục tiêu
            matched = [c for c in cycles if
                       any(st.session_state.students_data[s]['has'] == st.session_state.target_book for s in c)]

            if matched:
                # --- ÁP DỤNG GREEDY: SẮP XẾP VÀ LỌC TOP 5 NGẮN NHẤT ---
                matched.sort(key=len)  # Sắp xếp chu trình theo số lượng người (ít nhất lên đầu)
                top_5_matches = matched[:5]  # Chỉ lấy 5 mạng lưới tối ưu nhất

                st.success(f"🎉 Đã tìm ra {len(top_5_matches)} mạng lưới tối ưu nhất (ít trung gian nhất)!")

                # --- CHIA LÀM 2 CỘT: Trái (Chữ) - Phải (Hình) ---
                col_text, col_graph = st.columns([1.2, 1])

                with col_text:
                    for i, cycle in enumerate(top_5_matches):
                        st.markdown(f"**Top {i + 1} (Chu trình {len(cycle)} người):**")
                        path = " ➔ ".join(cycle) + f" ➔ {cycle[0]}"
                        st.code(path)

                with col_graph:
                    st.markdown("#### 🗺️ Sơ đồ Top 1")
                    try:
                        best_cycle = top_5_matches[0]
                        cycle_graph = nx.DiGraph()

                        for j in range(len(best_cycle)):
                            u = best_cycle[j]
                            v = best_cycle[(j + 1) % len(best_cycle)]
                            cycle_graph.add_edge(u, v)

                        # Thu nhỏ kích thước khung hình xuống còn (3, 3)
                        fig, ax = plt.subplots(figsize=(3, 3))
                        pos = nx.circular_layout(cycle_graph)

                        plt.rcParams['font.family'] = 'Malgun Gothic'
                        plt.rcParams['axes.unicode_minus'] = False

                        # Thu nhỏ node_size và font_size để vừa vặn, dùng draw_networkx
                        nx.draw_networkx(cycle_graph, pos, with_labels=True, node_color='#74b9ff',
                                         edge_color='#ff7675', node_size=1000, font_size=8,
                                         font_weight='bold', font_family='Malgun Gothic', ax=ax, arrows=True,
                                         arrowsize=15)

                        # Thêm khoảng trống lề (margin) để bong bóng không bị cắt lẹm ở rìa
                        ax.margins(0.3)
                        ax.axis('off')

                        # Hiển thị biểu đồ
                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"Lỗi hiển thị đồ thị mạng lưới: {e}")
            else:
                st.error("⚠️ Không tìm thấy mạng lưới trao đổi khép kín trong kho sách hiện tại.")
                st.write(
                    "Đề xuất: Bạn có thể thêm sách mình đang có vào **Tab 1** để mở rộng mạng lưới, hoặc mua sách mới tại đây:")
                col_btn1, col_btn2 = st.columns(2)
                col_btn1.link_button("🛒 Mua tại Coupang", "https://www.coupang.com/")
                col_btn2.link_button("📚 Nhà sách trường", "https://gachon.ac.kr/")

            # Nút quay lại Tab 1
            st.button("Xóa tìm kiếm / Quay lại", on_click=reset_action)
        else:
            st.write("Hãy quay lại Tab 1 chọn sách để bắt đầu khớp lệnh.")

    # ==========================================
    # TAB 3: Ví điểm
    # ==========================================
    elif st.session_state.active_tab == "💳 3. Ví Điểm / Thanh Khoản":
        st.subheader("💳 Ví Điểm (Exit Strategy)")
        st.metric("Số dư hiện tại", "45,000 P")
        st.selectbox("Chọn cửa hàng", ["Căn tin Tòa Gachon", "Cửa hàng tiện lợi CU"])
        st.button("Thanh toán bữa ăn bằng điểm")