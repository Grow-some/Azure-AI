import os
import streamlit as st
def main():
    # アプリのタイトル
    st.title("Streamlitで作る簡単なWebアプリ")

    # ユーザーからの入力を受け付ける
    name = st.text_input("名前を入力してください：")

    # ボタンを表示してアクションを設定
    if st.button("挨拶する"):
        st.write(f"こんにちは、{name}さん！")

    # スライダーで数値を選択
    age = st.slider("年齢を選択してください：", 0, 100, 25)
    st.write(f"あなたの年齢は {age} 歳です。")



if __name__ == "__main__":
    main()