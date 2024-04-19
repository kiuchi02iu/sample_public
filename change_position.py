
#========================================================================================================================================================================================
#IfcOpenShell
#========================================================================================================================================================================================

import ifcopenshell



import numpy as np
import math
import ifcopenshell.util.element
import ifcopenshell.util.placement
import ifcopenshell.geom
import ifcopenshell.api



#実行ボタンの処理
def Import():
    ImportFile=EditBox.get()
    Dirdialog=EditBox2.get()
    model=ifcopenshell.open(ImportFile)

    x=EditBox_x.get()
    y=EditBox_y.get()
    z=EditBox_z.get()
    theta=int(EditBox_a.get())

    move_x=int(x)/1000
    move_y=int(y)/1000
    move_z=int(z)/1000


                       
    for storey in model.by_type("IfcBuildingStorey"):
        elements = ifcopenshell.util.element.get_decomposition(storey)
        for element in elements:
            if "基点" in element.Name:
                    matrix_new=ifcopenshell.util.placement.get_local_placement(element.ObjectPlacement)/1000 #元のmatrix
                    ifcopenshell.api.run("geometry.edit_object_placement", model, product=element, matrix=matrix_new)
            elif "AW" in element.Name:
                matrix_new=ifcopenshell.util.placement.get_local_placement(element.ObjectPlacement)/1000 #元のmatrix
                ifcopenshell.api.run("geometry.edit_object_placement", model, product=element, matrix=matrix_new)
            elif "SD" in element.Name:
                matrix_new=ifcopenshell.util.placement.get_local_placement(element.ObjectPlacement)/1000 #元のmatrix
                ifcopenshell.api.run("geometry.edit_object_placement", model, product=element, matrix=matrix_new)
                
            else:
                matrix_old= ifcopenshell.util.placement.get_local_placement(element.ObjectPlacement)/1000 #元のmatrix
                x_old=float(matrix_old[0,3])
                y_old=float(matrix_old[1,3])
                z_old=float(matrix_old[2,3])
                cosr=float(matrix_old[0,0])
                sinr=float(matrix_old[1,0])

                if cosr==0 and sinr>0:
                     r=90
                elif cosr==0 and sinr<0:
                    r=270
                elif sinr==0 and cosr>0:
                    r=0
                elif sinr==0 and cosr<0:
                    r=180
                elif cosr!=0 and sinr!=0:
                    r=math.degrees(math.atan(sinr/cosr)) #元のmatrixの回転角
                    
                a=int(theta)+r

                sint=math.sin(math.radians(theta))
                cost=math.cos(math.radians(theta))
                sinu=sint*(-1)

                sina=math.sin(math.radians(a))
                cosa=math.cos(math.radians(a))
                sinb=sina*(-1)
                

                matrix=np.array([[cost,sinu,0,0],
                                [sint,cost,0,0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])

                matrixp=[[x_old],
                        [y_old],
                        [z_old],
                        [1]]

                matrix_n=np.dot(matrix,matrixp)

                x_new=float(matrix_n[0])+move_x
                y_new=float(matrix_n[1])+move_y
                z_new=float(matrix_n[2])+move_z

                matrix_new=np.array([[cosa,sinb,0,x_new],
                                    [sina,cosa,0,y_new],
                                    [0,0,1,z_new],
                                    [0,0,0,1]])            #回転後の座標
                
                # print(x_new)
                # print(y_new)
                # print(z_new)
                # # print(matrix_old)
                # print(matrix)
                # print(matrixp)
                # # print(matrix_n)
                # print(matrix_new)
                ifcopenshell.api.run("geometry.edit_object_placement", model, product=element, matrix=matrix_new)
                

        
    model.write(Dirdialog+'\【New】.ifc')
   
def close_window():
    root.destroy()



import os
import tkinter 
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


root=tkinter.Tk()
root.title(u"softwear Title") #ウィンドウのタイトルバーの表記
root.geometry("400x500") #ウィンドウサイズ（"横x縦"）

dy=50
de=20
#変換元ファイルの選択＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
ly=10
ey=ly+de
by=25

#ラベル
Static1=tkinter.Label(text=u'変換元ファイル') #ラベルのハンドルが格納
Static1.pack() #ハンドルをウィンドウのウィジェットに格納
Static1.place(x=10,y=ly)

#エントリー
EditBox=tkinter.Entry(width=50)
EditBox.pack()
EditBox.place(x=10,y=ey)

#ファイルを開く
def open_file_command():
    file_path = filedialog.askopenfilename(filetypes=[('','ifc')])
    EditBox.delete(0,tkinter.END)
    EditBox.insert(tkinter.END,file_path)
    
 
#ボタン
Button=tkinter.Button(text=u'選択',command=open_file_command)
Button.pack()
Button.place(x=340,y=by)


#エントリーの中身の取得
# ImportFile=EditBox.get()



#変換後ファイルの保存場所の選択＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
ly+=dy
ey+=dy
by+=dy

#ラベル
Static1=tkinter.Label(text=u'保存先') 
Static1.pack() 
Static1.place(x=10,y=ly)

#エントリー
EditBox2=tkinter.Entry(width=50)
EditBox2.pack()
EditBox2.place(x=10,y=ey)

#保存先のフォルを選択
def dirdialog_clicked():
    dir_path = filedialog.askdirectory()
    EditBox2.delete(0,tkinter.END)
    EditBox2.insert(tkinter.END,dir_path)


#ボタン
Button=tkinter.Button(text=u'選択',command=dirdialog_clicked)
Button.pack()
Button.place(x=340,y=by)

#エントリーの中身の取得
# Dirdialog=EditBox2.get()


#========================================================================================================================================================================================
#座標の設定
#========================================================================================================================================================================================
ly+=dy
d2y=30

#ラベル'基準位置座標変換'
Static1=tkinter.Label(text=u'基準位置座標変換') 
Static1.pack() 
Static1.place(x=10,y=ly)

l2y=ly+d2y
#ラベルX
Static1=tkinter.Label(text=u'X') 
Static1.pack() 
Static1.place(x=50,y=l2y)
#エントリー
EditBox_x=tkinter.Entry(width=15)
EditBox_x.pack()
EditBox_x.place(x=150,y=l2y)
#エントリーの中身の取得
# x=EditBox_x.get()

l2y+=d2y
#ラベルY
Static1=tkinter.Label(text=u'Y') 
Static1.pack() 
Static1.place(x=50,y=l2y)
#エントリー
EditBox_y=tkinter.Entry(width=15)
EditBox_y.pack()
EditBox_y.place(x=150,y=l2y)
#エントリーの中身の取得
# y=EditBox_y.get()

l2y+=d2y
#ラベルZ
Static1=tkinter.Label(text=u'Z') 
Static1.pack() 
Static1.place(x=50,y=l2y)
#エントリー
EditBox_z=tkinter.Entry(width=15)
EditBox_z.pack()
EditBox_z.place(x=150,y=l2y)
#エントリーの中身の取得
# z=EditBox_z.get()

#保存ボタンの処理
def save():
    root=tkinter.Tk()
    root.title(u"設定の保存") #ウィンドウのタイトルバーの表記
    root.geometry("200x100") #ウィンドウサイズ（"横x縦"）

 
    save=tkinter.Label(text=u'設定名を入力してください') #ラベルのハンドルが格納
    save() #ハンドルをウィンドウのウィジェットに格納
    save.place(x=10,y=20)

    #エントリー
    saveBox=tkinter.Entry(width=50)
    saveBox.pack()
    saveBox.place(x=10,y=ey)

    name=saveBox.get()
    ComboBox.add(name)


#保存ボタン
Button=tkinter.Button(text=u'保存',command=save)
Button.pack()
Button.place(x=340,y=l2y)

l2y+=d2y
#ラベル角度
Static1=tkinter.Label(text=u'角度(反時計回り)') 
Static1.pack() 
Static1.place(x=20,y=l2y)
#エントリー
EditBox_a=tkinter.Entry(width=15)
EditBox_a.pack()
EditBox_a.place(x=150,y=l2y)
#エントリーの中身の取得
# theta=EditBox_a.get()

#実行ボタンの処理
# def Import():
def close():
    root.destroy()


#実行ボタン===================================================================================================================================================================================
#  def open():
#     print(matrix_old)
#     print(matrix_add)
# Button=tkinter.Button(text=u'実行',command=open)
def importclose():
    return[Import(),close()]

Button=tkinter.Button(text=u'実行',command=importclose)
Button.pack()
Button.place(x=340,y=l2y)

#設定を読み込む＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
ly=l2y+dy
ey=ly+de
#ラベル
Static1=tkinter.Label(text=u'設定を読み込む') 
Static1.pack() 
Static1.place(x=10,y=ly)

#コンボボックス
module = ('tkinter', 'math', 'os', 'pyinstaller', 'pathlib', 'sys')
ComboBox = ttk.Combobox(root, values=module)
ComboBox.pack()
ComboBox.place(x=10,y=ey)

#コンボボックス選択の処理
# def 関数(event):

# ComboBox.bind('<<ComboboxSelected>>',関数)

#削除ボタンの処理
# def Import():

#削除ボタン
Button=tkinter.Button(text=u'削除')
Button.pack()
Button.place(x=340,y=ey)

root.mainloop()


