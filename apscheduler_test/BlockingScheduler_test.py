#!/usr/bin/env python
# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler


def my_job():
    print 'hello world'


sched = BlockingScheduler()
sched.add_job(my_job, 'interval', seconds=1)
sched.start()