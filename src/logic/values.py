from __future__ import absolute_import

import uuid
from typing import Dict, List


class ValueGenerator:
    @staticmethod
    def random_string() -> str:
        """
        Generate a random string
        :return: a random string
        """
        return str(uuid.uuid4().hex)

    @staticmethod
    def generate_field_names(number_of_fields: int) -> List[str]:
        """
        Generate the names of the various fields
        :param number_of_fields: number of fields to be generated
        :return: the list of names of the fields
        """
        fields = []
        for _ in range(number_of_fields):
            fields.append(ValueGenerator.random_string())
        return fields
