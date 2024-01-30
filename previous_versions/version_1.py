import matplotlib.pyplot as plt
import numpy as np 
import math

# calcul des positions
# unités : angles en radians, temps en secondes, vitesses en m/s

def position_x(v0, alpha, t):
	res = v0*math.cos(alpha)*t
	return res

def position_y(v0, alpha, h0, g, t):
	res = (-1/2)*g*t**2 + v0*math.sin(alpha)*t + h0
	return res

# calcul des vecteurs position et temps selon des conditions données
# unités : angles en radians, temps en secondes, vitesses en m/s, g en m/s^2


def position(v0, angle, h0, g, deltaT):
	posX = []
	posY = []
	posT = []

	finCalcul = False
	t = 0
	while not finCalcul :
		posT.append(t)
		posX.append(position_x(v0, angle, t))
		posY.append(position_y(v0, angle, h0, g, t))
		# arret du calcul quand on touche le sol sur un pas de temps
		if (t>0) and (posY[-1] <= 0):
			finCalcul = True
		t += deltaT

	return [posX, posY, posT]

# formatage de la chaine pour la légende du graphe

def stat2text(v0, ang, X, Y, Z, deltaT):
	# portée max 
	xmax = round( X[-1], 2)
	# altitude max
	ymax = round( np.max( Y ), 2)
	# durée vol
	tmax = len(T) -1
	# chaine a retourner
	ret = 'v0={}m/s, ang={}°, xmax={}m, ymax={}m, tmax={}s'.format(v0, ang, xmax, ymax, tmax*deltaT)
	return ret

# ########################################
# initialisations pour courbes à tracer
# ########################################
ListeX=[] 
ListeY=[]
ListeT=[]
ListeP=[]
deltaT = 0.01 # pas de temps pour calcul des positions

# ########################################
# etapes pour la définition d'une courbe
# ########################################

# saisie des paramètres
v0 = float(input("vitesse initiale (m/s) = "))
alpha = float(input("angle de départ (degrés) = "))
g = float(input("accélération gravitationelle (m/s^2) = "))
h0 = float(input("hauteur initiale (m) = "))
# calcul des positions
[X,Y,T] = position(v0, math.radians(alpha), h0, g, deltaT)
# mémorisation des données
ListeX.append(X)
ListeY.append(Y)
ListeT.append(T)
ListeP.append( stat2text( v0, alpha, X, Y, T, deltaT ) )

# ########################################
# tracé des courbes
# ########################################
fig, ax = plt.subplots()
for index in range(0, len(ListeT)):
	ax.plot(ListeX[index], ListeY[index], label=ListeP[index])

ax.set(xlabel='portée (m)', ylabel='altitude (m)', title='trajectoire du solide')
ax.grid()
ax.legend()

plt.show()