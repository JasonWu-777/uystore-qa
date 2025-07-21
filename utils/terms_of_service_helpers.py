import os
from pypdf import PdfReader
from config.constants import PDF_SAVE_FOLDER
from datetime import datetime, timedelta


PDF_SAVE_FOLDER = "../download"

def download_pdf(page, pdf_url: str, save_file_name: str) -> str:
    """下載 PDF 文件到指定路徑，並返回文件路徑"""
    os.makedirs(PDF_SAVE_FOLDER, exist_ok=True)
    pdf_file_path = os.path.join(PDF_SAVE_FOLDER, save_file_name)
    response = page.request.get(pdf_url)
    if response.status == 200:
        with open(pdf_file_path, "wb") as pdf_file:
            pdf_file.write(response.body())
        print(f"PDF 檔案已下載並保存到: {pdf_file_path}")
    else:
        raise Exception(f"無法下載 PDF 文件，HTTP 狀態碼 {response.status}")
    return pdf_file_path

def validate_pdf_content(pdf_file_path: str, expected_text: str) -> None:
    """驗證 PDF 文件是否包含指定內容"""
    reader = PdfReader(pdf_file_path)
    pdf_text = "".join(page.extract_text() for page in reader.pages)
    assert expected_text in pdf_text, f"PDF 驗證失敗: 未找到預期文字 '{expected_text}'"
    print("PDF 驗證成功，包含正確內容！")


# 共用函式：獲取使用者名稱和密碼
def get_credentials(user_credentials, user_type):
    credentials = user_credentials[user_type]
    username = credentials["username"]
    password = credentials["password"]
    return username, password


def select_date_in_three_months(page, date_selector):
    today = datetime.now()
    three_months_later = today + timedelta(days=90)  # 推算大約90天
    # 格式化為適合你的日期輸入框的格式，例如 "YYYY/MM/DD"
    target_date = three_months_later.strftime("%Y/%m/%d")
    # 模擬點擊日期欄位
    page.click(date_selector)
    page.fill(date_selector, target_date)
    page.keyboard.press("Enter")

# 獲取並拼接 PDF 文件的 URL
def get_conect_URL(page, filename, url):
    page.get_by_role("link", name=filename).click()
    relative_href = page.get_by_role("link", name=filename).get_attribute("href")
    popup_url = f"https://stage.upyoung.com.tw{relative_href}" if relative_href.startswith("/") else relative_href
    return popup_url