import streamlit as st
from openai import OpenAI


class FortuneService:
    """OpenAI API를 이용한 오늘의 운세 서비스"""
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def get_fortune(self, user_birth: str) -> str:
        """생년월일 기반 오늘의 운세 생성"""
        input_text = f"""
        당신은 주역 전문가입니다. 양력 생년월일이 {user_birth}인 사용자에 대해 오늘의 운세를 알려주세요.
        오늘의 운세는 총운, 일/사업, 애정/연예, 재물/금전, 건강/안전 5가지 관점에서 다음 [출력 예] 와 같은 형식으로 간략히 요약해 주세요.

        [출력 예]
        총운 : [오늘의 운세를 종합적으로 요약해 주세요.]\n\n
        일/사업 : [일/사업 관점에서 오늘의 운세를 요약해 주세요.]\n\n
        애정/연예 : [애정/연예 관점에서 오늘의 운세를 요약해 주세요.]\n\n
        재물/금전 : [재물/금전 관점에서 오늘의 운세를 요약해 주세요.]\n\n
        건강/안전 : [건강/안전 관점에서 오늘의 운세를 요약해 주세요.]
        """
        try:
            response = self.client.responses.create(
                model="gpt-5",
                input=input_text
            )
            return response.output_text
        except Exception as e:
            return f"오류 발생: {str(e)}"


class FortuneUI:
    """Streamlit UI 담당"""
    def __init__(self):
        self.api_key = None
        self.user_birth = None

    def render_inputs(self):
        """입력 UI 구성"""
        st.header("오늘의 운세")
        self.api_key = st.text_input("OPENAI API KEY를 입력하세요.", type="password")

        year = st.number_input("출생년도 입력:", min_value=1950, max_value=2010, step=1)
        month = st.number_input("출생월 입력:", min_value=1, max_value=12, step=1)
        day = st.number_input("출생일 입력:", min_value=1, max_value=31, step=1)

        self.user_birth = f"{year}년 {month}월 {day}일"

    def render_result(self, answer: str):
        """결과 UI 출력"""
        st.markdown(f"### 오늘의 운세")
        st.success(answer)


class FortuneApp:
    """운세 앱 실행 관리"""
    def __init__(self):
        self.ui = FortuneUI()
        self.service = None

    def run(self):
        self.ui.render_inputs()

        if st.button("운세 보기"):
            if not self.ui.api_key:
                st.warning("API 키를 입력해주세요.")
                return

            self.service = FortuneService(self.ui.api_key)

            with st.spinner(f"{self.ui.user_birth}생 오늘의 운세를 확인 중..."):
                answer = self.service.get_fortune(self.ui.user_birth)
                self.ui.render_result(answer)


if __name__ == "__main__":
    app = FortuneApp()
    app.run()