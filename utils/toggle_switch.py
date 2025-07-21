def toggle_switch(page, target_state, locator):
    """
    切換開關狀態為指定的目標狀態 (toggle-on 或 toggle-off)。

    :param page: Playwright 的 Page 對象。
    :param target_state: 要切換到的目標狀態，"toggle-on" 或 "toggle-off"。
    :param locator: 開關按鈕的 CSS 選擇器。
    :raises ValueError: 當指定的目標狀態無效時。
    :raises Exception: 當切換失敗時。
    """
    # 確認目標狀態是否有效
    if target_state not in ["toggle-on", "toggle-off"]:
        raise ValueError(f"Invalid target_state: {target_state}. Must be 'toggle-on' or 'toggle-off'.")

    # 定位元素
    toggle_element = page.locator(locator)

    # 獲取當前按鈕的 class 屬性來判斷狀態
    current_class = toggle_element.get_attribute("class")
    if not current_class:
        raise Exception("Unable to fetch class attribute from the toggle element.")

    # 判斷是否需要切換
    if target_state in current_class:
        print(f"Already in the desired state: {target_state}. No action needed.")
        return  # 已經是目標狀態，無需切換

    # 執行點擊切換
    toggle_element.click()

    # 等待操作完成
    page.wait_for_timeout(1000)  # 等待 1 秒讓狀態穩定

    # 驗證是否已經切換為目標狀態
    new_class = toggle_element.get_attribute("class")
    if target_state in new_class:
        print(f"Toggle successfully switched to '{target_state}'.")
    else:
        raise Exception(f"Failed to switch toggle to '{target_state}'. Current state: {new_class}")

'''
example:test_006_店長為訂閱[消費查詢]功能
# 將開關切換到 "關閉" 狀態
toggle_switch(page, "toggle-off", '[for="monitorEnabled"].btn-primary')

# 將開關切換到 "開啟" 狀態
toggle_switch(page, "toggle-on", '[for="monitorEnabled"].btn-primary')


'''