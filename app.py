import streamlit as st

from utils.gemini_generation import Gemini
from utils.alodokter_retreiver import AlodokterRetreiver
from utils.prompt import Prompt


st.set_page_config(
    page_title="Simple RAG Health Chatbot 🤖",
    page_icon="🤖",
    layout="wide",
)


@st.cache_resource()
def initialize_gemini():
    with st.spinner("Initializing gemini... \n Don't stop it!"):
        gemini = Gemini()
    return gemini


gemini = initialize_gemini()


def get_search_query(user_input, previous_question=None):
    search_query_prompt = Prompt.search_query(user_input, previous_question)
    search_query = gemini.generate(search_query_prompt)

    return search_query


def get_article(search_query):
    search_results = AlodokterRetreiver.search_articles(search_query)[:3]
    article_data = []

    for article in search_results:
        article_content = AlodokterRetreiver.get_article(article['url'])
        article_data.append(article_content)

    return article_data, search_results
    

st.title("🤖 Simple RAG Health Chatbot")

with st.expander("📋 About this app", expanded=True):
    st.markdown("""
    * Simple RAG Health Chatbot app is an easy-to-use tool that allows you to consult health related topic with AI based on Alodokter Article and Community Data.
    * AI used in this app is Gemini 1.5 Pro paired with Alodokter Article and Community as Data Source for RAG.
    * Made by [Rizky Adi](https://www.linkedin.com/in/rizky-adi-7b008920b/).
    """
    )
    st.markdown(" ")


st.markdown(' ')

st.header("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_session = gemini.start_chat()

message_container = st.container(height=400)

for message in st.session_state.messages:
    message_container.chat_message(message["role"]).write(message["content"])

if prompt := st.chat_input("What is up?"):
    message_container.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with message_container:
        with st.spinner('Searching related article...'):
            if len(st.session_state.messages) > 0:
                previous_question = [message["content"] for message in st.session_state.messages if message["role"] == "user"]
                search_query = get_search_query(prompt, previous_question)
            else:
                search_query = get_search_query(prompt)

            search_query = search_query.replace("```", "").replace('"', '').strip()
            print(search_query)

        with st.spinner(f'Searching related article to "{search_query}"...'):
            related_articles, articles_data = get_article(search_query)

        with st.spinner('Generating response..'):
            if len(related_articles) > 0:
                rag_prompt = Prompt.simple_rag(prompt, related_articles)
                response = st.session_state.chat_session.send_message(rag_prompt).text.replace("```", "")
                
                url_markdown = ""
                for article_data in articles_data:
                    url_markdown += f"* [{article_data['title']}]({article_data['url']})\n"

                response += f"\n\nSources:\n{url_markdown}"
            elif len(st.session_state.chat_session.history) > 0:
                response = st.session_state.chat_session.send_message(prompt).text.replace("```", "")
            else:
                response = f"No related Alodokter article found for this question."

    message_container.chat_message("assistant").write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})