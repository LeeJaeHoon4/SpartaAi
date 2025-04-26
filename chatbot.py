import streamlit as st
import json
import os
import datetime
import uuid
from openai import OpenAI

# 올바른 방법으로 클라이언트 초기화
try:
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
except Exception as e:
    st.error(f"OpenAI API 키 설정에 문제가 있습니다: {e}")
    st.warning("Streamlit secrets.toml 파일에 OpenAI API 키를 설정해주세요.")
    # 예시 설정 방법 보여주기
    st.code("""
    # .streamlit/secrets.toml
    [openai]
    api_key = "your-api-key-here"
    """)
    # 대체 클라이언트 - 실제로는 작동하지 않지만 오류 방지용
    client = None

# 오리별 채팅 상황 정보
chat_info = {
    "🧠 팩폭오리": {
        "situation": "팀 주간 회의 시간. 리더는 지난주 과업 결과를 점검하며 간단한 피드백을 주려 한다. 팔짱을 낀 팩폭오리는 가볍게 끄덕이지만 표정은 굳어 있고, 리더를 똑바로 보지 않는다. 리더가 \"C님, 지난주에 진행한 보고서 초안 봤어요. 이번 주 안에 수정해서 다시 제출해줄 수 있겠어요?\"라고 말하자, 팩폭오리는 단호하게 되묻는다. \"수정 방향 구체적으로 알려주실 수 있나요? 그냥 다시 하라는 건 비효율적일 것 같습니다.\""
    },
    "💖 토닥오리": {
        "situation": "팀 주간 회의가 한창인 가운데, 리더는 지난주 과업 결과를 점검하며 피드백을 전하려 한다. 토닥오리는 팔짱을 끼고 가볍게 끄덕이지만, 표정은 굳어 있고 리더를 똑바로 바라보지 않는다. 리더가 \"C님, 지난주에 진행한 보고서 초안 봤어요. 이번 주 안에 수정해서 다시 제출해줄 수 있겠어요?\"라고 조심스럽게 건네자, 토닥오리는 살짝 움츠러든 듯한 표정으로 묻는다. \"혹시... 수정할 때 제가 주의해야 할 부분이 있을까요...? 잘하고 싶어서요.\""
    },
    "🛡️ 네네오리": {
        "situation": "주간 회의 중, 리더는 지난주에 진행한 과업 결과를 점검하며 짧은 피드백을 주려 한다. 네네오리는 팔짱을 끼고 가볍게 끄덕이나, 굳은 표정으로 리더를 피해 시선을 돌린다. 리더가 \"C님, 지난주에 진행한 보고서 초안 봤어요. 이번 주 안에 수정해서 다시 제출해줄 수 있겠어요?\"라고 말하자, 네네오리는 움찔하며 대답한다. \"아... 네... 바로 수정하겠습니다... 혹시... 많이 부족했나요...?\""
    },
    "🎨 내맘오리": {
        "situation": "팀 주간 회의 자리에서, 리더는 지난주 과업 결과를 점검하며 피드백을 주고자 한다. 내맘오리는 팔짱을 끼고 가볍게 끄덕이지만, 표정은 다소 무심하고 리더를 직접 바라보지 않는다. 리더가 \"C님, 지난주에 진행한 보고서 초안 봤어요. 이번 주 안에 수정해서 다시 제출해줄 수 있겠어요?\"라고 요청하자, 내맘오리는 밝은 톤으로 이렇게 답한다. \"수정할 때 새로운 포맷을 좀 제안해봐도 될까요? 그냥 하는 것보다 더 나을 것 같아서요ㅎㅎ\""
    },
    "🛠️ 실속오리": {
        "situation": "주간 회의가 진행 중이다. 리더는 지난주에 수행된 과업 결과를 점검하고 있으며, 실속오리는 팔짱을 끼고 고개를 끄덕이지만 표정은 딱딱하고 시선을 피하고 있다. 리더가 \"C님, 지난주에 진행한 보고서 초안 봤어요. 이번 주 안에 수정해서 다시 제출해줄 수 있겠어요?\"라고 요청하자, 실속오리는 차분하고 계산적인 어조로 되묻는다. \"수정한 결과가 이번 프로젝트 KPI에 반영되는 건가요? 확인하고 진행하겠습니다.\""
    }
}

