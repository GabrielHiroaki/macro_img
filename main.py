# Aluno: Daniel Ortega de Carvalho, RA:170088
# Aluno: Gabriel Hiroaki da Silva Kanezaki, RA:179292


#_#_#_#_#_#_#_#_#_ INSTRUÇÕES _#_#_#_#_#_#_#_#_#_#
# Execute o programa

# Selecione a imagem da folha antes da herbivoria

# Selecione a imagem da folha após a herbivoria

# Pressione qualquer botão do teclado para continuar

# Decida se deseja salvar a imagem 

# Caso desejar salvar, escolha o diretório e o nome
# da imagem, a extensão será colocada conforme a 
# imagem original (nesse caso .TIF)


import numpy as np
import cv2
import tkinter as tk
from os import system
from timeit import default_timer as t
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox


system('clear')

# referência: utilizando o retângulo vermelho da foto, 
# temos 650 pixels (anotados manualmente) para cada 5cm,
# logo 1px = 1/130cm e 1px² = (1/130)²cm²
areaPix = 1/130**2

# seleciona as imagens Antes e Depois no Tkinter
def abrir_imagem(string):
    path = askopenfilename(title=string)
    img = cv2.imread(path)
    if type(img) == np.ndarray:
        return img, path
    print('Imagem inválida.')
    return abrir_imagem(string)

root = tk.Tk()
root.withdraw()

imgARGB, path = abrir_imagem('Folha - Antes')
imgDRGB, _ = abrir_imagem('Folha - Depois')

# salvando a extensão da imagem
ext = path.replace('\\','/').split('/')[-1].split('.')[-1]

# salva as imagens no espaço de cor HSV
imgA = cv2.cvtColor(imgARGB,cv2.COLOR_BGR2HSV)
imgD = cv2.cvtColor(imgDRGB,cv2.COLOR_BGR2HSV)
H, L = imgA.shape[:2]

# Definindo um filtro threshold inicial
HSVif_int = [32,64,0,66,255,80]
HSVif_str = ['Hi','Si','Vi','Hf','Sf','Vf']
mask = cv2.cvtColor(cv2.inRange(np.concatenate((imgA, imgD), axis = 1), tuple(HSVif_int[0:3]), tuple(HSVif_int[3:6])), cv2.COLOR_GRAY2BGR)

# parâmetros do texto da imagem
pos = [(int(L*0.07),int(H*0.7)),(int(L*0.07),int(H*0.8)),(int(L*0.07),int(H*0.9))]
par = {'font':cv2.FONT_HERSHEY_SIMPLEX,'fscale':4.5,'thick':10,'color':(51, 153, 102)}
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = int(0.001*L)
thickness = int(0.002*L)
color = (51, 153, 102)

# criação da trackbar
def calculoArea(trackbar):
    global mask
    # criando o filtro threshold da imagem antes e depois
    # para concatená-las em seguida.
    maskA = cv2.inRange(imgA, tuple(HSVif_int[0:3]), tuple(HSVif_int[3:6]))
    maskD = cv2.inRange(imgD, tuple(HSVif_int[0:3]), tuple(HSVif_int[3:6]))
    mask = cv2.cvtColor(np.concatenate((maskA, maskD), axis = 1),cv2.COLOR_GRAY2BGR)
    
    # conta a quantidade total de pixels na image, na folha
    # anterior e na folha posterior.
    pixPretos = H*L
    pixBrancosA = int(np.sum(maskA)/255)+1
    pixBrancosD = int(np.sum(maskD)/255)+1

    # criação dos textos da imagem final, mostrando em cm²
    # o total de área inicial e a final, também mostrando
    # suas diferenças em porcentagem.
    txt1 = f'Area Inicial : {pixBrancosA*areaPix:.2f}cm2'
    txt2 = f'Area Final : {pixBrancosD*areaPix:.2f}cm2'
    txt3 = f'Diferenca : {(pixBrancosA-pixBrancosD)*areaPix:.2f}cm2 ({(1-pixBrancosD/pixBrancosA)*100:.2f})%'

    # Inserção dos textos na imagem
    mask = cv2.putText(mask, txt1, pos[0], par['font'], par['fscale'], 
                    par['color'], par['thick'], cv2.LINE_AA, False)
    mask = cv2.putText(mask, txt2, pos[1], par['font'], par['fscale'], 
                    par['color'], par['thick'], cv2.LINE_AA, False)
    mask = cv2.putText(mask, txt3, pos[2], par['font'], par['fscale'], 
                    par['color'], par['thick'], cv2.LINE_AA, False)

    cv2.namedWindow('HSV', cv2.WINDOW_NORMAL)
    cv2.imshow('HSV', mask)

def hsv(x):
    global HSVif_int
    HSVif_int = [ cv2.getTrackbarPos(s,'HSV') for s in HSVif_str]
    calculoArea(HSVif_int)

trackbar = [['Hi','HSV',HSVif_int[0],179],['Hf','HSV',HSVif_int[3],179],['Si','HSV',HSVif_int[1],255],
            ['Sf','HSV',HSVif_int[4],255],['Vi','HSV',HSVif_int[2],255],['Vf','HSV',HSVif_int[5],255]]

cv2.namedWindow('HSV', cv2.WINDOW_NORMAL)
cv2.resizeWindow('HSV', 1000, 600)

calculoArea(trackbar)

for i in trackbar:
    cv2.createTrackbar(i[0],i[1],i[2],i[3],hsv)
cv2.waitKey(0)

# salva a imagem no diretório escolhido
def salvar_imagem():
    MsgBox = tk.messagebox.askquestion ('Salvar imagem','Você deseja salvar a imagem?',icon = 'warning')
    if MsgBox == 'yes':
        path = asksaveasfilename()
        if path != '':
            cv2.imwrite(f'{path}.{ext}', mask)
            tk.messagebox.showinfo('Return',f'Imagem Salva em {path}.{ext}')
    root.destroy()
salvar_imagem()

root.mainloop()
cv2.destroyAllWindows()
