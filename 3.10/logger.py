from datetime import datetime
import logging

class Logger:

    ## ロガーの取得
    # コンソール&ログへの出力設定
    # 統計の出力設定
    def __init__(self, outputlog, outputstatistics):
        logger = logging.getLogger("log")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        log = logging.FileHandler(filename=outputlog, mode='w')
        log.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logger.addHandler(console)
        logger.addHandler(log)

        logger = logging.getLogger("statistics")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        filename = '{}_{}'.format(
            datetime.now().strftime('%Y%m%d_%H%M%S'), outputstatistics)
        statistics = logging.FileHandler(filename, mode='w')
        logger.addHandler(statistics)

        Logger.__instance = self


    ## コンソール＆ログファイルへのINFO出力
    def loginfo(self, msg):
        log = logging.getLogger("log")
        log.info(msg)

    ## コンソール＆ログファイルへのERROR出力
    def logerror(self, msg):
        log = logging.getLogger("log")
        log.error(msg)

    ## コンソール＆ログファイルへのDEBUG出力
    def logdebug(self, msg):
        log = logging.getLogger("log")
        log.debug(msg)

    ## 統計ファイルへのINFO出力
    def statinfo(self, msg):
        log = logging.getLogger("statistics")
        log.info(msg)

    ## 統計ファイルへのINFO出力
    def staterror(self, msg):
        log = logging.getLogger("statistics")
        log.error(msg)

    ## 統計ファイルへのDEBUG出力
    def statdebug(self, msg):
        log = logging.getLogger("statistics")
        log.debug(msg)
