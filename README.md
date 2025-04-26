# Streamlit 챗봇 선택기 애플리케이션

## 프로젝트 개요

이 프로젝트는 Streamlit을 사용하여 다양한 유형의 챗봇을 선택하고 대화할 수 있는 웹 애플리케이션입니다. 사용자는 5가지 서로 다른 유형의 챗봇 중에서 선택할 수 있으며, 선택한 챗봇과 대화를 나눌 수 있습니다.

## 주요 기능

- 5가지 챗봇 유형 선택 화면
- 챗봇 유형 선택 시 상세 정보를 보여주는 모달 팝업
- 챗봇과의 대화 인터페이스
- 세션 상태 유지 기능
- 페이지 간 이동 기능

## 설치 및 실행 방법

### 필수 조건

- Python 3.9 이상
- Streamlit 1.32.0 이상

### 설치

1. 저장소 클론 또는 다운로드:
```
git clone <repository-url>
cd <repository-directory>
```


2. 필요한 패키지 설치:
```
pip install streamlit pillow
```


### 실행 방법

프로젝트 디렉토리에서 다음 명령어를 실행합니다:
```
streamlit run app.py
```

### 3. 중앙 정렬된 모달 구현

**요구사항**:
각 유형 선택 시 화면 중앙에 정보를 보여주는 모달 팝업이 필요했습니다.

**해결 방법**:
`@st.dialog` 데코레이터와 CSS 스타일링을 사용하여 중앙 정렬된 모달 창을 구현했습니다.

## 프로젝트 구조

- `app.py`: 메인 애플리케이션 파일

## 주요 코드 설명

### 세션 상태 관리
```python
if 'page' not in st.session_state:
    st.session_state.page = 'index'
if 'selected_bot' not in st.session_state:
    st.session_state.selected_bot = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'show_dialog' not in st.session_state:
    st.session_state.show_dialog = False
```


### 모달 다이얼로그 구현
```python
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
    </style>
    """, unsafe_allow_html=True)
    
    # 유형 타이틀 및 내용
    st.markdown(f"<h1 style='text-align: center;'>{info['name']}</h1>", unsafe_allow_html=True)
    
    # 이미지, 설명, 버튼 등 구현
```


### 화면 전환 로직
```python
# 현재 페이지에 따라 해당 함수 호출
if st.session_state.show_dialog:
    show_confirm_dialog()

if st.session_state.page == 'index':
    show_index_page()
elif st.session_state.page == 'chat':
    show_chat_page()
```


## 챗봇 유형 정보

| 유형 번호 | MBTI | 설명 |
|---------|------|-----|
| 유형 1 | ESTJ | 냉철한 성격을 가지고 있습니다. |
| 유형 2 | INFP | 감성적이고 창의적인 성격을 가지고 있습니다. |
| 유형 3 | ENFJ | 사교적이고 리더십이 있는 성격을 가지고 있습니다. |
| 유형 4 | INTP | 논리적이고 분석적인 성격을 가지고 있습니다. |
| 유형 5 | ISFJ | 신중하고 배려심이 깊은 성격을 가지고 있습니다. |

## 향후 개선 사항

- 실제 챗봇 API 연동
- 사용자 정의 프롬프트 지원
- 대화 기록 저장 및 불러오기 기능
- 반응형 디자인 개선
- 다크/라이트 테마 지원

## 참고 자료

- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [Streamlit Dialog API 문서](https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog)
- [Streamlit Session State 가이드](https://docs.streamlit.io/library/api-reference/session-state)

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 기여 방법

1. 이슈를 생성하거나 기존 이슈에 참여하세요.
2. 변경사항을 포함한 Pull Request를 보내주세요.
3. 코드 리뷰 후 변경사항이 적용됩니다.
