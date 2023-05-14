import os
import streamlit as st
import time
import streamlit.components.v1 as components
import re

from streamlit_extras.card import card
from streamlit_extras.badges import badge
from streamlit_extras.metric_cards import style_metric_cards

apikey = st.secrets["OPENAI_API_KEY"]
propmpt_template1 = st.secrets["prompt_template1"]
propmpt_template2 = st.secrets["prompt_template2"]
fake_answer = st.secrets["fake_answer"]


use_fake_prompt = True

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper
from langchain.callbacks import get_openai_callback

##### Card Title


##### Dictionaries
food_images = {
    "tacos de ternera clásicos": "https://i.ibb.co/84wKHLc/Receita-de-tacos-mexicanos-150x150.png",
    "tacos de pollo a la parrilla": "https://i.ibb.co/84wKHLc/Receita-de-tacos-mexicanos-150x150.png",
    "baja fish tacos": "https://i.ibb.co/84wKHLc/Receita-de-tacos-mexicanos-150x150.png",
    "veggie tacos": "https://i.ibb.co/84wKHLc/Receita-de-tacos-mexicanos-150x150.png",
    "nachos cargados": "https://i.ibb.co/vHRW7Yk/SOFT-BEEF-TACOS-770x628-150x150.jpg",
    "quesadilla": "https://i.ibb.co/r4h76Ld/breakfast-quesadilla-150x150.jpg",
    "hamburguesa a la brasa": "https://i.ibb.co/MRQv5qQ/meatless-chipotle-pesto-burger-3-150x150.jpg",
    "alitas de pollo": "https://i.ibb.co/KNPdqkq/alitas-de-pollo-teriyaki-150x150.jpg",
    "aros de cebolla rebozados con cerveza": "https://i.ibb.co/jV5jk9J/conoce-la-receta-de-los-aros-de-cebolla-y-cautiva-a-tus-invitados-150x150.jpg",
    "fried avocado bites": "https://i.ibb.co/R9mrVhZ/Air-Fryer-Fried-Avocado-Picture-150x150.png",
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
    "chimay blue": "6€",
    "weihenstephaner hefeweissbier": "7€",
    "hitachino nest white ale": "5€",
    "la chouffe": "6€",
    "rodenbach grand cru": "11€",
    "augustiner helles": "7€",
    "founders breakfast stout": "4€",
    "westvleteren 12": "6€",
}
food_descriptions = {
    "tacos de ternera clásicos": "carne molida sazonada, queso rallado, lechuga, tomate, nata y salsa servidos en una tortilla caliente",
    "tacos de pollo a la parrilla": "pollo a la parrilla marinado, aguacate, pico de gallo y queso fresco servido en una tortilla calentita",
    "baja fish tacos": "bacalao rebozado con cerveza, ensalada de col, mayonesa de chipotle y lima servido en una tortilla caliente",
    "veggie tacos": "batata asada, frijoles negros, maíz, aguacate y cilantro servidos en una tortilla caliente",
    "nachos cargados": "chips de tortilla crujientes cubiertos con carne molida sazonada, queso, jalapeños, tomates, aceitunas negras y crema agria",
    "quesadilla": "queso cheddar y jack derretido, pollo o bistec a la parrilla, cebollas y pimientos salteados, servida con salsa y crema agria",
    "hamburguesa a la brasa": "1/3 lb de hamburguesa de ternera, lechuga, tomate, pepinillos y salsa especial sobre pan brioche",
    "alitas de pollo": "salsa de búfalo, barbacoa de miel o parmesano con ajo, servidas con apio y aderezo ranch o queso azul",
    "aros de cebolla rebozados con cerveza": "aros de cebolla crujientes servidos con salsa chipotle mayonesa",
    "fried avocado bites": "gajos de aguacate rebozados y fritos servidos con salsa ranchera",
    "chimay blue": "Cerveza belga con un color marrón intenso y un sabor rico y complejo. Tiene notas de frutos negros y especias, con un final ligeramente amargo.",
    "weihenstephaner hefeweissbier": "Cerveza de trigo alemana es de color dorado claro y tiene un aspecto turbio debido a la levadura. Tiene un sabor refrescante y afrutado con toques de plátano y clavo.",
    "hitachino nest white ale": "Cerveza japonesa se elabora con cilantro y nuez moscada, lo que le da un sabor picante y ligeramente dulce. Tiene un aroma ligero y cítrico y un final crujiente.",
    "la chouffe": "Cerveza belga tiene un color dorado y un aroma afrutado con toques de pera y manzana. Tiene un sabor ligeramente dulce con un final seco.",
    "rodenbach grand cru": "Cerveza agria belga tiene un color rojo intenso y un sabor agrio y afrutado. Es envejecido durante dos años en barricas de roble, lo que le da un perfil de sabor complejo.",
    "augustiner helles": "Cerveza alemana es de color dorado pálido y tiene un sabor ligero y crujiente con un toque de dulzura de miel. Tiene un final limpio y refrescante.",
    "founders breakfast stout": "Cerveza estadounidense se elabora con café y chocolate, lo que le da un sabor rico y cremoso. Tiene un fuerte aroma a café y un final ligeramente amargo.",
    "westvleteren 12": "Cerveza belga es elaborada por monjes trapenses y es considerada una de las mejores cervezas del mundo. Tiene un color marrón oscuro y un sabor complejo con notas de caramelo, chocolate y frutos negros.",
}
food_types = {
    "tacos de ternera clásicos": "principales",
    "tacos de pollo a la parrilla": "principales",
    "baja fish tacos": "principales",
    "veggie tacos": "principales",
    "nachos cargados": "entrantes",
    "quesadilla": "entrantes",
    "hamburguesa a la brasa": "entrantes",
    "alitas de pollo": "entrantes",
    "aros de cebolla rebozados con cerveza": "entrantes",
    "fried avocado bites": "entrantes",
    "chimay blue": "cervezas",
    "weihenstephaner hefeweissbier": "cervezas",
    "hitachino nest white ale": "cervezas",
    "la chouffe": "cervezas",
    "rodenbach grand cru": "cervezas",
    "augustiner helles": "cervezas",
    "founders breakfast stout": "cervezas",
    "westvleteren 12": "cervezas",
}
logo_url = "https://i.ibb.co/84wKHLc/Receita-de-tacos-mexicanos-150x150.png"
restaurant_name = "Cervezas y Tacos"

