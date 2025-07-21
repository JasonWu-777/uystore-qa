from config.constants import TIMEOUT_SHORT, EXPECT_UY_SECOND_STORE_TEST_ENV, EXPECT_TEST_ENV, TIME_OUT_500_MS
from playwright.sync_api import expect

def add_store(page, store_name: str):
    """
    在網頁中添加指定的店鋪項目。
    """
    try:
        page.locator("#storeKeyword").click()
        page.wait_for_selector(".ui-menu-item-wrapper", timeout=TIMEOUT_SHORT)
        page.locator(".ui-menu-item-wrapper").filter(has_text=store_name).click()
        page.locator("#addStoreBtn").click()
        # 開始無資料，第一次加入進入下拉選單時候這種狀態會在 thead 標題行
        # expect(page.locator(f"#addedStoreTable thead tr >> text={store_name}")).to_be_visible(timeout=TIMEOUT_SHORT)
        # 進入頁面當兩個店家已經在之前選好在下拉選單當中 tbody 是數據行
        # expect(page.locator(f"#addedStoreTable tbody tr:has-text('{store_name}')")).to_be_visible(timeout=TIMEOUT_SHORT)
        page.wait_for_timeout(TIME_OUT_500_MS)
    except Exception as e:
        print(f"Failed to add store '{store_name}': {e}")
        raise

def handle_two_store(page):
    """
    處理店鋪表格，確保只包含兩個目標項目，並更新設定。
    """
    try:
        # 等待表格出現
        page.wait_for_selector("#addedStoreTable", state="visible", timeout=10000)
        # 獲取所有行
        rows = page.locator("#addedStoreTable tbody tr").all()

        # 處理空表格
        if len(rows) == 0:
            print("表格無數據，直接添加目標店鋪")
            add_store(page, EXPECT_TEST_ENV)
            add_store(page, EXPECT_UY_SECOND_STORE_TEST_ENV)
        else:
            # 檢查目標項目是否存在（精確匹配）
            target_29_exists = any(
                row.locator(".addedStoreAlias").inner_text(timeout=5000).strip() == EXPECT_TEST_ENV for row in rows
            )
            target_70_exists = any(
                row.locator(".addedStoreAlias").inner_text(timeout=5000).strip() == EXPECT_UY_SECOND_STORE_TEST_ENV for row in rows
            )

            # 移除非目標項目
            for row in rows:
                store_name = row.locator(".addedStoreAlias").inner_text(timeout=5000).strip()
                if store_name != EXPECT_TEST_ENV and store_name != EXPECT_UY_SECOND_STORE_TEST_ENV:
                    row.locator(".removeStore").click()
                    expect(row).not_to_be_attached(timeout=TIMEOUT_SHORT)

            # 添加缺失的目標項目
            if not target_29_exists:
                add_store(page, EXPECT_TEST_ENV)
            if not target_70_exists:
                add_store(page, EXPECT_UY_SECOND_STORE_TEST_ENV)

        # 更新並關閉模態框
        page.locator("#updateUserBtn").click()
        page.locator("#messageModalBtn").click()
        page.wait_for_timeout(TIMEOUT_SHORT)
    except Exception as e:
        print(f"處理店鋪表格時出錯: {e}")
        raise