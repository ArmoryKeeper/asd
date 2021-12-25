from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

student_dict = {'15585':['Ivan', 'Ivanovic', '7.55'],'123665':['Markio', 'Simovic', '9.99'],'569842':['Mirko', 'Miric', '8.91']}

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            index = parse_qs(self.path[2:])['index'][0]
        except:
            self.send_response_to_client(404, 'Nepravilni parametri prosledjeni')
            self.log_message("Korisnik je uneo nepravilne parametre")
            return

        if index in student_dict.keys():
            self.send_response_to_client(200, student_dict[index])
        else:
            self.send_response_to_client(400, 'Student nije pronadjen')
            self.log_message("Korisnik je uneo pogresan broj indeksa " + index)

    def do_POST(self):
        self.log_message('Krece upis')
        data = parse_qs(self.path[2:])
        try:
            student_dict[data['index'][0]] = [data['ime'][0], data['prezime'][0], data['prosek'][0]]
            self.send_response_to_client(200, student_dict)
        except KeyError:
            self.send_response_to_client(404, 'Pogresan upis parametara')
            self.log_message("Korisnik je uneo nepravilne parametre")
             
    def send_response_to_client(self, status_code, data):
        # Send OK status
        self.send_response(status_code)
        # Send headers
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
     
        # Send the response
        self.wfile.write(str(data).encode())
 
server_address = ('127.0.0.1', 8080)
http_server = HTTPServer(server_address, RequestHandler)
http_server.serve_forever()

