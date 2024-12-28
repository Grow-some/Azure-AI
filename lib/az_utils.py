from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from openai import AzureOpenAI

# Azure Key Vaultのクライアントを取得
def get_key_vault_client():
    key_vault_name = "chatbotkey2"
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    client_vault = SecretClient(vault_url=key_vault_uri, credential=credential)
    return client_vault

def get_openai_client():
    client_vault = get_key_vault_client()
    # シークレットの取得これを使ってAsure OpenAIのクライアントを作成
    api_key = client_vault.get_secret("openai-api-key-chatbot").value
    api_version = client_vault.get_secret("openai-api-version").value
    endpoint = client_vault.get_secret("openai-endpoint").value
    
    try:   
        Azure_openai = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key
        )
    except Exception as e:
        Azure_openai = None
    return Azure_openai