import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.utils.reader import get_file_previews, get_file_list
from src.utils.api_client_factory import get_client
from src.utils.prompts import recognize_filename_patterns_prompt, rename_files_prompt

class FileRenameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件重命名助手")
        self.root.geometry("800x600")
        
        self.client = get_client()
        self.current_directory = ""
        self.file_previews = []
        self.rename_suggestions = {}
        self.pattern = ""  # 添加这行来存储识别的模式

        self.create_widgets()

    def create_widgets(self):
        # 顶部区域
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)

        ttk.Button(top_frame, text="选择目录", command=self.select_directory).pack(side=tk.LEFT)
        self.directory_label = ttk.Label(top_frame, text="未选择目录")
        self.directory_label.pack(side=tk.LEFT, padx=10)

        # 主区域
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧文件列表
        self.file_listbox = tk.Listbox(main_frame, width=30)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.Y)
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)

        # 右侧区域
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 文件预览和模式显示
        preview_frame = ttk.LabelFrame(right_frame, text="文件预览 / 识别模式", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)

        self.preview_text = tk.Text(preview_frame, wrap=tk.WORD, height=10)
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        self.preview_text.bind('<KeyRelease>', self.update_pattern)

        # 重命名建议
        rename_frame = ttk.LabelFrame(right_frame, text="重命名建议", padding="10")
        rename_frame.pack(fill=tk.BOTH, expand=True)

        self.rename_text = tk.Text(rename_frame, wrap=tk.WORD, height=15)  # 增加高度
        self.rename_text.pack(fill=tk.BOTH, expand=True)

        # 底部按钮
        bottom_frame = ttk.Frame(self.root, padding="10")
        bottom_frame.pack(fill=tk.X)

        ttk.Button(bottom_frame, text="识别模式", command=self.recognize_pattern).pack(side=tk.LEFT)
        ttk.Button(bottom_frame, text="生成建议", command=self.generate_suggestions).pack(side=tk.LEFT, padx=10)

        # 状态栏
        self.status_bar = ttk.Label(self.root, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 菜单栏
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="打开目录", command=self.select_directory)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)

    def select_directory(self):
        self.current_directory = filedialog.askdirectory()
        if self.current_directory:
            self.directory_label.config(text=self.current_directory)
            self.update_file_list()

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        self.file_previews = get_file_previews(self.current_directory)
        for file_info in self.file_previews:
            self.file_listbox.insert(tk.END, file_info['filename'])

    def on_file_select(self, event):
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            file_info = self.file_previews[index]
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, f"文件名: {file_info['filename']}\n\n")
            self.preview_text.insert(tk.END, f"创建时间: {file_info['creation_time']}\n\n")
            self.preview_text.insert(tk.END, f"预览内容:\n{file_info['preview']}")

            if file_info['filename'] in self.rename_suggestions:
                self.rename_text.delete(1.0, tk.END)
                self.rename_text.insert(tk.END, f"建议的新文件名:\n{self.rename_suggestions[file_info['filename']]}")

    def recognize_pattern(self):
        if not self.current_directory:
            messagebox.showwarning("警告", "请先选择一个目录")
            return
        
        self.status_bar.config(text="正在识别文件名模式...")
        files = get_file_list(self.current_directory)
        prompt = recognize_filename_patterns_prompt(files)
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        self.pattern = response.choices[0].message.content
        
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, f"识别的文件名模式:\n\n{self.pattern}")
        self.status_bar.config(text="文件名模式识别完成")
        self.preview_text.edit_modified(False)  

    def generate_suggestions(self):
        if not self.current_directory:
            messagebox.showwarning("警告", "请先选择一个目录")
            return
        
        if not self.pattern:
            messagebox.showwarning("警告", "请先识别文件名模式")
            return
        
        self.status_bar.config(text="正在生成重命名建议...")
        files = get_file_previews(self.current_directory)
        prompt = rename_files_prompt(files, self.pattern)
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        suggestions = response.choices[0].message.content
        
        # 直接将 AI 返回的内容放入重命名建议框
        self.rename_text.delete(1.0, tk.END)
        self.rename_text.insert(tk.END, suggestions)
        
        self.status_bar.config(text="重命名建议生成完成")

    def update_pattern(self, event):
        if self.preview_text.edit_modified():
            content = self.preview_text.get("1.0", tk.END).strip()
            if content.startswith("识别的文件名模式:"):
                self.pattern = content.split("\n\n", 1)[1]
            else:
                self.pattern = content
            self.preview_text.edit_modified(False)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenameApp(root)
    root.mainloop()
