import streamlit as st
import pandas as pd
import random

# CSVの読み込み
def load_data():
    df = pd.read_csv('quiz_data.csv')
    return df

# モード選択
def select_mode():
    mode = st.radio("モードを選択してください", ["ランダムモード", "難易度モード"])
    return mode

# ゲームのループ処理
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
        unique_key = f"answer_{question_idx}_{question['question'][:10]}"  # 質問内容の最初の10文字を利用
        user_answer = st.radio("○か×で答えてください", ['○', '×'], key=unique_key)
        
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

# ランダムモード
def random_mode(df):
    st.markdown("### ランダムモード")
    # 問題をシャッフルしてランダムに出題
    df_shuffled = df.sample(frac=1).reset_index(drop=True)
    game_loop(df_shuffled, "ランダムモード")

# 難易度モード
def difficulty_mode(df):
    st.markdown("### 難易度モード")
    difficulty = st.selectbox("難易度を選択してください", ["易しい", "普通", "難しい"])

    # 難易度に応じたフィルタリング
    df_filtered = df[df['difficulty'] == difficulty]
    game_loop(df_filtered, "難易度モード")

# メイン関数
def main():
    # データの読み込み
    df = load_data()

    # モード選択
    mode = select_mode()

    # モードに応じてゲーム開始
    if mode == "ランダムモード":
        random_mode(df)
    elif mode == "難易度モード":
        difficulty_mode(df)

if __name__ == "__main__":
    main()
