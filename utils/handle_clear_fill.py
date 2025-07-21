def handle_clear_fill(page, locatID):
    def clear_and_fill(locator, value=""):
        locator.click()
        locator.press("Control+A")  # 全選
        locator.press("Backspace")  # 删除
        current_value = locator.input_value()
        print(f"鍵盤清空後 #{locatID} 的值: {current_value}")
        locator.fill(value)

    locat_input = page.locator(f"#{locatID}")
    clear_and_fill(locat_input)
