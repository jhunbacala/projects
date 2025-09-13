
import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import argparse

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("credentials.json not found.")
                print("Please enable the Gmail API and download your credentials.json file from the Google Cloud Console:")
                print("https://developers.google.com/gmail/api/quickstart/python#authorize-credentials-for-a-desktop-application")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def list_emails(service, count):
    """Lists the user's emails."""
    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=count).execute()
        messages = results.get('messages', [])

        if not messages:
            print("No new messages found.")
            return

        print(f"Listing the latest {count} emails:")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            headers = msg['payload']['headers']
            subject = next(header['value'] for header in headers if header['name'] == 'Subject')
            sender = next(header['value'] for header in headers if header['name'] == 'From')
            snippet = msg['snippet']
            
            print(f"\nFrom: {sender}")
            print(f"Subject: {subject}")
            print(f"Snippet: {snippet}")
            print("-" * 30)

    except HttpError as error:
        print(f'An error occurred: {error}')


def send_email(service, to, subject, body):
    """Sends an email."""
    print(f"Sending email to: {to}")
    # This is a placeholder. Implementation will be in the next step.
    print("Functionality to send emails is not yet implemented.")


def main():
    parser = argparse.ArgumentParser(description='A command-line interface for Gmail.')
    subparsers = parser.add_subparsers(dest='command')

    # 'list' command
    list_parser = subparsers.add_parser('list', help='List emails.')
    list_parser.add_argument('-c', '--count', type=int, default=10, help='Number of emails to list.')

    # 'send' command
    send_parser = subparsers.add_parser('send', help='Send an email.')
    send_parser.add_argument('to', help='Recipient of the email.')
    send_parser.add_argument('subject', help='Subject of the email.')
    send_parser.add_argument('body', help='Body of the email.')

    args = parser.parse_args()

    service = get_gmail_service()

    if not service:
        return

    if args.command == 'list':
        list_emails(service, args.count)
    elif args.command == 'send':
        send_email(service, args.to, args.subject, args.body)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
