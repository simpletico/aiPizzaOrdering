import os
import tempfile, requests, re, json
import streamlit as st
from streamlit_chat import message
from chat_openai import chatBot
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

API_URL = 'http://localhost:3000/order' 
st.set_page_config(page_title="Pizza Ordering")
confirmationModel = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            agent_text = st.session_state["assistant"].ask(query = user_text)
            agent_text = checkOrderCompletion(agent_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))

    st.session_state["user_input"] = ""

def checkOrderCompletion(responseText : str):
    if ("Your Order Summary" in responseText) and (confirmOrderSummary(responseText)):
        processOrderRequest(responseText)
    return responseText


def processOrderRequest(responseText : str):
    print( "processing order request:", responseText)
    try:
        oType = re.search(r'\n- Type: (.*)\n', responseText).group(0).split(':')[1].strip()
    except:
        oType = 'None'
    try: 
        oSize = re.search(r'\n- Size: (.*)\n', responseText).group(0).split(':')[1].strip()
    except:
        oSize = 'None' 
    try:
        oToppings = re.search(r'\n- Toppings: (.*)\n', responseText).group(0).split(':')[1].strip()
    except:
        oToppings = 'None'
    try:
        oExtras = re.search(r'\n- Extras: (.*)\n', responseText).group(0).split(':')[1].strip()
    except:
        oExtras = 'None'
    try:
        oDrinks = re.search(r'\n- Drinks: (.*)\n', responseText).group(0).split(':')[1].strip() 
    except:
        oDrinks = 'None'

    jsonText = f"{{\"Type\": \"{oType}\", \"Size\": \"{oSize}\", \"Toppings\": \"{oToppings}\", \"Extras\": \"{oExtras}\", \"Drinks\": \"{oDrinks}\"}}"
    print("json order for request:", jsonText)
    r = requests.post(API_URL, json=json.loads(jsonText))

def confirmOrderSummary(orderText : str):
    print( "confirming order with AI")
    botConfirmation = confirmationModel.invoke([
        HumanMessage(
            content = f"""
                Your task is to confirm that the following text includes an order summary in the following format: 'Your Order Summary' : - Type: [pizza type] - Size: [pizza size] - Extras: [extras] - Toppings: [toppings] - Drinks: [drinks]
                you should answer only with 'yes' or 'no'

                Here are some examples:
                Text: Your Order Summary : - Type: pepperoni pizza - Size: medium - Extras: fries large, greek salad - Toppings: mushrooms, sausage, canadian bacon - Drinks: coke
                Answer: 'yes'

                Text: Your Order Summary : 
                - Type: cheese pizza 
                - Size: large 
                - Toppings: canadian bacon 
                - Extras: greek salad 
                - Drinks: coke, sprite
                Answer: 'yes'

                Text: Your Order Summary : - Type: pepperoni pizza - Size: medium - Toppings: Not specified - Extras: None - Drinks: coke
                Answer: 'yes'

                Text: Thank you for your order, your order is confirmed 
                Answer: 'no'

                Text: Your Order Summary : A small pepperoni pizza with  large fries and greek salad, adding mushrooms, sausage and canadian bacon with coke
                Answer: 'no'

                Text: {orderText}
                Answer:
            """
        )
    ])
        
    print(f"AI response for confirmation: {botConfirmation.content}")

    if "yes" in botConfirmation.content:
        return True
    
    if "no" in botConfirmation.content:
        print(f" --- Confirmation fail for Text: {orderText}") 

    return False


def page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["assistant"] = chatBot()

    st.header("Pizza Ordering Chatbot")

    display_messages()
    st.text_input("Message", key="user_input", on_change=process_input)


if __name__ == "__main__":
    page()
