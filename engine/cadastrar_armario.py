# -*- encoding: utf-8 -*-
from tkinter import *
from tkinter import ttk as t
from tkinter import messagebox as msg
from data import Banco

class Janela(object):
    
    def __init__(self, master=None):
        style = t.Style()
        style.configure( "TLabel", font="Arial, 14")
        style.configure("TButton", font="Arial, 14", background="#222930", foreground="white", relief="FLAT", width=10, heigth=25)
        
        

        self.frame_principal = t.Frame(master)
        self.frame_principal.pack()
        self.container_lbl = t.Frame(master=self.frame_principal)
        self.container_lbl.pack()
        self.label_pergunta = t.Label(master=self.frame_principal, text="Determine o tipo de armário classe : A, B, C ou D")
        self.label_pergunta.pack()
        self.container_botoes = t.Frame(master=self.frame_principal)
        self.container_botoes.pack()
        self.bt_a = t.Button(master=self.container_botoes, text="A")
        self.bt_a["command"] = self.cad_armario
        self.bt_a.pack(side=LEFT,pady=2, padx=2)
        self.bt_b = t.Button(master=self.container_botoes, text="B")
        self.bt_b["command"] = self.cad_armario
        self.bt_b.pack(side=LEFT,pady=2, padx=2)
        self.bt_c = t.Button(master=self.container_botoes, text="C")
        self.bt_c["command"] = self.cad_armario
        self.bt_c.pack(side=LEFT,pady=2, padx=2)
        self.bt_d = t.Button(master=self.container_botoes, text="D")
        self.bt_d["command"] = self.cad_armario
        self.bt_d.pack(side=LEFT,pady=2, padx=2)

    

    def cad_armario(self):
            banco = Banco()
            print("a")
            answer = msg.askokcancel("novo armario","cadastrar novo armário tamanho A?")
            
            if answer:
                    banco.cadastrar_armario()
            else:
                    root

    
    

root = Tk()
Janela(root)
root.geometry("550x100")
root.mainloop()