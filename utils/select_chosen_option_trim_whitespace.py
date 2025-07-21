from playwright.sync_api import Page, expect
import logging
from config.constants import TIMEOUT_1_SEC, TIMEOUT_500_MS

logger = logging.getLogger("conftest")  # 使用模組名稱作為 logger 的名稱
logger.info("在 select_chosen_option 文件中使用 conftest Logger")

def select_chosen_option(page, select_id: str, target_text: str, display_text: str, timeout: int = 10000) -> None:
    """
    選擇指定的 Chosen 下拉選單選項並驗證顯示文字。

    Args:
        page (Page): Playwright 的 Page 對象
        select_id (str): 下拉選單的 ID（例如 'q_uystore'）
        target_text (str): 目標選項的完整文字（例如 'uy_2f_stage(上洋29號 stage 環境)'）
        display_text (str): 預期顯示的文字（例如 'uy_2f_stage(上洋29號 stage 環境)'）
        timeout (int): 超時時間（毫秒），預設為 10000 毫秒
    """
    chosen_container = page.locator(f"#{select_id}_chosen")
    expect(chosen_container).to_be_visible()
    page.wait_for_timeout(TIMEOUT_1_SEC)

    # 先等待 Chosen 下拉選單完全載入（確保 option 存在）
    page.wait_for_selector(f"#{select_id} option", state="attached", timeout=timeout)

    # 評估 JavaScript：忽略多餘空格匹配，並添加 debug 輸出所有 option 文字
    result = page.evaluate(f"""
        var selectElement = document.getElementById('{select_id}');
        var options = selectElement.getElementsByTagName('option');
        var optionTexts = [];
        var found = false;
        var normalizedTarget = '{target_text}'.replace(/\\s+/g, ' ').trim().toLowerCase();

        for (var i = 0; i < options.length; i++) {{
            var optionText = options[i].text.replace(/\\s+/g, ' ').trim().toLowerCase();
            optionTexts.push(options[i].text);  // 收集所有原始 option 文字用於 debug
            if (optionText.includes(normalizedTarget)) {{
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
        return optionTexts;  // 返回所有 option 文字用於 debug
    """)

    # 輸出 debug 資訊：所有 option 文字
    logger.info(f"所有 option 文字: {result}")

    page.wait_for_timeout(TIMEOUT_500_MS)
    expect(page.locator(f"#{select_id}_chosen span")).to_contain_text(display_text)