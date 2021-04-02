from plyer import email as email_client


class MailService:

    def open_blank_email(self, email: str):
        # send(self, recipient=None, subject=None, text=None,
        #              create_chooser=None)
        email_client.send(email)
