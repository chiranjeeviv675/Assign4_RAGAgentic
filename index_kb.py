import json
import chromadb
import config_secrets as secrets


from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=secrets.AZURE_OPENAI_API_KEY,
    api_version=secrets.AZURE_OPENAI_API_VERSION,
    azure_endpoint=secrets.AZURE_OPENAI_ENDPOINT,
    default_headers={"User-Agent": "agentic-rag"}
)



chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("kb_index")

with open("self_critique_loop_dataset.json", "r") as f:
    data = json.load(f)

for entry in data:
    response = client.embeddings.create(
        deployment_id=secrets.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        input=entry["answer_snippet"]
    )
    embedding = response.data[0].embedding

    collection.add(
        ids=[entry['doc_id']],
        embeddings=[embedding],
        metadatas=[{
            "source": entry["source"],
            "last_updated": entry["last_updated"],
            "confidence_indicator": entry["confidence_indicator"]
        }],
        documents=[entry["answer_snippet"]]
    )

print("All records indexed successfully")
