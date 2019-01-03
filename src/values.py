from __future__ import absolute_import

import uuid
from typing import Dict, List


class ValueGenerator:
    @staticmethod
    def random_string() -> str:
        return str(uuid.uuid4().hex)

    @staticmethod
    def generate_values(number_of_fields: int, number_of_values_per_field: int) -> Dict[str, List[str]]:
        fields = []
        for _ in range(number_of_fields):
            fields.append(ValueGenerator.random_string())
        values = {}
        for field in fields:
            val = []
            for _ in range(number_of_values_per_field):
                val.append(ValueGenerator.random_string())
            values[field] = val
        return values

    @staticmethod
    def generate_pattern_values(number_of_fields: int, number_of_values_per_field: int) -> Dict[str, List[str]]:
        fields = []
        for _ in range(number_of_fields):
            fields.append("_____" + ValueGenerator.random_string())
        values = {}
        for field in fields:
            val = []
            for _ in range(number_of_values_per_field):
                val.append("_____" + ValueGenerator.random_string())
            values[field] = val
        return values
