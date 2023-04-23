import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain import OpenAI

# Session State. Con esto podemos salvar las variables para guardar información
if 'generated' not in st.session_state:
    st.session_state['generated'] = [] #output
if 'past' not in st.session_state:
    st.session_state['past'] = [] #los vamos a guardar como el pasado
if 'input' not in st.session_state:
    st.session_state['input'] = "" # Es como un diccionario 
if 'stored_session' not in st.session_state:
    st.session_state['stored_session'] = []

# Funcion para recibir un input
def get_text():
    """
    Get the user input text.
    Returns:
        (str): The text entered by the user
    """
    input_text = st.text_input("You: ",
                               st.session_state["input"],
                               key="input", 
                               placeholder= "Your AI assitant here! Ask me anything ...",
                               label_visibility='hidden'
                               )
    return input_text 

st.title('Memory bot')
api = st.sidebar.text_input("API-Key", type= "password")

if api:
     # Creat instancia de Openai
     llm = OpenAI(
         temperature= 0.0,
         openai_api_key=api,
         model_name="gpt-3.5-turbo"
     )

    # Crear la memoria de la conversación
     if 'entity_memory' not in st.session_state:
         st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k =10)
     Conversation = ConversationChain(
        llm=llm, 
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory = st.session_state.entity_memory
    ) 
else:
    st.error('No API found')

# Aplicación
user_input = get_text()

# Generamos la conversación
if user_input:
    output = Conversation.run(input=user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

with st.expander("Conversation"):
    for i in range(len(st.session_state['generated']) -1,-1,-1):
        st.info(st.session_state["past"][i],icon="🧑‍💻")
        st.success(st.session_state["generated"][i], icon = "✨")
     
