import os
import subprocess
import platform
import time
from typing import List
from plyer import filechooser, storagepath
from fpdf import FPDF

import config
from data.repositories.dal_models import OrderDalModel


def _sys_open_file(filepath):
    """
    Open a file using system default app, on windows try to print

    Source: https://stackoverflow.com/a/435669/3109126

    :param filepath: The path of the file to open
    """
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(filepath)
    else:  # linux variants
        subprocess.call(('xdg-open', filepath))


class PDF(FPDF):
    def add_title(self, text):
        self.set_xy(0.0, 0.0)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(220, 50, 50)
        self.cell(w=297.0 / 2, h=40.0, align='C', txt=text, border=0)


class AddressLabelPDF(FPDF):
    """
    Generates an address label for the package
    """

    def add_order(self, order: OrderDalModel):
        self.add_page()
        self.set_xy(0.0, 0.0)
        self.set_font('Arial', 'B', 16)
        pad_x = 5
        line_pad = 5
        start_height = 10
        self.text(pad_x, start_height, "Ship To:")
        self.set_font('Arial', '', 14)
        current_line = start_height + line_pad + 2
        self.text(pad_x, current_line, order.customer_name)
        address_lines = order.address.split(",")
        for index, line in enumerate(address_lines):
            current_line = 23 + line_pad * index
            self.text(pad_x, current_line, line.strip())

        tracking_code = order.shipment.tracking_code if order.shipment else "N/A"
        provider = order.shipment.provider if order.shipment else "N/A"
        shipping_text = f"Tracking Reference Code: {tracking_code}"
        width = self.get_string_width(shipping_text)
        half_pad = line_pad / 2
        sep_line_y = current_line + (half_pad * 1.5)
        self.line(half_pad, sep_line_y, width + pad_x * 2 + half_pad, sep_line_y)
        current_line = current_line + line_pad * 2
        self.text(pad_x, current_line, f"Shipped by {provider}")
        current_line += line_pad
        self.text(pad_x, current_line, shipping_text)
        sep_line_y = current_line + (half_pad * 1.5)
        self.line(half_pad, sep_line_y, width + pad_x * 2 + half_pad, sep_line_y)
        current_line = current_line + line_pad * 2
        self.text(pad_x, current_line, f"From ACME corp via {order.storefront}")
        self.rect(half_pad, half_pad, width + pad_x * 2, current_line)


class PackingListPDF(FPDF):
    """
    Generates a printable packing list to be inserted into the order
    """

    def add_order(self, order: OrderDalModel):
        self.add_page()
        self.set_xy(0.0, 0.0)
        self.set_font('Arial', 'B', 16)
        pad_x = 5
        line_pad = 7
        start_height = 10
        self.text(pad_x, start_height, f"ORDER: #{order.id:04d}")
        self.set_font('Arial', '', 14)
        current_line = start_height + line_pad + 2
        self.text(pad_x, current_line, order.customer_name)
        current_line += line_pad
        self.text(pad_x, current_line, f"Ordered via {order.storefront}")
        current_line += line_pad
        self.text(pad_x, current_line, f"Shipping to:")

        address_lines = order.address.split(",")
        for line in address_lines:
            current_line += line_pad
            self.text(pad_x, current_line, line.strip())

        products = order.products
        current_line += line_pad * 1.5
        self.set_font('Arial', 'b', 14)
        self.text(pad_x, current_line, f"Products:")
        current_line += line_pad / 4
        self.set_font('Arial', '', 14)
        for po in products:
            current_line += line_pad
            self.text(pad_x, current_line, f"{po.product.name} £{po.price:.2f}")


class CancelPrintError(Exception):
    """
    An error indicating that a print should be cancelled
    """
    pass


def printer_method(func):
    """
    A decorator to easily and safely handle print cancellation
    """
    def applicator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CancelPrintError:
            print("Safely aborting print due to error")

    return applicator


class PrintService:
    """
    A service to handle all of the printing needs of the application

    Due to difficulties with cross platform apis, this class creates a relevant pdf file and instructs the system
    to open it allowing the user to print
    """

    def _get_output_pdf_name(self, filename="printme"):
        """
        Finds out where to save the pdf to

        Currently asks the user but could be changed to give a tmp directory before sending the file to the printer
        """

        if config.IS_WINDOWS:
            # Quick change to avoid crashes when built
            path = str(config.my_datadir / "prints")
        else:
            doc_dir = storagepath.get_documents_dir()
            recommended_path = os.path.join(doc_dir, filename)
            path = filechooser.choose_dir(multiple=False, path=recommended_path)
        if isinstance(path, List):
            if len(path) > 0:
                path = path[0]
            else:
                raise CancelPrintError()
        print(path)
        output_file = os.path.join(path, filename)
        output_file += f"{''.join(str(time.time()).split('.'))}.pdf"
        return output_file

    @printer_method
    def print_order_address_label(self, order: OrderDalModel):
        """
        Create an address label and open it
        """
        output_file = self._get_output_pdf_name(f"Order{order.id}-AddressLabel")
        print("PRINTING ADDRESS LABEL", output_file)
        pdf = AddressLabelPDF(format="A5")
        pdf.add_order(order)
        pdf.output(output_file, 'F')
        _sys_open_file(output_file)

    @printer_method
    def print_order_packing_list(self, order: OrderDalModel):
        """
        Create an order packing list and open it
        """
        output_file = self._get_output_pdf_name(f"Order{order.id}-PackingList")
        print("PRINTING ADDRESS LABEL", output_file)
        pdf = PackingListPDF(format="A5")
        # pdf.add_page()
        pdf.add_order(order)
        pdf.output(output_file, 'F')
        _sys_open_file(output_file)

    @printer_method
    def print(self, text, filename="printme"):
        """
        Create a test file to verify the printing process works
        """
        def _file_chosen(file_path):
            print(file_path)

        output_file = self._get_output_pdf_name(filename)
        pdf_file = PDF(format="A5")
        pdf_file.add_page()
        pdf_file.add_title("A Test File")
        pdf_file.output(output_file, 'F')
        _sys_open_file(output_file)
