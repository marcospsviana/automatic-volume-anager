# -*- encoding: utf-8 -*-
import os
import sys
sys.path.insert(0,"/home/marcos/projeto_coolbag/raspcontrol/")
from tkinter import *
from tkinter import ttk as t
from tkinter import messagebox as msg
from controllers import Management

class Janela(object):
    
    def __init__(self, master=None):
        style = t.Style()
        style.configure( "TLabel", font="Arial, 14")
        style.configure("TButton", font="Arial, 14", background="#222930", foreground="white", relief="FLAT", width=10, heigth=25)
        
        

        self.frame_principal = t.Frame(master)
        self.frame_principal.pack()
        self.container_armario = t.Frame(master=self.frame_principal)
        self.container_armario.grid(row=0, column=0, padx=5, pady=5)
        self.lbl_armario = t.Label(master=self.container_armario, text="Classe : ")
        self.lbl_armario.grid(column=0, row=0)
        self.entry_armario = t.Entry(master=self.container_armario)
        self.entry_armario.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_nivel = t.Label(master=self.container_armario, text="Nível : ")
        self.lbl_nivel.grid(column=2, row=0)
        self.entry_nivel = t.Entry(master=self.container_armario)
        self.entry_nivel.grid(row=0, column=3)

        self.lbl_terminal = t.Label(master=self.container_armario, text="Terminal : ")
        self.lbl_terminal.grid(column=0, row=1)
        self.entry_terminal = t.Entry(master=self.container_armario)
        self.entry_terminal.grid(row=1, column=1, padx=5, pady=5)

        self.lbl_coluna = t.Label(master=self.container_armario, text="Coluna : ")
        self.lbl_coluna.grid(column=2, row=1)
        self.entry_coluna = t.Entry(master=self.container_armario)
        self.entry_coluna.grid(row=1, column=3, padx=5, pady=5)

        self.lbl_local = t.Label(master=self.container_armario, text="Local : ")
        self.lbl_local.grid(column=0, row=3)
        self.entry_local= t.Entry(master=self.container_armario)
        self.entry_local.grid(row=3, column=1, padx=5, pady=5)



        
        self.container_botoes = t.Frame(master=self.frame_principal)
        self.container_botoes.grid(row=1, column=0, columnspan=10)
        
        self.bt_cad = t.Button(master=self.container_armario, text="Cadastrar Armário", command = self.cad_armario, width=18)
        
        
        self.bt_cad.grid(row=3, column=2, columnspan=5, padx=5, pady=5)
      

    

    def cad_armario(self):
            controller = Management()
            controller.cad_armarios()

    
    

root = Tk()
Janela(root)
root.title("CADASTRO DE ARMÁRIOS")
root.geometry("550x100")
root.mainloop()