from __future__ import absolute_import

from logic.generator import TransactionGenerator

print("Hello")
transactions = 20
patterns = 25
avg_pattern_length = 4
number_of_fields = 10
number_of_values = 100
threshold = 3
show = False
output_file = "output.csv"
generator = TransactionGenerator(transactions, patterns, avg_pattern_length, number_of_fields, number_of_values, threshold, show)
records = generator.generate_data()
