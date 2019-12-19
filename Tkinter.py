import pandas as pd
import numpy as np
from tkinter import*
from tkinter.filedialog import *
from tkinter import messagebox
import tkinter.scrolledtext as tkst


class cl_read():
    
    def __init__(self):
        self.window = Tk()
        self.window.title("csv_reader")
        self.window.geometry("800x750")
        self.window.resizable(width = True, height = True)
        
        # CSV 열기 Frame 설정
        frame_open = Frame(self.window)
        frame_open.pack(padx = 10, pady = 20)
        label_target = Label(frame_open, text = "Target : ")
        label_append = Label(frame_open, text = "Append : ")
                        
        label_target.grid(row = 1, column = 1)
        label_append.grid(row = 2, column = 1)
        
        label_target_dir = Label(frame_open, text = "Target 경로 : ")
        label_append_dir = Label(frame_open, text = "Append 경로 : ")
                        
        label_target_dir.grid(row = 3, column = 1)
        label_append_dir.grid(row = 4, column = 1)
           
        # 뭐지... 이게?
        # 입력창에 받을 주소값
        self.dir_target_self = StringVar()
        self.dir_append_self = StringVar()
        
        # 받은 주소값 출력용
        self.dir_target = "입력된 target 경로입니다."
        self.dir_append = "입력된 append 경로입니다."
        
        # CSV 저장 변수
        self.target = None
        self.append = None
        
        entryTarget = Entry(frame_open, width = 50, textvariable = self.dir_target_self)
        entryAppend = Entry(frame_open, width = 50, textvariable = self.dir_append_self)
        
        entryTarget.grid(row = 1, column = 2)
        entryAppend.grid(row = 2, column = 2)
        
        button_target_find = Button(frame_open, width = 8, text = "찾기", command = lambda: self.find_target_dir())
        button_append_find = Button(frame_open, width = 8, text = "찾기", command = lambda: self.find_append_dir())
        button_print_target = Button(frame_open, width = 8, text = "입력", command = lambda: self.read_target_dir())
        button_print_append = Button(frame_open, width = 8, text = "입력", command = lambda: self.read_append_dir())
        
        button_target_find.grid(row =1, column = 3)
        button_append_find.grid(row =2, column = 3)
        button_print_target.grid(row =1, column = 4)
        button_print_append.grid(row = 2, column = 4)
        
        self.label_dir_target = Label(frame_open, width = 40)
        self.label_dir_append = Label(frame_open, width = 40)
        self.label_dir_target.grid(row = 3, column = 2)
        self.label_dir_append.grid(row = 4, column = 2)
        
        self.label_dir_target.configure(text = self.dir_target)
        self.label_dir_append.configure(text = self.dir_append)
        
        # 인코딩 여부 체크박스
        self.chk_encod_target = IntVar()
        self.chk_encod_append = IntVar()
        
        cb_encod_target = Checkbutton(frame_open, text = "인코딩", variable = self.chk_encod_target)
        cb_encod_apppend = Checkbutton(frame_open, text = "인코딩", variable = self.chk_encod_append)
        cb_encod_target.grid(row = 3, column = 3)
        cb_encod_apppend.grid(row = 4, column = 3)
               
                
        button_open = Button(frame_open, width = 8, text = "열기", command = lambda: self.read_csv())
        button_open.grid(row = 4, column = 4)
        
        #데이터 표시하기
        
        self.data_frame_target = Frame(self.window)
        self.data_frame_target.pack(side = TOP)
        self.data_frame_append = Frame(self.window)
        self.data_frame_append.pack(side = TOP)
        
#   Label 이용하기
#         self.label_target = Label(self.data_frame_target, text = "Target Data")
#         self.label_target.pack()
#         self.label_append = Label(self.data_frame_append, text = "Append Data")
#         self.label_append.pack()

#   Scrollbar widget 이용하기

#-------------------------------------------------------------------------------------------------
# 가로 Scroll 안됨ㅜㅜ (somebody helps me to use horizontal Scroll bar also with vertical bar)
#-------------------------------------------------------------------------------------------------

        self.scroll_x_target = Scrollbar(self.data_frame_target, orient = "horizontal")
        self.scroll_x_target.pack(side = BOTTOM, fill = X)
        self.scroll_x_append = Scrollbar(self.data_frame_append, orient = "horizontal")
        self.scroll_x_append.pack(side = BOTTOM, fill = X)
        
        
        self.txt_target = tkst.ScrolledText(self.data_frame_target, height = 15, xscrollcommand = self.scroll_x_target.set, wrap = NONE)
        self.txt_append = tkst.ScrolledText(self.data_frame_append, height = 15, xscrollcommand = self.scroll_x_append.set, wrap = NONE)
        self.scroll_x_target.config(command = self.txt_target.xview())
        self.scroll_x_append.config(command = self.txt_append.xview())
        self.txt_target.pack()
        self.txt_append.pack()
        self.txt_target.insert(INSERT, "Target Data")
        self.txt_append.insert(INSERT, "Append Data")

# text widget으로 직접 형성.
        
