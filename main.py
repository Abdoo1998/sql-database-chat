import os
from dotenv import load_dotenv
import gradio as gr
from sqlalchemy import create_engine, inspect
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent

# Load environment variables from .env file
load_dotenv()
openai_key = os.getenv('OPENAI_API_KEY')

def diagnose_and_connect_database(db_path):
    print(f"Diagnosing database: {db_path}")
    engine = create_engine(f"sqlite:///{db_path}")
    inspector = inspect(engine)
    try:
        tables = inspector.get_table_names()
        print("Tables found in the database:")
        for table in tables:
            print(f"- {table}")
        return engine, tables
    except Exception as e:
        print(f"Error inspecting database: {e}")
        return None, []

def process_question(question, db_path):
    engine, available_tables = diagnose_and_connect_database(db_path)
    if not engine:
        return "Failed to connect to the database."

    db = SQLDatabase(engine, include_tables=available_tables)
    llm = ChatOpenAI(api_key=openai_key, model="gpt-3.5-turbo", temperature=0)
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

    try:
        result = agent_executor.invoke(question)
        return result['output']
    except Exception as e:
        error_message = f"An error occurred while processing the query: {str(e)}"
        return error_message

def gradio_interface():
    with gr.Blocks(theme=gr.themes.Soft()) as app:
        gr.Markdown(
            """
            # 🗃️💬 Chat with Your SQL Database

            Powered by GPT-3.5-turbo and LangChain

            Upload your SQLite database and start asking questions about your data!
            """
        )

        with gr.Row():
            with gr.Column(scale=2):
                file_output = gr.File(label="Upload SQLite Database", file_types=[".db", ".sqlite"])
                db_path = gr.Textbox(label="Database Path", value="./sample_database.db")

            with gr.Column(scale=3):
                chatbot = gr.Chatbot(label="Conversation", height=400)

        with gr.Row():
            with gr.Column(scale=4):
                msg = gr.Textbox(label="Ask your SQL-related question", placeholder="Type your question here...")
            with gr.Column(scale=1):
                send = gr.Button("Send", variant="primary")

        with gr.Row():
            clear = gr.Button("Clear Conversation")
            example_questions = gr.Dropdown(
                label="Example Questions",
                choices=[
                    "List the total sales per country. Which country's customers spent the most?",
                    "How many orders were placed in the last month?",
                    "What is the average order value per product category?",
                    "Who are the sales representatives with the highest number of closed deals?",
                    "What is the current inventory status for our top-selling products?"
                ],
                multiselect=False
            )

        def user(user_message, history):
            history = history + [[user_message, None]]
            return "", history

        def bot(history, db_path):
            user_message = history[-1][0]
            bot_message = process_question(user_message, db_path)
            history[-1][1] = bot_message
            return history

        def set_example_question(question):
            return question

        msg.submit(user, [msg, chatbot], [msg, chatbot]).then(
            bot, [chatbot, db_path], chatbot
        )
        send.click(user, [msg, chatbot], [msg, chatbot]).then(
            bot, [chatbot, db_path], chatbot
        )
        clear.click(lambda: None, None, chatbot, queue=False)
        example_questions.change(set_example_question, example_questions, msg)

        file_output.change(lambda x: x.name if x else "", file_output, db_path)

    return app

if __name__ == "__main__":
    gradio_interface().launch(debug=True)