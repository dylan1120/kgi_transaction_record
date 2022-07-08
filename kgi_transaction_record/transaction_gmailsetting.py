import numpy as np
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import config
import os
import base64
from google.auth.transport.requests import Request


class GmailSetting:
    def token_check(self):
        # Define the SCOPES. If modifying it, delete the token.pickle file.
        SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

        # Variable creds will store the user access token.
        # If no valid token found, we will create one.
        creds = None

        # The file token.pickle contains the user access token.
        # Check if it exists
        # if os.path.exists('token.pickle'):

        # Read the token from the file and store it in the variable creds
        with open(config.path["gmail_token"], "rb") as token:
            creds = pickle.load(token)

        # If credentials are not available or are invalid, ask the user to log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    config.path["gmail_api"], SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle file for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
        return creds

    def get_attachments(self, service, user_id, msg_id, message, prefix=""):
        """Get and store attachment from Message with given id.

        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: ID of Message containing attachment.
        prefix: prefix which is added to the attachment filename on saving
        """
        for part in message["payload"]["parts"]:
            if part["filename"]:
                if "data" in part["body"]:
                    data = part["body"]["data"]
                else:
                    att_id = part["body"]["attachmentId"]
                    att = (
                        service.users()
                        .messages()
                        .attachments()
                        .get(userId=user_id, messageId=msg_id, id=att_id)
                        .execute()
                    )
                    data = att["data"]
                file_data = base64.urlsafe_b64decode(data.encode("UTF-8"))
                path = prefix + part["filename"]

                with open(path, "wb+") as f:
                    f.write(file_data)
