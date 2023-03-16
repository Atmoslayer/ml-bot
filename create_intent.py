import argparse
import json
import logging
import os

from dotenv import load_dotenv
from google.api_core.exceptions import InvalidArgument
from google.cloud import dialogflow


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
        request={"parent": parent, "intent": intent}
    )

    logging.info(f'Intent created: {response}')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Questions path parser')
    parser.add_argument('--questions_path', help='Enter path to access questions json file', type=str, default='questions')
    arguments = parser.parse_args()
    questions_path = arguments.questions_path

    load_dotenv()
    google_token = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    google_cloud_project = os.getenv('GOOGLE_CLOUD_PROJECT')
    chat_id = os.getenv('CHAT_ID')
    project_id = os.getenv('PROJECT_ID')

    with open(f'{questions_path}.json', 'r', encoding='utf8') as file:
        questions_json = file.read()

    questions = json.loads(questions_json)
    for questions_title in questions:
        questions_sections = questions[questions_title]
        titled_questions = questions_sections['questions']
        titled_answer = questions_sections['answer']
        crutch = [titled_answer, '']
        try:
            create_intent(project_id, questions_title, titled_questions, crutch)
        except InvalidArgument as exception:
            logging.warning(exception)
