from langchain.chains import ConversationalRetrievalChain

def new_crc_from_llm(model, retriever):
    return ConversationalRetrievalChain.from_llm(model, retriever=retriever)
