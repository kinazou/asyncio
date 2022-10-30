# Python: Default Interpreter Path
#  python
import asyncio

class Task:

    def __init__(self, logger, row):
        self._logger = logger
        self._title = row[0]
        self._sql = row[1]

    ## アイテムの作成
    def create(self):
        self._logger.loginfo("ChildTask: create ->{0}".format(self._sql))

    ## アイテムの実行
    async def execute(self):
        await asyncio.sleep(1)
        self._logger.loginfo("ChildTask: execute ->{}: {}s".format(self._sql, 1))
        return self._title

class Producer:

    def __init__(self):
        self._tasks = []

    def set_tasks(self, tasks):
        self._tasks = tasks

    ## キューにアイテム挿入
    async def run(self, queue):
        for task in self._tasks:
            task.create()
            await queue.put(task)

class Consumer:

    def __init__(self):
        self._waittime = 1

    ## キュー内のアイテム逐次実行
    #
    # キューのアイテム存在確認
    # キューからアイテム取得(溜まっていたアイテムを全て取得)
    # アイテムの実行(取得したアイテムを並列実行)
    # アイテムの使用完了をキューに伝える
    async def run(self, queue):
        while True:
            while queue.empty():
                await asyncio.sleep(self._waittime)

            tasks = []
            for _ in range(queue.qsize()):
                task = await queue.get()
                tasks.append(task)

            results = await asyncio.gather(
                *[task.execute() for task in tasks]
            )
            print("Consumer: done -> {0}".format(results))

            for _ in range(len(tasks)):
                queue.task_done()

class Coordinator:

    def __init__(self, tasks, maxqueuesize = 5, 
                 consumer = Consumer(), producer = Producer()):
        producer.set_tasks(tasks)
        self._producer = producer
        self._consumer = consumer
        self._maxqueuesize = maxqueuesize

    ## 非同期処理の実行(内部)
    # キューの生成
    # キューの監視
    # キューへのデータ投入
    # キューの中にあるタスクが全て完了したら終了
    async def _execute(self):
        queue = asyncio.Queue(self._maxqueuesize)
        asyncio.create_task(self._consumer.run(queue))
        await asyncio.create_task(self._producer.run(queue))
        await queue.join()

    ## 非同期処理の実行
    def run(self):
        asyncio.run(self._execute())
