import csv
from Logger import Logger
import Option
import Asyn

## オプションの取得
args = Option.get(5, 'input.csv', 'output.log', 'statistics.log')
## ロガーの取得
logger = Logger(args.outputlog, args.statistics)

class ChildTask(Asyn.Task):

    def __init__(self, row):
        self._title = row[0]
        self._sql = row[1]

    ## アイテムの作成
    def create(self):
        logger.loginfo("ChildTask: create ->{0}".format(self._sql))

    ## アイテムの実行
    async def execute(self):
        logger.loginfo("ChildTask: execute ->{0}".format(self._sql))
        return self._title

## タスクリストの生成
def make_tasks(inputcsv):
    tasks = []
    csv_file = open(args.inputcsv, "r", encoding="utf-8")
    rows = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    header = next(rows)
    logger.loginfo(header)
    for row in rows:
        tasks.append(ChildTask(row))
    return tasks

## メイン
def main():
    logger.loginfo("Start!!")

    logger.loginfo('  Max Queue Size    : ' + str(args.maxqueuesize))
    logger.loginfo('  Input Csv         : ' + str(args.inputcsv))
    logger.loginfo('  Output Log        : ' + str(args.outputlog))
    logger.loginfo('  Output Statistics : ' + str(args.statistics))

    tasks = make_tasks(args.inputcsv)
    coordinator = Asyn.Coordinator(tasks, args.maxqueuesize)
    coordinator.run()

    logger.loginfo("Finish!!")

if __name__ == '__main__':
    main()
