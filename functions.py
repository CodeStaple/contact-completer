import os
import pickle
import requests
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# The scopes required to access the People API
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']


def get_authenticated_service():
    """Authenticate the user and return the People API service."""
    creds = None
    token_file = 'token.pickle'

    # Check if token file exists and is valid
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    # Build the People API service
    service = build('people', 'v1', credentials=creds)
    return service


def retrieve_phone_numbers(service):
    """Retrieve phone numbers from Google contacts."""
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=1000,
        personFields='phoneNumbers'
    ).execute()

    connections = results.get('connections', [])

    if not connections:
        print('No contacts found.')
        return

    phone_numbers = []
    for person in connections:
        names = person.get('names', [])
        if names:
            name = names[0].get('displayName')
            numbers = person.get('phoneNumbers', [])
            if numbers:
                for number in numbers:
                    phone_numbers.append((name, number.get('value')))

    return phone_numbers


def get_reverse_info(phone_number):
    """Fetch reverse information for a given phone number."""
    url = f'https://reversera.com/{phone_number}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        result_element = soup.find(class_='result')
        if result_element:
            return result_element.text.strip()

    return None