add_to_cart_list = []
remove_from_cart_list = []
##### Custom Functions
def image_parser(answer, food_images):
    recomendations = re.findall(r"\[.*?\]", answer)

    i = 0

    for dish in recomendations:
        dish_aux = dish.replace("[", "")
        dish_aux = dish_aux.replace("]", "")
        dish_aux = dish_aux.lower()
        split_answer = answer.split(sep=dish, maxsplit=1)

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
            button_clicked = False
            if dish_aux in food_images:
                col1, col2, col3, col4 = st.columns(4)
                with col2:
                    add_image(source=food_images[dish_aux])
                with col3:
                    button_clicked = st.button(
                        ":white[Añadir a la lista: \n **"
                        + dish_aux.title()
                        + "** ("
                        + food_prices[dish_aux]
                        + ")]",
                        type="primary",
                    )
                    if dish_aux in st.session_state:
                        st.caption(
                            "**Añadidos: "
                            + str(st.session_state[dish_aux])
                            + "**  :heavy_check_mark:"
                        )
                    if button_clicked == True:
                        add_to_cart_list.append(dish_aux)

            else:
                col1, col2, col3 = st.columns(3)
                with col2:
                    button_clicked = st.button(
                        ":white[Añadir a la lista: \n **"
                        + dish_aux.title()
                        + "** ("
                        + food_prices[dish_aux]
                        + ")]",
                        type="primary",
                    )
                    if dish_aux in st.session_state:
                        st.caption(
                            "**Añadidos: "
                            + str(st.session_state[dish_aux])
                            + "**  :heavy_check_mark:"
                        )
                    if button_clicked == True:
                        add_to_cart_list.append(dish_aux)

        answer = split_answer[1]

        i = i + 1

    add_remove_cart_items(
        add_to_cart_list=add_to_cart_list,
        remove_from_cart_list=remove_from_cart_list,
    )
    split_answer = answer.split(sep=recomendations[-1], maxsplit=1)
    split_answer_aux = split_answer[-1]
    if split_answer_aux[0:2] == ". ":
        split_answer_aux = split_answer_aux.replace(". ", "", 1)
    st.markdown(split_answer_aux.strip().capitalize(), unsafe_allow_html=True)


def add_remove_cart_items(
    add_to_cart_list,
    remove_from_cart_list,
):
    for item in add_to_cart_list:
        if item in food_prices:
            if item not in st.session_state:
                st.session_state[item] = 0
            st.session_state[item] = st.session_state[item] + 1

    for item in remove_from_cart_list:
        if item in food_prices:
            if item not in st.session_state:
                st.session_state[item] = 0
            if st.session_state[item] > 0:
                st.session_state[item] = st.session_state[item] - 1
    if not add_to_cart_list == []:
        st.experimental_rerun()
    if not remove_from_cart_list == []:
        st.experimental_rerun()


def format_answer(title):
    answer = title.replace(";", ".")
    # answer = answer.replace("[", "**")
    # answer = answer.replace("]", "**")
    if answer[0:2] == ", ":
        answer = answer.replace(", ", "", 1)

    answer = answer.capitalize()
    phrases = answer.split(sep=".")

    answer = ""
    for phrase in phrases:
        answer = answer + ". " + phrase.strip().capitalize()
    answer = answer.replace(". ", "", 1)
    answer = answer.replace(". ", ". <br>")
    return answer


