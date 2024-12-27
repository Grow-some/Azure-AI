from flask import Flask, request, jsonify
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import argparse
from openai import AzureOpenAI
import datetime

#   
# 以下のコードは、Azure OpenAIのチャットボットにメッセージを送信し、その結果をファイルに保存するものです。
# コードの実行時には、引数として-nと-cを指定してください。
# -n: 保存するファイル名
# -c: チャットボットに送信するメッセージ
# 例: python chat.py -n result_1 -c "Hello, how are you?"
# 作った背景：OpenAIはちょくちょく障害が発生するため、いつでも生成AIが使えるようにする。

# コマンドライン引数の解析
parser = argparse.ArgumentParser(description="Chat with Azure OpenAI")
parser.add_argument("-n", type=str, help="The filename to save the result")
parser.add_argument("-c", type=str, required=True, help="The message content to send to the chatbot")
args = parser.parse_args()

# 引数-nが指定されていない場合は、現在の日時をファイル名として使用
if args.n is None:
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
else:
    filename = args.n
    
# Azure Key Vaultのクライアントを取得
key_vault_name = "chatbotkey2"
key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_uri, credential=credential)

# シークレットの取得これを使ってAsure OpenAIのクライアントを作成
api_key = client.get_secret("openai-api-key-chatbot").value
api_version = client.get_secret("openai-api-version").value
endpoint = client.get_secret("openai-endpoint").value

# これがクライアント。これでチャットする。
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=api_key
)

# チャットボットにメッセージを送信
chat_response = client.chat.completions.create(
    model="chatbot",
    messages=[
        {"role": "user", "content": args.c},
    ],
)

# 結果をファイルに保存.こっちはメタデータこみ込み
with open(filename + ".txt", 'w', encoding='utf-8') as file:
    file.write(str(chat_response))

# 結果をファイルに保存.こっちはメッセージだけ
with open("result_" + filename + ".txt", 'w', encoding='utf-8') as file:
    file.write(str(chat_response.choices[0].message.content))
    
print(f"{chat_response.usage.total_tokens}トークン使ったよ！")