#         self.scroll_y = Scrollbar(self.data_frame)
#         self.scroll_y.pack(side = RIGHT, fill = Y)        
#         self.scroll_x = Scrollbar(self.data_frame, command = self.data_frame.xview)
#         self.scroll_x.pack(side = BOTTOM, fill = X)
#         self.txt_target = Text(self.data_frame, wrap = NONE, yscrollcommand = self.scroll_y.set, xscrollcommand = self.scroll_x.set)
#         self.txt_target.pack(side = LEFT)
#         self.txt_append = Text(self.data_frame, wrap = NONE, yscrollcommand = self.scroll_y.set)
#         self.txt_append.pack(side = LEFT)
        self.frame_merge = Frame(self.window)
        self.frame_merge.pack()
    
        button_merge = Button(self.frame_merge, width = 8, text = "merge", command = lambda: self.open_merge_window())
        button_merge.grid(row = 1, column = 4)
    
    
        self.window.mainloop()
    
    def find_target_dir(self):
        self.dir_target = askopenfilename(initialdir = "C:/", title = "작업할 CSV 파일 입력", filetypes = [("csv files","*.csv"),("all files","*.*")])
        self.label_dir_target.configure(text = self.dir_target)
        print("이것은 target 경로입니다. : ", self.dir_target)
                                    
    def find_append_dir(self):
        self.dir_append = askopenfilename(initialdir = "C:/", title = "작업할 CSV 파일 입력", filetypes = [("csv files","*.csv"),("all files","*.*")])
        self.label_dir_append.configure(text = self.dir_append)
        print("이것은 append 경로입니다. : ", self.dir_append)
    
    def read_target_dir(self):
        self.dir_target = self.dir_target_self.get()
        self.label_dir_target.configure(text = self.dir_target)
        print("이것은 target 경로입니다. : ", self.dir_target)
        
    def read_append_dir(self):
        self.dir_append = self.dir_append_self.get()
        self.label_dir_append.configure(text = self.dir_append)
        print("이것은 append 경로입니다. : ", self.dir_append)
    
#     def labeling_data(self):
#         self.label_target.configure(text = self.target.head())
#         self.label_append.configure(text = self.append.head())
        
    def texting_data(self):
        # 기존 텍스트 제거
        self.txt_target.delete(1.0, END)
        self.txt_append.delete(1.0, END)
        # 읽어온 CSV 값 표시
        self.txt_target.insert(INSERT, self.target)
        self.txt_append.insert(INSERT, self.append)
    
    def read_csv(self):
               
        if (self.chk_encod_target.get() == 1) & (self.chk_encod_append.get() == 1):
            try:
                self.target = pd.read_csv(self.dir_target, encoding = "utf-8-sig", engine = "python")
                self.append = pd.read_csv(self.dir_append, encoding = "utf-8-sig", engine = "python")
                self.texting_data()
                               
            except Exception as e:
                messagebox.showinfo("Warning", e)
            
        elif ~(self.chk_encod_target.get() == 1) & (self.chk_encod_append.get() == 1):
            try:
                self.target = pd.read_csv(self.dir_target, engine = "python")
                self.append = pd.read_csv(self.dir_append, encoding = "utf-8-sig", engine = "python")
                self.texting_data()
            except Exception as e:
                messagebox.showinfo("Warning", e)
                       
        elif (self.chk_encod_target.get() == 1) & ~(self.chk_encod_append.get() == 1):
            try:
                self.target = pd.read_csv(self.dir_target, encoding = "utf-8-sig", engine = "python")
                self.append = pd.read_csv(self.dir_append, engine = "python")
                self.texting_data()
            except Exception as e:
                messagebox.showinfo("Warning", e)
        else:
            try:
                self.target = pd.read_csv(self.dir_target, engine = "python")
                self.append = pd.read_csv(self.dir_append, engine = "python")
                self.texting_data()
            except Exception as e:
                messagebox.showinfo("Warning", e)
        
        print(self.target.head())
        print(self.append.head())
    
    def tg_col_sel(self):
        self.merge_target_col = self.col_name_tg.get()
        print("target의 기준 열은 : ", self.merge_target_col)
        
    def ap_col_sel(self):
        self.merge_append_col = self.col_name_ap.get()
        print("append의 기준 열은 : ", self.merge_append_col)
        
    def opt_sel(self):
        self.merge_howto = self.opt_howto.get()
        print("선택한 옵션은 : ", self.merge_howto)
    
        
    # 새로운 window 창 (merge용) open 함수
    
    def open_merge_window(self):
        #Toplevel class 사용
        self.merge_window = Toplevel(self.window)
        
        self.merge_window.title("file_merge")
        self.merge_window.geometry("800x750")
        self.merge_window.resizable(width = True, height = True)
        
        self.List_target = list(self.target.columns)
        self.List_append = list(self.append.columns)
             
        # error check
        print(self.List_target)
        print(self.List_append)        
                
        fr_menu = Frame(self.merge_window)
        fr_menu.configure(width = 700, height = 50, borderwidth = 1, relief = "sunken" )
        fr_menu.pack(anchor = CENTER)
        
        col_info_tg = Label(fr_menu, text = "Target", borderwidth = 2, relief = "raised")
        col_info_ap = Label(fr_menu, text = "Append", borderwidth = 2, relief = "raised")
        opt_info = Label(fr_menu, text = "Option", borderwidth = 2, relief = "raised")
        
        col_info_tg.pack(side = LEFT, padx = 105, pady = 2)
        col_info_ap.pack(side = LEFT, padx = 105, pady = 2)
        opt_info.pack(side = LEFT, padx = 105, pady = 2)
        
        fr_ls = Frame(self.merge_window)
        fr_ls.configure(width = 700, height = 500, borderwidth = 1, relief = "sunken")
        fr_ls.pack(anchor = CENTER, pady = 20)
                
        fr_tg_ls = Frame(fr_ls)
        
        fr_tg_ls.configure(width = 180, height = 400, borderwidth = 1, relief = "solid")
        fr_tg_ls.pack(side = LEFT, anchor = "center", padx = 40, pady = 10)
        fr_tg_ls.propagate(0)
        
        fr_ap_ls = Frame(fr_ls)
        
        fr_ap_ls.configure(width = 180, height =400, borderwidth = 1, relief = "solid")
        fr_ap_ls.pack(side = LEFT, anchor = "center", padx = 40, pady = 10)
        fr_ap_ls.propagate(0)
        
        fr_opt_ls = Frame(fr_ls)
        fr_opt_ls.configure(width = 180, height = 200, borderwidth = 1, relief = "solid")
        fr_opt_ls.pack(side = TOP, anchor = "center", padx = 40, pady = 10)
        fr_opt_ls.propagate(0)
        
        self.col_name_tg = StringVar()
        self.col_name_ap = StringVar()
        self.opt_howto = StringVar()
        
                
