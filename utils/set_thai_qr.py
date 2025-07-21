def set_thai_qr(page) -> None:
    """Set the Thai QR toggle if it's not already enabled."""

    # 打開 Payment Setting 頁面並選擇店鋪
    page.get_by_role("link", name="Payment Setting").click()
    page.get_by_role("textbox", name="Query a shop").fill("u")  # 依據篩選條件填寫
    page.get_by_text("Query").click()
    page.wait_for_load_state("networkidle")
    page.get_by_role("cell", name="EXPECT_UYSTORE_TEST_NAME").click()



    # 檢查是否需要切換開關
    thai_qr_toggle_off = page.locator("label[for='thaiQREnabled'].toggle-off")  # 定位關閉狀態
    thai_qr_toggle_on = page.locator("label[for='thaiQREnabled'].toggle-on")  # 定位開啟狀態

    if thai_qr_toggle_off.count() == 1:
        print("Thai QR toggle is off. Turning it on.")
        thai_qr_toggle_off.click()  # 點擊切換為開啟狀態
    elif thai_qr_toggle_on.count() == 1:
        print("Thai QR toggle is already on. Skipping.")
    else:
        print("Unable to determine the exact state of the Thai QR toggle.")

    page.wait_for_load_state("networkidle")
    page.get_by_text("Confirm", exact=True).click()

    page.wait_for_load_state("networkidle")
    page.locator("#messageModalBtn").click()