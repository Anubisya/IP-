from functools import partial
import socket
import threading
import ipaddress
import tkinter as tk
from tkinter import filedialog

def scan_from_file(ip_file, ports_entry, threads_entry, scan_c_var, stop_flag, result_text):
    try:
        with open(ip_file, "r") as file:
            ips = file.read().splitlines()

        for ip in ips:
            scan_ip(tk.Entry(), ports_entry, threads_entry, scan_c_var, stop_flag, result_text)
    except Exception as e:
        result_text.insert(tk.END, f"Error scanning IPs from file: {str(e)}\n")

def scan_port(ip, port, result_text, stop_flag):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            result_text.insert(tk.END, f"{ip}:{port} 是开放端口\n")
            result_text.update_idletasks()  # Update the result text widget in real-time
            result_text.see(tk.END)  # Scroll to the end of the result text
        sock.close()
    except Exception as e:
        result_text.insert(tk.END, f"Error scanning port {port}: {str(e)}\n")

def scan_ip(ip_entry, ports_entry, threads_entry, scan_c_var, stop_flag, result_text):
    try:
        ip_range_str = ip_entry.get()
        ip_range = ipaddress.IPv4Network(ip_range_str, strict=False)
        ports_str = ports_entry.get()
        threads = int(threads_entry.get())
        scan_c = scan_c_var.get()

        result_text.insert(tk.END, f"开始扫描: {ip_range_str}\n")

        for ip in ip_range:
            if stop_flag.is_set():
                break

            if scan_c:
                for port in parse_ports(ports_str):
                    thread = threading.Thread(target=partial(scan_port, str(ip), port, result_text, stop_flag))
                    thread.start()
            else:
                for port in parse_ports(ports_str):
                    thread = threading.Thread(target=partial(scan_port, str(ip), port, result_text, stop_flag))
                    thread.start()
                    break  # Only scan one port for single IP
    except Exception as e:
        result_text.insert(tk.END, f"Error scanning IP range: {str(e)}\n")

def parse_ports(ports_str):
    ports = []
    if "-" in ports_str:
        start_port, end_port = map(int, ports_str.split("-"))
        ports = range(start_port, end_port + 1)
    else:
        ports.append(int(ports_str))
    return ports

def stop_scan(stop_flag):
    stop_flag.set()

def save_result(result_text, ip_range):
    result = result_text.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            lines = result.strip().split('\n')
            for line in lines:
                file.write(f"{ip_range}:{line}\n")
        tk.messagebox.showinfo("保存成功", "扫描结果已成功保存")

def browse_file(ip_file_entry):
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    ip_file_entry.delete(0, tk.END)
    ip_file_entry.insert(0, file_path)
