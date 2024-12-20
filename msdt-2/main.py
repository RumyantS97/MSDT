#Classe Main
#Auteur: Carette Antonin

from Animals import Animal
from Animals import Hamster
from Animals import Perruche
from Animals import Dog
from Animals import Snake
from Petshop import Petshop
from Person import Person
from Person import Player
from Person import Workman
from Person import Visitor

import sys
import random

#Paramètres généraux
nomJoueur = ""
sexeJoueur = ""
nbrTours = 1
nbrVisiteurs = 0
difficulte = ""
argentDepart = 0
choix_animalerie = -1
liste_animaleries = []
liste_cmd = ["aide", "acheter_animal", "acheter_nourriture", "info_animaux", "info_banque", "info_attirance", "embaucher", "virer","reparer", "q"]
liste_animaux = ["Hamster", "Perruche", "Chien", "Serpent"]
achat_animaux = []
achat_nourriture = {"Hamster":0, "Chien":0, "Perruche":0, "Serpent":0}
personnel_a_embaucher = []
#Liste de tours représentant les jours de chaleur - pour la reproduction des animaux
joursDeChaleur = [4,14,17,23,29]

#Instanciation
liste_animaleries.append(Petshop.Petshop("A Rebrousse Poil", 20, 15, 4500))
liste_animaleries.append(Petshop.Petshop("Pattoune", 15, 15, 3700))
liste_animaleries.append(Petshop.Petshop("Animalia", 15, 18, 3200))
liste_animaleries.append(Petshop.Petshop("Hamsteragram", 12, 20, 2200))

personnel_a_embaucher.append(Workman.Workman("Nadine", "Femelle", "Maitre"))
personnel_a_embaucher.append(Workman.Workman("Gérard", "Male", "Medium"))
personnel_a_embaucher.append(Workman.Workman("Xavier", "Male", "Maitre"))
personnel_a_embaucher.append(Workman.Workman("Laurent", "Male", "Expert"))
personnel_a_embaucher.append(Workman.Workman("Lucie", "Femelle", "Novice"))
personnel_a_embaucher.append(Workman.Workman("Lola", "Femelle", "Novice"))
personnel_a_embaucher.append(Workman.Workman("Maxime", "Male", "Medium"))
personnel_a_embaucher.append(Workman.Workman("Kyllian", "Male", "Expert"))

#Fonctions

def sexeJoueurOk(sexe):
	"""Vérification de la bonne entrée du sexe du joueur"""
	return (sexe == "Homme" or sexe == "Femme")

def infoJoueur():
	"""Demande les informations principales du joueur"""
	global nomJoueur
	global sexeJoueur
	nomJoueur = input("Tout d'abord, veuillez choisir un nom: ")
	while (not sexeJoueurOk(sexeJoueur)):
		print("Entrez votre sexe [Homme, Femme]: ",)
		sexeJoueur = sys.stdin.readline().capitalize().strip()

def getArgent():
	"""Choix de la somme d'argent de départ, en fonction de la difficulté"""
	global difficulte
	if (difficulte == "easy"):
		return 10000
	if (difficulte == "medium"):
		return 5000
	if (difficulte == "hard"):
		return 2500

def transfertCommande(player):
	"""Méthode permettant de transférer les commandes vers le stock de l'animalerie"""
	global animalerie_choisie
	global achat_animaux
	global achat_nourriture
	paiementLivraisonAnimaux(player)
	paiementLivraisonNourriture(player)
	for animal in achat_animaux:
		animalerie_choisie.addAnimal(animal)
		print("Un",animal.getRace(),"vient d'être ajouté à votre stock!")
	reinitAchatAnimaux()
	for animal in achat_nourriture:
		animalerie_choisie.addNourritureParAnimal(animal, achat_nourriture[animal])
		print(achat_nourriture[animal],"unités de nourriture pour",animal,"vient d'être ajouté à votre stock!")
	reinitAchatNourriture()
	print("\n")

def paiementLivraisonAnimaux(player):
	"""Méthode permettant de payer la livraison des animaux à l'animalerie -> Si 10 animaux (et plus), paiement de 20 crédits - sinon, 3 * le nombre d'animaux présents"""
	global achat_animaux
	nbrAnimaux = len(achat_animaux)
	if (nbrAnimaux >= 10):
		montant = 20
	else:
		montant = 3 * nbrAnimaux
	player.rmMontant(montant)
	print(nbrAnimaux,"animal(aux) a(ont) été livré(s) - paiement de", montant,"crédits.")

