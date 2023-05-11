import os
import streamlit as st

apikey = st.secrets["OPENAI_API_KEY"]
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

##### REMEMBER TO SAVEEE! #####

os.environ[
    "OPENAI_API_KEY"
] = apikey  # Setting a dictionary so that we can send the API Key to OpenAI

# pip install streamlit langchain openai wikipedia chromadb tiktoken

# TABS
tab1, tab2 = st.tabs(["Paco", "Menu Completo"])

with tab1:
    # App framework
    st.title("🍻 ¡Birras y Tacos! 🌮")
    st.header("Chatea con Paco, nuestro sugeridor favorito")
    st.divider()

    add_selectbox = st.sidebar.selectbox(
        "How would you like to be contacted?", ("Email", "Home phone", "Mobile phone")
    )
    col1, col2 = st.columns(2)
    with col1:
        prompt = st.text_input("¿Qué te apetece hoy 😏?")
        st.write("Puedes probar cosas como: ")
        st.write("· delicioso y vegetariano ")
        st.write("· algo ligero ")
        st.write("· algo con tomate y queso ")
        st.write(". algo de 6 euros o menos ")

    with col2:
        st.image(
            "https://images.app.goo.gl/FHo81MaycGWWuJSC8", "Nuestros deliciosos tacos"
        )
    # Prompt templates
    title_template = PromptTemplate(
        input_variables=["user_input"],
        template="You are Paco, the best waiter of Beers and tacos. \n \
        You must answer the customers only if the query is related to the restaurant, otherwise just refer them to Mery. \n \
        This is the menu: \n \
            Classic Beef Tacos (7.99€): seasoned ground beef, shredded cheese, lettuce, tomato, sour cream, and salsa served in a warm tortilla \n \
            Grilled Chicken Tacos (6.99€): marinated grilled chicken, avocado, pico de gallo, and queso fresco served in a warm tortilla \n \
            Baja Fish Tacos (9.99€): beer-battered cod, cabbage slaw, chipotle mayo, and lime served in a warm tortilla \n \
            Veggie Tacos (5.99€): roasted sweet potato, black beans, corn, avocado, and cilantro served in a warm tortilla \n \
            Loaded Nachos(10.99€): crispy tortilla chips topped with seasoned ground beef, queso cheese, jalapeños, tomatoes, black olives, and sour cream \n \
            Quesadilla (7.49€): melted cheddar and jack cheese, grilled chicken or steak, sautéed onions and peppers, served with salsa and sour cream \n \
            Char-Grilled Burger(9.49€): 1/3 lb beef patty, lettuce, tomato, pickles, and special sauce on a brioche bun \n \
            Chicken Wings (5.49€): choice of buffalo, honey BBQ, or garlic parmesan served with celery and ranch or blue cheese dressing \n \
            Beer-battered Onion Rings(3.49€): crispy onion rings served with chipotle mayo dipping sauce \n \
            Fried Avocado Bites (2.49€): breaded and fried avocado wedges served with ranch dipping sauce \n \
        Remember to: \n \
            1. be polite and to also include pricing.\n \
            2. include pricing using € \n \
            3. give a detailed description of the dish \n \
            4. explain why do you recommend it \n \
            5. give an alternative \n \
            6. divide each suggestion into a different paragraph \n \
        This is the query of the customer: {user_input}",
    )

    script_template = PromptTemplate(
        input_variables=["title", "restaurant_menu"],
        template="write me a youtube video script based on this title. Title: {title}.  You can leverage this wikipedia research: {restaurant_menu}, as long as your answer has the format of a script",
    )
    director_template = PromptTemplate(
        input_variables=["title", "director"],
        template="Add a very short paragraph explaining why {director} is perfect for the presenter role for the video titled {title}",
    )
    # Memory
    title_memory = ConversationBufferMemory(
        input_key="user_input", memory_key="chat_history"
    )
    script_memory = ConversationBufferMemory(
        input_key="title", memory_key="chat_history"
    )
    # Llms
    llm = OpenAI(temperature=0.4)
    title_chain = LLMChain(
        llm=llm,
        prompt=title_template,
        verbose=True,
        output_key="title",
        memory=title_memory,
    )
    script_chain = LLMChain(
        llm=llm,
        prompt=script_template,
        verbose=True,
        output_key="script",
        memory=script_memory,
    )
    director_chain = LLMChain(
        llm=llm,
        prompt=director_template,
        verbose=False,
        output_key="director_script",
    )
    wiki = WikipediaAPIWrapper()
    # show stuff if there is a prompt
    if prompt:

        title = title_chain.run(prompt)
        # wiki_research = wiki.run(prompt)
        # script = script_chain.run(title=title, restaurant_menu=wiki_research)
        # director = director_chain.run(title=title, director="Enrique")
        print(title)
        st.divider()
        st.write(title)
        st.success("Success message!", icon="✅")
        # st.write(response["title"])
        # st.write(script)
        # st.write(director)
        # with st.expander("Title History"):
        #    st.info(title_memory.buffer)

        # with st.expander("Script History"):
        # st.info(script_memory.buffer)

        # with st.expander("Wikipedia Research History"):
        # st.info(wiki_research)
