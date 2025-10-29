"""API request handler for fake data generation."""

import json
import logging
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any

from .fake_data import FakeDataGenerator


class APIRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler with API endpoints for fake data generation."""

    # Class-level generator instance
    fake_generator = FakeDataGenerator()

    def log_message(self, format, *args):
        """Override to use logging module instead of stderr."""
        logging.info("%s - %s" % (self.address_string(), format % args))

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # API endpoints
        if path == '/api/generate':
            self.handle_generate()
        elif path == '/api/types':
            self.handle_types()
        elif path == '/api/health':
            self.handle_health()
        elif path == '/' or path == '/api' or path == '/api/':
            self.handle_root()
        else:
            # Return 404 for non-API routes
            self.send_error_response(404, f"Endpoint not found: {path}")

    def handle_generate(self):
        """Handle /api/generate endpoint to generate fake data."""
        try:
            parsed_path = urlparse(self.path)
            params = parse_qs(parsed_path.query)

            # Get parameters
            data_type = params.get('type', ['name'])[0]
            count = int(params.get('count', ['1'])[0])
            locale = params.get('locale', ['en_US'])[0]

            # Validate count
            if count < 1 or count > 100:
                self.send_error_response(400, "Count must be between 1 and 100")
                return

            # Generate fake data
            generator = FakeDataGenerator(locale=locale)
            data = generator.generate(data_type, count)

            # Send response
            response = {
                'success': True,
                'type': data_type,
                'count': count,
                'data': data if count > 1 else data[0]
            }
            self.send_json_response(200, response)

        except ValueError as e:
            self.send_error_response(400, str(e))
        except Exception as e:
            logging.error(f"Error generating fake data: {e}")
            self.send_error_response(500, "Internal server error")

    def handle_types(self):
        """Handle /api/types endpoint to list available data types."""
        types = self.fake_generator.get_available_types()
        response = {
            'success': True,
            'count': len(types),
            'types': types
        }
        self.send_json_response(200, response)

    def handle_health(self):
        """Handle /api/health endpoint for health checks."""
        response = {
            'success': True,
            'status': 'healthy',
            'service': 'fake-data-api'
        }
        self.send_json_response(200, response)

    def handle_root(self):
        """Handle root endpoint with API documentation."""
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Fake Data Generator API</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 50px auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 { color: #333; }
        h2 { color: #555; margin-top: 30px; }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
        }
        pre {
            background: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .endpoint {
            background: #e8f4f8;
            padding: 10px;
            margin: 10px 0;
            border-left: 4px solid #0066cc;
        }
        .example {
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>Fake Data Generator API</h1>
    <p>A simple API for generating fake data for testing and development.</p>

    <h2>Endpoints</h2>

    <div class="endpoint">
        <h3>GET /api/generate</h3>
        <p>Generate fake data of a specified type.</p>
        <p><strong>Parameters:</strong></p>
        <ul>
            <li><code>type</code> - Type of fake data (default: name)</li>
            <li><code>count</code> - Number of items to generate (1-100, default: 1)</li>
            <li><code>locale</code> - Locale for data generation (default: en_US)</li>
        </ul>
        <div class="example">
            <strong>Examples:</strong>
            <pre>/api/generate?type=email&count=5
/api/generate?type=profile
/api/generate?type=address&count=3</pre>
        </div>
    </div>

    <div class="endpoint">
        <h3>GET /api/types</h3>
        <p>Get a list of all available data types.</p>
        <div class="example">
            <strong>Example:</strong>
            <pre>/api/types</pre>
        </div>
    </div>

    <div class="endpoint">
        <h3>GET /api/health</h3>
        <p>Health check endpoint.</p>
        <div class="example">
            <strong>Example:</strong>
            <pre>/api/health</pre>
        </div>
    </div>

    <h2>Available Data Types</h2>
    <p>Common types include:</p>
    <ul>
        <li><strong>Personal:</strong> name, first_name, last_name, email, phone, username, password</li>
        <li><strong>Address:</strong> address, street_address, city, state, zipcode, country</li>
        <li><strong>Company:</strong> company, job, company_email</li>
        <li><strong>Internet:</strong> url, domain_name, ipv4, ipv6, mac_address</li>
        <li><strong>Text:</strong> text, sentence, paragraph, word</li>
        <li><strong>Date/Time:</strong> date, time, datetime, year</li>
        <li><strong>Other:</strong> uuid4, credit_card_number, color_name, profile, user</li>
    </ul>
    <p>For a complete list, visit <a href="/api/types">/api/types</a></p>

    <h2>Examples</h2>
    <pre>
# Generate a single email
curl "http://localhost:8000/api/generate?type=email"

# Generate 10 names
curl "http://localhost:8000/api/generate?type=name&count=10"

# Generate a complete user profile
curl "http://localhost:8000/api/generate?type=profile"

# Get all available types
curl "http://localhost:8000/api/types"
    </pre>
</body>
</html>"""
        self.send_html_response(200, html)

    def send_json_response(self, status_code: int, data: Dict[str, Any]):
        """Send a JSON response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

    def send_html_response(self, status_code: int, html: str):
        """Send an HTML response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def send_error_response(self, status_code: int, message: str):
        """Send an error response."""
        response = {
            'success': False,
            'error': message
        }
        self.send_json_response(status_code, response)