def paiementLivraisonNourriture(player):
	"""Méthode permettant de payer la livraison de la nourriture à l'animalerie -> Si 6 unités (et plus) de nourriture, paiement de 10 crédits - sinon, 2 * le nombre d'unités de nourriture"""
	global achat_nourriture
	nbrNourriture = 0
	for animal in achat_nourriture:
		nbrNourriture = nbrNourriture + achat_nourriture[animal]
	if (nbrNourriture >= 6):
		montant = 10
	else:
		montant = 2 * nbrNourriture
	player.rmMontant(montant)
	print(nbrNourriture,"unité(s) de nourriture livré(s) - paiement de", montant,"crédits.")

def reinitAchatAnimaux():
	"""Méthode permettant de réinitialiser la liste des animaux achetés"""
	global achat_animaux
	achat_animaux = []

def diminuer_pts_de_vie(pts):
	"""Méthode permettant de diminuer tous les points de vie des animaux présents dans l'animalerie"""
	global animalerie_choisie
	animalerie_choisie.diminuerPtsDeVie(pts)

def apport_soin_animaux():
	"""Fonction permettant d'apporter un soin aux animaux, en fonction de la qualification de l'/des employé(s)"""
	global animalerie_choisie
	global nbrTours
	if len(animalerie_choisie.getListeEmployes()) == 0:
		return
	if animalerie_choisie.getNbrAnimaux() == 0:
		return
	if nbrTours % 5 == 0:
		max = 0
		for employe in animalerie_choisie.getListeEmployes():
			if employe.getSoin() > max:
				max = employe.getSoin()
		liste_animaux = animalerie_choisie.returnListeAnimaux()
		for animals in liste_animaux.values():
			for animal in animals:
				animal.addPtsDeVie(max)

def consommationDeNourriture():
	"Méthode permettant aux animaux de l'animalerie de consommer de la nourriture"
	global animalerie_choisie
	animalerie_choisie.consommationDeNourriture()

def reinitAchatNourriture():
	"""Méthode permettant de réinitialiser la liste de nourriture achetée"""
	global achat_nourriture
	for animal in achat_nourriture:
		achat_nourriture[animal] = 0

def delAll():
	"""Supprime les objets créés"""
	player.__del__
	for animalerie in liste_animaleries:
		animalerie.__del__

def paiementDesEmployes(player):
	"""Fonction permettant de payer les employés, en fonction de leur date d'embauche"""
	global nbrTours
	global animalerie_choisie
	#Pour tous les employés
	for employe in animalerie_choisie.getListeEmployes():
		#Si date anniversaire, on paye
		if (employe.getDateEmbauche() == (nbrTours % 30)):
			player.rmMontant(employe.getPaye())
			#employe.incrMontant(employe.getPaye())
			print("Employé",employe.getNom(),"payé!")
			employe.incrContent()
	print("\n")

def checkEmployes():
	"""Fonction permettant de mettre à jour la base de données des employés, et d'en faire démissionner si les conditions de travail ne leur plaise pas..."""
	global animalerie_choisie
	for employe in animalerie_choisie.getListeEmployes():
		if employe.getContent() < 10:
			animalerie_choisie.rmEmploye(employe)
			print("L'employé",employe.getNom(),"a démissionné...")

def setDateEmbauche(employe):
	"""Fonction permettant d'ajouter une date d'embauche dans un objet Workman"""
	global nbrTours
	nbrTours = nbrTours % 30
	if nbrTours == 0:
		nbrTours = 1
	employe.setDateEmbauche(nbrTours)

