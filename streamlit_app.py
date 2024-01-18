import streamlit as st
import replicate
import os

#app title
st.set_page_config(page_title = 'Llama Chatbot')

#Replicate Credentials
with st.sidebar:
    st.title('Llama Chatbot')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided',icon='()')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:',type = 'password')
        if not (replicate_api.startwith('r8_') and len(replicate_api)==40):
            st.warning('Please enter a valid API key',icon = ':(')
        else:
            st.success('Proceed to entering your prompt message!')
os.environ['REPLICATE_API_TOKEN'] = replicate_api


#Store LLM Generated Reasonses
if 'messages' not in st.session_state.keys():
    st.session_state.messages = [{'role':'assistant','content':'How may I assist you?'}]

#Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

def clear_chat_history():
    st.session_state.messages = [{'role':'assistant','content':'How may I assist you?'}]
st.sidebar.button('Clear Chat History',on_click = clear_chat_history)

#Function to generate Llama response
def generate_llama_response(prompt):
    string_dialogue = "You are a helpful assistant. You do not respond as user or pretend to be user.You only respond once as an assistant"
    for dict_message in st.session_state.messages:
        if dict_message['role']=='user':
            string_dialogue +='User: ' +dict_message['content'] +"\n\n"
        else:
            string_dialogue += 'Assistant:' + dict_message['content'] +'\n\n'
        output = replicate.run('',input = {'prompt':f"{string_dialogue}{prompt} Assistant:",'temperature':0.1,'top_p':0.9,'max_length':512,'repetition_penalty':1})
        st.session_state.messages.append({'role':'assistant','content':output['generated_text']})
    return output

#User Provided prompt

if prompt :=st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({'role':'user','content':prompt})
    with st.chat_message('user'):
        st.write(prompt)

#generate a new response if the last response not from assistant
        
if st.session_state.messages[-1]['role'] !='assistant':
    with st.chat_message('assistant'):
        with st.spinner('Thinking...'):
            response = generate_llama_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response +=item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {'role':'assistant','content': full_response}
    st.session_state.messages.append(message)