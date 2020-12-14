#Importer les modules nécessaires :
import mysql.connector as mysql
import numpy as np
import tkinter
from tkinter import *


class Connection:
    #Connection MySQL :
    def __init__(self):
        self.lien = mysql.connect(host='localhost', password='ISEN', user='ISEN', database='breizhibus_1')
        self.curseur = self.lien.cursor()

    #Boutons Tkinter par ligne de bus :
    def boutons_lignes(self):
        self.curseur.execute("SELECT * FROM lignes")
        for id, nom, couleur in self.curseur.fetchall():
            bouton_ligne = tkinter.Button(fenetre, text=f"Ligne {id} : {nom}", bg=couleur, command=lambda id=id: self.afficher_arrets_bus(id))
            bouton_ligne.grid(row=1, column=int(id-1))

    #Joindre les méthodes pour arrêts et bus :
    def afficher_arrets_bus(self, id_ligne):
        self.afficher_arrets(id_ligne)
        self.afficher_bus(id_ligne)

    #Affichage des arrêts d'une ligne :
    def afficher_arrets(self, id_ligne):
        for widget in cadre_arrets.winfo_children():
            widget.grid_forget()
        self.curseur.execute(f"SELECT nom FROM lignes WHERE id_ligne = {id_ligne}")
        nom_ligne = self.curseur.fetchall()[0]
        nom_ligne = str(*nom_ligne)
        tkinter.Label(cadre_arrets, text=f"Ligne {id_ligne} : {nom_ligne}", font="Helvetica 12 bold").grid(row=0, column=0, columnspan=3)
        self.curseur.execute(f"SELECT id_arret FROM arrets_lignes WHERE id_ligne = {id_ligne}")
        liste_id_arrets = self.curseur.fetchall()
        hauteur = 1
        for id_arret in liste_id_arrets:
            self.curseur.execute(f"SELECT nom, adresse FROM arrets WHERE id_arret = {id_arret[0]}")
            for nom, adresse in self.curseur.fetchall():
                tkinter.Label(cadre_arrets, text=hauteur).grid(row=hauteur, column=0)
                tkinter.Label(cadre_arrets, text=nom).grid(row=hauteur, column=1)
                tkinter.Label(cadre_arrets, text=adresse).grid(row=hauteur, column=2)
            hauteur += 1

    #Affichage des bus d'une ligne :
    def afficher_bus(self, id_ligne):
        for widget in cadre_bus.winfo_children():
            widget.grid_forget()
        self.curseur.execute(f"SELECT numero FROM bus WHERE id_ligne = {id_ligne}")
        liste_bus = self.curseur.fetchall()
        tkinter.Label(cadre_bus, text="Bus de la ligne :", font="Helvetica 10 bold").grid(row=0, column=0, columnspan=3)
        hauteur = 1
        for numero_bus in liste_bus:
            numero_bus = str(*numero_bus)
            self.curseur.execute(f"SELECT immatriculation FROM bus WHERE numero = '{numero_bus}'")
            imma_bus = self.curseur.fetchall()[0]
            imma_bus = str(*imma_bus)
            tkinter.Label(cadre_bus, text=f"Bus {numero_bus} immatriculé {imma_bus}").grid(row=hauteur, column=0, columnspan=3)
            hauteur += 1

    #Demande d'insertion d'un nouveau bus dans la base :
    def insertion_bus(self):
        self.vider_cadre_insertion()

        label_numero = tkinter.Label(cadre_insertion, text="Entrez le numéro (ex : BB01) du bus...")
        entree_numero = tkinter.Entry(cadre_insertion)
        label_numero.grid(row=1, column=0, columnspan=3)
        entree_numero.grid(row=2, column=0, columnspan=3)

        label_imma = tkinter.Label(cadre_insertion, text="... son n° d'immatriculation...")
        entree_imma = tkinter.Entry(cadre_insertion)
        label_imma.grid(row=3, column=0, columnspan=3)
        entree_imma.grid(row=4, column=0, columnspan=3)

        label_places = tkinter.Label(cadre_insertion, text="... le nombre de places...")
        entree_places = tkinter.Entry(cadre_insertion)
        label_places.grid(row=5, column=0, columnspan=3)
        entree_places.grid(row=6, column=0, columnspan=3)

        label_ligne = tkinter.Label(cadre_insertion, text="... et le numéro de ligne (ex : 1).")
        entree_ligne = tkinter.Entry(cadre_insertion)
        label_ligne.grid(row=7, column=0, columnspan=3)
        entree_ligne.grid(row=8, column=0, columnspan=3)

        bouton_creer_bus = tkinter.Button(cadre_insertion, text="Créer le Bus", bg='#FF6A00', command=lambda: self.insertion_bus_base(entree_numero.get(), entree_imma.get(), entree_places.get(), entree_ligne.get())).grid(row=9, column=0, columnspan=3)

    #Envoi du nouveau bus en base :
    def insertion_bus_base(self, numero, immatriculation, places, ligne):
        table = "INSERT INTO bus (numero, immatriculation, nombre_place, id_ligne) VALUES (%s, %s, %s, %s)"
        valeurs = (numero, immatriculation, places, ligne)
        self.curseur.execute(table, valeurs)
        self.lien.commit()
        self.vider_cadre_insertion()

    #Demande de suppression de bus:
    def supprimer_bus(self):
        self.vider_cadre_insertion()

        label_suppression = tkinter.Label(cadre_insertion, text="Entrez le numéro (ex : BB01) du bus à supprimer :")
        entree_suppression = tkinter.Entry(cadre_insertion)
        label_suppression.grid(row=0, column=0, columnspan=3)
        entree_suppression.grid(row=1, column=0, columnspan=3)

        bouton_supprimer_bus = tkinter.Button(cadre_insertion, text="Supprimer le Bus", bg='#FF6A00', command=lambda: self.supprimer_bus_base(entree_suppression.get()))
        bouton_supprimer_bus.grid(row=2, column=0, columnspan=3)

    #Suppression du bus en base:
    def supprimer_bus_base(self, numero_bus):
        self.curseur.execute("DELETE FROM bus WHERE numero = %s", (numero_bus, ))
        self.lien.commit()
        self.vider_cadre_insertion()

    #Créer les entrées pour chercher un itinéraire:
    def entrees_chemin(self):
        self.vider_cadres_chemin()

        label_depart = tkinter.Label(cadre_entrees_chemin, text="Entrez l'arrêt de départ (ex : Korrigan).")
        entree_depart = tkinter.Entry(cadre_entrees_chemin)
        label_depart.grid(row=0, column=0, columnspan=3)
        entree_depart.grid(row=1, column=0, columnspan=3)
        
        label_fin = tkinter.Label(cadre_entrees_chemin, text="Entrez l'arrêt de sortie (ex : Morgana).")
        entree_fin = tkinter.Entry(cadre_entrees_chemin)
        label_fin.grid(row=2, column=0, columnspan=3)
        entree_fin.grid(row=3, column=0, columnspan=3)

        bouton_chercher_chemin = tkinter.Button(cadre_entrees_chemin, text="Chercher cet Itinéraire", bg='#007F7F', command=DISABLED).grid(row=4, column=0, columnspan=3)

    #Chercher le chemin le plus court :
    def recherche_chemin(self, depart, fin):
        

    #Vider cadre_insertion:
    def vider_cadre_insertion(self):
        for widget in cadre_insertion.winfo_children():
            widget.grid_forget()
            
    #Vider cadre_insertion:
    def vider_cadres_chemin(self):
        for widget in cadre_entrees_chemin.winfo_children():
            widget.grid_forget()

    
