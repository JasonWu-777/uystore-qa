import sys
import time
import itertools
import logging
import shutil
from pathlib import Path

# 設置日誌
logger = logging.getLogger("test_utils")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - [%(levelname)s] - %(filename)s:%(lineno)d (%(funcName)s) - %(message)s'
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def animation_worker(stop_event):
    """顯示測試正在執行中的動畫"""
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while not stop_event.is_set():
        sys.stdout.write('\r正在執行自動化測試中... ' + next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
    # 清除動畫行
    sys.stdout.write('\r' + ' ' * 50 + '\r')
    sys.stdout.flush()

def clear_pytest_cache(root_dir: str):
    """清理 pytest 快取以避免環境汙染"""
    cache_dir = Path(root_dir) / ".pytest_cache"
    if cache_dir.exists():
        try:
            shutil.rmtree(cache_dir)
            logger.info(f"已清理 pytest 快取：{cache_dir}")
        except Exception as e:
            logger.warning(f"清理 pytest 快取失敗：{e}")