# coding:utf-8
import re
import logging
import logging.handlers

LOG_FILE = './log/weibo_crawler'

sh = logging.StreamHandler()
trfh = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when="H", interval=4, backupCount=36)  # 实例化handler
trfh.suffix = "%Y-%m-%d_%H-%M.log"
trfh.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")

fmt = '[%(levelname)s]%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)   # 实例化formatter
trfh.setFormatter(formatter)      # 为handler添加formatter

logger = logging.getLogger('weibo_crawler')    # 获取名为tst的logger
logger.addHandler(trfh)           # 为logger添加handler
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)