# config/constants.py

# 時間相關配置

TIMEOUT_VERY_SHORT = 500
TIMEOUT_SHORT = 6000  # 用於短時等待時間，例如按鈕點擊後的超時
TIMEOUT_LONG = 12000  # 用於較長等待的操作
DEFAULT_PAGE_TIMEOUT = 20000
DEFAULT_TIMEOUT = 15000

TIMEOUT_500_MS = 500
TIMEOUT_1_SEC = 1000
TIMEOUT_2_SEC = 2000
TIMEOUT_3_SEC = 3000
TIMEOUT_5_SEC = 5000
# 其他常數
MAX_TEXT_LENGTH = 10  # 限制文字輸入框的最大字元數


# 預設測試 URL
CLEANCHAIN_VN = "cleanchainvn"
SESA_VN = "artemisvn"
AQUA_MY = "artemismy"
AQUA_US = "artemisus"
STORE_OWNER_U = "storeowneru"
AQUA_TW = "artemis"


# 預設測試 URL
BASE_URL = "https://stage.upyoung.com.tw"
# 這些網址不要組合起來變成 f"{BASE_URL}/artemis/storeowneru/login 因為這樣會很難做測試，降低工作效率

ARTEMIS_MONITOR_URL = "https://stage.upyoung.com.tw/artemis/monitor/gZK70"
# 泰國
CLEAN_CHAIN_URL = "https://stage.upyoung.com.tw/artemisthc/storeowneru/login"
# 越南
SESA_VN_URL="https://stage.upyoung.com.tw/artemisvn/storeowneru/login"
PDF_SAVE_FOLDER = "../download"

#資料匯出
# "洗 烘 少量"
VENA_EXPECT_WORD="Giặt sấy lượng ít"

EXPECT_CLIENT_TEXT ="親愛的客戶"
EXPECT_SERVE_TEXT="親愛的客戶，您在本系統平台的訂閱服務已到期，如您有意繼續使用本平台的服務，請於詳閱「SeSA洗衣吧店長系統-蒐集個人資料告知事項暨個人資料提供同意書」、「"
EXPECT_NO_SERVE_TEXT="此服務尚未申請開通"
EXPECT_NO_SUPPLY="未訂閱此服務，請至店鋪管理設定"
EXPECT_EXPIRE_TEXT ="Dear customer, your subscription service on this system platform will expire"
EXPECT_EXPIRE_ON_TEXT ="Notification service will expire on"
# 台灣店家名稱:上洋29號 stage 環境
EXPECT_TEST_ENV="自動化測試店"
EXPECT_TEST_DROP_CHOSE="自動化測試店"
EXPECT_UYSTORE_TEST_NAME="qa_test_store"

EXPECT_TEST_29_ENV = "上洋29號 stage 環境"
EXPECT_TEST_29_TEST_NAME = "uy_2f_stage"
# 泰國 Thailand
EXPECT_THAI_TEST_ENV = "CleanChain - สาขาจรัญสนิทวงศ์ 75"
EXPECT_THAI_CHOSE_ENV = "CleanChain"

# 越南vn : SESA COIN LAUNDRY- 33A NGUYEN HUU CANH
EXPECT_SESA_TEST_ENV = "SESA COIN LAUNDRY- 33A NGUYEN HUU CANH"
EXPECT_SESA_CHOSE_ENV= "SESA COIN LAUNDRY"
EXPECT_UY_SECOND_STORE_TEST_ENV = "上洋公司"
EXPECT_UY_SECOND_STORE_TEST_ENV_NAME = "upyoung"

# 台灣入口網站
LOGIN_URL = f"https://stage.upyoung.com.tw/artemis/storeowneru/login"
#正式環境
STAGE_MONITOR_URL = "https://stage.upyoung.com.tw/artemis/monitor/gZK70"
MIS_LOGIN_URL = "https://stage.upyoung.com.tw/galaxy/login.jsp"

# SeSA洗衣吧_壢殯店
SeSA_Coin_Laundry_Lee_Funeral_Store = "https://service.upyoung.com.tw/artemis/monitor/EsOcR"
# SeSA洗衣吧_壢殯店 API
SeSA_STORE_INFO_API = "https://service.upyoung.com.tw/artemis/public/fun/getStoreInfo"

PDF_SAVE_FOLDER = "../download"

# 預設的超時設置（單位：毫秒）
DEFAULT_TIMEOUT = 10000
BUTTON_CLICK_TIMEOUT = 2000  # 按鈕點擊的超時時間
TIMEOUT_SHORT  = 2000  # 用於短時等待時間，例如按鈕點擊後的超時
TIMEOUT_MIDDLE = 3000
TIMEOUT_LONG = 10000  # 用於較長等待的操作
TIMEOUT_LONG_5 = 5000
TIMEOUT_LONG_15 = 15000

TIME_OUT_500_MS = 500
TIME_OUT_1000_MS = 1000
