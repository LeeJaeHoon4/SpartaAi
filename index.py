import streamlit as st
import subprocess
import webbrowser
import os

# 페이지 제목
st.title("채팅봇 선택 페이지")

# 세션 상태 초기화
if 'selected_bot' not in st.session_state:
    st.session_state['selected_bot'] = None

# 5개의 버튼 생성
st.subheader("원하는 챗봇을 선택하세요")

# 버튼을 가로로 배치하기 위해 컬럼 사용
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("챗봇 1"):
        st.session_state['selected_bot'] = 1

with col2:
    if st.button("챗봇 2"):
        st.session_state['selected_bot'] = 2

with col3:
    if st.button("챗봇 3"):
        st.session_state['selected_bot'] = 3

with col4:
    if st.button("챗봇 4"):
        st.session_state['selected_bot'] = 4

with col5:
    if st.button("챗봇 5"):
        st.session_state['selected_bot'] = 5

# 선택된 챗봇 표시
if st.session_state['selected_bot']:
    st.success(f"챗봇 {st.session_state['selected_bot']}이(가) 선택되었습니다.")

# 시작하기 버튼
if st.button("시작하기", disabled=st.session_state['selected_bot'] is None):
    # 선택한 챗봇 정보를 app.py에 전달
    st.session_state['start_chat'] = True
    st.session_state['bot_type'] = st.session_state['selected_bot']

    # app.py로 리디렉션
    st.switch_page("pages/app")
    # 참고: st.switch_page는 최신 Streamlit 버전에서만 작동합니다.
    # 지원되지 않는 경우 아래 대체 코드를 사용하세요:
    # st.experimental_set_query_params(page='app')
    # st.experimental_rerun()

# 시작하기 전에 챗봇을 선택해야 한다는 메시지 표시
if st.session_state['selected_bot'] is None:
    st.info("시작하기 전에 챗봇을 선택해주세요.")
