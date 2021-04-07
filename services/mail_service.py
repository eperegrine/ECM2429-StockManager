import os
import subprocess

from config import IS_WINDOWS, IS_MACOS, IS_LINUX
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

from data.repositories.dal_models import OrderDalModel


def send(recipient: str=None, subject: str =None, text: str=None):
    """
    This method has been taken and modified from plyer source code - there is a build issue with plyer so I copied it
    to ensure the built version works

    :param recipient: The person to receive the email
    :param subject: The subject of the email
    :param text: The contents of the email
    """
    uri = "mailto:"
    if recipient:
        uri += str(recipient)
    if subject:
        uri += "?" if "?" not in uri else "&"
        uri += "subject="
        uri += quote(str(subject))
    if text:
        uri += "?" if "?" not in uri else "&"
        uri += "body="
        uri += quote(str(text))

    # WE + startfile are available only on Windows
    if IS_WINDOWS:
        try:
            os.startfile(uri)
        except WindowsError:
            print("Warning: unable to find a program able to send emails.")
    elif IS_MACOS:
        subprocess.Popen(["open", uri])
    elif IS_LINUX:
        subprocess.Popen(["xdg-open", uri])



class MailService:
    """
    Handles sending emails
    """

    def send_order_confirmed_email(self, o: OrderDalModel):
        """
        Send the email with order confirmation details

        :param o: The order to be confirmed
        """
        send(
            recipient=o.email_address,
            subject=f"ORDER #{o.id:04d} CONFIRMED",
            text=f"""Hi {o.customer_name},

Your order with us has been confirmed, we will update you when the order is shipped

Kind regards,
ACME corp.
"""
        )

    def send_shipping_confirmation(self, o: OrderDalModel):
        """
        Send the email to confirm the order has been shipped

        :param o: The order
        """
        if o.shipment is None:
            raise Exception("Shipment is None will sending shipping confirmation")

        product_list = ""
        for index, po in enumerate(o.products):
            product_list += f"{po.product.name} - £{po.price:.2f}"
            if index != len(o.products) - 1:
                product_list += os.linesep

        send(
            recipient=o.email_address,
            subject=f"ORDER #{o.id:04d} SHIPPED",
            text=f"""Hi {o.customer_name},

Your order with us has been shipped via {o.shipment.provider}

Tracking code: {o.shipment.tracking_code}

Order Items:
{product_list}

Kind regards,
ACME corp.
"""
        )

    def open_blank_email(self, email: str):
        """
        Open an email client with an empty message

        :param email: The email to prefill
        :return:
        """
        # send(self, recipient=None, subject=None, text=None,
        #              create_chooser=None)
        send(email)
