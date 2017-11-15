# -*- coding: utf-8 -*-
#!/usr/bin/python
#encoding: utf-8
import sys
import ctypes
import logging
import logging.handlers

reload(sys)
sys.setdefaultencoding('utf-8')

LOG_FILE = 'test_log'

logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s - %(levelname)s -%(process)d- %(filename)s:%(funcName)s:%(lineno)d - %(message)s',
    level=logging.DEBUG)
logging.handlers.TimedRotatingFileHandler(LOG_FILE, when='W0', backupCount=5)
logger = logging.getLogger(__name__)
def ttt():
    print '..........'
    logger.info('-*-*-*-*-*-*-*-*-*-*-')

if __name__ == "__main__":
    ttt()
    logger.info("hello info")
    logger.error("hello info")
    logger.warn("hello info")