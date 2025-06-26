#!/usr/bin/env python3
# project_manager.py - 项目管理工具

import os
import subprocess
import sys
import threading
import time
from paths import *

def show_project_structure():
    """显示项目结构"""
    print("📁 DNS隧道检测项目结构:")
    print("=" * 50)
    print(f"📂 项目根目录: {PROJECT_ROOT}")
    print(f"📂 数据目录: {DATA_DIR}")
    print(f"📂 模型目录: {MODELS_DIR}")
    print(f"📂 输出目录: {OUTPUT_DIR}")
    print(f"📂 脚本目录: {SCRIPTS_DIR}")
    print(f"📂 图片目录: {PICTURE_DIR}")
    print()
    
    print("📋 主要文件:")
    files_info = [
        ("数据文件", [
            ("DNS流量CSV", DNS_TRAFFIC_CSV),
            ("特征文件", FEATURES_TXT),
            ("标准化特征", FEATURES_SCALED_CSV),
            ("带标签特征", FEATURES_LABELED_CSV),
            ("可疑域名", SUSPICIOUS_DOMAINS_CSV),
            ("PCAP文件", PCAP_FILE),
            ("物理网卡PCAP", SAMPLE_PHYSICAL_PCAP),
            ("回环网卡PCAP", SAMPLE_LOOPBACK_PCAP),
        ]),
        ("模型文件", [
            ("随机森林模型", MODEL_FILE),
        ]),
        ("Python脚本", [
            ("DNS特征提取", os.path.join(SCRIPTS_DIR, "dns_feature_extract.py")),
            ("特征标准化", os.path.join(SCRIPTS_DIR, "standardize_features.py")), 
            ("添加标签", os.path.join(SCRIPTS_DIR, "add_label.py")),
            ("模型训练", os.path.join(SCRIPTS_DIR, "model_train.py")),
            ("模型检测", os.path.join(SCRIPTS_DIR, "model_detect.py")),
            ("流量生成", os.path.join(SCRIPTS_DIR, "traffic_gen.py")),
            ("客户端", os.path.join(SCRIPTS_DIR, "client.py")),
            ("服务器", os.path.join(SCRIPTS_DIR, "server.py")),
        ])
    ]
    
    for category, files in files_info:
        print(f"\n{category}:")
        for name, path in files:
            if os.path.exists(path):
                size = os.path.getsize(path)
                if size < 1024:
                    size_str = f"{size} bytes"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/(1024*1024):.1f} MB"
                status = f"✅ ({size_str})"
            else:
                status = "❌ 不存在"
            print(f"  {name}: {status}")

def run_full_pipeline():
    """运行完整的数据处理管道"""
    print("🚀 开始运行完整的数据处理管道...")
    
    # 确保在src目录下运行
    original_dir = os.getcwd()
    os.chdir(SCRIPTS_DIR)
    
    steps = [
        ("1. 生成训练数据", "traffic_gen.py"),
        ("2. 提取DNS特征", "dns_feature_extract.py"),
        ("3. 标准化特征", "standardize_features.py"),
        ("4. 添加标签", "add_label.py"),
        ("5. 训练模型", "model_train.py"),
    ]
    
    try:
        for step_name, script in steps:
            print(f"\n{step_name}...")
            try:
                result = subprocess.run([sys.executable, script], 
                                       capture_output=True, text=True, encoding='utf-8', errors='ignore')
                if result.returncode == 0:
                    print(f"✅ {step_name} 完成")
                    if result.stdout:
                        print(f"输出: {result.stdout[:200]}{'...' if len(result.stdout) > 200 else ''}")
                else:
                    print(f"❌ {step_name} 失败:")
                    print(result.stderr[:500] if result.stderr else "未知错误")
                    return False
            except Exception as e:
                print(f"❌ {step_name} 出错: {e}")
                return False
    finally:
        os.chdir(original_dir)
    
    print("\n🎉 完整管道执行完毕！")
    return True

