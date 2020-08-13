# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 12:31:42 2020
@author: GoodOasis
Exercice proposé par Graven www.youtube.com/channel/UCIHVyohXw6j2T-83-uLngEg
J'ai été plus loin avec une POO et une fenetre dynamique.
Le résulat est différent à chaque lancement.
"""

import random
from tkinter import *

# Couleurs.
BLACK = 'black'
RED = 'red'


class Movie:
    """
    CLass créant un objet "film" contenant le nom du film
    la salle de projection ainsi que les horaires.
    """

    def __init__(self, name, room, seat, schedule):
        self.name = name
        self.room = room
        self.total_seat = seat
        # Le nombre de places disponiles est généré aléatoirement.
        self.free_seat = random.randint(1, 50)
        self.schedule = schedule

    def __str__(self):
        """
        Methode qui transforme notre objet movie en 1 str compréhensible.
        """
        return self.name + "//Salle " + str(self.room) + "-" + self.schedule

    def __repr__(self):
        """ Méthode de representation qui appel __str__. """
        return self.__str__()

    def take_seat(self):
        """ Méthode qui permet de reserver une place. """
        # Vérifie s'il reste des place avant de décrémenter.
        if self.free_seat > 0:
            self.free_seat -= 1
        return self.free_seat


# Creation des films
movie_list = {}
name_list = ["Interstellar", "Blow", "Inception", "Oss 117", "Harry Potter"]
# Mélange la liste pour ne pas avoir toujours le même ordre.
random.shuffle(name_list)

schedule_list = ["18h05", "12h50", "15h44", "17h21", "12h28"]
seat_list = [80, 120, 200, 144, 120]

# Creation du dictionnaire contenant les Movies
for i in range(random.randint(1, 5)):
    movie_list[i] = Movie(name=name_list[i], room=(i+1),
                          seat=seat_list[i], schedule=schedule_list[i])


class CineManager:

    def __init__(self, dict_):
        """
        Constructeur de class qui prend en parametre un dictionnaire
        contenant des objets de la class Movie.
        """
        # Initialisation de la fenetre principal Tkinter
        self.window = Tk()
        # Nom de la fenetre.
        self.window.title("CineManager")
        # Image de la fenetre.
        self.window.iconbitmap("cinemanager.ico")
        # Taille d'ouverture de la fenetre.
        self.window.geometry("1400x630")
        # Taille minimaal de la fenetre.
        self.window.minsize(300, 300)
        # Couleur de la fond dela fenetre.
        self.window.config(background=BLACK)
        # Initialisation d'un dictionnaire renseigné en arguments
        self.dict = dict_

        # Creation de la frame princiaple
        self.main_frame = Frame(self.window, bg=BLACK)
        self.sub_frame = Frame(self.main_frame, bg=BLACK)

        # Initialisation des variables de class
        self.subframe_dict = {}

        # Creation des frames et de leurs widgets
        self.create_movieframes()
        self.create_widgets()

        # Empactage
        self.main_frame.pack(side=TOP)
        self.sub_frame.pack(expand=YES)

    def create_widgets(self):
        """ Méthode qui creer le tire principal. """
        main_title = Label(self.main_frame,
                           text="Reservez votre seance\nde cinema:",
                           font=("Palanito", 30, "bold"), bg=BLACK, fg=RED)
        # Empactage
        main_title.pack(pady=80, side=TOP)

    def create_movieframes(self):
        """
        Méthode qui créer une frame par film et
        qui appel create_movie_widgets() pour la remplir.
        puis l'empacte.
        """
        # initialisation de l'image du ticket.
        self.movie_image = PhotoImage(file="ticket.png").zoom(2).subsample(2)
        # Creation du dict qui va contenir toutes les frames (1film = 1 frame).
        self.frame_dict = {}
        for i in self.dict:
            self.frame_dict[i] = Frame(self.sub_frame, bg=BLACK,
                                       highlightthickness=1)
            # Ajout des widgets
            self.create_movie_widgets(self.dict[i], i)
            # Empactage
            self.frame_dict[i].grid(padx=10, row=0, column=i)

    def create_movie_widgets(self, Movie, i):
        """
        Méthode qui creer une tuile par film avec titre, horaires et
        nombres de places disponibles.
        Elle ajoute aussi un bouton pour reserver la place et une image.
        """
        # Label du titre du film.
        movie_title = Label(self.frame_dict[i], text=self.dict[i].name,
                            font=("Arial Black", 20, "bold"),
                            bg=BLACK, fg=RED)

        # Label de la salle de projection du film.
        movie_room = Label(self.frame_dict[i],
                           text=("Salle " + str(self.dict[i].room)),
                           font=("Arial Black", 18, "bold"),
                           bg=BLACK, fg="orange")

        # Label de l'horaire de la séances.
        movie_schedule = Label(self.frame_dict[i],
                               text=("a " + str(self.dict[i].schedule)),
                               font=("Arial Black", 10, "bold"),
                               bg=BLACK, fg="orange")

        # Label du nombre de places disponibles.
        movie_seat = Label(self.frame_dict[i],
                           text=("Place disponible " +
                                 str(self.dict[i].free_seat)),
                           font=("Arial Black", 15, "bold"),
                           bg=BLACK, fg="orange")

        # Ajout d'un canvas pour accueillir l'image de ticket.
        width = 128
        height = width
        movie_canvas = Canvas(self.frame_dict[i], width=width, height=height,
                              bg=BLACK, highlightthickness=0)
        movie_canvas.create_image(width/2, height/2, image=self.movie_image)

        # Le boutton. Utilisation de lambda afin de renseinger des arguments.
        movie_button = Button(self.frame_dict[i], text="Reserver",
                              bg="yellow", fg=RED,
                              command=lambda: self.reserve(movie_seat, self.dict[i], i))
        # Empactage
        movie_title.pack(side=TOP)
        movie_room.pack()
        movie_schedule.pack()
        movie_seat.pack()
        movie_canvas.pack()
        movie_button.pack(side=BOTTOM)

    def reserve(self, wdgt, movie, i):
        """ Méthode d'action du boutton "resever. """
        free_seat = movie.take_seat()
        # Si le film renseigné en argument n'a plus de place.
        if free_seat == 0:
            wdgt.config(text=("Seance complete"))
        else:
            # Sinon on décrémente free_seat.
            wdgt.config(text=("Place disponible " + str(free_seat)))


# Lancement de l'appli
APP = CineManager(movie_list)
APP.window.mainloop()