def getInteretPourVisiteur():
	"""Fonction permettant de connaitre l'intéret du visiteur pour acheter, en fonction de divers paramètres de l'animalerie..."""
	global animalerie_choisie
	liste_employes = animalerie_choisie.getListeEmployes()
	#Calcul de l'intérêt selon l'attirance envers l'animalerie
	if animalerie_choisie.getAttirance() >= 18:
		return 1
	#Calcul de la moyenne de contentement, chez les ouvriers
	if len(liste_employes) > 0:
		taux_contentement = 0;
		for employe in liste_employes:
			taux_contentement = taux_contentement + employe.getContent()
		taux_contentement = taux_contentement / len(liste_employes)
		if taux_contentement >= 15:
			return 1
		if taux_contentement >= 10:
			return random.randrange(0,2,1)
		else:
			print("Vos employés ne sont pas contents... Ils font fuir les clients!!\n")
	if animalerie_choisie.getDegats() <= 16:
		return 1
	if animalerie_choisie.getDegats() <= 20 and animalerie_choisie.getAttirance() >= 13:
		return random.randrange(0,2,1)
	else:
		print("Votre animalerie est en très mauvais état, et celà n'attire pas grand monde... Il va falloir la réparer!!\n")
		return 0

def addReproduction():
	"""Fonction permettant de faire reproduire deux animaux de meme race, s'ils sont de sexes différents (obviously...)"""
	global animalerie_choisie
	global joursDeChaleur
	global nbrTours
	liste_animaux = animalerie_choisie.returnListeAnimaux()
	if len(liste_animaux) == 0:
		return
	else:
		if (nbrTours % 30) in joursDeChaleur: 
			sexeFemelle = False
			animalFemelle = None
			sexeMale = False
			for animals in liste_animaux.values():
				for animal in animals:
					if animal.getSexe() == "Femelle" and animal.getEnceinte() != True:
						sexeFemelle = True
						animalFemelle = animal
					else:
						sexeMale = True
				if sexeFemelle == True and sexeMale == True:
					animalFemelle.setEnceinte()
					print("Un animal de race", animalFemelle.getRace(),"est enceinte!\n")

def surveillanceMiseABas():
	"""Fonction permettant de surveiller si un animal va mettre à bas ou non..."""
	global animalerie_choisie
	decTpsGestationGlobal()
	liste_animaux = animalerie_choisie.returnListeAnimaux()
	for animals in liste_animaux.values():
		for animal in animals:
			if animal.getEnceinte():
				if animal.getTpsGestation() <= 0:
					animal.metBas(animalerie_choisie)
				else:
					print("Temps de gestation pour un animal de race", animal.getRace(),":",animal.getTpsGestation())

def decTpsGestationGlobal():
	"""Fonction permettant de décrémenter le temps de gestation pour tous les animaux présents dans l'animalerie"""
	global animalerie_choisie
	liste_animaux = animalerie_choisie.returnListeAnimaux()
	for animals in liste_animaux.values():
		for animal in animals:
			animal.decTpsGestation()

#Fonctions PRINT

def printBienvenue():
	"""Affichage d'un message de bienvenue"""
	print("\nJOUEUR, BIENVENUE DANS \"PETSHOP\"!!\n")

def printAnimaleries():
	"""Affichage des animaleries créés"""
	global liste_animaleries
	print("\n")
	i = 1
	for animalerie in liste_animaleries:
		print(i,":", )
		animalerie.printInfo()
		print("\n")
		i = i + 1

def printInfoJoueur(player):
	"""Affichage des données du joueur - en début de tour"""
	player.printInfo()

def printInfoAnimalerie():
	global animalerie_choisie
	animalerie_choisie.printInfoTour()