#Raccourci Connection() :
connection = Connection()

#Créer la fenêtre entière :
fenetre = tkinter.Tk()

#Ligne 0 de la grille = titre Breizhibus :
tkinter.Label(fenetre, text="BREIZHIBUS", font="Helvetica 18 bold").grid(row=0, column=0, columnspan=3)

#Ligne 1 = les boutons de choix de lignes :
connection.boutons_lignes()

#Ligne 2 = l'affichage des arrêts d'une ligne :
cadre_arrets = tkinter.Frame(fenetre)
cadre_arrets.grid(row=2, column=0, columnspan=3)

#Ligne 3 = l'affichage des bus de la ligne :
cadre_bus = tkinter.Frame(fenetre)
cadre_bus.grid(row=3, column=0, columnspan=3)

#Ligne 4 = les boutons pour chercher un chemin :
cadre_boutons_chemin = tkinter.Frame(fenetre)
bouton_chemin = tkinter.Button(cadre_boutons_chemin, text="Chercher Itinéraire", bg='#007F7F', command=connection.entrees_chemin)
bouton_chemin.grid(row=0, column=0)
bouton_annuler_chemin = tkinter.Button(cadre_boutons_chemin, text=f"Annuler", bg='#007F7F', command=lambda: connection.vider_cadres_chemin())
bouton_annuler_chemin.grid(row=0, column=2)
cadre_boutons_chemin.grid(row=4, column=0, columnspan=3)

#Ligne 5 = l'affichage des entrées de requette de chemin :
cadre_entrees_chemin = tkinter.Frame(fenetre)
cadre_entrees_chemin.grid(row=5, column=0, columnspan=3)

#Ligne 6 = l'affichage du chemin recherché :
cadre_chemin = tkinter.Frame(fenetre)
cadre_chemin.grid(row=6, column=0, columnspan=3)

#Ligne 7 = les boutons d'ajout et de suppression d'un bus :
cadre_boutons_bas = tkinter.Frame(fenetre)
cadre_boutons_bas.grid(row=7, column=0, columnspan=3)

bouton_insertion = tkinter.Button(cadre_boutons_bas, text=f"Nouveau Bus", bg='#FF6A00', command=connection.insertion_bus)
bouton_insertion.grid(row=0, column=0)

bouton_suppression = tkinter.Button(cadre_boutons_bas, text=f"Supprimer Bus", bg='#FF6A00', command=connection.supprimer_bus)
bouton_suppression.grid(row=0, column=1)

bouton_annuler_bas = tkinter.Button(cadre_boutons_bas, text=f"Annuler", bg='#FF6A00', command=lambda: connection.vider_cadre_insertion())
bouton_annuler_bas.grid(row=0, column=2)

#Ligne 8 = l'affichage des requettes de nouveau bus/supprimer un bus :
cadre_insertion = tkinter.Frame(fenetre)
cadre_insertion.grid(row=8, column=0, columnspan=3)

#Initier la fenêtre entière :
fenetre.mainloop()