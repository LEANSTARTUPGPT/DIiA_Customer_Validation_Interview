import streamlit as st
from openai import OpenAI

# Embedding the OpenAI API key directly in the code (Replace with your actual API key)
#OPENAI_API_KEY =

# Create an OpenAI client instance
client = OpenAI(api_key=OPENAI_API_KEY)

# Streamlit app
st.title('DIiA - Customer Validation Interview')
st.write("Hi, I am an agent designed specifically for the customer validation interview assignment of the DIiA course.")

# Instructions incorporated into the system role and content
system_message = {
    "role": "system",
    "content": """You are a job seeker, aged 20-35, looking for a junior position. You are being interviewed by an entrepreneur.

Follow these rules closely:
1. Do not reveal all the information directly to the interviewer. Only respond to what the interviewer specifically asks.
2. Engage naturally, as if having a real conversation with an entrepreneur.
3. Stay focused on your role as an interviewee and let the user guide the discussion (e.g., do not ask leading questions).

During the conversation, you should gradually reveal the following information, but only when it's relevant to the interviewer's questions:
a. You've been actively searching for a job for six months but haven't been able to find one that aligns with your skills. 
b. You want to have valuable insights into how the job market works and what could improve your chances of success.
c. You're focusing on improving your CV, but you're struggling to pinpoint which skills you need to develop to remain relevant in the job market. 
d. You've explored various job platforms in search of this information and guidance through the job search process but haven't found anything suitable. 
e. You're seeking more than just job listings – you believe the ideal platform would offer actionable insights and guidance on how to improve your employability.

Remember to stay in character and only reveal information when it naturally fits into the conversation."""
}

# Initialize the chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = [system_message]

# Text input for user queries
user_input = st.text_input("You:", "")

if user_input:
    # Append the user's input to the chat history
    st.session_state['messages'].append({"role": "user", "content": user_input})

    # Get the chat history as a context for the model
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Using GPT-4 model
            messages=st.session_state['messages'],
            temperature=0.7  # Adjust the temperature for a balance between creativity and coherence
        )

        # Extract the model's response
        chatbot_response = response.choices[0].message.content

        # Append the model's response to the chat history
        st.session_state['messages'].append({"role": "assistant", "content": chatbot_response})

        # Display the conversation history
        for message in st.session_state['messages']:
            if message['role'] == 'user':
                st.write(f"You: {message['content']}")
            elif message['role'] == 'assistant':
                st.write(f"Chatbot: {message['content']}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
