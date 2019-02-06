# BigData Generator

Data generator for a tree-like transactions.

Usage:
`pip install -r requirements.txt`, to install the needed requirements.

`python src/main.py arguments`, making sure to use a python version at least `3.6`.
Arguments:
- `-out filename` to specify the filename on which the output is written. Default is _output_;
- `-t 10` to specify how many transaction generate. Default is _20_;
- `-p 10` number of patterns to create. Default is _4_;
- `-avg 10` the average length of a pattern. Default is _3_;
- `-nf 10` number of fields each records will have. Default is _10_;
- `-avg 10` the average length of a pattern. Default is _3_;
- `-thr 3` minimum number of times a pattern appears. Default is _4_;
- `-pp true` to print on the standard output the generated patterns. Default is _false_;
