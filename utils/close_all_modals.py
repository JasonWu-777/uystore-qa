from playwright.sync_api import Page, expect

def close_all_modals(page: Page) -> None:
    modal_buttons = [
        "#messageModalBtn",
        "#checkPaymentModalBtn",
        "#checkDateModalBtn",
        "#confirmModalBtn"
    ]
    max_attempts = 5  # 避免無限循環
    for attempt in range(max_attempts):
        modal_closed = True
        # 記錄當前可見的模態按鈕
        visible_buttons = [btn for btn in modal_buttons if page.locator(btn).is_visible(timeout=3000)]
        print(f"嘗試 {attempt + 1}/{max_attempts} - 可見的模態按鈕: {visible_buttons}, URL: {page.url}")

        for btn in modal_buttons:
            try:
                if page.locator(btn).is_visible(timeout=3000):
                    print(f"點擊模態按鈕 {btn}")
                    page.locator(btn).click(timeout=10000)
                    page.wait_for_timeout(2000)  # 增加等待時間以確保動畫完成
                    modal_closed = False
            except Exception as e:
                print(f"無法點擊按鈕 {btn} (URL: {page.url}): {e}")
                continue

        # 檢查並移除 modal-backdrop
        try:
            backdrop_count = page.locator(".modal-backdrop").count()
            if backdrop_count > 0:
                print(f"檢測到 {backdrop_count} 個 modal-backdrop，嘗試移除")
                for _ in range(3):
                    page.evaluate(
                        '() => document.querySelectorAll(".modal-backdrop").forEach(el => el.remove())')
                    page.wait_for_timeout(2000)
                    if page.locator(".modal-backdrop").count() == 0:
                        break
                if page.locator(".modal-backdrop").count() > 0:
                    print(f"移除 {backdrop_count} 個 modal-backdrop 失敗")
                    modal_closed = False
                else:
                    page.wait_for_selector(".modal-backdrop", state="detached",
                                           timeout=10000)
                    print("modal-backdrop 已成功移除")
        except Exception as e:
            print(f"移除 modal-backdrop 失敗 (URL: {page.url}): {e}")
            continue

        # 每次循環後等待頁面穩定
        try:
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception as e:
            print(f"等待 networkidle 失敗 (URL: {page.url}): {e}")

        # 如果所有模態對話框和背景遮罩都關閉，退出循環
        if modal_closed:
            print(f"所有模態對話框已關閉，嘗試次數: {attempt + 1}")
            break

    # 最終檢查模態對話框狀態
    modal_ids = ["#messageModal", "#checkPaymentModal", "#checkDateModal"]
    for modal_id in modal_ids:
        try:
            if page.locator(modal_id).count() > 0:
                if page.locator(modal_id).is_visible(timeout=3000):
                    print(f"模態對話框 {modal_id} 仍可見，檢查 aria-hidden")
                    expect(page.locator(modal_id)).to_have_attribute("aria-hidden", "true", timeout=10000)
                else:
                    print(f"模態對話框 {modal_id} 已不可見")
            else:
                print(f"模態對話框 {modal_id} 不存在")
        except Exception as e:
            print(f"檢查模態對話框 {modal_id} 失敗: {e}")

    # 確保 modal-backdrop 已移除
    try:
        expect(page.locator(".modal-backdrop")).to_have_count(0, timeout=10000)
    except Exception as e:
        print(f"modal-backdrop 未完全移除: {e}")

    # 最終檢查是否有殞留的模態對話框
    if any(page.locator(btn).is_visible(timeout=3000) for btn in modal_buttons):
        raise Exception(f"仍有模態對話框未關閉，測試失敗: {visible_buttons}")