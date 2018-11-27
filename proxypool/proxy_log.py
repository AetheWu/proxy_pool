import logging

'''设置日志格式'''

logger = logging.getLogger('parent')

logger.setLevel(level=logging.DEBUG)

formattr = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('errors.log')
stream_handler = logging.StreamHandler()

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

