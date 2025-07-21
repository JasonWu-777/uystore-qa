import os
import subprocess
import argparse
import logging
import sys
import threading
from utils.test_utils import animation_worker, clear_pytest_cache

# 指定測試資料夾的根目錄，方便更改
test_root_dir = r"C:\Users\User\PycharmProjects\artemis-qa\tests"
DEFAULT_TIMEOUT = 20000  # 預設超時時間（毫秒）
DEFAULT_SLOWMO = 500  # 預設 slowmo 值（毫秒）

# 設置日誌
logger = logging.getLogger("run_pytest_by_folder")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def run_pytest_by_folder(root_dir, timeout=DEFAULT_TIMEOUT, slowmo=DEFAULT_SLOWMO):
    """執行指定根目錄下所有子資料夾的 pytest 測試

    Args:
        root_dir: 測試檔案的根目錄
        timeout: 全域超時設置（毫秒）
        slowmo: Playwright slowmo 值（毫秒）
    """
    # 記錄使用的參數
    logger.info(f"使用全域超時設置: {timeout}ms")
    logger.info(f"使用 slowmo 值: {slowmo}ms")

    # 檢查根目錄是否存在
    if not os.path.isdir(root_dir):
        logger.error(f"錯誤：{root_dir} 不是一個有效的資料夾")
        return

    # 清理 pytest 快取
    clear_pytest_cache(root_dir)

    # 遍歷根目錄下的所有子資料夾
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)

        # 只處理資料夾
        if os.path.isdir(folder_path):
            logger.info(f"\n=== 開始執行資料夾 {folder_path} 的測試 ===")

            # 創建動畫線程
            stop_animation = threading.Event()
            animation_thread = threading.Thread(target=animation_worker, args=(stop_animation,))
            animation_thread.daemon = True
            animation_thread.start()

            # 執行 pytest，指定資料夾並使用 UTF-8 編碼
            try:
                # 定義 pytest 參數
                pytest_params = [
                    "-v", 
                    f"--slowmo={slowmo}", 
                    "--tracing",
                    "retain-on-failure",
                    f"--timeout={timeout}"
                ]

                logger.info(f"運行 pytest 使用的參數: {' '.join(pytest_params)}")
                logger.info(f"slowmo 的數值: {slowmo}")
                logger.info(f"timeout 的數值: {timeout}")

                result = subprocess.run(
                    ["pytest", folder_path] + pytest_params,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",  # 明確指定 UTF-8 編碼
                    errors="replace",  # 替換無法解碼的字元
                    shell=True  # Windows 兼容
                )
                # 輸出 pytest 執行結果
                logger.info(result.stdout)
                if result.returncode == 0:
                    logger.info(f"資料夾 {folder_path} 測試成功")
                else:
                    logger.error(f"資料夾 {folder_path} 測試失敗")
                    logger.error(f"錯誤輸出：{result.stderr}")
            except Exception as e:
                logger.error(f"執行資料夾 {folder_path} 時發生錯誤：{e}")
                logger.warning("測試可能因編碼問題失敗，請檢查 pytest 輸出")
            finally:
                # 停止動畫
                stop_animation.set()
                animation_thread.join()


if __name__ == "__main__":
    # 設置命令行參數解析
    parser = argparse.ArgumentParser(description='執行 pytest 測試，支援全域超時設置')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT,
                        help=f'全域超時設置（毫秒），預設值: {DEFAULT_TIMEOUT}')
    parser.add_argument('--slowmo', type=int, default=DEFAULT_SLOWMO,
                        help=f'Playwright slowmo 值（毫秒），預設值: {DEFAULT_SLOWMO}')
    parser.add_argument('--dir', type=str, default=test_root_dir,
                        help=f'測試檔案的根目錄，預設值: {test_root_dir}')

    args = parser.parse_args()

    # 執行測試，使用命令行參數
    run_pytest_by_folder(args.dir, args.timeout, args.slowmo)
