# 简单浏览器项目

这个项目实现了一个基本的网络浏览器，用于学习和理解 HTTP 协议、网络编程和图形用户界面开发。

## 文件结构

- `frontend/`: 包含前端相关文件
  - `browser_ui.html`: 浏览器的主要HTML界面
  - `script.js`: 前端JavaScript脚本
  - `styles.css`: 前端样式表

- `backend/`: 包含后端Python模块
  - `__init__.py`: 将目录标记为Python包
  - `browser.py`: 浏览器核心功能
  - `gui.py`: 用户界面
  - `network.py`: 网络连接和HTTP请求处理
  - `html_parser.py`: HTML解析和渲染
  - `cache.py`: 缓存机制
  - `dns_resolver.py`: DNS解析
  - `bookmarks.py`: 书签管理
  - `history.py`: 历史记录管理
  - `cleanup_logs.py`: 日志清理

- `main.py`: 主程序入口
- `test_browser.py`: 浏览器测试脚本
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

2. 在打开的图形界面中，您会看到一个地址栏和导航按钮。

3. 在地址栏中输入一个 URL（例如 http://example.com），然后点击"Go"按钮或按回车键。

4. 使用导航按钮（后退、前进、刷新）来浏览网页。

5. 使用书签按钮来管理您的收藏网页。

## 功能

- 基本的网页浏览功能
- 地址栏和导航按钮（后退、前进、刷新）
- 主页按钮
- 书签功能
- 历史记录
- 简单的缓存机制
- DNS解析（基础实现）

## 注意事项

- 这是一个教育项目，主要用于学习目的，不建议用于日常的网页浏览。
- 某些复杂的网页可能无法正确显示。
- 项目仍在开发中，可能存在一些bug或未完善的功能。

## 测试

运行 `test_browser.py` 脚本来执行自动化测试：

```
python test_browser.py
```

## 贡献

欢迎提交 issues 和 pull requests 来改进这个项目。

## 许可

[在此添加您的许可信息]
