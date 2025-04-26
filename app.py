import streamlit as st
import openai
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드 (선택적)
load_dotenv()

# API 키 설정 (환경 변수 또는 직접 입력)
# 보안을 위해 .env 파일이나 Streamlit의 secrets 관리 기능 사용 권장
openai.api_key = st.secrets["openai"]["api_key"]

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
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = {}

# 챗봇 유형별 정보
bot_info = {
    1: {
        "name": "유형 1",
        "mbti": "ESTJ",
        "description": "냉철한 성격을 가지고 있습니다.",
        "system_prompt": "당신은 ESTJ 성격을 가진 냉철하고 논리적인 챗봇입니다. 사용자의 질문에 명확하고 직접적인 답변을 제공하세요."
    },
    2: {
        "name": "유형 2",
        "mbti": "INFP",
        "description": "감성적이고 창의적인 성격을 가지고 있습니다.",
        "system_prompt": "당신은 INFP 성격을 가진 감성적이고 창의적인 챗봇입니다. 사용자의 질문에 공감하고 상상력이 풍부한 답변을 제공하세요."
    },
    3: {
        "name": "유형 3",
        "mbti": "ENFJ",
        "description": "사교적이고 리더십이 있는 성격을 가지고 있습니다.",
        "system_prompt": "당신은 ENFJ 성격을 가진 사교적이고 리더십 있는 챗봇입니다. 사용자를 격려하고 영감을 주는 답변을 제공하세요."
    },
    4: {
        "name": "유형 4",
        "mbti": "INTP",
        "description": "논리적이고 분석적인 성격을 가지고 있습니다.",
        "system_prompt": "당신은 INTP 성격을 가진 논리적이고 분석적인 챗봇입니다. 사용자의 질문에 깊이 있는 분석과 다양한 관점을 제공하세요."
    },
    5: {
        "name": "유형 5",
        "mbti": "ISFJ",
        "description": "신중하고 배려심이 깊은 성격을 가지고 있습니다.",
        "system_prompt": "당신은 ISFJ 성격을 가진 신중하고 배려심이 깊은 챗봇입니다. 사용자의 질문에 따뜻하고 세심한 답변을 제공하세요."
    }
}

# GPT API 호출 함수
def get_gpt_response(messages, bot_type):
    try:
        # 챗봇 유형에 맞는 시스템 프롬프트 추가
        system_prompt = bot_info[bot_type]["system_prompt"]

        # API 호출용 메시지 배열 구성
        api_messages = [{"role": "system", "content": system_prompt}]

        # 기존 대화 내역 추가
        for msg in messages:
            if msg['is_user']:
                api_messages.append({"role": "user", "content": msg['text']})
            else:
                api_messages.append({"role": "assistant", "content": msg['text']})

        # OpenAI API 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 또는 원하는 모델 (gpt-4 등)
            messages=api_messages,
            temperature=0.7,
            max_tokens=1024
        )

        # 응답 추출
        return response.choices[0].message.content

    except Exception as e:
        # 오류 처리
        st.error(f"GPT API 호출 중 오류가 발생했습니다: {str(e)}")
        return f"죄송합니다. 응답을 생성하는 중 오류가 발생했습니다. 다시 시도해 주세요."

# 페이지 전환 함수
def switch_to_chat():
    st.session_state.page = 'chat'
    # 챗봇 선택 시 해당 챗봇의 대화 기록 초기화
    if st.session_state.selected_bot not in st.session_state.chat_history:
        st.session_state.chat_history[st.session_state.selected_bot] = []

    st.session_state.messages = st.session_state.chat_history[st.session_state.selected_bot]

def switch_to_index():
    st.session_state.page = 'index'

# 챗봇 선택 함수
def select_bot(bot_number):
    st.session_state.dialog_type = bot_number
    st.session_state.show_dialog = True
    st.rerun()

# 확인 모달 다이얼로그
@st.dialog("챗봇 유형 선택", width="medium")
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
            switch_to_chat()
            st.rerun()

# 인덱스 페이지 (선택 화면)
def show_index_page():
    st.title("챗봇 선택 페이지")

    # 5개의 버튼 생성
    st.subheader("원하는 챗봇을 선택하세요")

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
        st.success(f"챗봇 {st.session_state.selected_bot}이(가) 선택되었습니다.")

    # 시작하기 버튼
    if st.button("시작하기", disabled=st.session_state.selected_bot is None):
        switch_to_chat()
        st.rerun()

    # 시작하기 전에 챗봇을 선택해야 한다는 메시지 표시
    if st.session_state.selected_bot is None:
        st.info("시작하기 전에 챗봇을 선택해주세요.")

# 채팅 페이지
def show_chat_page():
    bot_type = st.session_state.selected_bot
    info = bot_info[bot_type]

    # 홈으로 돌아가기 버튼
    if st.button("⬅️ 홈으로 돌아가기"):
        switch_to_index()
        st.rerun()

    # 선택된 챗봇 표시
    st.title(f"챗봇 {info['name']} ({info['mbti']})")

    # 챗봇 설명 표시
    st.info(info['description'])

    # 이전 메시지 표시 (채팅 UI 개선)
    if st.session_state.messages:
        for message in st.session_state.messages:
            if message['is_user']:
                with st.chat_message("user"):
                    st.write(message['text'])
            else:
                with st.chat_message("assistant"):
                    st.write(message['text'])

    # 입력창 초기화 함수
    def clear_input():
        st.session_state["user_message"] = ""

    # 사용자 메시지 입력
    user_input = st.chat_input('메시지를 입력하세요...', key='user_message')

    # 메시지 입력 처리
    if user_input:
        # 사용자 메시지를 기록에 추가
        with st.chat_message("user"):
            st.write(user_input)

        st.session_state.messages.append({
            'text': user_input,
            'is_user': True
        })

        # GPT로부터 응답 생성
        with st.spinner('응답 생성 중...'):
            bot_response = get_gpt_response(st.session_state.messages, bot_type)

        # 봇 응답을 기록에 추가
        with st.chat_message("assistant"):
            st.write(bot_response)

        st.session_state.messages.append({
            'text': bot_response,
            'is_user': False
        })

        # 챗봇별 대화 기록 저장
        st.session_state.chat_history[bot_type] = st.session_state.messages

        # 입력창 초기화하기 위한 페이지 재실행
        clear_input()

# 현재 페이지에 따라 해당 함수 호출
if st.session_state.show_dialog:
    show_confirm_dialog()

if st.session_state.page == 'index':
    show_index_page()
elif st.session_state.page == 'chat':
    show_chat_page()