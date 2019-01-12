from __future__ import absolute_import

from logic.generator import TransactionGenerator
import argparse
import numpy as np

# TODO: test
# TODO: update README with instructions
argument_parser = argparse.ArgumentParser(description="A data generator for frequent itemset mining in tree-like sequences of complex objects")
argument_parser.add_argument("-out", dest="output", type=str, help="Output file name (csv format)", action="store", default="output")
argument_parser.add_argument("-t", dest="transactions", type=int, help="The number of transaction to generate (int)", action="store", default=20)
argument_parser.add_argument("-p", dest="patterns", type=int, help="The number of patterns that will be generated and used (int)", action="store", default=4)
argument_parser.add_argument("-avg", dest="average", type=float, help="The average length of a pattern (float)", action="store", default=3)
argument_parser.add_argument("-nf", dest="fields", type=int, help="The total number of fields which every record will have (int)", action="store", default=10)
argument_parser.add_argument("-nv", dest="values", type=int, help="The number of possible values that each field can be generated with (int)", action="store", default=100)
argument_parser.add_argument("-thr", dest="threshold", type=int, help="The minimum number of times that each pattern will appear among all the transactions (int)", action="store", default=4)
argument_parser.add_argument("-pp", dest="print", type=bool, help="Print the generated patterns (boolean)", action="store", default=False)
args = argument_parser.parse_args()
output_file = args.output + ".csv"
transactions = args.transactions
patterns = args.patterns
avg_pattern_length = args.average
number_of_fields = args.fields
number_of_values = args.values
threshold = args.threshold
show = args.print
generator = TransactionGenerator(transactions, patterns, avg_pattern_length, number_of_fields, number_of_values, threshold, show)
trees = generator.generate_data()
np.random.shuffle(trees)
fields = []
for field in [field for field in trees[0].fields]:
    if field not in ["tid", "rid", "parent"]:
        fields.append(field)
file = open(output_file, "w")
file.write("transaction_id,record_id,parent_id")
for field in fields:
    file.write("," + field)
file.write("\n")
for tree in trees:
    for record in tree.get_nodes_list():
        file.write(record.fields["tid"] + "," + record.fields["rid"] + "," + ("None" if record.fields["parent"] is None else record.fields["parent"]))
        for field in fields:
            file.write("," + record.fields[field])
        file.write("\n")
