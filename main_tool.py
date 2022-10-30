import sys
import csv
import option

sys.path.append('.')
from logger import Logger
#from v306.asyn import Coordinator, Task
from v309.asyn import Coordinator, Task

## オプションの取得
args = option.get(5, 'input.csv', 'output.log', 'statistics.log')
## ロガーの取得
logger = Logger(args.outputlog, args.statistics)

## タスクリストの生成
def make_tasks(inputcsv):
    tasks = []
    csv_file = open(args.inputcsv, "r", encoding="utf-8")
    rows = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    header = next(rows)
    logger.loginfo(header)
    for row in rows:
        tasks.append(Task(logger, row))
    return tasks

## メイン
def main():
    logger.loginfo("Start!!")

    logger.loginfo('  Max Queue Size    : ' + str(args.maxqueuesize))
    logger.loginfo('  Input Csv         : ' + str(args.inputcsv))
    logger.loginfo('  Output Log        : ' + str(args.outputlog))
    logger.loginfo('  Output Statistics : ' + str(args.statistics))

    tasks = make_tasks(args.inputcsv)
    coordinator = Coordinator(tasks, args.maxqueuesize)
    coordinator.run()

    logger.loginfo("Finish!!")

if __name__ == '__main__':
    main()
