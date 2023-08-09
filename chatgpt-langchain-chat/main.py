from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory


if "responses" not in st.session_state:
    st.session_state["responses"] = ["Ho can I assist you?"]
if "requests" not in st.session_state:
    st.session_state["requests"] = []
if "buffer_memory" not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

memory = ConversationBufferWindowMemory(k=1)
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)

conversation = ConversationChain(
    llm=llm,
    memory = memory
)

st.title("Chat")

response_cont = st.container()
spinner_cont = st.container()
text_cont = st.container()

with text_cont:
    query = st.text_input("search: ", key="input")

with spinner_cont:
    if query:
        with st.spinner("typing..."):
            response = conversation.predict(input=query)
        st.session_state.requests.append(query)
        st.session_state.responses.append(response)

with response_cont:
    if st.session_state["responses"]:
        for i in range(len(st.session_state["responses"])):
            message(st.session_state["responses"][i], key=str(i))
            if i < len(st.session_state["requests"]):
                message(st.session_state["requests"][i], is_user=True, key=str(i)+"_user")
            
