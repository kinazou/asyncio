import time
import math

class Timer:
    start_time = 0
    end_time = 0
    result_time = 0
    lap_st = 0

    def start(self):
        self.start_time = time.time()
        self.lap_st = self.start_time

    def stop(self):
        self.end_time = time.time()
        self.result_time = round(self.end_time - self.start_time, 2)

    def get_string(self):
        return self.make_string(self.result_time)

    def get_string_lap(self):
        lap = time.time()
        st = self.lap_st
        self.lap_st = lap
        return self.make_string(round(lap - st, 2))

    def get(self):
        return self.result_time

    def make_string(self, result_time):
        ms, hms = math.modf(result_time)
        hour = math.floor(hms / 3600)
        mint = math.floor((hms % 3600) / 60)
        secd = math.floor(hms % 60)
        msec = math.floor(ms * 100)
        return str(hour).zfill(2) + "時間" + str(mint).zfill(2) + "分" + \
            str(secd).zfill(2) + "秒" + str(msec).zfill(2) + "ミリ秒"