def run_server_async():
    """异步运行DNS隧道服务器"""
    script_path = os.path.join(SCRIPTS_DIR, "server.py")
    if not os.path.exists(script_path):
        print(f"❌ 脚本不存在: {script_path}")
        return False
    
    print(f"🚀 启动DNS隧道服务器...")
    print("💡 提示：服务器将在后台运行，按 Ctrl+C 可以停止")
    print("💡 服务器启动后，您可以继续使用其他功能")
    
    original_dir = os.getcwd()
    os.chdir(SCRIPTS_DIR)
    
    try:
        # 使用subprocess.Popen启动服务器进程，不等待完成
        process = subprocess.Popen(
            [sys.executable, "server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        print(f"✅ 服务器进程已启动 (PID: {process.pid})")
        
        # 等待一小段时间检查进程是否成功启动
        time.sleep(2)
        if process.poll() is None:
            print("✅ 服务器正在运行中...")
            return True
        else:
            stdout, stderr = process.communicate()
            print("❌ 服务器启动失败:")
            if stderr:
                print(stderr)
            return False
            
    except Exception as e:
        print(f"❌ 启动服务器时出错: {e}")
        return False
    finally:
        os.chdir(original_dir)

def run_client_async():
    """异步运行DNS隧道客户端"""
    script_path = os.path.join(SCRIPTS_DIR, "client.py")
    if not os.path.exists(script_path):
        print(f"❌ 脚本不存在: {script_path}")
        return False
    
    print(f"🚀 启动DNS隧道客户端...")
    print("💡 提示：客户端将在后台运行")
    
    original_dir = os.getcwd()
    os.chdir(SCRIPTS_DIR)
    
    try:
        # 使用subprocess.Popen启动客户端进程，不等待完成
        process = subprocess.Popen(
            [sys.executable, "client.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        print(f"✅ 客户端进程已启动 (PID: {process.pid})")
        
        # 等待一小段时间检查进程是否成功启动
        time.sleep(2)
        if process.poll() is None:
            print("✅ 客户端正在运行中...")
            return True
        else:
            stdout, stderr = process.communicate()
            if stdout:
                print("输出:", stdout)
            if stderr:
                print("错误:", stderr)
            return True  # 客户端可能执行完就退出，这是正常的
            
    except Exception as e:
        print(f"❌ 启动客户端时出错: {e}")
        return False
    finally:
        os.chdir(original_dir)

def run_server_interactive():
    """交互式运行DNS隧道服务器"""
    script_path = os.path.join(SCRIPTS_DIR, "server.py")
    if not os.path.exists(script_path):
        print(f"❌ 脚本不存在: {script_path}")
        return False
    
    print(f"🚀 启动DNS隧道服务器...")
    print("💡 提示：服务器将显示实时输出，按 Ctrl+C 可以停止并返回菜单")
    
    original_dir = os.getcwd()
    os.chdir(SCRIPTS_DIR)
    
    try:
        # 使用实时输出方式运行服务器
        process = subprocess.Popen(
            [sys.executable, "server.py"],
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        print(f"✅ 服务器进程已启动 (PID: {process.pid})")
        print("🔍 实时输出 (按 Ctrl+C 停止):")
        print("-" * 50)
        
        try:
            process.wait()  # 等待进程结束
        except KeyboardInterrupt:
            print("\n🛑 用户中断，正在停止服务器...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            print("✅ 服务器已停止")
        
        return True
            
    except Exception as e:
        print(f"❌ 启动服务器时出错: {e}")
        return False
    finally:
        os.chdir(original_dir)

def run_client_interactive():
    """交互式运行DNS隧道客户端"""
    script_path = os.path.join(SCRIPTS_DIR, "client.py")
    if not os.path.exists(script_path):
        print(f"❌ 脚本不存在: {script_path}")
        return False
    
    print(f"🚀 启动DNS隧道客户端...")
    print("💡 提示：客户端将显示实时输出")
    
    original_dir = os.getcwd()
    os.chdir(SCRIPTS_DIR)
    
    try:
        # 使用实时输出方式运行客户端
        result = subprocess.run(
            [sys.executable, "client.py"],
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            print("✅ 客户端执行完成")
        else:
            print(f"❌ 客户端执行失败 (退出码: {result.returncode})")
        
        return result.returncode == 0
            
    except Exception as e:
        print(f"❌ 启动客户端时出错: {e}")
        return False
    finally:
        os.chdir(original_dir)

def run_single_script(script_name, show_realtime=False):
    """运行单个脚本"""
    # 对于服务器和客户端脚本，使用交互式方式运行
    if script_name == "server.py":
        return run_server_interactive()
    elif script_name == "client.py":
        return run_client_interactive()
    
    # 其他脚本根据参数选择运行方式
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    if not os.path.exists(script_path):
        print(f"❌ 脚本不存在: {script_path}")
        return False
    
    print(f"🏃 运行脚本: {script_name}")
    original_dir = os.getcwd()
    os.chdir(SCRIPTS_DIR)
    
    try:
        if show_realtime:
            # 实时输出模式
            print("🔍 实时输出:")
            print("-" * 50)
            result = subprocess.run([sys.executable, script_name], 
                                   text=True, encoding='utf-8', errors='ignore')
            print("-" * 50)
            if result.returncode == 0:
                print(f"✅ {script_name} 执行完成")
            else:
                print(f"❌ {script_name} 执行失败 (退出码: {result.returncode})")
        else:
            # 捕获输出模式
            result = subprocess.run([sys.executable, script_name], 
                                   capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if result.returncode == 0:
                print(f"✅ {script_name} 执行完成")
                if result.stdout:
                    print("📄 输出:")
                    print(result.stdout)
            else:
                print(f"❌ {script_name} 执行失败:")
                if result.stderr:
                    print("📄 错误信息:")
                    print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        return False
    finally:
        os.chdir(original_dir)

def clean_data():
    """清理数据文件"""
    print("🧹 清理数据文件...")
    
    files_to_clean = [
        DNS_TRAFFIC_CSV,
        FEATURES_TXT,
        FEATURES_SCALED_CSV,
        FEATURES_LABELED_CSV,
        SUSPICIOUS_DOMAINS_CSV,
        PCAP_FILE,
        SAMPLE_PHYSICAL_PCAP,
        SAMPLE_LOOPBACK_PCAP,
    ]
    
    cleaned_count = 0
    for file_path in files_to_clean:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ 已删除: {os.path.basename(file_path)}")
                cleaned_count += 1
            except Exception as e:
                print(f"❌ 删除失败 {os.path.basename(file_path)}: {e}")
    
    print(f"✅ 数据清理完成，共删除 {cleaned_count} 个文件")

def setup_environment():
    """设置项目环境"""
    print("🔧 设置项目环境...")
    ensure_directories()
    print("✅ 目录结构已创建")
    
    # 检查依赖
    requirements_file = os.path.join(SCRIPTS_DIR, "requirements.txt")
    if os.path.exists(requirements_file):
        print("📦 检查Python依赖...")
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file],
                                   capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ 依赖安装完成")
            else:
                print("❌ 依赖安装失败:")
                print(result.stderr)
        except Exception as e:
            print(f"❌ 安装依赖时出错: {e}")

def main():
    """主菜单"""
    # 确保环境设置
    ensure_directories()
    
    while True:
        print("\n" + "="*60)
        print("🎯 DNS隧道检测项目管理器")
        print("="*60)
        print("1. 查看项目结构")
        print("2. 生成训练数据")
        print("3. 提取DNS特征")
        print("4. 标准化特征")
        print("5. 添加标签")
        print("6. 训练模型")
        print("7. 运行检测")
        print("8. 启动DNS隧道服务器")
        print("9. 启动DNS隧道客户端")
        print("10. 运行完整数据处理管道")
        print("11. 清理数据文件")
        print("12. 设置项目环境")
        print("0. 退出")
        
        choice = input("\n请选择操作 (0-12): ").strip()
        
        if choice == "1":
            show_project_structure()
        elif choice == "2":
            run_single_script("traffic_gen.py", True)
        elif choice == "3":
            run_single_script("dns_feature_extract.py", True)
        elif choice == "4":
            run_single_script("standardize_features.py", True)
        elif choice == "5":
            run_single_script("add_label.py", True)
        elif choice == "6":
            run_single_script("model_train.py", True)
        elif choice == "7":
            run_single_script("model_detect.py", True)
        elif choice == "8":
            run_single_script("server.py")
        elif choice == "9":
            run_single_script("client.py")
        elif choice == "10":
            run_full_pipeline()
        elif choice == "11":
            clean_data()
        elif choice == "12":
            setup_environment()
        elif choice == "0":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    main()
