from argparse import ArgumentParser

## オプションの取得
def get(maxqueuesize, inputcsv, outputlog, statistics):
    argparser = ArgumentParser()
    argparser.add_argument('-qs', '--maxqueuesize', type=int,
                           default=maxqueuesize,
                           help='Max queue size')
    argparser.add_argument('-ic', '--inputcsv', type=str,
                           default=inputcsv,
                           help='Input csv file')
    argparser.add_argument('-ol', '--outputlog', type=str,
                           default=outputlog,
                           help='Output log file')
    argparser.add_argument('-os', '--statistics', type=str,
                           default=statistics,
                           help='Output statistics file')
    return argparser.parse_args()
