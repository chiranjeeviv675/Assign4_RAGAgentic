from agentic_rag_simplified import app

while True:
    user_input = input("Ask your software engineering question: ")
    if user_input.lower() == "exit":
        break

    final_state = app.invoke({"question": user_input})
    print("\n-------------------")
    print("QUESTION:", final_state["question"])
    print("ANSWER:", final_state["answer"])
    print("CRITIQUE:", final_state["critique"])
    print("-------------------")
