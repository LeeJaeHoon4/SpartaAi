import streamlit as st
import json
from PIL import Image
import os
from chatbot import display_chatbot  # 새로 만든 파일 임포트

# 페이지 설정
st.set_page_config(page_title="오리 유형 선택", layout="wide")

# 세션 상태 초기화
if "selected_duck" not in st.session_state:
    st.session_state.selected_duck = None
if "page" not in st.session_state:
    st.session_state.page = "selection"

# 오리 정보 딕셔너리
bot_info = {
    1: {
        "name": "🧠 팩폭오리",
        "alias": "팩폭 신입 (팩트폭격기)",
        "caution": "감정 섞인 말 피하고 결론부터 전달",
        "example": "이거 효율적이지 않은데 왜 하죠?",
        "system_prompt": """\n- 논리와 근거 최우선
                       \n- 감정 표현 없음
                       \n- 효율성 집착
                       \n- 감정, 분위기 모두 무시하고 '팩트'만 추구
                       \n- 논리적 허점 발견하면 대놓고 질문함
                       \n- 장황한 설명 싫어함""",
        "img_file" : "팩폭오리.png",
        "img_file2" : "팩폭오리2.png"
    },
    2: {
        "name": "💖 토닥오리",
        "alias": "눈치 보는 감성파",
        "caution": "작은 칭찬, 감정적 연결 유지",
        "example": "저 혹시... 제가 뭔가 실수한 건가요...?",
        "system_prompt": """\n- 따뜻한 공감 필요
                            \n- 작은 무시에도 깊게 상처
                            \n- 칭찬 한마디에 부활
                            \n- 감정 연결에 엄청 민감
                            \n- 톤, 눈빛 하나에 상처 받음
                            \n- 칭찬 한 마디로 몰입도 급상승""",
        "img_file" : "토닥오리.png",
        "img_file2" : "토닥오리2.png"
    },
    3: {
        "name": "🛡️ 네네오리",
        "alias": "방어형 생존러",
        "caution": "지시 전에 먼저 심리적 안심 주기",
        "example": "네… 아… 아닌가요…? 하겠습니다…",
        "system_prompt": """
        \n- 지적에 과민 반응
        \n- 책임 회피 경향/책임 지기 싫어함
        \n- 항상 방어 모드 대기
        \n- 꾸중, 비판에 민감
        \n- 시킨 대로는 하지만 적극성 없음""",
        "img_file" : "네네오리.png",
        "img_file2" : "네네오리2.png"
    },
    4: {
        "name": "🎨 내맘오리",
        "alias": "자유로운 창의꾼",
        "caution": "방법은 자유롭게 맡기기",
        "example": "저 이거 다르게 해봤어요ㅎㅎ",
        "system_prompt": """
        \n- 통제 싫어함
        \n- 틀 짜면 흥미 급감
        \n- 자율 주제일 때 몰입
        \n- 자유와 자율성 중시
        \n- 규칙, 프로세스 싫어함
        \n- 신나면 몰입도 미친 듯 올라감""",
        "img_file" : "내맘오리.png",
        "img_file2" : "내맘오리2.png"
    },
    5: {
        "name": "🛠️ 실속오리",
        "alias": "실리적 결과맨",
        "caution": "결과/성과와 연결해서 지시",
        "example": "이거 KPI에 영향 있나요?",
        "system_prompt": """
        \n- 실익 없는 일 거부
        \n- 감성팔이에 냉정
        \n- 실적 목표 있을 때 최강
        \n- 실질적 이득, 결과 중요
        \n- 감정적 설득 불가
        \n- 목표-성과 연결하면 열정 폭발""",
        "img_file" : "실속오리.png",
        "img_file2" : "실속오리2.png"
    }
}

# 폴더가 없으면 생성
img_folder = "img"
os.makedirs(img_folder, exist_ok=True)

# 이미지 파일이 없는 경우를 대비한 함수
def get_image_path(img_file):
    full_path = os.path.join(img_folder, img_file)
    if os.path.exists(full_path):
        return full_path
    else:
        st.warning(f"이미지 파일을 찾을 수 없습니다: {full_path}")
        return None

# 버튼 클릭 이벤트 핸들러
def show_duck_modal(duck_id):
    st.session_state.selected_duck = duck_id

# 챗봇 페이지로 이동
def go_to_chatbot():
    st.session_state.page = "chatbot"

# 선택 페이지로 돌아가기
def back_to_selection():
    st.session_state.page = "selection"
    st.session_state.selected_duck = None

# 메인 애플리케이션 로직
def main():
    if st.session_state.page == "selection":
        st.title("오리 유형 선택")
        st.subheader("당신의 상대할 유형의 오리를 선택하세요")

        # 오리 선택 버튼 - 3열 레이아웃
        col1, col2, col3 = st.columns(3)

        with col1:
            st.button(f"{bot_info[1]['name']}",
                      key="duck1",
                      on_click=show_duck_modal,
                      args=(1,),
                      use_container_width=True)

            st.button(f"{bot_info[4]['name']}",
                      key="duck4",
                      on_click=show_duck_modal,
                      args=(4,),
                      use_container_width=True)

        with col2:
            st.button(f"{bot_info[2]['name']}",
                      key="duck2",
                      on_click=show_duck_modal,
                      args=(2,),
                      use_container_width=True)

            st.button(f"{bot_info[5]['name']}",
                      key="duck5",
                      on_click=show_duck_modal,
                      args=(5,),
                      use_container_width=True)

        with col3:
            st.button(f"{bot_info[3]['name']}",
                      key="duck3",
                      on_click=show_duck_modal,
                      args=(3,),
                      use_container_width=True)

        # 모달 다이얼로그 표시
        if st.session_state.selected_duck:
            duck_id = st.session_state.selected_duck
            duck = bot_info[duck_id]

            with st.container():
                modal = st.container(border=True)
                with modal:
                    st.subheader(f"{duck['name']}")

                    # 이미지 표시
                    img_path = get_image_path(duck['img_file'])
                    if img_path:
                        st.image(img_path, width=300)

                    # 오리 정보 표시
                    st.write(f"**별명:** {duck['alias']}")
                    st.write(f"**대표 발언:** \"{duck['example']}\"")
                    st.write("**주의사항:**")
                    st.text(duck['system_prompt'])

                    # 확인/취소 버튼
                    col1, col2 = st.columns(2)
                    with col1:
                        if "button_clicked" not in st.session_state:
                            st.session_state.button_clicked = False

                        if st.button("확인", key="confirm", use_container_width=True) or st.session_state.button_clicked:
                            st.session_state.button_clicked = True
                            go_to_chatbot()

                    with col2:
                        if st.button("취소", key="cancel", use_container_width=True):
                            st.session_state.selected_duck = None
                            st.rerun()

    elif st.session_state.page == "chatbot":
        duck_id = st.session_state.selected_duck
        duck = bot_info[duck_id]

        st.title(f"{duck['name']} 챗봇")
        st.subheader(f"{duck['alias']}")
        # 이미지 표시
        img_path = get_image_path(duck['img_file2'])
        if img_path:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(img_path, width=150)
            with col2:
                st.info(f"오리의 성격: {duck['system_prompt']}")

        # 여기서 챗봇 인터페이스 파일 호출
        display_chatbot(duck_id, duck, back_to_selection)

if __name__ == "__main__":
    main()