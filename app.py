import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq


st.set_page_config(page_title="🦜🔗 Chat with SQL DB")
st.title("🦜🔗 Chat with SQL DB")


LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"


radio_opt = ["Use SQLite3 Database", "Connect to your MySQL Database"]
selected_opt = st.sidebar.radio("Choose the DB you want to chat with", options=radio_opt)


if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("Enter the MySQL host")
    mysql_user = st.sidebar.text_input("MySQL user")
    mysql_password = st.sidebar.text_input("MySQL password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database")
else:
    db_uri = LOCALDB


api_key = st.sidebar.text_input("Enter your Groq API key", type="password")


llm = None


if api_key:
    try:
        llm = ChatGroq(groq_api_key=api_key, model="Llama-3.3-70b-Versatile", streaming=True)
    except Exception as e:
        st.error(f"Error initializing Groq: {e}")
else:
    st.info("Please enter your Groq API key to proceed.")


@st.cache_resource(ttl='2h')
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all the MySQL credentials")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))


if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_uri)


if llm and db:
    try:
       
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        agent = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
        )

       
        if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

   
        user_query = st.chat_input(placeholder="Ask me anything from the database")

    
        if user_query:
            st.session_state.messages.append({"role": "user", "content": user_query})
            st.chat_message("user").write(user_query)
            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container())
                response = agent.run(user_query, callbacks=[st_cb])
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)
    except Exception as e:
        st.error(f"Error creating SQL agent: {e}")
else:
    st.warning("Please provide the necessary credentials (API key and database info) to proceed.")