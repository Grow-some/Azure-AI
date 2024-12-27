from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from openai import AzureOpenAI

class AzureOpenAI:
    def __init__(self, api_version, azure_endpoint, api_key):
        self.api_version = api_version
        self.azure_endpoint = azure_endpoint
        self.api_key = api_key
        self.client = AzureOpenAI(api_key=self.api_key, api_version=self.api_version, azure_endpoint=self.azure_endpoint)
        
    def chat(self, model, messages):
        return self.client.completions.create(model=model, messages=messages)
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
        print(f"Error: {e}")
        Azure_openai = None
    return Azure_openai

if __name__ == "__main__":
    client = get_openai_client()
    if client is None:
        exit(1)
    print(client)
    print("get_openai_client() is working")