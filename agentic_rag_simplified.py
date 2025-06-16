import json
import chromadb
import config_secrets as secrets
from openai import AzureOpenAI
from langgraph.graph import StateGraph
from typing import TypedDict

# Azure OpenAI Client
client = AzureOpenAI(
    api_key=secrets.AZURE_OPENAI_API_KEY,
    api_version=secrets.AZURE_OPENAI_API_VERSION,
    azure_endpoint=secrets.AZURE_OPENAI_ENDPOINT
)

# Load Chroma
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("kb_index")

# Define schema
class WorkflowState(TypedDict):
    question: str
    answer: str
    critique: str

# Node functions
def retrieve_kb(state):
    try:
        # Query the collection for relevant documents
        results = collection.query(
            query_texts=[state["question"]],
            n_results=3
        )
        
        # Combine retrieved answers
        retrieved_answer = "Based on the knowledge base: " + " ".join(results.get('documents', [[]])[0])
        return {"question": state["question"], "answer": retrieved_answer, "critique": ""}
    except Exception as e:
        print(f"Error in retrieve_kb: {str(e)}")
        return {"question": state["question"], "answer": "Error retrieving information", "critique": ""}


def generate_answer(state):
    try:
        completion = client.chat.completions.create(
            deployment_id=secrets.AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides accurate software engineering answers."},
                {"role": "user", "content": f"Question: {state['question']}\nContext: {state['answer']}\nProvide a comprehensive answer."}
            ]
        )
        generated_answer = completion.choices[0].message.content
        return {"question": state["question"], "answer": generated_answer, "critique": ""}
    except Exception as e:
        print(f"Error in generate_answer: {str(e)}")
        return {"question": state["question"], "answer": "Error generating answer", "critique": ""}


def critique_answer(state):
    return {"question": state["question"], "answer": state["answer"], "critique": "Needs refinement"}

def refine_answer(state):
    return {"question": state["question"], "answer": f"Refined answer for: {state['question']}", "critique": state["critique"]}

def decide_if_refine(state):
    if "REFINE" in state["critique"].upper():
        return "refine"
    return "complete"

# Build LangGraph
workflow = StateGraph(schema=WorkflowState)

workflow.add_node("retrieve_kb", retrieve_kb)
workflow.add_node("generate_answer", generate_answer)
workflow.add_node("critique_answer", critique_answer)
workflow.add_node("refine_answer", refine_answer)
workflow.add_node("end", lambda state: state)    # safe terminal node

workflow.set_entry_point("retrieve_kb")

workflow.add_edge("retrieve_kb", "generate_answer")
workflow.add_edge("generate_answer", "critique_answer")
workflow.add_edge("refine_answer", "end")   # <-- move this BEFORE conditional_edges

workflow.add_conditional_edges("critique_answer", decide_if_refine, {
    "refine": "refine_answer",
    "complete": "end"
})
workflow.set_finish_point("end")
app = workflow.compile()
