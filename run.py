#!/usr/bin/env python3
# 快速启动DNS隧道检测项目管理器

import os
import sys

# 添加src目录到Python路径
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
sys.path.insert(0, src_dir)

# 导入并运行项目管理器
if __name__ == "__main__":
    os.chdir(src_dir)
    from project_manager import main
    main()
