from config.constants import (TIMEOUT_VERY_SHORT, TIMEOUT_SHORT,TIMEOUT_LONG,
                              TIMEOUT_1_SEC,EXPECT_SESA_TEST_ENV,EXPECT_SESA_CHOSE_ENV)

def handle_store_selection_vn_sesa(page):
    """
    處理店鋪選擇：
    1. 確認表格是否有資料。
    2. 如果有資料，檢查表格內是否有目標選項 `"EXPECT_TEST_ENV"`。
    3. 移除目標選項以外的其他選項。
    4. 如果目標選項不存在，添加該選項。
    5. 保存改動，並等待彈出保存成功通知。
    """
    # 等待表格加載完成
    # 檢查表格是否存在數據
    if page.locator("#addedStoreTable tbody tr").count() == 0:
        print("表格無數據，直接進入添加流程")
    else:
        page.wait_for_selector("#addedStoreTable tbody tr", timeout=TIMEOUT_LONG)

    # 檢查是否已存在「EXPECT_TEST_ENV」
    target_exists = page.locator(f"#addedStoreTable .addedStoreAlias:has-text('{EXPECT_SESA_TEST_ENV}')").count() > 0

    while True:
        # 獲取當前表格中的所有行
        non_target_rows = page.locator("#addedStoreTable tbody tr").all()
        removed_any = False  # 標誌是否有項目被移除

        for row in non_target_rows:
            # <talbe id="addedStoreTable">
            # <span class="addedStoreAlias">29 號測試環境</span>
            store_name = row.locator(".addedStoreAlias").inner_text().strip()
            # 跳過目標項「29 號測試環境」
            if EXPECT_SESA_CHOSE_ENV in store_name:

                continue

            # 定位移除按鈕
            # remove_button = row.locator("td div.removeStore:not([data-name='EXPECT_UYSTORE_TEST_NAME'])")
            remove_button = row.locator("td div.removeStore")
            if remove_button.count() > 0:
                try:
                    # 點擊按鈕並等待行移除
                    remove_button.wait_for(state="visible", timeout=TIMEOUT_SHORT)
                    remove_button.click()
                    row.wait_for(state="detached", timeout=TIMEOUT_SHORT) #元素確認從 DOM 中移除
                    removed_any = True
                    print(f"成功移除非目標項: {store_name}")
                except Exception as e:
                    # 移除操作失敗，記錄錯誤並跳過
                    print(f"移除失敗: {store_name}, 錯誤: {e}")
                    continue

        # 如果沒有任何項目被移除，則退出循環
        if not removed_any:
            break

    # 如果目標選項不存在，則添加它
    if not target_exists:
        try:
            page.locator("#storeKeyword").wait_for(state="visible", timeout=TIMEOUT_LONG)
            page.locator("#storeKeyword").fill(EXPECT_SESA_TEST_ENV)
            print(page.locator(".ui-menu-item-wrapper").all_text_contents())
            # .ui-menu-item-wrapper:has-text 這是一個選擇器，旨在查找包含指定文本（`EXPECT_THAI_SESA_ENV`）的 HTML 元件。
            # #CSS 選擇器中的 `has-text` 選項是 Playwright 提供的語法，表示查找包含特定文本的元素（如 `<span>` 或 `<div>` 元素）。
            page.wait_for_timeout(TIMEOUT_1_SEC)
            page.locator(".ui-menu-item-wrapper").filter(has_text=EXPECT_SESA_CHOSE_ENV).click()
            #點擊 加入
            page.wait_for_timeout(TIMEOUT_1_SEC)
            page.locator("#addStoreBtn").wait_for(state="visible", timeout=TIMEOUT_LONG)
            page.locator("#addStoreBtn").click()
            print(f"已添加目標選項：{EXPECT_SESA_TEST_ENV}")

        except Exception as e:
            print(f"添加目標項失敗: {e}")

    # 最後儲存變更 - 點擊「更新/儲存」按鈕
    try:
        page.on("dialog", lambda dialog: dialog.accept())
        # 儲存變更按鈕
        page.wait_for_timeout(TIMEOUT_1_SEC)
        save_button = page.locator("#updateUserBtn")
        save_button.wait_for(state="visible", timeout=TIMEOUT_LONG)
        save_button.click()
        page.wait_for_timeout(TIMEOUT_SHORT)

        #儲存成功 確認框
        page.wait_for_selector("#messageModalBtn", timeout=TIMEOUT_LONG)  # 等待成功訊息
        page.locator("#messageModalBtn").click()

        print("儲存變更成功")
    except Exception as e:
        print(f"儲存變更失敗: {e}")

