"代理池全局参数设置"


#代理池参数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
POOL_CAPACITY = 200

#Mongo数据库连接
MONGO_HOST = 'mongodb://localhost:27017'
MONGO_KEY = 'proxy'

#调度器循环周期：
TEST_CYCLE = 60
GET_CYCLE = 20
API_ENABLED = True
TEST_ENABLED = True
GET_ENABLED = False

#测试模块设置
TEST_URL = 'http://www.bilibili.com'
BATCH_TEST_SIZE = 20
VALID_STATUS_CODES = [200]

#页面爬取设置
STEP_PAGES = 10 #每次爬取的页面数量
MAX_PAGE = 50 #爬取的最大页数设置
