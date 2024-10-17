def recognize_filename_patterns_prompt(file_list):
    file_list_str = "\n".join(file_list)
    return f"""作为专业的文件命名模式分析器，请分析以下文件列表并提供命名规则建议：

{file_list_str}

请按照以下步骤进行分析和建议：

1. 模式识别：
   - 观察文件名的结构、使用的字符和共同特征
   - 识别可能的命名类别（如日期、序列号、项目名称等）
   - 总结出现的命名模式（如前缀、后缀、分隔符等）

2. 命名规则设计：
   - 必须根据分析结果，提出一个统一的命名规则，确保：
     a) 保留关键信息
     b) 格式一致
     c) 易于理解和应用
     d) 适用于所有文件

3. 规则说明：
   - 详细解释新命名规则的结构（如：日期_项目名_版本号.扩展名）
   - 说明每个部分的格式（如：日期格式为YYYYMMDD）
   - 指定使用的分隔符和大小写规则

4. 应用示例：
   - 提供3个具体例子，展示如何将现有文件名转换为新格式

5. 实施指南：
   - 提供清晰的步骤，指导如何将新规则应用到所有文件

请提供简洁明了的分析结果和建议，确保用户可以轻松理解和实施。
"""

def rename_files_prompt(file_list, rename_rule):
    files_info = "\n".join([f"文件名: {file['filename']}\n预览: {file['preview']}\n创建时间: {file['creation_time']}\n" for file in file_list])
    
    return f"""作为专业的文件重命名助手，请根据以下提供的重命名规则，为给定的文件列表生成新的文件名：

重命名规则：
{rename_rule}

文件列表：
{files_info}

请按照以下步骤进行重命名：

1. 仔细阅读并理解给定的重命名规则。
2. 对每个文件进行分析，考虑其文件名、内容预览和创建时间。
3. 根据重命名规则，为每个文件生成一个新的文件名。
4. 确保新文件名符合规则要求，并且能够准确反映文件的内容或属性。
5. 如果规则中有任何模糊或难以应用的部分，请做出合理的判断和解释。

请提供一个列表，其中包含每个文件的原始文件名和建议的新文件名，格式如下：

原始文件名 -> 新文件名

同时，请简要解释您是如何应用重命名规则的，特别是在做出任何重要决定或解释时。

请确保您的重命名建议既符合给定的规则，又实用且易于理解。
"""