from datetime import datetime, timedelta
from config.constants import TIMEOUT_VERY_SHORT

# 30天內到期 狀控使用之
def select_date_after_30_day(page, date_selector):
    today = datetime.now()
    thirty_days_later = today + timedelta(days=30)
    target_date = thirty_days_later.strftime("%Y/%m/%d")
    page.click(date_selector)
    page.fill(date_selector, target_date)
    page.keyboard.press("Enter")