#         frame_merge_opt = Frame(self.merge_window)
#         frame_merge_opt.pack(side = LEFT)
#         frame_merge_opt.grid(row =1 , column =1)
        
#         self.col_name_target = StringVar()
#         self.col_name_append = StringVar()
        
#         col_info_tg = Label(self.merge_window, text = "Target", borderwidth = 2, relief = "raised")
#         col_info_tg.place(x = 50, y =100, width = 50, height=20)
        
        for col_name in self.List_target:
            col_name = str(col_name)
            radiobutton = Radiobutton(fr_tg_ls, text = col_name, value = col_name, variable = self.col_name_tg, command = lambda: self.tg_col_sel())
            radiobutton.pack(side = TOP, anchor = W)
            
        for col_name in self.List_append:
            col_name = str(col_name)
            radiobutton1 = Radiobutton(fr_ap_ls, text = col_name, value = col_name, variable = self.col_name_ap, command = lambda: self.ap_col_sel())
            radiobutton1.pack(side = TOP, anchor = W)
        
        for howto in ["left", "right", "outer"]:
            howto = str(howto)
            radiobutton2 = Radiobutton(fr_opt_ls, text = howto, value = howto, variable = self.opt_howto, command = lambda: self.opt_sel())
            radiobutton2.pack(side = TOP, anchor = W)
            
        fr_finish_mg = Frame(self.merge_window)    
        fr_finish_mg.configure(width = 700, height = 100, borderwidth = 1, relief = "sunken")
        fr_finish_mg.pack(anchor = CENTER)
        fr_finish_mg.propagate(0)
                
        bt_merge = Button(fr_finish_mg, width = 8, text = "merge", command = lambda: self.merge_final())
        bt_save = Button(fr_finish_mg, width = 8, text = "save", command = lambda: self.save_dat())
        bt_save.pack(side = RIGHT, padx = 10, pady = 10)
        bt_merge.pack(side = RIGHT, padx = 10, pady = 10)
        
        
        self.txt_result = tkst.ScrolledText(fr_finish_mg, width = 400, height = 20, borderwidth = 1, relief = "solid")
        self.txt_result.pack(side = BOTTOM, anchor = CENTER)
        self.txt_result.insert(INSERT, "LOG below \n")
        
#         self.lb_result = Label(fr_finish_mg, width = 400, height = 10, borderwidth = 1, relief = "solid")
#         self.lb_result.pack(side = BOTTOM, anchor = CENTER)
        
    
    def save_dat(self):
        try:
            self.save_name = asksaveasfilename(initialdir = "C:/", title = "저장할 xlsx 파일 입력", filetypes = [("Excel files","*.xlsx"),("all files", "*.*")])
            self.save_name = self.save_name + ".xlsx"
            log_text = "\n" + self.save_name
            self.txt_result.insert(END, log_text)
            self.merge_dat.to_excel(self.save_name, encoding = "utf-8-sig", index = None)
            self.txt_result.insert(END, "\n저장되었습니다.")
        except Exception as e:
            messagebox.showinfo("Warning", e)
        
    def merge_final(self):
        try:
            self.merge_dat = pd.merge(self.target, self.append, left_on = self.merge_target_col, right_on = self.merge_append_col, how = self.merge_howto)
            self.txt_result.insert(END, "\n정상적으로 merge되었습니다.")
        except Exception as e:
            messagebox.showinfo("Warning", e)
            
main_window = cl_read()
