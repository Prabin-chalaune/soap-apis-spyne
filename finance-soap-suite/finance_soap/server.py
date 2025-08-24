import argparse
from wsgiref.simple_server import make_server
from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from finance_soap.services import FinanceService
from finance_soap.config import settings
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def build_app():
    # here Spyne Application auto-generates WSDL at '/?wsdl'
    app = Application(
        [FinanceService],
        tns=settings.TARGET_NAMESPACE,
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11()
    )
    return WsgiApplication(app)

def run_dev():
    app = build_app()
    with make_server(settings.HOST, settings.PORT, app) as server:
        print(f"Serving SOAP on http://{settings.HOST}:{settings.PORT} (WSDL: /?wsdl)")
        server.serve_forever()

def run_waitress():
    from waitress import serve
    app = build_app()
    print(f"Serving SOAP via waitress on http://0.0.0.0:{settings.PORT} (WSDL: /?wsdl)")
    serve(app, host="0.0.0.0", port=settings.PORT)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--waitress", action="store_true", help="Serve with waitress (prod-style)")
    args = parser.parse_args()
    if args.waitress:
        run_waitress()
    else:
        run_dev()
