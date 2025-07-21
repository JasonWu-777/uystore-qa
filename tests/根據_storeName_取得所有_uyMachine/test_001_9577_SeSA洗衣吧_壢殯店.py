import pytest
import logging
import json
import re
from playwright.sync_api import sync_playwright, Page, expect

from config.constants import SeSA_Coin_Laundry_Lee_Funeral_Store, TIMEOUT_5_SEC

# 設置日誌（無變化）
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
if not logger.handlers:
    logger.addHandler(handler)

def extract_json_from_html(page: Page):
    """
    從 HTML 頁面中提取 JSON 數據（無變化，但添加維護檢查）
    """
    logger.info(f"正在從 {SeSA_Coin_Laundry_Lee_Funeral_Store} 提取數據")
    page.wait_for_load_state("networkidle")
    content = page.content()

    # 检查维护状态
    if "系統維護中" in content or "此服務尚未申請開通" in content:
        logger.warning("頁面顯示系統維護中")
        return None

    # 嘗試 regex 找 storeInfo（無變化）
    json_match = re.search(r'var\s+storeInfo\s*=\s*({.*?});', content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            logger.error("無法解析 JSON")
            return None

    # 執行 JS 找數據（無變化）
    try:
        result = page.evaluate("""() => {
            if (typeof storeInfo !== 'undefined') {
                return storeInfo;
            }
            const dataElement = document.querySelector('#storeData');
            if (dataElement) {
                return JSON.parse(dataElement.textContent);
            }
            return null;
        }""")
        return result
    except Exception as e:
        logger.error(f"JS 提取失敗: {e}")
        return None

@pytest.fixture(scope="function")
def browser_page(page: Page):
    page.set_default_timeout(30000)  # 增加 timeout
    yield page
    page.close()

def test_store_info_api(browser_page: Page):
    """
    測試 SeSA洗衣吧 壢殯店 API 回應
    """
    logger.info("開始測試")

    # 訪問頁面
    logger.info(f"訪問頁面: {SeSA_Coin_Laundry_Lee_Funeral_Store}")
    browser_page.goto(SeSA_Coin_Laundry_Lee_Funeral_Store)
    browser_page.wait_for_load_state("networkidle")

    # 新增調試：截圖和 print 內容
    logger.info(f"頁面內容片段: {browser_page.content()[:500]}...")  # 只 print 前 500 字，避免太長

    # 使用 on(response) 監聽 API 回應（更穩健的方法）
    data = None
    logger.info("使用 on(response) 監聽 API 回應")
    api_response = [None]  # 用 list 避免 nonlocal 問題
    def handle_response(resp):
        if "getStoreInfo" in resp.url and resp.status == 200:
            api_response[0] = resp
            logger.info(f"監聽到 API: {resp.url}")

    browser_page.on("response", handle_response)
    # 重新載入頁面觸發請求
    browser_page.reload()
    browser_page.wait_for_timeout(TIMEOUT_5_SEC)

    if api_response[0]:
        data = api_response[0].json()
    else:
        logger.info("未攔截到 API，fallback 到頁面提取")
        data = extract_json_from_html(browser_page)

    if not data:
        pytest.fail("無法獲取數據")

    logger.info(f"數據: {json.dumps(data, ensure_ascii=False, indent=2)}")

    # 斷言（無變化）
    assert "success" in data and data["success"], "success 不為 True"
    assert "notDtcMachines" in data, "無 notDtcMachines"
    not_dtc_machines = data["notDtcMachines"]
    assert len(not_dtc_machines) > 0, "陣列空"

    target = next((m for m in not_dtc_machines if m.get("alias") == "9號機上烘"), None)
    assert target, "沒找到機器"
    assert target.get("type_code") == "dryer", f"type_code 錯: {target.get('type_code')}"

    logger.info("測試通過 9號機上烘 type_code== dryer")
