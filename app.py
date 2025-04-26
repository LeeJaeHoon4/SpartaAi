import streamlit as st
from PIL import Image
import base64

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'index'  # 초기 페이지 설정 (index 또는 chat)
if 'selected_bot' not in st.session_state:
    st.session_state.selected_bot = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'show_dialog' not in st.session_state:
    st.session_state.show_dialog = False
if 'dialog_type' not in st.session_state:
    st.session_state.dialog_type = None

# 챗봇 유형별 정보
bot_info = {
    1: {"name": "유형 1", "mbti": "ESTJ", "description": "냉철한 성격을 가지고 있습니다."},
    2: {"name": "유형 2", "mbti": "INFP", "description": "감성적이고 창의적인 성격을 가지고 있습니다."},
    3: {"name": "유형 3", "mbti": "ENFJ", "description": "사교적이고 리더십이 있는 성격을 가지고 있습니다."},
    4: {"name": "유형 4", "mbti": "INTP", "description": "논리적이고 분석적인 성격을 가지고 있습니다."},
    5: {"name": "유형 5", "mbti": "ISFJ", "description": "신중하고 배려심이 깊은 성격을 가지고 있습니다."}
}

# 페이지 전환 함수
def switch_to_chat():
    st.session_state.page = 'chat'

def switch_to_index():
    st.session_state.page = 'index'

# 챗봇 선택 함수
def select_bot(bot_number):
    st.session_state.dialog_type = bot_number
    st.session_state.show_dialog = True
    st.rerun()

# 확인 모달 다이얼로그
@st.dialog("사원 페르소나 선택", width="medium")
def show_confirm_dialog():
    bot_type = st.session_state.dialog_type
    info = bot_info[bot_type]

    # 중앙 정렬을 위한 CSS
    st.markdown("""
    <style>
    div.stMarkdown {
        text-align: center;
    }
    div.stButton > button {
        display: inline-block;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

    # 유형 타이틀
    st.markdown(f"<h1 style='text-align: center;'>{info['name']}</h1>", unsafe_allow_html=True)

    # 이미지 추가 (여기에서는 예시 이미지를 사용)
    # 실제로는 각 유형별 이미지 파일을 사용하세요
    cols = st.columns([1, 2, 1])
    with cols[1]:
        # 예시 이미지 (플레이스홀더)
        st.image("https://via.placeholder.com/300x200?text=Bot+Type+"+str(bot_type), width=300)

    # 설명
    st.markdown(f"<p style='text-align: center;'>유형 {bot_type}은 MBTI {info['mbti']}이고 {info['description']}</p>", unsafe_allow_html=True)

    # 버튼 중앙 정렬
    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button("취소", use_container_width=True):
            st.session_state.show_dialog = False
            st.rerun()

    with cols[2]:
        if st.button("선택하기", use_container_width=True):
            st.session_state.selected_bot = bot_type
            st.session_state.show_dialog = False
            st.session_state.page = 'chat'
            st.rerun()

# 인덱스 페이지 (선택 화면)
def show_index_page():
    st.title("사원 유형 선택 페이지")

    # 5개의 버튼 생성
    st.subheader("원하는 유형을 선택하세요")

    # 버튼을 가로로 배치하기 위해 컬럼 사용
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("유형 1", key="bot1"):
            select_bot(1)

    with col2:
        if st.button("유형 2", key="bot2"):
            select_bot(2)

    with col3:
        if st.button("유형 3", key="bot3"):
            select_bot(3)

    with col4:
        if st.button("유형 4", key="bot4"):
            select_bot(4)

    with col5:
        if st.button("유형 5", key="bot5"):
            select_bot(5)

    # 선택된 챗봇 표시
    if st.session_state.selected_bot:
        st.success(f" {st.session_state.selected_bot}이(가) 선택되었습니다.")

    # 시작하기 버튼
    if st.button("시작하기", disabled=st.session_state.selected_bot is None):
        switch_to_chat()
        st.rerun()

    # 시작하기 전에 챗봇을 선택해야 한다는 메시지 표시
    if st.session_state.selected_bot is None:
        st.info("시작하기 전에 챗봇을 선택해주세요.")

# 채팅 페이지
def show_chat_page():
    # 홈으로 돌아가기 버튼
    if st.button("⬅️ 홈으로 돌아가기"):
        switch_to_index()
        st.rerun()

    # 선택된 챗봇 표시
    st.title(f"{bot_info[st.session_state.selected_bot]['name']}")

    # 이전 메시지 표시
    for message in st.session_state.messages:
        if message['is_user']:
            st.write(f"You: {message['text']}")
        else:
            st.write(f"Bot: {message['text']}")

    # 사용자 메시지 입력
    st.markdown('<h3>상황 설명:</h3>', unsafe_allow_html=True)
    user_input = st.text_input('', key='user_message', placeholder="여기에 메시지를 입력하세요...")

    # 전송 버튼
    if st.button('전송', key='send_button'):
        if user_input:
            # 사용자 메시지를 기록에 추가
            st.session_state.messages.append({
                'text': user_input,
                'is_user': True
            })

            # 선택된 챗봇에 따라 다른 응답 생성
            bot_type = st.session_state.selected_bot
            if bot_type == 1:
                bot_response = f"챗봇 1의 응답: {user_input}"
            elif bot_type == 2:
                bot_response = f"챗봇 2의 응답: {user_input}"
            elif bot_type == 3:
                bot_response = f"챗봇 3의 응답: {user_input}"
            elif bot_type == 4:
                bot_response = f"챗봇 4의 응답: {user_input}"
            elif bot_type == 5:
                bot_response = f"챗봇 5의 응답: {user_input}"
            else:
                bot_response = f"기본 응답: {user_input}"

            # 봇 응답을 기록에 추가
            st.session_state.messages.append({
                'text': bot_response,
                'is_user': False
            })

            # 입력창 초기화
            st.session_state.user_message = ""

            # UI 업데이트
            st.rerun()

# 현재 페이지에 따라 해당 함수 호출
if st.session_state.show_dialog:
    show_confirm_dialog()

if st.session_state.page == 'index':
    show_index_page()
elif st.session_state.page == 'chat':
    show_chat_page()
