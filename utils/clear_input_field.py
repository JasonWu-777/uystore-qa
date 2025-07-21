from playwright.sync_api import Page, expect

def clear_input_field(page, selector):
    """
       使用模擬鍵盤操作清空指定的輸入框。

       :param page: Playwright 的 Page 對象
       :param selector: locator 輸入框的 CSS 選擇器，例如 "#refundDate"
       """
    # 定位輸入框
    input_field = page.locator(selector)

    # 確保輸入框可見並可交互
    input_field.wait_for(state="visible")

    # 點擊輸入框以獲得焦點
    input_field.click()

    # 模擬按下 Control+A 全選文本
    input_field.press("Control+A")

    # 模擬按下 Backspace 鍵刪除選中文本
    input_field.press("Backspace")

    # 驗證輸入框是否已清空
    current_value = input_field.input_value()
    print(f"鍵盤清空後 {selector} 的值: {current_value}")
    assert current_value == "", f"無法清空 {selector}，當前值為: {current_value}"