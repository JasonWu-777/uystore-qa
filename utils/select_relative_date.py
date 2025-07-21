from datetime import datetime, timedelta


def select_relative_date(page, date_selector, days):
    """
    選擇相對於當前日期的日期。

    :param page: Playwright 的 Page 對象
    :param date_selector: 日期選擇器
    :param days: 相對於今天偏移的天數，正數表示未來，負數表示過去
    """
    target_date = (datetime.now() + timedelta(days=days)).strftime("%Y/%m/%d")
    page.click(date_selector)
    page.fill(date_selector, target_date)
    page.keyboard.press("Enter")
