import os
import time
import logging
import sys

def cleanup_logs():
    log_file = 'browser.log'
    wait_time = 30  # 等待30秒

    logging.info("Log cleanup scheduled")
    time.sleep(wait_time)

    try:
        with open(log_file, 'w') as f:
            f.write('')  # 清空文件内容
        print(f"Log file {log_file} has been cleared after {wait_time} seconds.")
    except IOError as e:
        print(f"Error clearing log file {log_file}: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred while trying to clear {log_file}: {str(e)}")

    # 发送信号给主程序，表示清理完成
    print("CLEANUP_COMPLETE")
    sys.stdout.flush()

if __name__ == "__main__":
    cleanup_logs()
