import os
import streamlit as st
import time
import streamlit.components.v1 as components
import re

apikey = st.secrets["OPENAI_API_KEY"]
propmpt_template1 = st.secrets["prompt_template1"]
propmpt_template2 = st.secrets["prompt_template2"]
fake_answer = st.secrets["fake_answer"]
# food_images = st.secrets["food_images"]
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper
from langchain.callbacks import get_openai_callback

food_images = {
    "tacos de ternera clásicos": "https://drive.google.com/uc?export=view&id=17RzYwLWvEIYy99AQ064guCIWx7XgjkrX",
    "tacos de pollo a la parrilla": "https://drive.google.com/uc?export=view&id=17RzYwLWvEIYy99AQ064guCIWx7XgjkrX",
    "baja fish tacos": "https://drive.google.com/uc?export=view&id=17RzYwLWvEIYy99AQ064guCIWx7XgjkrX",
    "veggie tacos": "https://drive.google.com/uc?export=view&id=17RzYwLWvEIYy99AQ064guCIWx7XgjkrX",
    "nachos cargados": "https://drive.google.com/uc?export=view&id=1OsX--f4iCrWcluxLmCWQ628HpJpwqBmI",
    "quesadilla": "https://drive.google.com/uc?export=view&id=1CVK6ZiKQbEV1Ev4C5COe9QI90EcBD42t",
    "hamburguesa a la brasa": "https://drive.google.com/uc?export=view&id=1SGA2ccyiuaiDwUoHtrq-EPTWJ1n6C6gv",
    "alitas de pollo": "https://drive.google.com/uc?export=view&id=12SystKdDfoNBvu6PE7j88Uvy2cOWTjzd",
    "aros de cebolla rebozados con cerveza": "https://drive.google.com/uc?export=view&id=1HIofkJJkBiik4Jvs86WhGEgRjEPBB_8q",
    "fried avocado bites": "https://drive.google.com/uc?export=view&id=1D87paeSaif7pw9jtT5ZoRLnwdmbleyY_",
}
food_prices = {
    "tacos de ternera clásicos": "7,99€",
    "tacos de pollo a la parrilla": "6,99€",
    "baja fish tacos": "9,99€",
    "veggie tacos": "5,99€",
    "nachos cargados": "10,99 €",
    "quesadilla": "7,49€",
    "hamburguesa a la brasa": "9,49€",
    "alitas de pollo": "5,49€",
    "aros de cebolla rebozados con cerveza": "3,49€",
    "fried avocado bites": "2,49€",
}
##### REMEMBER TO SAVEEE! #####
##### Custom Functions


def image_parser(answer, food_images):
    recomendations = re.findall(r"\[.*?\]", answer)

    for dish in recomendations:
        dish_aux = dish.replace("[", "")
        dish_aux = dish_aux.replace("]", "")
        dish_aux = dish_aux.lower()
        split_answer = answer.split(sep=dish, maxsplit=1)
        print(split_answer)
        split_answer_aux = split_answer[0]
        if split_answer_aux[0:2] == ". ":
            split_answer_aux = split_answer_aux.replace(". ", "", 1)
        if split_answer_aux[0:2] == ", ":
            split_answer_aux = split_answer_aux.replace(", ", "", 1)
        st.markdown(
            split_answer_aux.strip().capitalize() + " **" + dish_aux.title() + "**",
            unsafe_allow_html=True,
        )
        container = st.container()
        with container:
            col1, col2, col3, col4 = st.columns(4)
            with col2:
                st.components.v1.iframe(
                    src=food_images[dish_aux],
                    width=150,
                    height=150,
                )
            with col3:
                st.subheader(food_prices[dish_aux])
        print(dish_aux)
        print(food_images[dish_aux])
        answer = split_answer[1]
    split_answer = answer.split(sep=recomendations[-1], maxsplit=1)
    split_answer_aux = split_answer[-1]
    if split_answer_aux[0:2] == ". ":
        split_answer_aux = split_answer_aux.replace(". ", "", 1)
    st.markdown(split_answer_aux.strip().capitalize(), unsafe_allow_html=True)


os.environ[
    "OPENAI_API_KEY"
] = apikey  # Setting a dictionary so that we can send the API Key to OpenAI

# pip install streamlit langchain openai wikipedia chromadb tiktoken

###### Hide Menu
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
# add_selectbox = st.sidebar.selectbox(
#        "How would you like to be contacted?", ("Email", "Home phone", "Mobile phone")
#    )

####### TABS
tab1, tab2 = st.tabs(["Sugeridor", "Menu Completo"])

