# SQL Database Chat Interface

This project provides a Gradio-based chat interface for interacting with SQL databases using natural language queries. It utilizes GPT-3.5-turbo and LangChain to interpret user questions and generate SQL queries.

## Features

- Upload and connect to SQLite databases
- Ask questions about your data in natural language
- Get AI-generated responses based on the database content
- Example questions for quick start

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/sql-database-chat.git
   cd sql-database-chat
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

## Usage

1. Run the main script:
   ```
   python main.py
   ```

2. Open the provided URL in your web browser to access the Gradio interface.

3. Upload your SQLite database or provide the path to an existing database.

4. Start asking questions about your data!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).