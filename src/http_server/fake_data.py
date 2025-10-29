"""Fake data generator module using Faker library."""

import json
from typing import Any, Dict, List
from faker import Faker


class FakeDataGenerator:
    """Generate fake data of various types."""

    def __init__(self, locale: str = 'en_US'):
        """
        Initialize the fake data generator.

        Args:
            locale: Locale for generated data (e.g., 'en_US', 'fr_FR')
        """
        self.fake = Faker(locale)

    def generate(self, data_type: str, count: int = 1) -> List[Any]:
        """
        Generate fake data based on the specified type.

        Args:
            data_type: Type of fake data to generate
            count: Number of items to generate

        Returns:
            List of generated fake data items
        """
        generator_map = {
            # Personal
            'name': self.fake.name,
            'first_name': self.fake.first_name,
            'last_name': self.fake.last_name,
            'email': self.fake.email,
            'phone': self.fake.phone_number,
            'ssn': self.fake.ssn,
            'username': self.fake.user_name,
            'password': self.fake.password,

            # Address
            'address': self.fake.address,
            'street_address': self.fake.street_address,
            'city': self.fake.city,
            'state': self.fake.state,
            'zipcode': self.fake.zipcode,
            'country': self.fake.country,
            'latitude': self.fake.latitude,
            'longitude': self.fake.longitude,

            # Company
            'company': self.fake.company,
            'job': self.fake.job,
            'company_email': self.fake.company_email,

            # Internet
            'url': self.fake.url,
            'domain_name': self.fake.domain_name,
            'ipv4': self.fake.ipv4,
            'ipv6': self.fake.ipv6,
            'mac_address': self.fake.mac_address,
            'user_agent': self.fake.user_agent,

            # Text
            'text': self.fake.text,
            'sentence': self.fake.sentence,
            'paragraph': self.fake.paragraph,
            'word': self.fake.word,

            # Date/Time
            'date': lambda: self.fake.date(),
            'time': lambda: self.fake.time(),
            'datetime': lambda: self.fake.date_time().isoformat(),
            'year': self.fake.year,

            # Numbers
            'random_int': lambda: self.fake.random_int(min=0, max=1000),
            'random_digit': self.fake.random_digit,

            # Credit Card
            'credit_card_number': self.fake.credit_card_number,
            'credit_card_provider': self.fake.credit_card_provider,
            'credit_card_expire': self.fake.credit_card_expire,

            # Currency
            'currency_code': self.fake.currency_code,
            'currency_name': self.fake.currency_name,

            # File
            'file_name': self.fake.file_name,
            'file_extension': self.fake.file_extension,
            'mime_type': self.fake.mime_type,

            # Color
            'color_name': self.fake.color_name,
            'hex_color': self.fake.hex_color,
            'rgb_color': self.fake.rgb_color,

            # UUID
            'uuid4': lambda: str(self.fake.uuid4()),

            # Profile (comprehensive)
            'profile': self.generate_profile,
            'user': self.generate_user,
        }

        generator = generator_map.get(data_type)
        if not generator:
            raise ValueError(f"Unknown data type: {data_type}")

        return [generator() for _ in range(count)]

    def generate_profile(self) -> Dict[str, Any]:
        """Generate a complete user profile."""
        return {
            'username': self.fake.user_name(),
            'name': self.fake.name(),
            'email': self.fake.email(),
            'phone': self.fake.phone_number(),
            'address': self.fake.address(),
            'job': self.fake.job(),
            'company': self.fake.company(),
            'birthdate': self.fake.date_of_birth().isoformat(),
            'website': self.fake.url(),
        }

    def generate_user(self) -> Dict[str, Any]:
        """Generate a simple user object."""
        return {
            'id': self.fake.random_int(min=1, max=100000),
            'username': self.fake.user_name(),
            'email': self.fake.email(),
            'name': self.fake.name(),
            'created_at': self.fake.date_time().isoformat(),
        }

    def get_available_types(self) -> List[str]:
        """Get list of all available data types."""
        return [
            'name', 'first_name', 'last_name', 'email', 'phone', 'ssn',
            'username', 'password', 'address', 'street_address', 'city',
            'state', 'zipcode', 'country', 'latitude', 'longitude',
            'company', 'job', 'company_email', 'url', 'domain_name',
            'ipv4', 'ipv6', 'mac_address', 'user_agent', 'text',
            'sentence', 'paragraph', 'word', 'date', 'time', 'datetime',
            'year', 'random_int', 'random_digit', 'credit_card_number',
            'credit_card_provider', 'credit_card_expire', 'currency_code',
            'currency_name', 'file_name', 'file_extension', 'mime_type',
            'color_name', 'hex_color', 'rgb_color', 'uuid4', 'profile', 'user'
        ]
