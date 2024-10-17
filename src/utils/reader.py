import os
from datetime import datetime

def get_file_list(directory):
    """
    读取指定目录，返回该目录下所有文件的文件名列表。

    :param directory: 要读取的目录路径
    :return: 包含所有文件名的列表
    """
    try:
        # 使用 os.listdir() 获取目录中的所有项目
        all_items = os.listdir(directory)
        
        # 过滤出文件（排除目录）
        files = [item for item in all_items if os.path.isfile(os.path.join(directory, item))]
        
        return files
    except FileNotFoundError:
        print(f"错误：目录 '{directory}' 不存在。")
        return []
    except PermissionError:
        print(f"错误：没有权限访问目录 '{directory}'。")
        return []
    except Exception as e:
        print(f"发生错误：{str(e)}")
        return []

def get_file_previews(directory):
    """
    读取指定目录中的所有文件，返回每个文件的名称、前10行内容和创建时间。

    :param directory: 要读取的目录路径
    :return: 包含文件信息的列表，每个元素是一个字典，包含文件名、内容预览和创建时间
    """
    file_previews = []
    encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030']
    
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                content = None
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as file:
                            # 读取前10行，并将换行符替换为空格
                            content = ' '.join(file.readlines()[:10]).replace('\n', ' ')
                        break  # 如果成功读取，跳出循环
                    except UnicodeDecodeError:
                        continue  # 如果解码失败，尝试下一种编码
                
                if content is None:
                    print(f"警告：无法读取文件 '{filename}'，尝试的所有编码都失败。")
                    continue
                
                creation_time = os.path.getctime(file_path)
                creation_time_str = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
                
                file_previews.append({
                    'filename': filename,
                    'preview': content,
                    'creation_time': creation_time_str
                })
        return file_previews
    except FileNotFoundError:
        print(f"错误：目录 '{directory}' 不存在。")
    except PermissionError:
        print(f"错误：没有权限访问目录 '{directory}'。")
    except Exception as e:
        print(f"发生错误：{str(e)}")
    return []

# 使用示例
if __name__ == "__main__":
    directory_path = "path/to/your/directory"  # 替换为你想要读取的目录路径
    file_list = get_file_list(directory_path)
    print("文件列表：", file_list)

    file_previews = get_file_previews(directory_path)
    for preview in file_previews:
        print(f"\n文件名: {preview['filename']}")
        print(f"创建时间: {preview['creation_time']}")
        print("内容预览:")
        print(preview['preview'])
