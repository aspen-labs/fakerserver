"""
Multithreaded Fake Data API Server
A simple API server for generating fake data that handles requests in separate threads.
"""

import http.server
import socketserver
import logging

from .api_handler import APIRequestHandler


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """HTTP Server that handles each request in a separate thread."""
    daemon_threads = True
    allow_reuse_address = True


def start_server(host='0.0.0.0', port=8000, verbose=False):
    """
    Start the multithreaded fake data API server.

    Args:
        host: Host address to bind to
        port: Port number to listen on
        verbose: Enable verbose logging
    """
    # Configure logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logging.info("Starting Fake Data API Server...")
    handler = APIRequestHandler

    with ThreadedHTTPServer((host, port), handler) as httpd:
        addr, port = httpd.server_address
        logging.info(f"Server started at http://{addr}:{port}")
        logging.info("Press Ctrl+C to stop the server")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logging.info("\nShutting down server...")
            httpd.shutdown()
