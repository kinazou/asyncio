# Python: Default Interpreter Path
#  C:\\Users\\XXX\\AppData\\Local\\Programs\\Python\\Python36
import time
import asyncio
from threading import Thread
from queue import Queue

class Task:

    def __init__(self, logger, row):
        self._logger = logger
        self._title = row[0]
        self._sql = row[1]

    ## アイテムの作成
    def create(self):
        self._logger.loginfo("ChildTask: create ->{0}".format(self._sql))

    ## アイテムの実行
    def execute(self):
        time.sleep(1)
        self._logger.loginfo("ChildTask: execute ->{}: {}s".format(self._sql, 1))
        return self._title

class Coordinator:

    def __init__(self, tasks, maxqueuesize = 5):
        self._tasks = tasks
        self._maxqueuesize = maxqueuesize
        self._queue = Queue(self._maxqueuesize)

    ## キュー内のアイテム逐次実行
    #
    # キューのアイテム存在確認
    # キューからアイテム取得(溜まっていたアイテムを全て取得)
    # アイテムの実行(取得したアイテムを並列実行)
    # アイテムの使用完了をキューに伝える
    def worker(self):
        while True:
            task = self._queue.get()
            if task is None:
                break

            task.execute()
            self._queue.task_done()

    ## 非同期処理の実行(内部)
    # キューの生成
    # キューの監視
    # キューへのデータ投入
    # キューの中にあるタスクが全て完了したら終了
    # async def _execute(self):
    async def _execute(self):
        threads = []
        for i in range(self._maxqueuesize):
            thread = Thread(target=self.worker)
            thread.start()
            threads.append(thread)

        for task in self._tasks:
            self._queue.put(task)

        self._queue.join()

        for i in range(self._maxqueuesize):
            self._queue.put(None)

        for thread in threads:
            thread.join()

    ## 非同期処理の実行
    def run(self):
        try:
            loop = asyncio.get_event_loop()
        finally:
            loop.run_until_complete(self._execute())
            loop.close()
