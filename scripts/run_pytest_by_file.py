import subprocess
from pathlib import Path
import logging
import sys
import os
import psutil
import argparse
import threading
from utils.test_utils import animation_worker, clear_pytest_cache

# 定義 slowmo 參數和目標測試位置
SLOWMO_VALUE = 500
DEFAULT_ROOT_DIR = r"C:\Users\User\PycharmProjects\artemis-qa\tests"
DEFAULT_TIMEOUT = 20000  # 預設超時時間（毫秒）

# 設置日誌
logger = logging.getLogger("conftest")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - [%(levelname)s] - %(filename)s:%(lineno)d (%(funcName)s) - %(message)s'
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info("scripts Logger 已設定。")

def run_pytest_by_file(root_dir: str, timeout: int = DEFAULT_TIMEOUT, slowmo: int = SLOWMO_VALUE):
    """執行指定根目錄下所有測試檔案的 pytest 測試，每次運行一個檔案

    Args:
        root_dir: 測試檔案的根目錄
        timeout: 全域超時設置（毫秒）- 注意：此參數目前未使用，因為 pytest-timeout 插件未安裝
        slowmo: Playwright slowmo 值（毫秒）
    """
    logger.info(sys.stdout.encoding)
    logger.info(f"使用 slowmo 值: {slowmo}ms")
    root_path = Path(root_dir)

    if not root_path.is_dir():
        logger.error(f"錯誤：{root_dir} 不是一個有效的資料夾")
        return

    # 清理 pytest 快取
    clear_pytest_cache(root_dir)

    # 尋找所有以 test_ 開頭的 .py 檔案
    test_files = list(root_path.rglob("test_*.py"))
    if not test_files:
        logger.warning(f"在 {root_dir} 中未找到任何測試檔案")
        return

    for test_file in test_files:
        logger.info(f"\n=== 開始執行測試檔案 {test_file} ===")
        # 創建動畫線程
        stop_animation = threading.Event()
        animation_thread = threading.Thread(target=animation_worker, args=(stop_animation,))
        animation_thread.daemon = True
        animation_thread.start()

        try:
            # 定義 pytest 參數
            pytest_params = [
                "-v", 
                f"--slowmo={slowmo}", 
                "--tracing",
                "retain-on-failure"
            ]
            slowmo_value = [p.split('=')[1] for p in pytest_params if p.startswith("--slowmo=")][0]

            # 記錄使用的參數和 slowmo 值
            logger.info(f"運行 pytest 使用的參數: {' '.join(pytest_params)}")
            logger.info(f"slowmo 的數值: {slowmo_value}")
            logger.info(f"timeout 參數已移除，因為 pytest-timeout 插件未安裝")

            # 確保每次運行使用新的 pytest 進程並獨立環境
            # 添加 --headed 和 --slowmo=500 參數
            result = subprocess.run(
                [
                    "pytest",
                    str(test_file),
                ] + pytest_params,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            logger.info(result.stdout)
            if result.returncode == 0:
                logger.info(f"測試檔案 {test_file} 執行成功")
            else:
                logger.error(f"測試檔案 {test_file} 執行失敗")
                logger.error(f"錯誤輸出：{result.stderr}")
        except Exception as e:
            logger.error(f"執行測試檔案 {test_file} 時發生錯誤：{e}")
            logger.warning("測試可能因編碼或環境問題失敗，請檢查 pytest 輸出")
        finally:
            # 停止動畫
            stop_animation.set()
            animation_thread.join()

            # 清理臨時檔案或瀏覽器快取（如果使用 Playwright）
            temp_storage = Path("playwright_storage_state.json")
            if temp_storage.exists():
                try:
                    temp_storage.unlink()
                    logger.info("已清理臨時儲存狀態")
                except Exception as e:
                    logger.warning(f"清理臨時儲存狀態失敗：{e}")

if __name__ == "__main__":
    # 設置命令行參數解析
    parser = argparse.ArgumentParser(description='執行 pytest 測試')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT,
                        help=f'全域超時設置（毫秒），預設值: {DEFAULT_TIMEOUT}（注意：此參數目前未使用，因為 pytest-timeout 插件未安裝）')
    parser.add_argument('--slowmo', type=int, default=SLOWMO_VALUE,
                        help=f'Playwright slowmo 值（毫秒），預設值: {SLOWMO_VALUE}')
    parser.add_argument('--dir', type=str, default=DEFAULT_ROOT_DIR,
                        help=f'測試檔案的根目錄，預設值: {DEFAULT_ROOT_DIR}')

    args = parser.parse_args()

    # 執行測試，使用命令行參數
    run_pytest_by_file(args.dir, args.timeout, args.slowmo)
