﻿from fileinput import filename
from tkinter import messagebox
import os, mimetypes, re, shutil
from email.mime import image
import tkinter as tk
from tkinter import ANCHOR, W, Label, PhotoImage, Canvas, Scrollbar, filedialog
from turtle import bgcolor, color, update, width
from datetime import datetime
from tkinter import simpledialog
import shutil
from Client import *
# import Client
def get_server_ip():
    global server_ip
    server_ip = simpledialog.askstring("Server IP", "Enter Server IP:")
    if server_ip:
        print("Server IP set to:", server_ip)
get_server_ip()

clientIP = socket.gethostbyname(socket.gethostname())
hostnameClient = "client" + clientIP.split('.')[-1]
client = Client(10, serverSocket = (server_ip, 1234), clientSocket = (clientIP, 5002), hostname = socket.gethostname())

client.connectServer()
client.publish(fname = None, allFile= True)

class Item:
    def __init__(self, file_type, name, last_fetch_time):
        self.file_type = file_type
        self.name = name
        self.last_fetch_time = last_fetch_time
        self.last_fetch_time = self.format_last_fetch_time()
        self.icon = self.get_icon_with_type()

    def set_property(self, file_type, name, last_fetch_time):
        self.file_type = file_type
        self.name = name
        self.last_fetch_time = last_fetch_time
        self.last_fetch_time = self.format_last_fetch_time()
        self.icon = self.get_icon_with_type()

    def get_icon_with_type(self):
        if self.file_type == "image/png":
            return "Images/png.png"
        elif self.file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return "Images/docx.png"
        elif self.file_type == "application/pdf":
            return "Images/pdf.png"
        else:
            return "Images/folder.png"
    
    def format_last_fetch_time(self):
        # Chuyển last_fetch_time từ dạng timestamp sang datetime và định dạng lại
        dt = datetime.fromtimestamp(self.last_fetch_time)
        formatted_time = dt.strftime("%I:%M:%S %p")
        return formatted_time


def create_item_frame(item):
    item_frame = tk.Frame(list_frame)
    item_frame.pack(fill="x")

    icon = PhotoImage(file = item.icon)
    icon_label = tk.Label(item_frame, image=icon)
    icon_label.image = icon
    icon_label.pack(side="left")
    icon_label.config(width=50, height=50)

    info_frame = tk.Frame(item_frame)
    info_frame.pack(side="left", fill="x", expand=True)

    info_frame.columnconfigure(0, weight=1)
    info_frame.columnconfigure(1, weight=1)
    info_frame.columnconfigure(2, weight=1)
    info_frame.columnconfigure(3, weight=1)
    info_frame.columnconfigure(4, weight=1)

    name_label = tk.Label(info_frame, text=item.name, width=20)
    name_label.grid(row=0, column=0)

    last_fetch_time_label = tk.Label(info_frame, text=item.last_fetch_time, width = 20)
    last_fetch_time_label.grid(row=0, column=4, padx=50)

    delete_button = tk.Button(item_frame, text="Delete", command=lambda: delete_item(item_frame, item), bg="red",fg="white", activebackground="#FFCCCC")
    delete_button.pack(side="right")

def delete_item(item_frame, item):
    item_frame.destroy()
    #todo : done
    os.remove(directory_path +"/"+item.name)
    items.remove(item)
    client.publish(fname = None, allFile=True)

def refresh_items():
    for widget in list_frame.winfo_children():
        widget.destroy()

    for item in items:
        create_item_frame(item)

    on_configure(None)

def publish_file_btn():
    def rename_file(tempdir):
        def on_accept():
            new_name = file_name_entry.get()
            if new_name:
                try:
                    file_name = os.path.basename(tempdir)
                    destination_path = os.path.join(os.getcwd(), "Repository", new_name)
                    # shutil.move(tempdir, destination_path)
                    shutil.copy(tempdir, destination_path)
                    print(f"File copied and renamed from {tempdir} to {destination_path}")
                    file_name = os.path.basename(destination_path)
                    add_item(file_name)
                    #update_item()
                    popup.destroy()
                    client.publish(new_name)
                except Exception as e:
                    print(f"Error: {e}")

        popup = tk.Toplevel(root)
        popup.title("Rename file")

        entry_frame = tk.Frame(popup)
        entry_frame.pack()

        file_name_label = tk.Label(entry_frame, text="Enter file new name:")
        file_name_label.pack(side="left")

        file_name_entry = tk.Entry(entry_frame)
        file_name_entry.pack(side="left")

        accept_button = tk.Button(popup, text="Accept", command=on_accept, bg="#00FF66", activebackground="#CCFF99")
        accept_button.pack()

    tempdir = search_for_file_path()
    if tempdir:
        rename_file(tempdir)

