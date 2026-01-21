#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试多进程修复是否生效
"""

import os
import sys
import multiprocessing

# 添加路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_subprocess_detection():
    """测试子进程检测函数"""
    print(f"主进程检测: 进程名={multiprocessing.current_process().name}, PID={os.getpid()}")
    
    # 模拟子进程检测
    current_process = multiprocessing.current_process()
    is_main = current_process.name == 'MainProcess'
    print(f"  - 是否为主进程: {is_main}")
    
    # 测试我们的检测逻辑
    import khQTTools
    detected_as_sub = khQTTools.is_subprocess()
    print(f"  - is_subprocess() 检测结果: {detected_as_sub}")
    

def worker_function():
    """测试子进程中的行为"""
    print(f"子进程检测: 进程名={multiprocessing.current_process().name}, PID={os.getpid()}")
    
    # 测试我们的检测逻辑
    import khQTTools
    detected_as_sub = khQTTools.is_subprocess()
    print(f"  - is_subprocess() 检测结果: {detected_as_sub}")
    
    # 检查环境变量设置
    qt_platform = os.environ.get('QT_QPA_PLATFORM', 'NOT_SET')
    print(f"  - QT_QPA_PLATFORM: {qt_platform}")


def test_multiprocessing():
    """测试多进程场景"""
    print("=== 测试主进程 ===")
    test_subprocess_detection()
    
    print("\n=== 测试子进程 ===")
    process = multiprocessing.Process(target=worker_function)
    process.start()
    process.join()
    
    if process.exitcode == 0:
        print("✓ 子进程正常退出")
    else:
        print(f"✗ 子进程异常退出，退出码: {process.exitcode}")


if __name__ == "__main__":
    # 设置多进程启动方法
    multiprocessing.freeze_support()
    try:
        multiprocessing.set_start_method('spawn', force=True)
    except RuntimeError:
        pass
    
    print("开始测试多进程修复...")
    test_multiprocessing()
    print("测试完成！")