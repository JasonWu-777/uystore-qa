from playwright.sync_api import Page, expect
import logging
from config.constants import TIMEOUT_1_SEC, TIMEOUT_500_MS


logger = logging.getLogger("conftest")  # 使用模組名稱作為 logger 的名稱
logger.info("在 select_chosen_option 文件中使用 conftest Logger")

def select_chosen_option(page, select_id: str, target_text: str, display_text: str, timeout: int = 10000) -> None:
    """
    這個方法的特點是不模擬使用者的滑鼠點擊，而是直接執行 JavaScript 來修改底層 <select> 元素的值，然後通知 Chosen 更新畫面。
    這種方法通常執行速度更快，也比較不容易受畫面動畫或延遲影響。
    選擇指定的 Chosen 下拉選單選項並驗證顯示文字。

    Args:
        page (Page): Playwright 的 Page 對象
        select_id (str): 下拉選單的 ID（例如 'poc_select_truck'）
        target_text (str): 目標選項的完整文字（例如 '(qa-sale) 測試車號'）
        display_text (str): 預期顯示的文字（例如 '測試車號'）
        timeout (int): 超時時間（毫秒），預設為 10000 毫秒
    """
    chosen_container = page.locator(f"#{select_id}_chosen")
    expect(chosen_container).to_be_visible()
    page.wait_for_timeout(TIMEOUT_1_SEC)
    page.evaluate(f"""
        var selectElement = document.getElementById('{select_id}');
        var options = selectElement.getElementsByTagName('option');
        var found = false;
        for (var i = 0; i < options.length; i++) {{
            if (options[i].text.includes('{target_text}')) {{
                selectElement.selectedIndex = i;
                found = true;
                selectElement.dispatchEvent(new Event('change', {{ bubbles: true }}));
                break;
            }}
        }}
        if (!found) {{
            throw new Error('未找到目標選項: {target_text}');
        }}
        if (window.jQuery) {{
            jQuery('#{select_id}').trigger('chosen:updated');
        }} else {{
            throw new Error('jQuery 未載入，無法更新 Chosen 下拉選單');
        }}
    """)

    page.wait_for_timeout(TIMEOUT_500_MS)
    expect(page.locator(f"#{select_id}_chosen span")).to_contain_text(display_text)