def publish_file(lname, fname):
    try:
        destination_path = os.getcwd() + "/Repository"
        new_path = os.path.join(destination_path, fname)
        # shutil.move(os.path.normpath(lname), destination_path)
        shutil.copy(os.path.normpath(lname), destination_path)
        os.rename(os.path.join(destination_path, os.path.basename(lname)), new_path)
        print(f"File copied from {lname} to {destination_path} and renamed to {fname}")

        # Lấy loại file từ đường dẫn mới
        file_type, _ = mimetypes.guess_type(new_path)
        
        file_name = os.path.basename(new_path)
        item = Item(file_type, file_name, os.path.getmtime(new_path))
        add_item(item)

        client.publish(fname)
    except Exception as e:
        print(f"Error: {e}")

    # thông báo lên server
def request_file_popup():
    def request_fetch():
        file_name = file_name_entry.get()
        if file_name:
            def fetch_file():
                success = client.fetch(file_name)
                print(f"Succes:",success)
                if int(success) == 2:
                    client.publish(file_name)
                    add_item(file_name)
                    messagebox.showinfo("Fetch Successfully", "File fetch successfully !")
                elif int(success) == 0:
                    messagebox.showerror("Fetch Failed", "Failed to fetch the file.")
                else:
                    messagebox.showerror("Fetch Failed",file_name + " has already existed in client's repository")
        
        # Tạo một thread mới để thực hiện việc fetch file
            fetch_thread = threading.Thread(target=fetch_file)
            fetch_thread.start()
        
            # Đóng cửa sổ popup sau khi xử lý xong
        request_popup.destroy()

    # Tạo cửa sổ popup
    request_popup = tk.Toplevel(root)
    request_popup.title("Request Fetch File")

    # Tạo một hộp để nhập tên file
    entry_frame = tk.Frame(request_popup)
    entry_frame.pack()

    file_name_label = tk.Label(entry_frame, text="Enter File Name:")
    file_name_label.pack(side="left")

    global file_name_entry
    file_name_entry = tk.Entry(entry_frame, width= 600)
    file_name_entry.pack(side="left")

    request_button = tk.Button(request_popup, text="Request", command=request_fetch, bg="#4CAF50", fg="white", activebackground="#CCFF99")
    request_button.pack()

# def show_accept_popup(client_request_name, request_file_name):
#     response = messagebox.askyesno(
#         "Accept fetch request",
#         f"Accept fetch request with file '{request_file_name}' from '{client_request_name}'?"
#     )

#     # if response:
#     #     if client.fetch(request_file_name):
#     #         client.publish(request_file_name)
#     #         add_item(request_file_name)
#     #     else:
#     #         messagebox.showerror("Fetch Failed", "Failed to fetch the file.")

def on_enter(event):
    # Lấy nội dung đã nhập từ trường nhập liệu
    def request_fetch(file_name):
        if file_name:
            def fetch_file():
                success = client.fetch(file_name)
                print(f"Succes:",success)
                if int(success) == 2:
                    client.publish(file_name)
                    add_item(file_name)
                    messagebox.showinfo("Fetch Successfully", "File fetch successfully !")
                elif int(success) == 0:
                    messagebox.showerror("Fetch Failed", "Failed to fetch the file.")
                else:
                    messagebox.showerror("Fetch Failed",file_name + " has already existed in client's repository")
            fetch_thread = threading.Thread(target=fetch_file)
            fetch_thread.start()
    cli_input = file_name_entry.get().strip()  # Loại bỏ khoảng trắng thừa
    publish_line = r'^publish\s+.+\s+.+$'
    fetch_line = r'^fetch\s+.+$'

    if re.match(publish_line, cli_input):  # publish
        parts = cli_input.split()
        command = parts[0]
        lname = parts[1]
        fname = parts[2]
        print(f"Command: {command}, Local Name: {lname}, File Name: {fname}")
        publish_file(lname, fname)
    elif re.match(fetch_line, cli_input):  # fetch
        parts = cli_input.split()
        command = parts[0]
        fname = parts[1]
        print(f"Command: {command}, Fetch Name: {fname}")
        # todo : done
        request_fetch(fname) ##hostname
    else:
        messagebox.showerror("CLI Failed", "Command syntax is wrong.")


    # Xóa nội dung trường nhập liệu
    file_name_entry.delete(0, 'end')

def show_cli_popup():
    popup = tk.Toplevel(root)
    popup.geometry("600x110+150+150")
    popup.title("CLI")

    # Tạo một hộp để nhập tên file
    entry_frame = tk.Frame(popup)
    entry_frame.pack()
    # Tạo một hộp để nhập tên file
    entry_frame = tk.Frame(popup)
    entry_frame.pack()
    publish_instruction_label = tk.Label(entry_frame, text="Publish: Publish {lname} {fname}\n + lname: path to the file to publish\n + fname: the name saved in the client's repository",justify="left")
    publish_instruction_label.pack(anchor="w")  # Căn chỉnh văn bản sang trái

    # Tạo một nhãn hướng dẫn cho Fetch
    fetch_instruction_label = tk.Label(entry_frame, text="Fetch: fetch {fname}\n + fname: The name of the file requested to fetch",justify="left")
    fetch_instruction_label.pack(anchor="w")
    file_name_label = tk.Label(entry_frame, text="CLI:")
    file_name_label.pack(side="left")

    global file_name_entry
    file_name_entry = tk.Entry(entry_frame, width=600)
    file_name_entry.pack(side="left")
    # Gắn sự kiện Enter với hàm on_enter
    file_name_entry.bind('<Return>', on_enter)

    # Chạy cửa sổ popup
    popup.mainloop() 