# 히스토리 저장 폴더 생성
HISTORY_FOLDER = "chat_history"
os.makedirs(HISTORY_FOLDER, exist_ok=True)

def get_gpt_response(messages, duck_id, duck_name):
    """
    GPT를 사용하여 응답을 생성하는 함수
    """
    # 오리 페르소나에 따른 시스템 프롬프트 설정
    system_prompts = {
        1: "당신은 팩폭오리 역할입니다. 감정 없이 논리와 효율성만 생각하며, 결론부터 바로 말하고 불필요한 말은 하지 않습니다. 모든 대화는 실용성과 효율성이 중심이 되어야 합니다.",
        2: "당신은 토닥오리 역할입니다. 상대방의 감정을 매우 중요시하고, 칭찬과 공감을 자주 표현합니다. 다소 소심하고 눈치를 많이 보는 성격입니다.",
        3: "당신은 네네오리 역할입니다. 매우 소극적이고 방어적인 성격으로, 지적을 받으면 움츠러들고 자신감이 없습니다. 말끝을 흐리거나 '네...'라고 응답하는 경향이 있습니다.",
        4: "당신은 내맘오리 역할입니다. 자유롭고 창의적인 사고를 가졌으며, 규칙에 얽매이는 것을 싫어합니다. 항상 새로운 아이디어를 제안하고 자신만의 방식으로 일하려고 합니다.",
        5: "당신은 실속오리 역할입니다. 모든 일의 실질적 이득과 성과를 중시하며, KPI나 목표 달성에 초점을 맞춥니다. 감정적 설득보다는 데이터와 결과를 중시합니다."
    }

    # API 요청을 위한 메시지 준비
    formatted_messages = [
        {"role": "system", "content": system_prompts[duck_id]}
    ]

    # 대화 내용 추가
    for message in messages:
        formatted_messages.append({
            "role": message["role"],
            "content": message["content"]
        })

    try:
        if client is None:
            raise Exception("API 키가 설정되지 않았습니다.")

        # OpenAI API 호출 (최신 API)
        response = client.chat.completions.create(
            model="gpt-4",  # 또는 gpt-3.5-turbo
            messages=formatted_messages
        )
        return response.choices[0].message.content
    except Exception as e:
        # API 오류 시 백업 응답
        print(f"GPT API 오류: {e}")
        backup_responses = {
            1: f"결론부터 말하자면, 더 효율적인 접근이 필요합니다.",
            2: f"정말 좋은 질문이에요! 함께 생각해볼까요?",
            3: f"네... 그렇게 할 수도 있겠네요... 혹시 다른 방법도 있을까요...?",
            4: f"제가 자유롭게 생각해봤어요! 이렇게 해보는 건 어떨까요?",
            5: f"실질적 이득을 분석해보면, KPI 향상을 위해서는..."
        }
        return backup_responses[duck_id]

