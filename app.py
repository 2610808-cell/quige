import streamlit as st
import random
import time

# ------------------------
# 문제 생성 함수
# ------------------------
def generate_question(level):

    if level == 1:
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)

        question = f"{num1} + {num2}"
        answer = num1 + num2
        solution = f"{num1} + {num2} = {answer}"

    elif level == 2:
        num1 = random.randint(-20, -1)
        num2 = random.randint(1, 20)

        question = f"({num1}) + ({num2})"
        answer = num1 + num2

        solution = (
            f"부호가 다를 때는 큰 수에서 작은 수를 빼고\n"
            f"큰 수의 부호를 붙여요.\n"
            f"{num2} - {abs(num1)} = {answer}"
        )

    elif level == 3:
        base = random.randint(2, 5)
        expo = random.randint(2, 4)

        question = f"{base}^{expo}"
        answer = base ** expo

        process = " × ".join([str(base)] * expo)
        solution = f"{process} = {answer}"

    return {
        "question": question,
        "answer": answer,
        "solution": solution
    }


# ------------------------
# 세션 상태 초기화
# ------------------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "question_count" not in st.session_state:
    st.session_state.question_count = 0

if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "wrong_answers" not in st.session_state:
    st.session_state.wrong_answers = []

# ------------------------
# 제목
# ------------------------
st.title("🧠 수학 퀴즈 게임")

st.write("난이도를 선택하고 문제를 풀어보세요!")

# ------------------------
# 난이도 선택
# ------------------------
level = st.selectbox(
    "난이도 선택",
    [1, 2, 3],
    format_func=lambda x: {
        1: "1️⃣ 쉬운 덧셈",
        2: "2️⃣ 음수 계산",
        3: "3️⃣ 거듭제곱"
    }[x]
)

# ------------------------
# 새 문제 생성
# ------------------------
if st.button("🎲 새 문제 만들기"):

    st.session_state.quiz = generate_question(level)
    st.session_state.start_time = time.time()

# ------------------------
# 문제 표시
# ------------------------
if st.session_state.quiz:

    q = st.session_state.quiz

    st.subheader(f"❓ 문제")
    st.write(q["question"])

    user_answer = st.text_input("정답 입력")

    if st.button("정답 확인"):

        try:
            elapsed = round(
                time.time() - st.session_state.start_time,
                2
            )

            if int(user_answer) == q["answer"]:

                st.success(
                    f"🎉 정답입니다! ({elapsed}초)"
                )

                st.session_state.score += 1

            else:
                st.error("❌ 틀렸습니다.")

                st.write(f"정답: {q['answer']}")

                st.info(f"💡 풀이\n\n{q['solution']}")

                st.session_state.wrong_answers.append(q)

            st.session_state.question_count += 1

        except:
            st.warning("숫자를 입력하세요!")

# ------------------------
# 점수 표시
# ------------------------
st.divider()

st.subheader("📊 현재 기록")

st.write(f"점수: {st.session_state.score}")
st.write(f"푼 문제 수: {st.session_state.question_count}")

# ------------------------
# 오답노트
# ------------------------
if st.session_state.wrong_answers:

    st.subheader("📚 오답노트")

    for idx, wrong in enumerate(
        st.session_state.wrong_answers,
        1
    ):

        st.write(f"{idx}. {wrong['question']}")
        st.write(f"정답: {wrong['answer']}")
        st.write(f"풀이: {wrong['solution']}")

        st.divider()
