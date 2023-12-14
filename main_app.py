import tkinter as tk
from tkinter import messagebox
import threading
from functools import partial
from scan_utils import scan_ip, scan_from_file, stop_scan, save_result, browse_file

def show_update_notification():
    messagebox.showinfo("更新提示", "有新版本可用，请更新！")

def main():
    root = tk.Tk()
    root.title("IP端口扫描 - 1024fw")

    entry_frame = tk.Frame(root)
    entry_frame.pack()

    ip_label = tk.Label(entry_frame, text="IP地址:")
    ip_label.grid(row=0, column=0, padx=5, pady=5)

    ip_entry = tk.Entry(entry_frame)
    ip_entry.grid(row=0, column=1, padx=5, pady=5)

    scan_c_var = tk.BooleanVar()
    scan_c_checkbox = tk.Checkbutton(entry_frame, text="扫描整个C段", variable=scan_c_var)
    scan_c_checkbox.grid(row=0, column=2, padx=5, pady=5)

    ports_label = tk.Label(entry_frame, text="扫描的端口:")
    ports_label.grid(row=1, column=0, padx=5, pady=5)

    ports_entry = tk.Entry(entry_frame)
    ports_entry.grid(row=1, column=1, padx=5, pady=5)

    threads_label = tk.Label(entry_frame, text="设置线程数:")
    threads_label.grid(row=2, column=0, padx=5, pady=5)

    threads_entry = tk.Entry(entry_frame)
    threads_entry.grid(row=2, column=1, padx=5, pady=5)

    result_text = tk.Text(root, height=10, width=50)
    result_text.pack()

    scan_button = tk.Button(root, text="开始扫描", command=partial(scan_ip, ip_entry, ports_entry, threads_entry, scan_c_var, threading.Event(), result_text))
    scan_button.pack()

    browse_button = tk.Button(root, text="导入IP文件", command=partial(browse_file, ip_entry))
    browse_button.pack()

    scan_file_button = tk.Button(root, text="扫描导入的IP文件", command=partial(scan_from_file, ip_entry.get(), ports_entry, threads_entry, scan_c_var, threading.Event(), result_text))
    scan_file_button.pack()

    button_frame = tk.Frame(root)
    button_frame.pack()

    stop_scan_button = tk.Button(button_frame, text="停止扫描", command=partial(stop_scan, threading.Event()))
    stop_scan_button.pack(side=tk.LEFT)

    save_button = tk.Button(button_frame, text="保存结果", command=partial(save_result, result_text, ip_entry.get()))
    save_button.pack(side=tk.LEFT)

    # Commented out the check_update_button for now
    # check_update_button = tk.Button(root, text="检查更新", command=check_for_updates)
    # check_update_button.pack(side=tk.RIGHT, anchor=tk.S)

    root.mainloop()

if __name__ == "__main__":
    main()