def search_for_file_path ():
    currdir = os.getcwd()
    tempdir = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Select file to publish')
    if len(tempdir) > 0:
        print ("You chose: %s" % tempdir)
    return tempdir
#------------------------------------------------------------------------------------------- MAIN


# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("Danh sách các mục của "+ client.hostname)
root.geometry("600x400+100+100")
root.resizable(width=False, height=False)

# Tạo khung cho vùng phía trên
header_frame = tk.Frame(root, borderwidth=2, relief="solid", bg="#4CAF50")  
header_frame.pack(fill="x")

header_icon_label = tk.Label(header_frame, text="Icon", bg="#4CAF50", fg="white")  
header_icon_label.grid(row=0, column=0, padx=10, sticky="w")

header_name_label = tk.Label(header_frame, text="Name", bg="#4CAF50", fg="white")  
header_name_label.grid(row=0, column=1, padx=60, sticky="w")

header_time_label = tk.Label(header_frame, text="Last Fetch Time", bg="#4CAF50", fg="white")  
header_time_label.grid(row=0, column=2, padx=80, sticky="e")

# Tạo thanh trượt
scrollbar = Scrollbar(root)
scrollbar.pack(side="right", fill="y")

# Tạo một vùng hiển thị danh sách
canvas = Canvas(root, yscrollcommand=scrollbar.set)
canvas.pack(side="top", fill="both", expand=True)

# Tạo một khung cho danh sách
list_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=list_frame, anchor="nw")

# Đường dẫn đến thư mục bạn muốn kiểm tra trong kho
directory_path = os.getcwd()+"/Repository"

items = []
def update_item():
    if os.path.exists(directory_path):
        files = os.listdir(directory_path)

        for file in files:
            file_path = os.path.join(directory_path, file)  # Đường dẫn đầy đủ đến tệp
            file_type, encoding = mimetypes.guess_type(file_path)
            item = Item(file_type, file, os.path.getmtime(file_path))  # Lấy thời gian sửa đổi từ đường dẫn đầy đủ
            item.get_icon_with_type()  # Gọi phương thức này để thiết lập biểu tượng dựa trên loại tệp
            items.append(item)
    # Thêm các mục vào danh sách
    for item in items:
        create_item_frame(item)
def add_item(file):
    file_path = os.path.join(directory_path, file)  # Đường dẫn đầy đủ đến tệp
    file_type, encoding = mimetypes.guess_type(file)
    item = Item(file_type, file, os.path.getmtime(file_path))  # Lấy thời gian sửa đổi từ đường dẫn đầy đủ
    item.get_icon_with_type()  # Gọi phương thức này để thiết lập biểu tượng dựa trên loại tệp
    items.append(item)
    create_item_frame(item)
    list_frame.update_idletasks()
    list_frame_height = sum(child.winfo_height() for child in list_frame.winfo_children())
    canvas.configure(scrollregion=canvas.bbox("all"), height=min(list_frame_height, canvas.winfo_height()))
    on_configure(None)
update_item()

# Thiết lập canvas để làm việc với thanh trượt
list_frame.update_idletasks()

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
list_frame_id = canvas.create_window((0, 0), window=list_frame, anchor="nw")
canvas.bind('<Configure>', on_configure)

scrollbar.config(command=canvas.yview)

# Tạo khung cho nút
button_frame = tk.Frame(root, borderwidth=2, relief="solid", pady=10)
button_frame.pack(side="bottom", fill="x", anchor="s")  

# Tạo nút button
button_publish = tk.Button(button_frame, text="Publish file", command=publish_file_btn, bg="#004d00", fg="white", activebackground="#CCFF99", highlightbackground="#004d00")
button_request = tk.Button(button_frame, text="Request fetch file", command=request_file_popup, bg="#004d00", fg="white", activebackground="#CCFF99", highlightbackground="#004d00")
button_cli = tk.Button(button_frame, text="Open CLI", command=show_cli_popup, bg="#004d00", fg="white", activebackground="#CCFF99", highlightbackground="#004d00")
button_publish.grid(row=0, column=0, padx=10, pady=5, sticky="ew")  
button_request.grid(row=0, column=1, padx=10, pady=5, sticky="ew")  
button_cli.grid(row=0, column=2, padx=10, pady=5, sticky="ew")  
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)




# Chạy ứng dụng

def on_closing():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
