
from config.constants import TIMEOUT_VERY_SHORT, TIMEOUT_SHORT, TIMEOUT_LONG, TIMEOUT_1_SEC
from config.constants import EXPECT_TEST_ENV

def handle_store_selection(page):
    """
    處理店鋪選擇：
    1. 確認表格是否有資料。
    2. 如果有資料，檢查表格內是否有目標選項 `EXPECT_TEST_ENV`。
    3. 移除目標選項以外的其他選項。
    4. 如果目標選項不存在，添加該選項。
    5. 保存改動，並等待彈出保存成功通知。
    """
    # 檢查表格是否存在數據
    page.wait_for_load_state("networkidle")
    print("頁面載入完成")

    if page.locator("#addedStoreTable tbody tr").count() == 0:
        print("表格無數據，直接進入添加流程")
        target_exists = False
    else:
        page.wait_for_selector("#addedStoreTable tbody tr", timeout=TIMEOUT_LONG)
        # 檢查是否已存在「EXPECT_TEST_ENV」
        target_exists = page.locator(f"#addedStoreTable .addedStoreAlias:has-text('{EXPECT_TEST_ENV}')").count() > 0

        # 移除非目標店鋪
        while True:
            # 假設這邊可以抓到兩行，因為方法.all()可以抓到"自動化測試店"和"上洋公司"這邊non_target_rows是一個list?
            rows = page.locator("#addedStoreTable tbody tr").all()
            if len(rows) == 0:
                print("表格無數據")
                break
            removed_any = False  # 標誌是否有項目被移除
            for row in rows:
                try:
                    store_name = row.locator(".addedStoreAlias").inner_text().strip()
                    print(f"檢查店鋪: {store_name}")
                    if EXPECT_TEST_ENV in store_name:
                        continue
                    remove_button = row.locator("td div.removeStore")
                    if remove_button.count() > 0:
                        remove_button.wait_for(state="visible", timeout=TIMEOUT_SHORT)
                        remove_button.click()
                        removed_any = True
                        print(f"成功移除非目標項: {store_name}")
                        page.wait_for_timeout(TIMEOUT_VERY_SHORT)
                except Exception as e:
                    print(f"處理行時出錯: {e}")
                    continue

            if not removed_any:
                break
    # 檢查目標店鋪是否存在
    target_exists = page.locator(f"#addedStoreTable .addedStoreAlias:has-text('{EXPECT_TEST_ENV}')").count() > 0
    print(f"目標店鋪是否存在: {target_exists}")
    # 如果目標選項不存在，則添加它
    if not target_exists:
        try:
            page.locator("#storeKeyword").wait_for(state="visible", timeout=TIMEOUT_LONG)
            page.locator("#storeKeyword").fill(EXPECT_TEST_ENV)
            # 等待下拉選單出現並選擇目標選項
            page.wait_for_selector(f".ui-menu-item-wrapper:has-text('{EXPECT_TEST_ENV}')", timeout=TIMEOUT_LONG)
            page.locator(".ui-menu-item-wrapper").filter(has_text=EXPECT_TEST_ENV).click()
            # 點擊「加入」按鈕
            page.wait_for_timeout(TIMEOUT_1_SEC)
            page.locator("#addStoreBtn").wait_for(state="visible", timeout=TIMEOUT_LONG)
            page.locator("#addStoreBtn").click()
            print(f"已添加目標選項：{EXPECT_TEST_ENV}")
        except Exception as e:
            print(f"添加目標項失敗: {e}")

    # 儲存變更
    try:
        page.on("dialog", lambda dialog: dialog.accept())
        save_button = page.locator("#updateUserBtn")
        save_button.wait_for(state="visible", timeout=TIMEOUT_LONG)
        save_button.click()
        page.wait_for_timeout(TIMEOUT_SHORT)
        # 等待並確認儲存成功
        page.wait_for_selector("#messageModalBtn", timeout=TIMEOUT_LONG)
        page.locator("#messageModalBtn").click()
        print("儲存變更成功")
    except Exception as e:
        print(f"儲存變更失敗: {e}")