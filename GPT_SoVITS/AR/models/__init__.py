# 在文件开头添加项目根目录到系统路径
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件绝对路径
project_root = os.path.dirname(os.path.dirname(current_dir))  # 上溯到AR目录的父目录
sys.path.append(project_root)  # 将父目录加入Python路径