import os

from plyer import email as email_client

from Data.Repositories.DalModels import OrderDalModel


class MailService:

    def send_order_confirmed_email(self, o: OrderDalModel):
        email_client.send(
            recipient=o.email_address,
            subject=f"ORDER #{o.id:04d} CONFIRMED",
            text=f"""Hi {o.customer_name},

Your order with us has been confirmed, we will update you when the order is shipped

Kind regards,
ACME corp.
"""
        )

    def send_shipping_confirmation(self, o: OrderDalModel, provider: str, tracking_code: str):

        product_list = ""
        for index, po in enumerate(o.products):
            product_list += f"{po.product.name} - £{po.price:.2f}"
            if index != len(o.products) - 1:
                product_list += os.linesep

        email_client.send(
            recipient=o.email_address,
            subject=f"ORDER #{o.id:04d} SHIPPED",
            text=f"""Hi {o.customer_name},

Your order with us has been shipped via {provider}

Tracking code: {tracking_code}

Order Items:
{product_list}

Kind regards,
ACME corp.
"""
        )

    def open_blank_email(self, email: str):
        # send(self, recipient=None, subject=None, text=None,
        #              create_chooser=None)
        email_client.send(email)
