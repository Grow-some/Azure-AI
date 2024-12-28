# チャットAPIWEBアプリ
ChatGPTで障害が発生したとき、チャット出来なくなり困ったのでAzureのリソース構築で乗り切ったアプリ

# 使い方
1. `git clone`を使ってこのソースを取得する。
2. AzureでLLMをデプロイする。
   `az login`
   ```
    az cognitiveservices account deployment create `
    -g AI_agent_service `
    -n home-service `
    --deployment-name CLI_model `
    --model-name gpt-4o `
    --model-format OpenAI `
    --model-version "2024-08-06" `
    --sku-capacity 10 `
    --sku-name "GlobalStandard" `
    --debug
   ```
3. Azureでapikeyなどの機密データをkeyvaultに登録する。詳細はソースを確認すること。
    ```
    az keyvault secret set `
    --vault-name "chatbotkey2" `
    --name "openai-api-key-chatbot" `
    --value "" `
    --debug
    ```
4. `apt install apache2`を使ってWEBサービスを立ち上げる。
5. 設定をstreamlitに合わせて書き換える。
6. streamlitをサービス化する。
7. streamlit →apache2の順で起動する。