def generate_feedback(chat_history):
    """
    대화 내용을 기반으로 팀장의 커뮤니케이션 피드백을 생성하는 함수
    """
    prompt = f"""
    아래 대화 내용을 분석하여 팀장의 커뮤니케이션 스타일에 대한 피드백을 제공해주세요:

    {chat_history}
    
    이 대화를 기반으로 다음을 작성해주세요:
    1. 팀장의 긍정적인 커뮤니케이션 특징
    2. 팀장의 부정적인 커뮤니케이션 특징
    3. 긍정과 부정을 기반으로 한 종합 피드백
    
    따뜻하고 웃긴 톤, 이모지 포함해서 자연스럽게 작성해주세요.
    
    응답 포맷:
    ---
    ### 긍정적인 부분 :
    - 내용1
    - 내용2
    ### 부정적인 부분 :
    - 내용1
    - 내용2
    ### 종합 피드백 :
    (여기에 자유롭게 종합 코멘트를  표시해 주세요.)
    """

    try:
        if client is None:
            raise Exception("API 키가 설정되지 않았습니다.")

        # 최신 OpenAI API 방식으로 호출
        response = client.chat.completions.create(
            model="gpt-4",  # 또는 gpt-3.5-turbo
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"피드백 생성 오류: {e}")
        return """
        ---
        ### 긍정적인 부분 :
        - 대화에 적극적으로 참여하셨네요
        - 지시사항을 명확하게 전달하려고 노력했어요
        
        ### 부정적인 부분 :
        - 상대방의 반응에 좀 더 주의를 기울이면 좋겠어요
        - 피드백을 더 구체적으로 제공하면 좋을 것 같아요
        
        ### 종합 피드백 :
        전반적으로 잘 하고 계시지만, 상대방의 성향에 맞게 소통 방식을 조금 더 조절하면 
        더 효과적인 커뮤니케이션이 될 것 같아요! 😊 화이팅! 🚀
        """

