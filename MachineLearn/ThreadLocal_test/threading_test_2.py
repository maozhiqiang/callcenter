# coding=utf-8
import threading
from time import sleep, ctime

loops = [4, 2]  # 睡眠时间


class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):  # run()函数
        apply(self.func, self.args)


def loop(nloop, nsec):
    print "Start loop", nloop, 'at:', ctime()
    sleep(nsec)
    print 'Loop', nloop, 'done at:', ctime()


def main():
    print 'Starting at:', ctime()
    threads = []
    nloops = range(len(loops))  # 列表[0,1]

    for i in nloops:
        # 子类MyThread实例化，创建所有线程
        t = MyThread(loop, (i, loops[i]), loop.__name__)
        threads.append(t)

        # 开始线程
    for i in nloops:
        threads[i].start()

        # 等待所有结束线程
    for i in nloops:
        threads[i].join()

    print 'All end:', ctime()


if __name__ == '__main__':
    main()