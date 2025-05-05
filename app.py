import streamlit as st
import pandas as pd
import random

# CSVの読み込み
def load_questions():
    df = pd.read_csv("questions.csv")
    return df

# 数値を星（★）に変換
def get_stars(difficulty):
    """難易度に基づいて星の数を返す"""
    return "★" * difficulty

# ランダムモード
def random_mode(questions_df):
    # ランダムに問題を選択
    question = random.choice(questions_df.to_dict(orient="records"))
    
    # SNS風の投稿表示
    st.write(f"**SNS投稿**: {question['post_content']}")
    
    # 問題文表示
    st.write(f"**問題**: {question['question_text']}")
    
    # 難易度表示（星★で表示）
    stars = get_stars(int(question['difficulty']))  # 数値を★に変換
    st.write(f"**難易度**: {stars}")

    # 画像の表示（URLがあれば）
    if pd.notna(question['image_url']):
        st.image(question['image_url'], caption="問題に関連する画像", use_column_width=True)
    
    # ユーザーの回答選択
    answer = st.radio("答えを選んでください:", ("◯", "✕"))
    
    if answer:
        # 正誤判定
        if answer == question['answer']:
            st.success("正解！")
        else:
            st.error("不正解...")
        
        # 解説表示
        st.write(f"**解説**: {question['explanation']}")
        
        # 次の問題へボタン
        if st.button("次の問題へ"):
            random_mode(questions_df)

# レベル別モード
def level_mode(questions_df, level):
    # レベル別に問題をフィルタリング
    filtered_questions = questions_df[questions_df['difficulty'] == level]
    
    # 問題が無ければ、メッセージを表示
    if filtered_questions.empty:
        st.write("このレベルには問題がありません。")
        return

    # ランダムに問題を選択
    question = random.choice(filtered_questions.to_dict(orient="records"))
    
    # SNS風の投稿表示
    st.write(f"**SNS投稿**: {question['post_content']}")
    
    # 問題文表示
    st.write(f"**問題**: {question['question_text']}")
    
    # 難易度表示（星★で表示）
    stars = get_stars(int(question['difficulty']))  # 数値を★に変換
    st.write(f"**難易度**: {stars}")

    # 画像の表示（URLがあれば）
    if pd.notna(question['image_url']):
        st.image(question['image_url'], caption="問題に関連する画像", use_column_width=True)
    
    # ユーザーの回答選択
    answer = st.radio("答えを選んでください:", ("◯", "✕"))
    
    if answer:
        # 正誤判定
        if answer == question['answer']:
            st.success("正解！")
        else:
            st.error("不正解...")
        
        # 解説表示
        st.write(f"**解説**: {question['explanation']}")
        
        # 次の問題へボタン
        if st.button("次の問題へ"):
            level_mode(questions_df, level)

# メインアプリケーション
def main():
    # CSVデータの読み込み
    questions_df = load_questions()

    # モード選択
    mode = st.radio("モードを選んでください", ("ランダム", "レベル別"))
    
    if mode == "ランダム":
        random_mode(questions_df)
    elif mode == "レベル別":
        level = st.selectbox("レベルを選んでください", ("1", "2", "3"))
        level_mode(questions_df, int(level))

# アプリ実行
if __name__ == "__main__":
    main()