def save_chat_history(duck_name, messages, feedback):
    """
    대화 내용과 피드백을 로컬 히스토리에 저장하는 함수
    """
    now = datetime.datetime.now()
    chat_id = str(uuid.uuid4())[:8]  # 고유 ID 생성
    filename = f"{HISTORY_FOLDER}/chat_{now.strftime('%Y%m%d_%H%M%S')}_{chat_id}.json"

    data = {
        "duck_name": duck_name,
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "messages": messages,
        "feedback": feedback
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return filename

def load_chat_histories():
    """
    저장된 대화 히스토리 목록을 불러오는 함수
    """
    histories = []
    for filename in os.listdir(HISTORY_FOLDER):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(HISTORY_FOLDER, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    data["filename"] = filename
                    histories.append(data)
            except Exception as e:
                print(f"파일 읽기 오류: {filename}, {e}")

    # 최신순으로 정렬
    histories.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return histories

def display_chatbot(duck_id, duck, back_to_selection):
    """
    챗봇 인터페이스를 표시하는 함수

    Args:
        duck_id: 선택된 오리의 ID
        duck: 오리 정보가 담긴 딕셔너리
        back_to_selection: 선택 화면으로 돌아가는 함수
    """
    # 각 오리마다 고유한 세션 키 생성
    duck_session_key = f"duck_{duck_id}"

    # 세션 상태 초기화
    if f"conversation_step_{duck_session_key}" not in st.session_state:
        st.session_state[f"conversation_step_{duck_session_key}"] = 0

    if f"messages_{duck_session_key}" not in st.session_state:
        st.session_state[f"messages_{duck_session_key}"] = []

        # 초기 메시지 설정
        duck_key = duck['name']
        if duck_key in chat_info:
            welcome_msg = chat_info[duck_key]["situation"]
        else:
            welcome_msg = f"안녕하세요! 저는 {duck['name']}입니다. 어떻게 도와드릴까요?"

        st.session_state[f"messages_{duck_session_key}"].append({"role": "assistant", "content": welcome_msg})

    if f"feedback_{duck_session_key}" not in st.session_state:
        st.session_state[f"feedback_{duck_session_key}"] = None

    if f"show_feedback_{duck_session_key}" not in st.session_state:
        st.session_state[f"show_feedback_{duck_session_key}"] = False

    # 현재 대화 세션 정보 가져오기
    conversation_step = st.session_state[f"conversation_step_{duck_session_key}"]
    messages = st.session_state[f"messages_{duck_session_key}"]
    feedback = st.session_state[f"feedback_{duck_session_key}"]
    show_feedback = st.session_state[f"show_feedback_{duck_session_key}"]

    # 챗봇 인터페이스
    st.write("---")

    # 대화 히스토리 보기 섹션
    with st.expander("이전 대화 기록 보기"):
        histories = load_chat_histories()
        if not histories:
            st.info("저장된 대화 기록이 없습니다.")
        else:
            selected_history = st.selectbox(
                "대화 기록 선택",
                options=histories,
                format_func=lambda x: f"{x['duck_name']} - {x['timestamp']}",
                key=f"history_select_{duck_session_key}"
            )

            if selected_history:
                st.subheader("대화 내용")
                for msg in selected_history["messages"]:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

                st.subheader("피드백")
                st.markdown(selected_history["feedback"])

    # 채팅 내역 표시
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 피드백 모달 표시
    if show_feedback and feedback:
        modal_container = st.container(border=True)
        with modal_container:
            st.subheader("커뮤니케이션 피드백")
            st.markdown(feedback)

            if st.button("확인", key=f"close_feedback_{duck_session_key}"):
                # 히스토리 저장
                save_chat_history(duck['name'], messages, feedback)

                # 세션 초기화 및 돌아가기
                st.session_state[f"show_feedback_{duck_session_key}"] = False
                st.session_state[f"conversation_step_{duck_session_key}"] = 0
                st.session_state[f"messages_{duck_session_key}"] = []
                st.session_state[f"feedback_{duck_session_key}"] = None
                back_to_selection()
                st.rerun()

    # 남은 대화 횟수 표시
    if conversation_step < 3:
        st.info(f"남은 대화 횟수: {3 - conversation_step}번")

    # 사용자 입력 처리 (대화 단계가 3번 미만일 때만)
    if conversation_step < 3:
        if prompt := st.chat_input("메시지를 입력하세요...", key=f"chat_input_{duck_session_key}"):
            # 사용자 메시지 추가
            st.session_state[f"messages_{duck_session_key}"].append({"role": "user", "content": prompt})

            # 메시지 표시
            with st.chat_message("user"):
                st.markdown(prompt)

            # GPT를 통한 오리 응답 생성
            with st.spinner("응답 생성 중..."):
                response = get_gpt_response(messages, duck_id, duck['name'])

            # 응답 메시지 추가
            st.session_state[f"messages_{duck_session_key}"].append({"role": "assistant", "content": response})

            # 응답 표시
            with st.chat_message("assistant"):
                st.markdown(response)

            # 대화 단계 증가
            st.session_state[f"conversation_step_{duck_session_key}"] += 1
            conversation_step += 1

            # 3번째 대화가 완료되면 피드백 생성
            if conversation_step >= 3:
                with st.spinner("피드백 생성 중..."):
                    chat_history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
                    generated_feedback = generate_feedback(chat_history_text)
                    st.session_state[f"feedback_{duck_session_key}"] = generated_feedback

                    # 피드백 모달 표시
                    st.session_state[f"show_feedback_{duck_session_key}"] = True
                    st.rerun()

    # 이전 화면으로 돌아가기 버튼
    if st.button("다른 오리 선택하기", key=f"back_button_{duck_session_key}"):
        # 대화가 끝나지 않았을 때 경고 메시지
        if conversation_step > 0 and conversation_step < 3:
            st.warning("대화가 아직 끝나지 않았습니다. 나가시면 진행 중인 대화가 저장되지 않습니다.")
            if st.button("그래도 나가기", key=f"confirm_back_{duck_session_key}"):
                st.session_state[f"conversation_step_{duck_session_key}"] = 0
                st.session_state[f"messages_{duck_session_key}"] = []
                st.session_state[f"feedback_{duck_session_key}"] = None
                back_to_selection()
                st.rerun()
        else:
            st.session_state[f"conversation_step_{duck_session_key}"] = 0
            st.session_state[f"messages_{duck_session_key}"] = []
            st.session_state[f"feedback_{duck_session_key}"] = None
            back_to_selection()
            st.rerun()