def printInstructions():
	"""Méthode permettant d'afficher les instructions à l'écran"""
	print("Voici les instructions")
	print("Vous êtes propriétaire d'une animalerie, et désirez que tout aille pour le mieux (logique!). Or, tout n'est pas aussi rose que celà...")
	print("Votre but est donc de survivre un maximum de tours.")
	print("Voici comment va se passer chaque tour de jeu:")
	print("\t --Vous dénombrez les animaux morts du jour (malheureusement... :'(),")
	print("\t --Vous recevez votre inventaire, et devez payer la livraison,")
	print("")
	print("\t --Vous pouvez commander de nouvelles choses pour le lendemain, effectuer des travaux dans votre animalerie, embaucher du personnel, etc... Et vous recevez un nombre indéfini de clients,")
	print("\n MAIS ATTENTION!")
	print("Vous avez une liste de choses qui pourront vous mettre dans l'embarras (ce ne serai pas marrant sinon!):")
	print("\t --Votre magasin détient des dégâts - cela influe sur la santé des animaux! Plus les dégâts seront forts et moins vos animaux vivront longtemps... De plus, plus ils seront vite malades, ce qui ne pourrai pas plaire au client...")
	print("\t --Votre animal a besoin de nourriture pour vivre! Il faudra donc en acheter régulièrement! Un animal sans nourriture s'affaibliera, et pourra être malade très vite...")
	print("\t --Les lois de la nature sont imprévisibles! Un papa + une maman = un enfant! Et ça marche aussi avec les animaux... Reproduction aléatoire, mais une nouvelle bouche de plus à nourrir (soit deux unités par femelle enceinte!)")
	print("\t --Faites attention à votre argent! Vous en avez besoin pour vivre. Aussi, vous avez droit à un découvert équivalent à votre somme de départ - si vous le dépassez, c'est foutu...")
	print("\t --La livraison est de 3 crédits par animal, 2 crédits par unité de nourriture.\n\t1 animal -> 3 crédits | 10 et + -> 20 crédits\n\t1 unité de nourriture -> 2 crédits | 6 et + -> 10 crédits")
	print("\t --Des clients pourraient venir vous apporter de petits animaux abandonnés (so cuuute!) - attention à celà! Les prendre pourraient diminuer drastiquement votre stock de nourriture, mais ne pas les prendre pourraient faire que vos clients vous prennent pour un monstre, vous fasse une mauvaise pub et fasse fuir vos employés...")
	print("\t --C'est bien d'avoir un beau magasin, et d'embaucher du personnel! Attention toutefois: plus vous avez d'animaux et plus de dégâts il y aura! Aussi, il se pourrai qu'un événement inattendu vienne vous causer du tord dans un tour (une tempête, une tornade, etc...). De plus, embaucher beaucoup de personnel coûte, et ils ne seront pas content si jamais vous les payez tard...")
	print("\n Alors, prêt à jouer? :-) C'est parti!")
	print("\nPour avoir une liste des commandes pouvant être exécutées durant le jeu, tapez aide dans la console!\n")

def printCredits():
	"""Affiche les crédits de fin"""
	print("**FIN DU JEU!!")
	print("Merci d'y avoir jouer!")
	print("Des remarques -> antonin[dot]carette[at]gmail[dot]com")

	#CMD

def print_aide():
	"""Fonction permettant d'afficher une liste exhaustive des commandes accessibles dans le terminal"""
	print("\n")
	print('Liste des commandes:')
	print('\taide:', 'affiche la liste des commandes du programme')
	print('\tinfo_animaux:', 'affiche les informations concernant la liste des animaux achetés')
	print('\tinfo_banque:', 'affiche les informations banquaires du joueur')
	print('\tinfo_attirance', 'affiche l\'attirance de votre animalerie (sur le moment)')
	print('\tacheter_animal:', 'permet d\'acheter un animal')
	print('\tacheter_nourriture:', 'permet d\'acheter de la nourriture')
	print('\tembaucher:', 'permet d\'embauche du personnel (qualifié ou non)')
	print('\tvirer:', 'permet de virer du personnel, si vous en avez...')
	print('\treparer:', 'permet de réparer quelques dégats de son animalerie')
	print('\tq:', 'permet de passer un tour')
	print("\n")

def print_info_animaux():
	"""Fonction permettant d'afficher une liste exhaustive des animaux et de leurs propriétés"""
	global animalerie_choisie
	print("\n")
	animalerie_choisie.getListeAnimaux()

def print_info_banquaire(player):
	"""Fonction permettant d'afficher une sortie du compte en banque du joueur"""
	print("\n")
	print("Compte en banque du joueur: ", player.getMontant())
	print("\n")

def print_personnel_a_embaucher():
	"""Fonction permettant d'afficher la liste du personnel à embaucher"""
	print("======= DEBUT LISTE PERSONNEL =======")
	print("\n")
	i = 1
	for candidat in personnel_a_embaucher:
		print(i,":")
		candidat.printInfo()
		i = i + 1
		print("\n")
	print("======== FIN LISTE PERSONNEL ========")

def print_info_attirance():
	"""Fonction permettant d'imprimer l'attirance de l'animalerie"""
	global animalerie_choisie
	print("\n");
	print("L'attirance de votre animalerie est de", animalerie_choisie.getAttirance())
	print("\n");

# Fonctions FUN -> Fonctions lourdes, avec achat, visites, etc... Très importantes pour la suite d'un tour!

