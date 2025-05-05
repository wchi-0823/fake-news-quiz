import streamlit as st
import pandas as pd
import random

# CSVファイルの読み込み
@st.cache_data
def load_questions():
    return pd.read_csv("questions.csv")

# 難易度表示（★を数値や記号から変換）
def render_stars(difficulty):
    if pd.isna(difficulty):
        return ""
    if isinstance(difficulty, str) and "★" in difficulty:
        return difficulty
    try:
        return "★" * int(difficulty)
    except:
        return difficulty

# ランダム出題モード
def random_mode(df):
    if 'question_index' not in st.session_state:
        st.session_state.question_index = random.randint(0, len(df) - 1)
        st.session_state.show_result = False

    question = df.iloc[st.session_state.question_index]

    show_question_block(question)

# 難易度選択モード
def level_mode(df):
    level = st.selectbox("難易度を選んでください", ["★", "★★", "★★★"])
    filtered = df[df["difficulty"].apply(lambda x: render_stars(x) == level)]

    if filtered.empty:
        st.warning("この難易度の問題はありません。")
        return

    if 'level_question_index' not in st.session_state:
        st.session_state.level_question_index = random.randint(0, len(filtered) - 1)
        st.session_state.show_result = False

    question = filtered.iloc[st.session_state.level_question_index]
    show_question_block(question, filtered=True)

# 問題の表示と○×の回答処理
def show_question_block(question, filtered=False):
    st.markdown("### SNS投稿")
    st.info(question["post_content"])

    st.markdown(f"**問題**: {question['question']}")
    st.markdown(f"**難易度**: {render_stars(question['difficulty'])}")

    if pd.notna(question["image_url"]) and isinstance(question["image_url"], str):
        st.image(question["image_url"], use_column_width=True)

    user_answer = st.radio("○か×かを選んでください", ("○", "×"), key=f"ans_{random.random()}")

    if st.button("決定"):
        st.session_state.show_result = True
        st.session_state.selected_answer = user_answer

    if st.session_state.get("show_result", False):
        correct = question["answer"]
        if st.session_state.selected_answer == correct:
            st.success("正解！ポイント +1")
        else:
            st.error("不正解！")

        st.markdown(f"**解説**: {question['explanation']}")

        if st.button("次の問題へ"):
            if filtered:
                st.session_state.level_question_index = random.randint(0, len(df[df["difficulty"].apply(lambda x: render_stars(x) == render_stars(question['difficulty']))]) - 1)
            else:
                st.session_state.question_index = random.randint(0, len(df) - 1)
            st.session_state.show_result = False
            st.experimental_rerun()

# メイン関数
def main():
    st.title("🧠 フェイクニュースクイズ")
    st.markdown("○×で答えるフェイクニュース判定クイズです。")

    global df
    df = load_questions()

    mode = st.radio("モードを選んでください", ("ランダム出題", "レベル別出題"))

    if mode == "ランダム出題":
        random_mode(df)
    else:
        level_mode(df)

if __name__ == "__main__":
    main()