def create_cart():
    add_to_cart_list = []
    remove_from_cart_list = []
    with tab5:
        key = 0
        session_aux = st.session_state
        for items in session_aux:
            if items in food_prices:
                button_clicked_add = False
                button_clicked_rem = False
                if session_aux[items] > 0:
                    col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
                    with col1:
                        st.button(
                            label=items.title(),
                            type="secondary",
                            key=key,
                        )
                    with col2:
                        st.button(
                            " (**" + str(session_aux[items]) + "**)",
                            type="secondary",
                            key=key + 1,
                        )
                    with col3:
                        button_clicked_rem = st.button(
                            label="**-**",
                            type="primary",
                            key=key + 2,
                        )
                        if button_clicked_rem == True:
                            remove_from_cart_list.append(items)
                    with col4:
                        button_clicked_add = st.button(
                            label="**+**",
                            type="primary",
                            key=key + 3,
                        )
                        if button_clicked_add == True:
                            add_to_cart_list.append(items)
                key = key + 4
    add_remove_cart_items(
        add_to_cart_list=add_to_cart_list,
        remove_from_cart_list=remove_from_cart_list,
    )


@st.cache_data
def add_image(source):
    st.components.v1.iframe(
        src=source,
        width=150,
        height=150,
    )


@st.cache_data
def run_llm(prompt, use_fake_prompt, fake_answer):
    if use_fake_prompt == True:
        title = fake_answer
    else:
        with get_openai_callback() as cb:
            title = title_chain.run(prompt)
            # title = script_chain.run(title=title)
            print(cb)
    return title


def full_menu(food_prices, food_images, type):
    i = 0
    for dish in food_prices:
        if food_types[dish] == type:
            dish_aux = dish.replace("[", "")
            dish_aux = dish_aux.replace("]", "")
            dish_aux = dish_aux.lower()
            container = st.container()
            with container:
                button_clicked = False
                if dish_aux in food_images:
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        add_image(source=food_images[dish_aux])
                    with col2:
                        button_clicked = st.button(
                            "" + dish_aux.title() + " (" + food_prices[dish_aux] + ")",
                            type="primary",
                        )
                        st.caption(food_descriptions[dish_aux].capitalize())
                        if dish_aux in st.session_state:
                            st.caption(
                                "**Añadidos: "
                                + str(st.session_state[dish_aux])
                                + "**  :heavy_check_mark:"
                            )

                        if button_clicked == True:
                            add_to_cart_list.append(dish_aux)

                else:
                    button_clicked = st.button(
                        "" + dish_aux.title() + " (" + food_prices[dish_aux] + ")",
                        type="primary",
                    )
                    st.caption(food_descriptions[dish_aux].capitalize())
                    if dish_aux in st.session_state:
                        st.caption(
                            "**Añadidos: "
                            + str(st.session_state[dish_aux])
                            + "**  :heavy_check_mark:"
                        )

                    if button_clicked == True:
                        add_to_cart_list.append(dish_aux)

            # answer = split_answer[1]

            i = i + 1

    add_remove_cart_items(
        add_to_cart_list=add_to_cart_list,
        remove_from_cart_list=remove_from_cart_list,
    )


def add_card(title, image):
    card(
        title=title,
        text="",
        image=image,
    )


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

####### TABS
items_in_list = 0
for item in st.session_state:
    if item in food_prices:
        items_in_list = items_in_list + st.session_state[item]
if items_in_list == 0:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Sugerencias :cook:",
            "Para Compartir :stew:",
            "Tacos :taco:",
            "Cervezas :beers:",
            "Mi Lista :memo:",
        ]
    )
else:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Sugerencias :cook:",
            "Para Compartir :stew:",
            "Tacos :taco:",
            "Cervezas :beers:",
            "Mi Lista (**" + str(items_in_list) + "**) :memo:",
        ]
    )
####### TAB1
with tab1:
    # App framework
    add_card(image=logo_url, title=restaurant_name)

    prompt_is_filled = False
    # st.subheader("🍻 Birras y Tacos 🌮", anchor=False)

    ###### Customer Inputs
    col1, col2 = st.columns([3, 2])

    with col1:
        prompt = st.text_input(
            "¿Qué te apetece hoy?",
            max_chars=80,
            placeholder="¿Qué te apetece hoy?",
            label_visibility="collapsed",
        )
    ###### Number of people
    with col2:
        search = st.button("**¡Pregunta sobre nuestra carta!**", type="primary")
    num_people = 1
    if num_people == 1:
        propmpt_num_people = ""
    else:
        propmpt_num_people = ". Para " + num_people + "personas"

    if prompt == "":
        ### Sugerencias preguntas
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
        title = run_llm(
            prompt=prompt, use_fake_prompt=use_fake_prompt, fake_answer=fake_answer
        )

        st.divider()

        ###### Format Output

        answer = format_answer(title=title)
        # st.markdown(answer, unsafe_allow_html=True)
        image_parser(answer=answer, food_images=food_images)
        ###### Create Expanders
        recomendations = re.findall(r"\[.*?\]", title)
        ###### Side Bar
    create_cart()

###### TAB 2
with tab2:
    full_menu(food_prices=food_prices, food_images=food_images, type="entrantes")
with tab3:
    full_menu(food_prices=food_prices, food_images=food_images, type="principales")
with tab4:
    full_menu(food_prices=food_prices, food_images=food_images, type="cervezas")
badge(type="twitter", name=restaurant_name)