def fun_acheter_animal(player):
	"""Fonction permettant d'acheter un animal, pour son animalerie"""
	global liste_animaux
	global animalerie_choisie
	global achat_animaux
	choixAnimal = ""
	nbrAchat = -1
	print("Veuillez entrer l'espèce animale que vous voulez choisir [Hamster, Perruche, Chien, Serpent]: ")
	while (choixAnimal not in liste_animaux):
		choixAnimal = sys.stdin.readline().capitalize().strip()
	print("Veuillez entrer le nombre d'animaux de cette espèce que vous voulez acheter [0 pour annuler]: ")
	while (nbrAchat <= -1):
		nbrAchat = int(input())
		print("nbrAchat", nbrAchat)
	for i in range (0, nbrAchat):
		alea = random.randrange(0,2,1)
		if (alea == 0):
			sexe = "Male"
		else:
			sexe = "Femelle"
		if (choixAnimal ==  "Hamster"):
			animal = Hamster.Hamster(sexe)
		if (choixAnimal == "Perruche"):
			animal = Perruche.Perruche(sexe)
		if (choixAnimal == "Chien"):
			animal = Dog.Dog(sexe)
		if (choixAnimal == "Serpent"):
			animal = Snake.Snake(sexe)
		player.rmMontant(animal.getPrixAchat())
		achat_animaux.append(animal)
		animal.printInfo()

def fun_acheter_nourriture(player):
	"""Fonction permettant d'acheter de la nourriture pour un type d'animal, ou plusieurs
		-> Choisir animal
		-> Choisir combien
		-> 3 unités * le nombre de nourriture par animal
	"""
	global liste_animaux
	global achat_nourriture
	choixAnimal = ""
	nbreNourriture = -1
	print("Veuillez entrer l'espèce animale dont vous voulez acheter de la nourriture [Hamster, Perruche, Chien, Serpent]: ")
	while (choixAnimal not in liste_animaux):
		choixAnimal = sys.stdin.readline().capitalize().strip()
	print("Veuillez entrer le nombre de kilogrammes de nourriture que vous voulez acheter pour cet animal [0 pour annuler]:  ")
	while (nbreNourriture <= -1):
		nbreNourriture = int(input())
	if nbreNourriture == 0:
		return
	achat_nourriture[choixAnimal] = achat_nourriture[choixAnimal] + nbreNourriture
	montantAchat = 3 * nbreNourriture
	player.rmMontant(montantAchat)
	print("\n")
	print("Vous venez d'acheter",nbreNourriture,"kilogrammes de nourriture pour",choixAnimal,": ",montantAchat," unités.")
	print("\n")

def fun_embaucher_personnel():
	"""Fonction permettant d'afficher toutes les informations utiles quant au personnel à embaucher"""
	global personnel_a_embaucher
	global animalerie_choisie
	choixPersonnel = -1
	if len(personnel_a_embaucher) > 0:
		print("Voici les candidats:\n")
		print_personnel_a_embaucher()
		while (choixPersonnel > len(personnel_a_embaucher) or choixPersonnel < 0):
			choixPersonnel = int(input("Veuillez sélectionner la personne à embaucher [0 si nul]:"))
		if (choixPersonnel == 0):
			print("Vous n'avez embauché personne...")
		else:
			choixPersonnel = choixPersonnel - 1
			setDateEmbauche(personnel_a_embaucher[choixPersonnel])
			animalerie_choisie.addEmploye(personnel_a_embaucher[choixPersonnel])
			print("Vous avez embauché",personnel_a_embaucher[choixPersonnel].getNom(),"!")
			print("\n")
			del(personnel_a_embaucher[choixPersonnel])
			animalerie_choisie.incrAttirance()
			print("L'attirance envers votre animalerie a augmenté!")
	else:
		print("Il n'y a personne à embaucher!")

