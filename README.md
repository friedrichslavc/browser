# 简单浏览器项目

这个项目实现了一个基本的网络浏览器，用于学习和理解 HTTP 协议、网络编程和图形用户界面开发。

## 文件结构

- `frontend/`: 包含前端相关文件
  - `browser_ui.html`: 浏览器的主要HTML界面

- `backend/`: 包含后端Python模块
  - `__init__.py`: 将目录标记为Python包
  - `browser.py`: 浏览器核心功能
  - `gui.py`: 用户界面
  - `network.py`: 网络连接和HTTP请求处理
  - `html_parser.py`: HTML解析和渲染（框架）
  - `cache.py`: 缓存机制（框架）
  - `dns_resolver.py`: DNS解析（框架）

- `main.py`: 主程序入口
- `requirements.txt`: 项目依赖
- `README.md`: 项目说明文档
- `project_summary.md`: 项目概要和设计思路

## 安装依赖

1. 确保您的系统已安装 Python 3.x。

2. 克隆或下载此项目到本地目录。

3. 打开命令行或终端，导航到项目目录。

4. 运行以下命令安装所需的依赖：
   ```
   pip install -r requirements.txt
   ```

## 使用教程

1. 完成依赖安装后，在项目目录中运行以下命令启动浏览器：
   ```
   python main.py
   ```

2. 在打开的图形界面中，您会看到一个地址栏和一个"Go"按钮。

3. 在地址栏中输入一个 HTTP URL（例如 http://example.com），然后点击"Go"按钮或按回车键。

4. 浏览器将显示网页的内容。

## 注意事项

- 当前版本只支持 HTTP 协议，不支持 HTTPS。
- HTML 内容渲染可能不完整，某些复杂的网页可能无法正确显示。
- 缓存和 DNS 解析功能尚未完全实现。
- 这是一个教育项目，不建议用于实际的网页浏览。

## 功能

- 基本的网页浏览功能
- 地址栏和导航按钮（后退、前进、刷新）
- 主页按钮
- 书签功能（基础实现）
- 支持 HTTP 协议（注意：当前版本不支持 HTTPS）

## 后续开发

- 完善 HTML 解析和渲染功能
- 完善缓存机制
- 完善 DNS 解析
- 添加对 HTTPS 的支持
- 改进错误处理和用户体验

## 贡献

欢迎提交 issues 和 pull requests 来改进这个项目。
