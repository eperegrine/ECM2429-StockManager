import os
import subprocess
import platform
import time
from typing import List
from plyer import filechooser, storagepath
from fpdf import FPDF

from Data.Repositories.DalModels import OrderDalModel


def _sys_open_file(filepath):
    """
    Open a file using system default app

    Source: https://stackoverflow.com/a/435669/3109126

    :param filepath: The path of the file to open
    """
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(filepath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', filepath))


class PDF(FPDF):
    def add_title(self, text):
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(220, 50, 50)
        self.cell(w=297.0/2, h=40.0, align='C', txt=text, border=0)


class AddressLabel(FPDF):
    def add_order(self, order: OrderDalModel):
        self.set_xy(0.0, 0.0)
        self.set_font('Arial', 'B', 16)
        pad_x = 5
        line_pad = 5
        start_height=10
        self.text(pad_x, start_height, "Ship To:")
        self.set_font('Arial', '', 14)
        current_line = start_height + line_pad + 2
        self.text(pad_x, current_line, order.customer_name)
        address_lines = order.address.split(",")
        for index, line in enumerate(address_lines):
            current_line = 23 + line_pad*index
            self.text(pad_x, current_line, line.strip())

        shipping_text = f"Shipping Ref: MADEUPFORTEST"
        width = self.get_string_width(shipping_text)
        half_pad = line_pad/2
        sep_line_y = current_line + (half_pad * 1.5)
        self.line(half_pad, sep_line_y, width + pad_x*2+half_pad, sep_line_y)
        current_line = current_line + line_pad*2
        self.text(pad_x, current_line, f"Shipping Ref: MADEUPFORTEST")
        sep_line_y = current_line + (half_pad * 1.5)
        self.line(half_pad, sep_line_y, width + pad_x*2+half_pad, sep_line_y)
        current_line = current_line + line_pad*2
        self.text(pad_x, current_line, f"From ACME corp via {order.storefront}")
        self.rect(half_pad, half_pad, width + pad_x*2, current_line)


class PrintService:

    def _get_output_pdf_name(self, filename="printme"):
        # doc_dir = storagepath.get_documents_dir()
        # reccomended_path = os.path.join(doc_dir, filename)
        # path = filechooser.choose_dir(multiple=False, path=reccomended_path, onselection=_file_chosen)
        path = "/Users/emilyperegrine/Documents/Uni/Year-2/ECM2429-Assignment/print_files"
        if isinstance(path, List):
            path = path[0]
        print(path)
        output_file = os.path.join(path, filename)
        output_file += f"{''.join( str(time.time()).split('.'))}.pdf"
        return output_file

    def print_order_address_label(self, order: OrderDalModel):
        output_file = self._get_output_pdf_name(f"Order{order.id}-AddressLabel")
        print("PRINTING ADDRESS LABEL", output_file)
        pdf = AddressLabel(format="A5")
        pdf.add_page()
        pdf.add_order(order)
        pdf.output(output_file, 'F')
        _sys_open_file(output_file)

    def print(self, text, filename="printme"):
        def _file_chosen(file_path):
            print(file_path)

        output_file = self._get_output_pdf_name(filename)
        pdf_file = PDF(format="A5")
        pdf_file.add_page()
        pdf_file.add_title("A Test File")
        pdf_file.output(output_file, 'F')
        _sys_open_file(output_file)
