import streamlit as st
import lib.az_utils as az_utils

def main():
    # Get Azure OpenAI client
    client = az_utils.get_openai_client()
    if client is None:
        st.write("Error: Azure OpenAI client is not available.")
        exit(1)
    # Initialize session state
    init()
    # Streamlit App
    streamlit_app(client)

def init():
    # メモリ上にチャットデータを保存
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}  # チャットID: メッセージ履歴
    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = None
    if "last_response_id" not in st.session_state:
        st.session_state.last_response_id = {}  # 前回の応答ID

def clear_text():
    # Set a separate flag for clearing the input box
    st.session_state.clear_input = True

def streamlit_app(client):
    # Title
    st.title("Chat Agent")
    # Subheader
    st.subheader("Welcome to the Chat Agent")
    # サイドバー: チャットIDを表示
    with st.sidebar:
        st.title("チャット一覧")
        chat_ids = list(st.session_state.chat_history.keys())
        
        # チャットIDをクリックで選択
        for chat_id in chat_ids:
            if st.button(chat_id):
                st.session_state.current_chat_id = chat_id
                st.rerun()  # 再描画
        
        # 新しいチャットを開始
        if st.button("新しいチャットを開始"):
            new_chat_id = f"チャット{len(chat_ids) + 1}"
            st.session_state.chat_history[new_chat_id] = {}
            st.session_state.current_chat_id = new_chat_id
            st.rerun()  # 再描画
            
    # メイン画面: メッセージ履歴と入力ボックス
    if st.session_state.current_chat_id:
        chat_id = st.session_state.current_chat_id
        st.title(f"チャットID: {chat_id}")

        # メッセージ履歴を表示
        st.subheader("メッセージ履歴")
        for response_id, messages in st.session_state.chat_history[chat_id].items():
            for message in messages:
                if message["role"] == "user":
                    st.markdown(f"**ユーザー**: {message['content']}")
                elif message["role"] == "assistant":
                    st.markdown(f"**アシスタント**: {message['content']}")

        # メッセージ入力ボックス
        user_input = st.text_input(
            "メッセージを入力してください",
            value="" if st.session_state.get("clear_input") else None,
            key="user_input",
            on_change=lambda: st.session_state.pop("clear_input", None)
        )
        if st.button("送信"):
            if user_input and user_input.strip():
                last_response_id = st.session_state.last_response_id.get(chat_id, None)
                messages = [
                    {"role": "system", "content": f"チャットID: {chat_id} - 利用者からの質問に答えてください。前回の応答IDからコンテキストを理解してください。"},
                    {"role": "user", "content": user_input},
                ]
                if last_response_id:
                    messages.insert(1, {"role": "system", "content": f"前回の応答ID: {last_response_id}"})
                
                print(messages)
                result = client.chat.completions.create(
                    model="chatbot",
                    messages=messages,
                    stream=False
                )
                print(result)
                if result:
                    response_id = result.id
                    bot_response = result.choices[0].message.content
                    if chat_id not in st.session_state.chat_history:
                        st.session_state.chat_history[chat_id] = {}
                    if response_id not in st.session_state.chat_history[chat_id]:
                        st.session_state.chat_history[chat_id][response_id] = []
                    st.session_state.chat_history[chat_id][response_id].append({"role": "user", "content": user_input})
                    st.session_state.chat_history[chat_id][response_id].append({"role": "assistant", "content": bot_response})
                    st.session_state.last_response_id[chat_id] = response_id  # 前回の応答IDを更新
                
                clear_text()  # 入力ボックスをリセット
                st.rerun()
    else:
        st.write("左側からチャットIDを選択するか、新しいチャットを開始してください。")

    st.text("ソースは随時公開中です。")
    st.markdown("[GitHub Repository](https://github.com/Grow-some/Azure-AI)")

if __name__ == "__main__":
    main()
