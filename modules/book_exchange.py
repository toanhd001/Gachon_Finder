import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


# ==========================================
# [프로그램 완성코드 필수 기재 사항]
# 1. 실행 환경: Streamlit 웹 애플리케이션 (Python 3.9+)
# 2. 필수 라이브러리: streamlit, pandas, networkx, matplotlib
# 3. Input 데이터: 가천대학교 IT학과 학생들의 가상 교재 물물교환 데이터 (자체 제작)
# ==========================================

# ==========================================
# 0. 콜백 함수 (화면 전환 및 상태 관리)
# ==========================================
def connect_action(book_name):
    st.session_state.target_book = book_name
    st.session_state.run_matching = True
    st.session_state.active_tab = "⚡ 2. 스마트 매칭 (DFS)"


def reset_action():
    st.session_state.run_matching = False
    st.session_state.active_tab = "🛒 1. 교재 장터 (KMP Search)"


# ==========================================
# 1. 핵심 알고리즘 (CORE ALGORITHMS)
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
# 2. UI 및 데이터 초기화 (UI & DATA)
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
        st.session_state.active_tab = "🛒 1. 교재 장터 (KMP Search)"

    st.header("🔄 가천대 스마트 교재 물물교환 에코시스템")
    st.caption("IT 학과 전용 교재 물물교환 시스템 | KMP Search · DFS Cycle Detection")

    st.radio(
        "네비게이션 메뉴",
        ["🛒 1. 교재 장터 (KMP Search)", "⚡ 2. 스마트 매칭 (DFS)", "💳 3. 포인트 지갑 / 결제"],
        horizontal=True,
        key="active_tab",
        label_visibility="collapsed"
    )

    # ==========================================
    # 탭 1: 검색 및 등록
    # ==========================================
    if st.session_state.active_tab == "🛒 1. 교재 장터 (KMP Search)":
        st.subheader("🛒 가천대 교재 장터")

        with st.expander("➕ 내 교재 등록하기 (물물교환 네트워크 참여)", expanded=False):
            with st.form("add_book_form"):
                st.info(
                    "예: 내가 '자료구조'를 원하지만 판매자는 '수학'을 원할 때, 내가 가진 책을 등록하면 시스템이 제3자를 찾아 교환 고리를 완성합니다!")
                user_name = st.text_input("학생 이름")
                col_h, col_w = st.columns(2)
                has_book = col_h.text_input("보유 중인 교재 (Has)")
                want_book = col_w.text_input("필요한 교재 (Wants)")
                desc = st.text_area("교재 상태 설명")

                if st.form_submit_button("시스템에 등록", type="primary"):
                    if user_name and has_book and want_book:
                        st.session_state.students_data[user_name] = {"has": has_book, "wants": want_book, "desc": desc}
                        st.success(f"등록 성공! 시스템에 [{has_book}] 교재가 등록되었습니다.")
                        st.rerun()

        st.divider()

        search_query = st.text_input("🔍 교재명 검색 (KMP Search):", placeholder="예: 운영체제 공룡책").strip()

        df = pd.DataFrame(
            [{"학생명": k, "보유 (Has)": v["has"], "필요 (Wants)": v["wants"]} for k, v in
             st.session_state.students_data.items()])

        if search_query:
            # ==========================================
            # 💡 [UI/UX 최적화] 전처리 (Preprocessing) 단계
            # 사용자의 오타(띄어쓰기, 대소문자)를 방지하기 위해
            # 검색어와 데이터 모두 '소문자 변환 + 공백 제거' 후 비교합니다.
            # ==========================================
            clean_query = search_query.lower().replace(" ", "")

            df = df[
                df["보유 (Has)"].str.lower().str.replace(" ", "").str.contains(clean_query) |
                df["필요 (Wants)"].str.lower().str.replace(" ", "").str.contains(clean_query)
                ]

            # --- 처리된 결과가 없을 경우 (Empty State) ---
            if df.empty:
                st.warning(f"'{search_query}' 교재를 보유하거나 찾는 학생이 없습니다.")
                st.write("💡 아래 옵션을 통해 교재를 구해보세요:")

                c1, c2 = st.columns(2)
                c1.link_button("🛒 쿠팡 종이책 바로 검색", f"https://www.coupang.com/np/search?q={search_query}")
                c2.link_button("📱 교보문고 전자책(eBook) 검색",
                               f"https://search.kyobobook.co.kr/search?keyword={search_query}&mallGb=EBO")

                with st.expander("🏫 가천대 구내서점 직접 방문 구매 (오프라인)"):
                    st.write("**📍 위치:** 가천대학교 글로벌캠퍼스 비전타워 지하 3층 (B103-1호)")
                    st.write("**📞 전화번호:** 031-759-9895")
                    st.caption("👉 외부 링크로 이동하지 않습니다. 현장 방문 시 위 위치 정보를 참고하세요.")

        for idx, row in df.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                col1.write(f"**📖 {row['보유 (Has)']}** (필요: {row['필요 (Wants)']})")
                col2.button("매칭 연결", key=f"btn_{idx}", on_click=connect_action, args=(row['보유 (Has)'],))

    # ==========================================
    # 탭 2: 매칭 결과
    # ==========================================
    elif st.session_state.active_tab == "⚡ 2. 스마트 매칭 (DFS)":
        st.subheader("⚡ 스마트 매칭 시스템")
        if st.session_state.run_matching:
            st.info(f"다음 교재를 위한 교환 네트워크 탐색 중: **{st.session_state.target_book}**")
            cycles, graph = find_barter_cycles(st.session_state.students_data)

            matched = [c for c in cycles if
                       any(st.session_state.students_data[s]['has'] == st.session_state.target_book for s in c)]

            if matched:
                matched.sort(key=len)
                top_5_matches = matched[:5]

                st.success(f"🎉 {len(top_5_matches)}개의 최적 교환 네트워크(최소 중개자)를 발견했습니다!")

                col_text, col_graph = st.columns([1.2, 1])

                with col_text:
                    for i, cycle in enumerate(top_5_matches):
                        st.markdown(f"**Top {i + 1} (교환 고리: {len(cycle)}명):**")
                        path = " ➔ ".join(cycle) + f" ➔ {cycle[0]}"
                        st.code(path)

                with col_graph:
                    st.markdown("#### 🗺️ Top 1 교환 네트워크 맵")
                    try:
                        best_cycle = top_5_matches[0]
                        cycle_graph = nx.DiGraph()

                        for j in range(len(best_cycle)):
                            u = best_cycle[j]
                            v = best_cycle[(j + 1) % len(best_cycle)]
                            cycle_graph.add_edge(u, v)

                        fig, ax = plt.subplots(figsize=(3, 3))
                        pos = nx.circular_layout(cycle_graph)

                        plt.rcParams['font.family'] = 'Malgun Gothic'
                        plt.rcParams['axes.unicode_minus'] = False

                        nx.draw_networkx(cycle_graph, pos, with_labels=True, node_color='#74b9ff',
                                         edge_color='#ff7675', node_size=1000, font_size=8,
                                         font_weight='bold', font_family='Malgun Gothic', ax=ax, arrows=True,
                                         arrowsize=15)

                        ax.margins(0.3)
                        ax.axis('off')
                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"네트워크 그래프 표시 오류: {e}")
            else:
                st.error("⚠️ 현재 등록된 교재 중에는 폐쇄형 교환 네트워크(사이클)를 찾을 수 없습니다.")
                st.write(
                    "제안: **Tab 1**에서 내가 가진 교재를 등록하여 네트워크를 확장하거나, 아래에서 새 책을 구매해 보세요:")
                col_btn1, col_btn2 = st.columns(2)
                col_btn1.link_button("🛒 쿠팡에서 구매", "https://www.coupang.com/")
                col_btn2.link_button("📚 가천대 구내서점", "https://gachon.ac.kr/")

            st.button("검색 초기화 / 돌아가기", on_click=reset_action)
        else:
            st.write("Tab 1으로 돌아가서 매칭할 교재를 선택해 주세요.")

    # ==========================================
    # 탭 3: 포인트 지갑
    # ==========================================
    elif st.session_state.active_tab == "💳 3. 포인트 지갑 / 결제":
        st.subheader("💳 포인트 지갑 (Exit Strategy)")
        st.metric("현재 잔여 포인트", "45,000 P")
        st.selectbox("사용처 선택", ["가천관 학생식당", "CU 편의점 (교내)"])
        st.button("포인트로 결제하기")