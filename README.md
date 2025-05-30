# HR Assistant Bot

A simple, interactive HR assistant bot built with Flask and a clean web interface.

## Features

*   **Interactive Chat Interface:** A clean and responsive web interface for employees to ask questions.
*   **FAQ Knowledge Base:** Frequently asked questions and answers are stored in an easy-to-update `faq.json` file.
*   **Keyword Matching:** The bot uses keyword matching to understand user queries and provide relevant answers.
*   **Follow-up Questions:** Supports basic multi-turn conversations with predefined follow-up questions for specific topics (e.g., Benefits).
*   **Easy FAQ Updates:** Easily update the bot's knowledge by modifying the `faq.json` file. Changes are automatically reloaded in debug mode.

## Getting Started

Follow these steps to set up and run the HR Assistant bot locally.

### Prerequisites

*   Python 3.6+
*   Git
*   (Optional, for deployment) [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd hr-bot
    ```

    (Replace `<repository_url>` with the actual URL of your Git repository.)

2.  **Set up a virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    *   On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

    *   On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Make sure your virtual environment is active.**

2.  **Run the Flask application:**

    ```bash
    python app.py
    ```

    The application will start, and you can access it in your web browser at `http://127.0.0.1:5000`.

## Updating FAQs

The bot's knowledge base is stored in the `faq.json` file.

This JSON array contains entries, each with:

*   `keywords`: A list of words or phrases that trigger this entry.
*   `question`: (Optional) A representative question.
*   `answer`: The primary response.
*   `follow_up`: (Optional) Defines subsequent questions and options.

Edit `faq.json` to add, modify, or remove questions and answers. Changes should reload automatically in debug mode.

## Screenshot

Here's a look at the HR Assistant bot interface:

![HR Assistant Bot Screenshot](static/image.png) 