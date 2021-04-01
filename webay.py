import random
from http.server import BaseHTTPRequestHandler, HTTPServer

# webay: a mock EBay sandbox.
# David Wakeling, February 2020
#
# usage: python3 webay.py
#
# test: curl -X GET http://localhost:8080
# or:   browse http://localhost:8080

HOST = "localhost"
PORT = 8080

N_ORDERS = 5

N_PEOPLE = 10
people = [("Leonardo di Caprio", "212 Brookbank Close, Cheltenham"),
          ("George Clooney", "98 Prospect Park, Newcastle"),
          ("Matt Daemon", "77 Station Road, Bath"),
          ("Tom Hanks", "The Palms, Kingsteighton"),
          ("Will Smith", "9 Lawrence Street, York"),
          ("Jennifer Lawrence", "25 Landsdowne Terrace, York"),
          ("Nicole Kidman", "15 Prospect Park, Exeter"),
          ("Sienna Miller", "147 Warrender Park Road, Edinburgh"),
          ("Natalie Portman", "12 Russell Square, London"),
          ("Julia Roberts", "88 Parliament Hill, London")
          ]

N_PRODUCTS = 8
products = [("Samsung Galaxy S21 Ultra", 799),
            ("OnePlus 8 Pro", 429),
            ("iPhone 12", 1299),
            ("Oppo Find X2 Pro", 899),
            ("Motorola Edge Plus", 300),
            ("Xiaomi Mi Note 10", 250),
            ("Sony Xperia 1", 479),
            ("Nokia 3310", 39)
            ]


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes("[ ", "utf-8"))

        r1 = random.randint(0, N_ORDERS)
        for i in range(r1):
            person = random.randint(0, N_PEOPLE - 1)
            product = random.randint(0, N_PRODUCTS - 1)
            name = people[person][0]
            address = people[person][1]
            item = products[product][0]
            price = products[product][1]
            self.wfile.write(bytes("{ ", "utf-8"))
            self.wfile.write(bytes("\"name\" : \"" + name + "\"", "utf-8"))
            self.wfile.write(bytes(", ", "utf-8"))
            self.wfile.write(bytes("\"address\" : \"" + address + "\"", "utf-8"))
            self.wfile.write(bytes(", ", "utf-8"))
            self.wfile.write(bytes("\"item\" : \"" + item + "\"", "utf-8"))
            self.wfile.write(bytes(", ", "utf-8"))
            self.wfile.write(bytes("\"price\" : " + str(price), "utf-8"))
            self.wfile.write(bytes(" }", "utf-8"))
            if i + 1 < r1:
                self.wfile.write(bytes(", ", "utf-8"))
        self.wfile.write(bytes(" ]", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((HOST, PORT), MyServer)
    print("Server running...")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")
