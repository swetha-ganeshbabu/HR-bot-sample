from flask import Flask, render_template, request, jsonify
import json
import uuid # Import uuid for simple session management

app = Flask(__name__)

# Dictionary to store conversation state for each session (simple in-memory)
# In a real application, this would be stored in a database or cache
sessions = {}

# Load FAQ data from JSON file
def load_faq_data():
    try:
        with open('faq.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("faq.json not found. Please create it.")
        return []

faq_data = load_faq_data()

def find_faq_entry(query):
    query = query.lower()

    # Separate greeting entries from other entries
    greeting_entry = None
    other_entries = []
    for entry in faq_data:
        if entry.get('question') == 'Greeting': # Assuming 'Greeting' question identifies the greeting entry
            greeting_entry = entry
        else:
            other_entries.append(entry)

    # First, try to match keywords in non-greeting entries
    for entry in other_entries:
        if any(keyword.lower() in query for keyword in entry.get('keywords', [])):
            return entry # Return the topic entry if matched

    # If no topic keyword matched, check for greeting keywords
    if greeting_entry:
        if any(keyword.lower() in query for keyword in greeting_entry.get('keywords', [])):
            return greeting_entry # Return the greeting entry if matched

    return None

@app.route('/')
def home():
    # Generate a simple session ID for the user
    session_id = str(uuid.uuid4())
    sessions[session_id] = {'current_topic': None} # Initialize session state
    return render_template('index.html', session_id=session_id)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    session_id = data.get('session_id') # Get session ID from frontend

    # Ensure session exists (or create a new one if not, though the home route should handle this)
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {'current_topic': None}

    session = sessions[session_id]
    answer = "I'm sorry, I don't have information about that. Please contact HR directly at hr@company.com"
    follow_up = None
    options = None
    clear_session = False

    # Check if we are in a follow-up conversation
    if session['current_topic']:
        # User is responding to a follow-up question
        matched_entry = find_faq_entry(session['current_topic']) # Find the original topic entry
        if matched_entry and 'follow_up' in matched_entry and 'next_step' in matched_entry['follow_up']:
            # Find the answer based on the user's option choice
            user_option = question.lower().strip()
            for option_key, detail_answer in matched_entry['follow_up']['next_step'].items():
                if user_option in option_key.lower():
                    answer = detail_answer
                    clear_session = True # End the follow-up conversation
                    break
            if not clear_session:
                 # If the user's response didn't match an option
                 answer = f"I didn't understand that option. Please type one of the following: {', '.join(matched_entry['follow_up']['options'])}"
                 follow_up = matched_entry['follow_up']['question']
                 options = matched_entry['follow_up']['options']

        # Clear the current_topic if the conversation is ending (either got a final answer or user entered something else)
        if clear_session:
             session['current_topic'] = None

    else:
        # User is asking a new question (not a follow-up)
        matched_entry = find_faq_entry(question)
        if matched_entry:
            # If the matched entry is a greeting, return its answer directly
            if matched_entry.get('question') == 'Greeting':
                answer = matched_entry['answer']
                session['current_topic'] = None # Greetings don't start a follow-up
            elif 'follow_up' in matched_entry:
                # Found an entry with follow-up questions
                answer = matched_entry['answer'] # The initial follow-up question text
                follow_up = matched_entry['follow_up']['question'] # The actual question for the next turn
                options = matched_entry['follow_up']['options'] # Options for the user
                session['current_topic'] = matched_entry['keywords'][0] # Store the primary keyword as the current topic
            else:
                # Found a direct answer
                answer = matched_entry['answer']
                session['current_topic'] = None # Ensure no follow-up is active

    # Return the response, including follow_up data if applicable
    response_data = {'answer': answer}
    if follow_up:
        response_data['follow_up_question'] = follow_up
    if options:
        response_data['follow_up_options'] = options

    return jsonify(response_data)

if __name__ == '__main__':
    # Reload FAQ data when the app reloads in debug mode
    if app.debug:
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler

            class FAQHandler(FileSystemEventHandler):
                def on_modified(self, event):
                    if not event.is_directory and event.src_path.endswith('faq.json'):
                        print("Reloading FAQ data...")
                        global faq_data
                        faq_data = load_faq_data()

            event_handler = FAQHandler()
            observer = Observer()
            observer.schedule(event_handler, '.', recursive=False)
            observer.start()
            print("Watching faq.json for changes...")

            # Run Flask app
            app.run(debug=True)
        except ImportError:
            print("Watchdog library not found. Auto-reloading of faq.json is disabled.")
            print("Please install it with: pip install watchdog")
            app.run(debug=True)
        except KeyboardInterrupt:
            if 'observer' in locals() and observer.is_alive():
                observer.stop()
            if 'observer' in locals():
                 observer.join()
    else:
        app.run(debug=False) 