####### TAB1
with tab1:
    # App framework
    prompt_is_filled = False
    st.subheader("🍻 Birras y Tacos 🌮", anchor=False)

    ###### Customer Inputs
    col1, col2 = st.columns([3, 1])

    with col1:
        prompt = st.text_input(
            "¿Qué te apetece hoy?",
            max_chars=80,
            placeholder="Algo fresco",
            label_visibility="collapsed",
        )
    ###### Number of people
    with col2:
        num_people = st.selectbox(
            "¿Para cuántas personas?",
            (
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10+",
                "Núm. Personas",
            ),
            label_visibility="collapsed",
            index=10,
        )
    if num_people == 1:
        propmpt_num_people = ""
    else:
        propmpt_num_people = ". Para " + num_people + "personas"

    search = st.button("**¡Pregunta a nuestro sugeridor!**", type="secondary")
    if prompt == "":
        # st.divider()
        st.write("Puedes preguntar cosas como: ")
        col1, col2 = st.columns(2)
        with col1:
            st.button("Algo delicioso y vegetariano ")
            st.button("Algo ligero ")
            st.button("Una cerveza de trigo y de importación ")
        with col2:
            st.button("Algo con tomate y queso ")
            st.button("Algo de 6 euros o menos ")
            st.button("Algo para compartir ")

    ###### Prompt templates
    title_template = PromptTemplate(
        input_variables=["user_input"],
        template=propmpt_template1
        + "Esta es la petición del cliente: {user_input}"  # "This is the query of the customer:
        + propmpt_template2
        + propmpt_num_people,
    )
    script_template = PromptTemplate(
        input_variables=["title"],
        template="Devuelve el siguiente texto corregido gramaticalmente, excepto que está entre corchetes []: \n{title}",
    )
    director_template = PromptTemplate(
        input_variables=["title", "director"],
        template="Add a very short paragraph explaining why {director} is perfect for the presenter role for the video titled {title}",
    )
    ###### Memory
    title_memory = ConversationBufferMemory(
        input_key="user_input", memory_key="chat_history"
    )
    script_memory = ConversationBufferMemory(
        input_key="title", memory_key="chat_history"
    )
    ###### Llms
    llm = OpenAI(temperature=0.4)
    title_chain = LLMChain(
        llm=llm,
        prompt=title_template,
        verbose=False,
        output_key="title",
        memory=title_memory,
    )
    script_chain = LLMChain(
        llm=llm,
        prompt=script_template,
        verbose=False,
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
    ###### show stuff if there is a prompt
    if prompt:
        prompt_is_filled = True
    if prompt_is_filled:
        # title = fake_answer
        print(prompt)
        with get_openai_callback() as cb:
            title = title_chain.run(prompt)
            # title = script_chain.run(title=title)
            print(cb)

        ###### Progress bar

        # progress_text = "Preguntando a Paco...😋"
        # my_bar = st.progress(0, text=progress_text)
        st.divider()
        # for percent_complete in range(100):
        #    time.sleep(0.01)
        #    progress_text = f"Preguntando a Paco... {percent_complete+1}% 😋"
        #    my_bar.progress(percent_complete + 1, text=progress_text)

        # wiki_research = wiki.run(prompt)
        # script = script_chain.run(title=title, restaurant_menu=wiki_research)
        # director = director_chain.run(title=title, director="Enrique")

        ###### Format Output
        answer = title.replace(";", ".")
        # answer = answer.replace("[", "**")
        # answer = answer.replace("]", "**")
        if answer[0:2] == ", ":
            answer = answer.replace(", ", "", 1)

        answer = answer.capitalize()
        phrases = answer.split(sep=".")
        print(phrases)
        answer = ""
        for phrase in phrases:
            answer = answer + ". " + phrase.strip().capitalize()
        answer = answer.replace(". ", "", 1)
        answer = answer.replace(". ", ". <br>")
        print(answer)
        # st.markdown(answer, unsafe_allow_html=True)
        image_parser(answer=answer, food_images=food_images)
        ###### Create Expanders
        recomendations = re.findall(r"\[.*?\]", title)

        with st.expander("Recomendaciones"):
            st.write(recomendations)

        # st.write(response["title"])
        # st.write(script)
        # st.write(director)
        # with st.expander("Title History"):
        #    st.info(title_memory.buffer)

        # with st.expander("Script History"):
        # st.info(script_memory.buffer)

        # with st.expander("Wikipedia Research History"):
        # st.info(wiki_research)


###### TAB 2
with tab2:
    st.components.v1.iframe(
        src="https://drive.google.com/uc?export=view&id=1hmwTFKwuLfBJm7kAy92EAxtCKg0y0nOS",
        width=900,
        height=900,
    )
    # st.image(
    #    "https://drive.google.com/file/d/1hmwTFKwuLfBJm7kAy92EAxtCKg0y0nOS/preview",
    #    "Nuestros deliciosos tacos",
    # )