def fun_virer_personnel(player):
	"""Fonction permettant de virer du personnel"""
	global animalerie_choisie
	if len(animalerie_choisie.getListeEmployes()) == 0:
		print("Vous n'avez pas de personnel à virer...")
		return
	choixPersonnel = ""
	while choixPersonnel != "Oui" and choixPersonnel != "Non":
		print("Virer du personnel est très mal vu... De plus, vous allez devoir payer deux fois le salaire de la personne que vous allez virer. Êtes-vous certain de faire celà...? [oui/non]")
		choixPersonnel = sys.stdin.readline().capitalize().strip()
	if choixPersonnel == "Non":
		return
	print("Veuillez choisir la personne à virer dans la liste ci-dessous:")
	cpt = 1
	for employe in animalerie_choisie.getListeEmployes():
		print(cpt,":")
		employe.printInfo()
		print("\n")
		cpt = cpt + 1
	nbrPersonnel = -1
	while nbrPersonnel <= 0 or nbrPersonnel > len(animalerie_choisie.getListeEmployes()):
		print("Numéro de l'employé à virer:")
		nbrPersonnel = int(input())
	employeVire = animalerie_choisie.getListeEmployes()[nbrPersonnel - 1]
	print("Vous avez choisi de virer", employeVire.getNom())
	aDebiter = employeVire.getPaye() * 2
	print("Votre compte va être débité de", aDebiter,"au profit de",employeVire.getNom())
	player.rmMontant(aDebiter)
	animalerie_choisie.rmEmploye(employeVire)
	animalerie_choisie.decrAttirance(1)
	print("L'attirance envers votre animalerie a diminué...")

def fun_reparer(player):
	"""Fonction permettant de réparer quelques dégats de l'animalerie"""
	global animalerie_choisie
	global argentDepart
	#(-argentDepart + 400) -> endetté + 400 de réparation minimum
	if player.getMontant() > (-argentDepart + 400):
		nbrDegats = -1
		print("La réparation est de 400 crédits pour 2 dégats en moins.\nCombien voulez-vous réparer de dégats [0 pour annuler]?")
		while nbrDegats < 0:
			nbrDegats = int(input())
			if (player.getMontant() - (nbrDegats * 400)) < (-argentDepart):
				print("Vous ne pouvez pas payer pour autant de réparations...")
				nbrDegats = -1  
		print("Réparation de", nbrDegats,"dégats en cours...")
		animalerie_choisie.setDegats(int(animalerie_choisie.getDegats()) - nbrDegats)
		if animalerie_choisie.getDegats() < 0:
			animalerie_choisie.setDegats(0)
		player.rmMontant(nbrDegats * 400)
		print("Réparation de votre animalerie effectuée!\n")
		animalerie_choisie.incrAttirance()
		print("L'attirance envers votre animalerie a augmenté!")
	else:
		print("Vous n'avez pas assez de crédits pour effectuer une réparation...\n")

def fun_venue_visiteurs(player):
	"""Fonction permettant de faire venir (ou non) un acheteur - à base d'aléatoire!"""
	global animalerie_choisie
	global liste_animaux
	global nbrVisiteurs
	if animalerie_choisie.getNbrAnimaux() > 0:
		nbrCreationVisiteurs = random.randrange(0,5,1)
		if nbrCreationVisiteurs == 0:
			return
		#Pour le nombre donné précédemment, on va créer une instance de Visitor
		for i in range (0,nbrCreationVisiteurs):
			visiteur_actuel = Visitor.Visitor()
			nbrVisiteurs = nbrVisiteurs + 1
			#Variable permettant de savoir si l'acheteur est intéressé pour acheter ou non
			interesse_pour_acheter = getInteretPourVisiteur()
			if interesse_pour_acheter == 0:
				print("\nAcheteur non interessé pour acheter...\n")
				return
			#Interessé -> on poursuit en choisissant un animal
			animal_choisi = liste_animaux[random.randrange(0,2,1)]
			#On choisi le premier animal de la liste
			animal = animalerie_choisie.returnAnimal(animal_choisi)
			#On paie le joueur, s'il a bien l'animal demandé...
			if animal != "None":
				player.incrMontant(animal.getPrixVente())
				#On vend l'animal définitivement (voir doc de delAnimal dans Petshop)
				animalerie_choisie.delAnimal(animal_choisi)
			else:
				print("\nUn acheteur voulait un(e)", animal_choisi,", mais vous n'en aviez pas... :-/\n")

#MAIN

