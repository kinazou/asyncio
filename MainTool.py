#import asyncio
import csv
from Logger import Logger
import Option
import Asyn

## オプションの取得
args = Option.get(5, 'input.csv', 'output.log', 'statistics.log')
## ロガーの取得
logger = Logger(args.outputlog, args.statistics)

class ChildTask(Asyn.Task):

    def __init__(self, title):
        self._title = title
        self._sql = ""

    ## アイテムの作成
    def make(self):
        self._sql = "select * from {0}".format(self._title)
        logger.loginfo("ChildTask: make ->{0}".format(self._sql))

    ## アイテムの実行
    async def execute(self):
        # await asyncio.sleep(3)
        logger.loginfo("ChildTask: execute ->{0}".format(self._sql))
        return self._title

## タスクリストの生成
def make_tasks(inputcsv):
    tasks = []
    for index in range(15):
        tasks.append(ChildTask("task{0}".format(index)))
    return tasks

## メイン
def main():
    logger.loginfo("Start!!")

    logger.loginfo('  Max Queue Size    : ' + str(args.maxqueuesize))
    logger.loginfo('  Input Csv         : ' + str(args.inputcsv))
    logger.loginfo('  Output Log        : ' + str(args.outputlog))
    logger.loginfo('  Output Statistics : ' + str(args.statistics))

    # coordinator = Asyn.Coordinator()
    tasks = make_tasks(args.inputcsv)
    coordinator = Asyn.Coordinator(tasks, args.maxqueuesize)
    coordinator.run()

    logger.loginfo("Finish!!")

if __name__ == '__main__':
    main()
