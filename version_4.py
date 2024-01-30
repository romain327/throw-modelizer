from tkinter import *
import matplotlib.pyplot as plt
import numpy as np 
import math

# calcul des positions
# unités : angles en radians, temps en secondes, vitesses en m/s

def position_x(v0, alpha, mu, t):
	res = 0
	# sans frottements
	if mu == 0:
		res = v0*math.cos(alpha)*t
	else:
	# avec frottements
		v0x = math.cos(alpha)*v0
		res = -v0x * math.exp(-mu*t)*1/mu + v0x/mu
	return res

def position_y(v0, alpha, mu, h0, g, t):
	res = 0
	# sans frottements
	if mu == 0:
		res = (-1/2)*g*t**2 + v0*math.sin(alpha)*t + h0
	else:
	# avec frottements
		v0y = math.sin(alpha)*v0
		res = (-1/2)*g*t**2 - v0y*math.exp(-mu*t)*1/mu + h0 + v0y/mu
	return res

# calcul des vecteurs position et temps selon des conditions données
# unités : angles en radians, temps en secondes, vitesses en m/s, g en m/s^2

def position(v0, angle, mu, h0, g, deltaT):
	posX = []
	posY = []
	posT = []

	finCalcul = False
	t = 0
	while not finCalcul :
		posT.append( t )
		posX.append( position_x(v0, angle, mu, t) )
		posY.append( position_y(v0, angle, mu, h0, g, t) )
		# arret du calcul quand on touche le sol sur un pas de temps
		if (t>0) and (posY[-1] <= 0):
			finCalcul = True
		t += deltaT

	return [posX, posY, posT]


# formatage de la chaine pour la légende du graphe
def stat2text(v0, ang, mu, X, Y, T, deltaT):
	# portée max 
	xmax = round( X[-1], 2)
	# altitude max
	ymax = round( np.max( Y ), 2)
	# durée vol
	tmax = len(T) -1
	# chaine a retourner
	ret = 'v0={}m/s, ang={}°, mu={}, xmax={}m, ymax={}m, tmax={}s'.format(
	v0, ang, mu, xmax, ymax, tmax*deltaT)
	return ret


############################################################
# TRACE DES COURBES
############################################################

ListeX=[] # positions X du solide
ListeY=[] # positions Y du solide
ListeT=[] # instants des positions
ListeP=[] # légendes pour les courbes
deltaT = 0.01 # pas de temps pour calcul des positions


def calcul_positions(v0, angle, h0, g, fr):
	
	[X,Y,T] = position(v0, math.radians(angle), fr, h0, g, deltaT)

	ListeX.append(X)
	ListeY.append(Y)
	ListeT.append(T)
	ListeP.append( stat2text( v0, angle, fr, X, Y, T, deltaT ) )



############################################################
# INTERFACE GRAPHIQUE
############################################################


# efface les valeurs des champs
def clear():
	
	vitesse_init_field.delete(0, END)
	angle_tir_field.delete(0, END)
	hauteur_init_field.delete(0, END)
	constante_g_field.delete(0, END)
	frottements_field.delete(0, END)


# mémorise les valeurs dans un dictionnaire quand on
# clique sur "ajouter"
def memorise_saisie():
	
	# clear the content of text entry box
	p1 = float( vitesse_init_field.get() )
	p2 = float( angle_tir_field.get() )
	p3 = float( hauteur_init_field.get() )
	p4 = float( constante_g_field.get() )
	p5 = float( frottements_field.get() )

	calcul_positions(p1, p2, p3, p4, p5)

	fig, ax = plt.subplots()
	for index in range(0, len(ListeT)):
		ax.plot(ListeX[index], ListeY[index], label=ListeP[index])

	ax.set(xlabel='portée (m)', ylabel='altitude (m)', title='trajectoire du solide')
	ax.grid()
	ax.legend()
	plt.show()

	clear()



# programme principal
if __name__ == "__main__":
	
	# create a GUI window
	root = Tk()
	# set the title of GUI window
	root.title("paramètres d'un tir")
	# set the configuration of GUI window
	root.geometry("500x300")

	# création des labels
	lbl_vitesse   = Label(root, text="vitesse initiale (m/s)")
	lbl_angle     = Label(root, text="angle de tir (°)")
	lbl_hauteur   = Label(root, text="hauteur initiale (m)")
	lbl_pesanteur = Label(root, text="pesanteur G (m/s^2)")
	lbl_frottemts = Label(root, text="forces de frottements")

	# placement des labels
	lbl_vitesse.grid(row=0, column=0)
	lbl_angle.grid(row=1, column=0)
	lbl_hauteur.grid(row=2, column=0)
	lbl_pesanteur.grid(row=3, column=0)
	lbl_frottemts.grid(row=4, column=0)

	# champs de saisie
	vitesse_init_field = Entry(root)
	angle_tir_field = Entry(root)
	hauteur_init_field = Entry(root)
	constante_g_field = Entry(root)
	frottements_field = Entry(root)

	# placement des champs de saisie
	vitesse_init_field.grid(row=0, column=1, ipadx="50")
	angle_tir_field.grid(row=1, column=1, ipadx="50")
	hauteur_init_field.grid(row=2, column=1, ipadx="50")
	constante_g_field.grid(row=3, column=1, ipadx="50")
	frottements_field.grid(row=4, column=1, ipadx="50")

	# bouton ajouter
	submit = Button(root, text="ajouter", command=memorise_saisie)
	submit.grid(row=6, column=1)

	# start the GUI
	root.mainloop()


