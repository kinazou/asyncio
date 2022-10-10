import asyncio

class Task:

    def __init__(self, title = "", exectime = 3):
        self._title = title
        self._exectime = exectime

    ## アイテムの作成
    def make(self):
        print("Task: make", self._title)

    ## アイテムの実行
    async def execute(self):
        print("Task: execute ->", self._title)
        await asyncio.sleep(self._exectime)
        return self._title

class Producer:

    def __init__(self):
        self._tasks = []

    def set_tasks(self, tasks):
        self._tasks = tasks

    ## キューにアイテム挿入
    async def run(self, queue):
        for task in self._tasks:
            task.make()
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
                 producer = Producer(), consumer = Consumer()):
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
