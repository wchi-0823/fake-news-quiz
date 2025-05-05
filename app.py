import streamlit as st
import pandas as pd
import random

# CSVを読み込む
@st.cache_data
def load_questions():
    # CSVファイルのパスを適切に設定
    df = pd.read_csv('questions.csv')
    return df

# ゲームの進行管理
def game_loop(df, mode):
    score = 0
    total_questions = len(df)
    question_idx = 0

    while question_idx < total_questions:
        question = df.iloc[question_idx]

        # 投稿文表示
        st.markdown(f"**投稿文**: {question['post_content']}")
        
        # 問題表示
        st.markdown(f"**問題**: {question['question']}")
        
        # 画像があれば表示
        if pd.notna(question['image_url']):
            st.image(question['image_url'], use_column_width=True)
        
        # ユーザーの回答選択
        user_answer = st.radio("○か×で答えてください", ['○', '×'], key=f"answer_{question_idx}")
        
        if st.button(f'答えを確認 ({question_idx+1}/{total_questions})'):
            # 正誤判定
            correct = question['answer'] == user_answer
            if correct:
                score += 10  # 正解時は得点加算
                st.markdown("**正解です！！**")
            else:
                st.markdown("**不正解です！！**")
            
            # 解説文表示
            st.markdown(f"**解説**: {question['explanation']}")
            
            # 次の問題へ
            question_idx += 1

            if question_idx == total_questions:
                st.markdown("### ゲーム終了！")
                st.markdown(f"**総合得点**: {score}点")
                break

# モード選択
def mode_selection():
    mode = st.radio("モード選択", ["ランダムモード", "難易度モード"])
    return mode

# 難易度フィルタリング
def filter_by_difficulty(df, difficulty):
    if difficulty != "全て":
        return df[df['difficulty'] == difficulty]
    return df

# メイン
def main():
    st.title("フェイクニュース発見クイズ")

    # モード選択
    mode = mode_selection()

    # 難易度選択（難易度モードの場合）
    difficulty = "全て"  # 初期値
    if mode == "難易度モード":
        difficulty = st.selectbox("難易度を選択", ["全て", "簡単", "普通", "難しい"])

    # CSVから問題を読み込む
    df = load_questions()

    # 難易度フィルタリング
    df_filtered = filter_by_difficulty(df, difficulty)

    # ゲームスタート
    if st.button('ゲームスタート'):
        game_loop(df_filtered, mode)

if __name__ == "__main__":
    main()