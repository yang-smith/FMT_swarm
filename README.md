# FMT_swarm

一个智能文件重命名工具demo，它使用AI来识别文件命名模式并提供重命名建议。


## 使用方法

1. 运行主程序：
   ```
   python main.py
   ```
2. 在打开的GUI界面中，点击"选择目录"按钮选择要处理的文件夹。
3. 点击"识别模式"按钮，程序将分析文件名并识别模式。
4. 点击"生成建议"按钮，程序将根据识别的模式生成重命名建议。
5. 在文件列表中选择文件，可以查看文件预览和对应的重命名建议。

## 示例

以下是一些文件重命名的示例：

```
01234d.txt -> 20241017_daily_life_summary.txt
2024-05-13-log.log -> 20241017_system_error_log_v1.log.txt
paul_graham_essay.txt -> 20241017_paul_graham_what_i_worked_on.txt
使用须知.txt -> 20241017_使用须知.txt
历史_万历十五年.txt -> 20241017_历史_万历十五年.txt
小说_大雁的庆典.txt -> 20241017_小说_大雁的庆典.txt
新建 文本文档.txt -> 20241017_新建文本文档.txt
```
[示例](./demo.png)

## 视频演示

查看 [视频演示](./output.webm) 以了解工具的使用方法。

## 技术细节

- 使用 Python 的 tkinter 库构建 GUI
- 利用 OpenAI 的 GPT 模型进行文件名模式识别和重命名建议生成
- 文件操作使用 Python 的内置库

## 贡献

欢迎提交 issues 和 pull requests 来帮助改进这个项目。

## 许可证

