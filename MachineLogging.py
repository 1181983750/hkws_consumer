import logging
from logging.handlers import TimedRotatingFileHandler

from django.conf import settings
from httpAsyncClient.Config import Config

# 创建 logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# logger.propagate = 0

formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
# fh = TimedRotatingFileHandler(Config.log_path, when='A', interval=1, backupCount=3, encoding='utf-8')
# fh.setFormatter(formatter)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
consoleHandler.setLevel(logging.DEBUG)
# 创建一个输出到文件的 handler
fileHandler = logging.FileHandler(Config.log_path, mode='a', encoding='utf-8')
fileHandler.setFormatter(formatter)
fileHandler.setLevel(logging.INFO)
if settings.DEBUG:
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)
else:
    fileHandler.setLevel(logging.INFO)

logger.addHandler(fileHandler)



