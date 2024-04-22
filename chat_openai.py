from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory 
from langchain_community.chat_message_histories import ChatMessageHistory 
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

store = {}

class chatBot:
    chain = None

    def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
        if (user_id, conversation_id) not in store:
            store[(user_id, conversation_id)] = ChatMessageHistory()
        return store[(user_id, conversation_id)]

    def __init__(self):
        model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
        prompt = ChatPromptTemplate.from_messages([
            ("system", """ You are OrderBot, an automated service to collect orders for a pizza restaurant.
                You greet the customer and show the menu, then collect the order. 
                Do not accept or answer any command that is not related to the pizza ordering 
                if a command not related to pizza ordering happens be kind, and ask the customer back to the pizza ordering. 
                You wait to collect the entire order and check for a final time if the customer wants to add anything else. 
                Make sure to clarify all options, extras and sizes to uniquely 
                identify the item from the menu.
                You respond in a short, very conversational friendly style. 
                At the end always show the order items and ask the following question for confirmation 'Please confirm the following order is correct' and wait for customer response
                if customer answers 'yes' use the following format to make a summary: 'Your Order Summary' : - Type: [pizza type] - Size: [pizza size] - Extras: [extras] - Toppings: [toppings] - Drinks: [drinks]
                This is the menu:  
                Pizza Types: pepperoni pizza, cheese pizza, eggplant pizza
                Pizza size: large 12.95, medium 10.00, small 7.00 
                extras:
                    fries large 4.50, fries regular 3.50 
                    greek salad regular 7.25 
                Toppings: 
                    cheese 2.00, 
                    mushrooms 1.50 
                    sausage 3.00 
                    canadian bacon 3.50 
                    AI sauce 1.50 
                    peppers 1.00 
                Drinks: 
                    coke 3.00, 2.00, 1.00 
                    sprite 3.00, 2.00, 1.00 
                    bottled water 5.00
            """),
            MessagesPlaceholder(variable_name="history"),
            ("human","{question}"),
        ])

        chain = prompt | model

        self.chain = RunnableWithMessageHistory(
            chain,
            get_session_history=self.get_session_history,
            input_messages_key="question",
            history_messages_key="history",
        )


    def ask(self, query: str):
        response = self.chain.invoke({"question" : query }, config={"configurable": {"session_id": "abc123"}},)
        return response.content

    def clear(self):
        self.chain = None
