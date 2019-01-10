from __future__ import absolute_import

from logic.generator import TransactionGenerator


# TODO: test
# TODO: read arguments in the main script and use them
# TODO: update README with instructions
print("Hello")
transactions = 20
patterns = 4
avg_pattern_length = 3
number_of_fields = 10
number_of_values = 100
threshold = 3
show = False
output_file = "output.csv"
generator = TransactionGenerator(transactions, patterns, avg_pattern_length, number_of_fields, number_of_values, threshold, show)
records = generator.generate_data()
for record in records:
    record.print_tree()
    print()