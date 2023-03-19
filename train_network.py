import argparse
import json
import logging
import os

from dotenv import load_dotenv
from google.api_core.exceptions import InvalidArgument
from google.cloud import dialogflow

logging.basicConfig(level=logging.INFO)


def detect_intent_texts(project_id, session_id, text):

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code='ru-RU')

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )
    is_fallback = response.query_result.intent.is_fallback
    return response.query_result.fulfillment_text, is_fallback


def train_network(questions_path, project_id):
    with open(f'{questions_path}.json', 'r', encoding='utf8') as file:
        questions_json = file.read()

    questions = json.loads(questions_json)
    for title, attributes in questions.items():
        questions = attributes['questions']
        answer = attributes['answer']
        crutch = [answer, '']
        try:
            create_intent(project_id, title, questions, crutch)
        except InvalidArgument as exception:
            logging.warning(exception)


def create_intent(project_id, display_name, training_phrases_parts, message_texts):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={'parent': parent, 'intent': intent}
    )

    logging.info(f'Intent created: {response}')


def main():
    parser = argparse.ArgumentParser(description='Questions path parser')
    parser.add_argument('--questions_path', help='Enter path to access questions json file', type=str,
                        default='questions')
    arguments = parser.parse_args()
    questions_path = arguments.questions_path

    load_dotenv()
    project_id = os.getenv('PROJECT_ID')

    train_network(questions_path, project_id)


if __name__ == '__main__':
    main()



