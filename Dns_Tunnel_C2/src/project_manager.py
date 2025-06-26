#!/usr/bin/env python3
# project_manager.py - 项目管理工具

import os
import subprocess
import sys
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

def run_single_script(script_name):
    """运行单个脚本"""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    if not os.path.exists(script_path):
        print(f"❌ 脚本不存在: {script_path}")
        return False
    
    print(f"🏃 运行脚本: {script_name}")
    original_dir = os.getcwd()
    os.chdir(SCRIPTS_DIR)
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                               capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if result.returncode == 0:
            print(f"✅ {script_name} 执行完成")
            if result.stdout:
                print("输出:")
                print(result.stdout)
        else:
            print(f"❌ {script_name} 执行失败:")
            if result.stderr:
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
        print("10. 清理数据文件")
        print("11. 设置项目环境")
        print("0. 退出")
        
        choice = input("\n请选择操作 (0-12): ").strip()
        
        if choice == "1":
            show_project_structure()
        elif choice == "2":
            run_single_script("traffic_gen.py")
        elif choice == "3":
            run_single_script("dns_feature_extract.py")
        elif choice == "4":
            run_single_script("standardize_features.py")
        elif choice == "5":
            run_single_script("add_label.py")
        elif choice == "6":
            run_single_script("model_train.py")
        elif choice == "7":
            run_single_script("model_detect.py")
        elif choice == "8":
            run_single_script("server.py")
        elif choice == "9":
            run_single_script("client.py")
        elif choice == "10":
            clean_data()
        elif choice == "11":
            setup_environment()
        elif choice == "0":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    main()