if __name__ == "__main__":

	##DÉBUT

	#Chargement des variables globales
	global nomJoueur
	global sexeJoueur
	global nbrTours
	global difficulte
	global choix_animalerie
	global liste_cmd
	global nbrVisiteurs
	global argentDepart

	#Affichage du message de bienvenue
	printBienvenue()

	#Demande des informations du joueur
	infoJoueur()

	#Choix de la difficulté
	while ((difficulte != "easy") and (difficulte != "medium") and (difficulte != "hard")):
		print("Veuillez entrer le niveau de difficulté du jeu [easy, medium, hard]:")
		difficulte = sys.stdin.readline()
		difficulte = difficulte.strip()

	#Sauvegarde de la somme d'argent initiale
	argentDepart = getArgent()

	#Création du joueur
	player = Player.Player(nomJoueur, sexeJoueur, argentDepart, False)

	print("Vous partez avec une mise de",argentDepart,"unités!\n")

	#Affichage des animaleries
	printAnimaleries()

	#Choix de la première animalerie
	while (choix_animalerie > len(liste_animaleries) or choix_animalerie < 1):
		choix_animalerie = int(input("Veuillez choisir une animalerie:"))

	#Le joueur devient propriétaire de l'animalerie qu'il a choisi
	liste_animaleries[choix_animalerie - 1].setProprietaire(True)

	animalerie_choisie = liste_animaleries[choix_animalerie - 1]

	player.rmMontant(animalerie_choisie.getPrix())

	print("\nVous avez choisi l'animalerie", animalerie_choisie.getNom())

	animalerie_choisie.setProprietaire(True, player)

	print("\nLe jeu va pouvoir commencer!")

	##LE JEU COMMENCE

	#Instructions
	printInstructions()

	#Variable contenant la commande principale du jeu à rentrer
	commande = ""

	#Condition de sortie -> Le joueur est endetté, et détient une dette de -(argentDepart)
	while (not player.isTerm(-argentDepart)):

		print("Tour n°:", nbrTours)

		#Diminution des points de vie de chaque animal
		diminuer_pts_de_vie(int(animalerie_choisie.getDegats()) / 10)

		#Apport de soins par les employés, tous les 5 tours
		apport_soin_animaux()

		#Surveillance de la mise à bas des animaux
		surveillanceMiseABas()

		#Paiement des employés
		paiementDesEmployes(player)

		#Check des employés contents/non-contents
		checkEmployes()

		#Arrivée des commandes et transfert sur le stock de l'animalerie
		if (nbrTours != 0):
			transfertCommande(player)

		#Affichage des infos du joueur
		printInfoJoueur(player)

		print("\n")

		#Affichage des infos de l'animalerie
		printInfoAnimalerie()

		print("\n")

		nbrCommandes = 0

		nbrVisiteurs = 0

		commande = ""

		#Tant que l'utilisateur n'a pas tapé "q", alors on continue sur le même tour
		while (commande != "q" and nbrCommandes < 5):

			commandesRestantes = 5 - nbrCommandes

			#Attente de la commande utilisateur
			print("Commande [q pour quitter -",commandesRestantes,"commandes restantes]:")

			commande = sys.stdin.readline().lower().strip()

			while (commande not in liste_cmd and commande != "q"):
				print("Mauvaise commande - veuillez réessayer")
				commande = sys.stdin.readline().lower().strip()

			if (commande == "aide"):
				print_aide()

			if (commande == "info_animaux"):
				print_info_animaux()

			if (commande == "info_banque"):
				print_info_banquaire(player)

			if (commande == "info_attirance"):
				print_info_attirance();

			if (commande == "acheter_animal"):
				fun_acheter_animal(player)

			if (commande == "acheter_nourriture"):
				fun_acheter_nourriture(player)

			if (commande == "embaucher"):
				fun_embaucher_personnel()

			if (commande == "virer"):
				fun_virer_personnel(player)

			if (commande == "reparer"):
				fun_reparer(player)

			if (commande != "aide" and commande != "contact"):
				nbrCommandes = nbrCommandes + 1

		fun_venue_visiteurs(player)

		consommationDeNourriture()

		addReproduction()

		print("Fin du tour", nbrTours,", vous avez eu", nbrVisiteurs,"visiteurs dans la journée.\n")

		animalerie_choisie.addNbrVisites(nbrVisiteurs)

		nbrTours = nbrTours+1;

		nbrVisiteurs = 0

	##FIN DU JEU##

	print("Vous avez perdu...")

	#Déconstruction des objets créés auparavant
	delAll()

	#Crédits de fin
	printCredits()