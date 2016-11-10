#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
sys.path.append('/Users/clementtailleur/PyQt-mac-gpl-4.11.4/sip')
import sqlite3
import subprocess
import datetime

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QCoreApplication, Qt
from PyQt4.QtGui import QListWidget, QListWidgetItem, QApplication
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Model import Model



class ViewController(QtGui.QMainWindow):

	####################################################################################################################
	#																												   #
	#												CONSTRUCTOR														   #
	#																												   #
	####################################################################################################################

	# In the constructor we initialize all the variables, they can be labels, text fields, list views... or just integers
	# We also connect all the items to their associated function which would be defined later.

	def __init__(self, model, parent=None):
		super(ViewController, self).__init__()
		self.model = model
		
		
		######################################################
		#													 #
		#						DISPLAY		   				 #
		#													 #
		######################################################

		# We will take care of the window, we add all the items that are necessary.

		##################
		#	1- APP ICON	 #
		##################

		# We create app_icon, which is of QIcon type, and we add it as the window icon
		# We add a Pixmap to the icon object, which is an image
		# We set the icon as window icon with the setWindowIcon command

		app_icon = QtGui.QIcon()
		app_icon.addPixmap(QtGui.QPixmap('Images/Functions/Dico.png'))
		self.setWindowIcon(app_icon)

		##################
		#	2- FONT  	 #
		##################

		# We create 3 objects of Qfont type, they are the font we are going to use in the code later. There is a default font,
		# a title font, and a font dedicated form explicatives labels

		font = QtGui.QFont()
		font.setFamily("Monaco")
		fontTitle = QtGui.QFont()
		fontTitle.setFamily("Monaco")
		fontTitle.setUnderline(True)
		fontexp = QtGui.QFont()
		fontexp.setFamily("Calibri")
		fontexp.setPixelSize(9)
		fontexp.setItalic(True)

		##########################
		#	3- LABEL WELCOME	 #
		##########################

		# We create a LBL_BIENVENUE that will be on the window and will print a welcome message in the selected language
		# With the setGeometry function we put the x and y coordinates of the item and its length, width
		# With the setAlignment command we can center the label
		# With the setFont command we set the font of the text in the label
		# We put the default valeu of LANGUAGE which is French

		self.LBL_BIENVENUE = QLabel("Bienvenue jeune pipiou dans notre dictionnaire !", self)
		self.LBL_BIENVENUE.setGeometry(QtCore.QRect(120, 68, 400, 31))
		self.LBL_BIENVENUE.setAlignment(QtCore.Qt.AlignCenter)
		self.LBL_BIENVENUE.setFont(fontTitle)
		self.LANGUAGE = "Francais"

		######################
		#	4- LABEL FLAG	 #
		######################

		# We create 2 labels containing the 2 flags that are displayed on the window and will change depending on 
		# the language selected, the default language is set to french

		self.LBL_FLAG1 = QtGui.QLabel(self)
		self.LBL_FLAG1.setGeometry(QtCore.QRect(50, 68, 40, 30))
		self.LBL_FLAG1.setPixmap(QtGui.QPixmap('Images/Countries/France.png'))
		self.LBL_FLAG1.setScaledContents(True)
		self.LBL_FLAG2 = QtGui.QLabel(self)
		self.LBL_FLAG2.setGeometry(QtCore.QRect(550, 68, 40, 30))
		self.LBL_FLAG2.setPixmap(QtGui.QPixmap('Images/Countries/France.png'))
		self.LBL_FLAG2.setScaledContents(True)


		######################
		#	5- MENU ACTION	 #
		######################

		# We create the menubar which contains the menus File, Edit and Help, which contain under-menus
		# to add the menus we use the addMenu command and to add Action to the menus, we use addAction command
		# File contains: Search for searching the definition of a word, Invert for searching a word by entering the definition,
		# Favorites that will display the user's favourites words and Close to close the window
		# Edit contains: Change current language, which has an under-menu for choosing the language between French, English, German and Spanish
		# Add and Delete word for add or delete words and also modifying them
		# Help contains: Information which opens a pdf file to explain how the dictionnary works.
		# All the under-menus contains an icon, and are connected to functions to make the desired actions when clicking on the menus.

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		searchAction = fileMenu.addAction('&Search', self.searchWord)
		iconSearch = QtGui.QIcon()
		iconSearch.addPixmap(QtGui.QPixmap('Images/Functions/Search.png'))
		searchAction.setIcon(iconSearch)
		invertAction = fileMenu.addAction('&Inverted Search', self.invert)
		iconInvert = QtGui.QIcon()
		iconInvert.addPixmap(QtGui.QPixmap('Images/Functions/Invert.png'))
		invertAction.setIcon(iconInvert)
		favoritesAction = fileMenu.addAction('&Favorites', self.displayFavorite_Correspondence)
		iconFav = QtGui.QIcon()
		iconFav.addPixmap(QtGui.QPixmap('Images/Functions/Fav.png'))
		favoritesAction.setIcon(iconFav)
		closeAction = fileMenu.addAction('&Close')
		iconClose = QtGui.QIcon()
		iconClose.addPixmap(QtGui.QPixmap('Images/Functions/Close.png'))
		closeAction.setIcon(iconClose)
		closeAction.triggered.connect(QtGui.qApp.quit)
		closeAction.setShortcut('Ctrl+Q')
		editMenu = menubar.addMenu('&Edit')
		languagesAction = editMenu.addMenu('&Change current language')
		iconWorld = QtGui.QIcon()
		iconWorld.addPixmap(QtGui.QPixmap('Images/Functions/Countries.png'))
		languagesAction.setIcon(iconWorld)
		helpMenu = menubar.addMenu('&Help')
		helpAction = helpMenu.addAction('&Documentation', self.helpme)
		iconHelp = QtGui.QIcon()
		iconHelp.addPixmap(QtGui.QPixmap('Images/Functions/Help.png'))
		helpAction.setIcon(iconHelp)
		newwordAction = editMenu.addAction('&Add/modify word', self.addWord)
		iconAdd = QtGui.QIcon()
		iconAdd.addPixmap(QtGui.QPixmap('Images/Functions/Add.png'))
		newwordAction.setIcon(iconAdd)
		deleteAction = editMenu.addAction('&Delete word', self.deleteWord_Correspondence)
		iconDelete = QtGui.QIcon()
		iconDelete.addPixmap(QtGui.QPixmap('Images/Functions/Delete.png'))
		deleteAction.setIcon(iconDelete)

		##################
		#	6- ENGLISH	 #
		##################

		# For all the languages, we add an under-action to languageAction (which is 'Current Language') and we connect it
		# to the concerned function, we add an icon and we set it as Checkable for the language to be checked is selected
		# with the setCheckable(True)

		self.english = languagesAction.addAction('English', self.english)
		iconEnglish = QtGui.QIcon()
		iconEnglish.addPixmap(QtGui.QPixmap('Images/Countries/England.png'))
		self.english.setIcon(iconEnglish)
		self.english.setCheckable(True)

		##################
		#	7- FRENCH	 #
		##################

		self.french = languagesAction.addAction('French', self.french)
		iconFrench = QtGui.QIcon()
		iconFrench.addPixmap(QtGui.QPixmap('Images/Countries/France.png'))
		self.french.setIcon(iconFrench)
		self.french.setCheckable(True)
		self.french.setChecked(True)

		##################
		#	8- GERMAN	 #
		##################

		self.german = languagesAction.addAction('German', self.german)
		iconGerman = QtGui.QIcon()
		iconGerman.addPixmap(QtGui.QPixmap('Images/Countries/Germany.png'))
		self.german.setIcon(iconGerman)
		self.german.setCheckable(True)

		##################
		#	9- SPANISH	 #
		##################

		self.spanish = languagesAction.addAction('Spanish', self.spanish)
		iconSpanish = QtGui.QIcon()
		iconSpanish.addPixmap(QtGui.QPixmap('Images/Countries/Spain.png'))
		self.spanish.setIcon(iconSpanish)
		self.spanish.setCheckable(True)


		######################################################
		#													 #
		#						FAVORITES	   				 #
		#													 #
		######################################################

		# Here we will take care of the necessaries objects to manage favorites

		##########################
		#	1- LABEL FAVORITE	 #
		##########################

		self.LBL_FAV = QLabel("Favoris :", self)
		self.LBL_FAV.setGeometry(QtCore.QRect(460, 140, 90, 16))
		self.LBL_FAV.setFont(font)

		##############################
		#	2- LIST VIEW FAVORITES	 #
		##############################

		# We create a list View LW_FAV under the previous label, which has to functions connected, one is for when the user click
		# on a word : self.item_click_Correspondence and the other is for when the user double click on a word displayed on this list view
		# item_doubleclick_Fav_Correspondence. those functions will be defined later. 
		self.LW_FAV = QtGui.QListWidget(self)
		self.LW_FAV.setGeometry(QtCore.QRect(460, 160, 151, 320))
		self.LW_FAV.itemClicked.connect(self.item_click_Correspondence)
		self.LW_FAV.itemDoubleClicked.connect(self.item_doubleclick_Fav_Correspondence)

		##########################
		#	3- LABEL EXPLICATIF	 #
		##########################

		# We create an explicative label to inform the user about how the Favourite feature works
		self.LBL_FAV_EXP = QLabel("Double-cliquez pour supprimer un mot de vos favoris", self)
		self.LBL_FAV_EXP.setGeometry(QtCore.QRect(460, 477, 120, 32))
		self.LBL_FAV_EXP.setWordWrap(True)
		self.LBL_FAV_EXP.setFont(fontexp)

		######################################################
		#													 #
		#						ADD WINDOW	   				 #
		#													 #
		######################################################

		# Here we will take care of the objects that are necessary for the Add a word feature.

		##############
		#	1- WORD	 #
		##############

		# We create a label that display 'Mot : ' and a textfield which will contain the word the user want to add
		# This Textfield is linked to a function when the text changes, with the .textChanged.connect command.
		self.LBL_ADD_WORD = QtGui.QLabel('Mot :', self)
		self.LBL_ADD_WORD.setGeometry(QtCore.QRect(10, 140, 85, 16))
		self.LBL_ADD_WORD.setFont(font)
		self.TF_ADD_WORD = QtGui.QLineEdit(self)
		self.TF_ADD_WORD.setGeometry(QtCore.QRect(10, 160, 261, 21))
		self.TF_ADD_WORD.textChanged.connect(self.text_changed_add_Correspondence)

		##############
		#	2- TYPE	 #
		##############

		# We create a label that display 'Type', next to it we add a Combo Box item that contains word types (Feminin noun, masculin noun...)
		# To add the word types we use the .addItem command
		self.LBL_ADD_TYPE = QtGui.QLabel('Type :', self)
		self.LBL_ADD_TYPE.setGeometry(QtCore.QRect(300, 140, 59, 16))
		self.LBL_ADD_TYPE.setFont(font)
		self.CB_ADD_TYPE = QtGui.QComboBox(self)
		self.CB_ADD_TYPE.setGeometry(QtCore.QRect(300, 157, 141, 31))
		self.CB_ADD_TYPE.addItem('N.F')
		self.CB_ADD_TYPE.addItem('N.M')
		self.CB_ADD_TYPE.addItem('V')
		self.CB_ADD_TYPE.addItem('ADV')
		self.CB_ADD_TYPE.addItem('ADJ')
		self.CB_ADD_TYPE.addItem('N.P')

		######################
		#	3- DEFINITION	 #
		######################

		# We create a label that display 'Definition :', next to it we create a Plaint text item that will contain the definition
		# of the word the user want to add.
		self.LBL_ADD_DEFINITION = QtGui.QLabel('Definition :', self)
		self.LBL_ADD_DEFINITION.setGeometry(QtCore.QRect(10, 200, 100, 16))
		self.LBL_ADD_DEFINITION.setFont(font)
		self.TF_ADD_DEFINITION = QtGui.QTextEdit(self)
		self.TF_ADD_DEFINITION.setGeometry(QtCore.QRect(10, 220, 431, 200))

		######################
		#	4- BUTTON OK	 #
		######################

		# We create a label that displays "Ajouter" ans a button OK, to confirm the adding of a word once everything 
		# is filled, the button is linked to the function okAdd with he command .connect
		# the variable ADDEDIT is set to 0 in the constructor, this will be used later to set if the button is for adding or editing a definition
		self.BT_ADD_OK = QtGui.QPushButton('OK', self)
		self.BT_ADD_OK.setFont(font)
		self.BT_ADD_OK.setGeometry(QtCore.QRect(200, 454, 100, 35))
		self.BT_ADD_OK.clicked.connect(self.okAdd)
		self.LBL_ADDEDIT = QLabel("Ajouter :", self)
		self.LBL_ADDEDIT.setGeometry(QtCore.QRect(130, 452, 100, 35))
		self.LBL_ADDEDIT.setFont(font)
		self.ADDEDIT = 0

		##########################
		#	5- NUMBER OF CHAR	 #
		##########################

		# We create a label which displays the count of letters contained in the PLainText item: TF_ADD_DEFINITION
		# We connect the TF_ADD_DEFINITION to the text_changed_add_definition function which will be used for limiting the
		# numbers of caracters in a definition and display the count in the LBL_ADD_COUNT
		self.LBL_ADD_COUNT = QtGui.QLabel('0 / 500 lettres', self)
		self.LBL_ADD_COUNT.setGeometry(QtCore.QRect(300, 200, 150, 16))
		self.LBL_ADD_COUNT.setFont(font)
		self.TF_ADD_DEFINITION.textChanged.connect(self.text_changed_add_definition)
		
		######################################################
		#													 #
		#					SEARCH WINDOW	   				 #
		#													 #
		######################################################

		# Here we take care of the items necessaries to take care of the Search feature

		######################
		#	1- LABEL SEARCH	 #
		######################

		# We create a label that displays 'Recherche : '
		self.LBL_SEARCH_SEARCH = QtGui.QLabel('Recherche :', self)
		self.LBL_SEARCH_SEARCH.setGeometry(QtCore.QRect(10, 140, 85, 16))
		self.LBL_SEARCH_SEARCH.setFont(font)

		##############
		#	2- WORD	 #
		##############

		# We create a text field which will contain the word the user is searching, and we connect it to the function
		# text_changed_search_Correspondence that will be used for analizing this word and display on a list View 
		# the words begining as the word entered by the user.
		self.TF_SEARCH_WORD = QtGui.QLineEdit(self)
		self.TF_SEARCH_WORD.setGeometry(QtCore.QRect(10, 160, 261, 21))
		self.TF_SEARCH_WORD.textChanged.connect(self.text_changed_search_Correspondence)

		##########################
		#	3- LIST DEFINITION	 #
		##########################

		# We create a list view which will contain the words begining like the word the user entered in the previous textfield
		# This list view is connected to two functions, item_click_Correspondence which will display the definition of the word
		# and item_doubleclick which will add word to favorites
		self.LW_SEARCH_DEFINITION = QtGui.QListWidget(self)
		self.LW_SEARCH_DEFINITION.setGeometry(QtCore.QRect(10, 185, 441, 150))
		self.LW_SEARCH_DEFINITION.itemClicked.connect(self.item_click_Correspondence)
		self.LW_SEARCH_DEFINITION.itemDoubleClicked.connect(self.item_doubleclick)
		self.item = ""

		##############################
		#	4- EXPLICATIVE LABEL	 #
		##############################
		#We create a explicative label to explain to the user how to add a word to favourites
		self.LBL_SEARCH_EXP = QtGui.QLabel('Double-cliquez pour ajouter un mot dans vos favoris', self)
		self.LBL_SEARCH_EXP.setGeometry(QtCore.QRect(10, 335, 300, 16))
		self.LBL_SEARCH_EXP.setFont(fontexp)

		##############################
		#	5- LABEL DEFINITION	   	 #
		##############################

		# We create a label definition which will contain the definition of the word you clicked on, by default it displays 'Definition :'
		self.LBL_SEARCH_DEFINITION = QtGui.QLabel('Definition :', self)
		self.LBL_SEARCH_DEFINITION.setGeometry(QtCore.QRect(10, 360, 441, 200))
		self.LBL_SEARCH_DEFINITION.setFont(font)
		self.LBL_SEARCH_DEFINITION.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
		self.LBL_SEARCH_DEFINITION.setWordWrap(True)


		######################################################
		#													 #
		#					INVERT WINDOW	   				 #
		#													 #
		######################################################

		# All the following is for creating objects used in the Invert feature, basically this feature is the same as the
		# Search feature, but inverted, instead of searching word, the user search definition

		##############################
		#	1- LABEL SEARCH	  	 	 #
		##############################

		self.LBL_INVERT_SEARCH = QtGui.QLabel('Recherche Inversee :', self)
		self.LBL_INVERT_SEARCH.setGeometry(QtCore.QRect(10, 140, 175, 16))
		self.LBL_INVERT_SEARCH.setFont(font)

		##############################
		#	2- SEARCH WORD		   	 #
		##############################

		self.TF_INVERT_SEARCH = QtGui.QLineEdit(self)
		self.TF_INVERT_SEARCH.setGeometry(QtCore.QRect(10, 160, 261, 21))
		self.TF_INVERT_SEARCH.textChanged.connect(self.text_changed_invert_Correspondence)

		##############################
		#	3- LIST WORD		   	 #
		##############################

		self.LW_INVERT_WORD = QtGui.QListWidget(self)
		self.LW_INVERT_WORD.setGeometry(QtCore.QRect(10, 185, 441, 150))
		self.LW_INVERT_WORD.itemClicked.connect(self.item_click_invert_Correspondence)
		self.LW_INVERT_WORD.itemDoubleClicked.connect(self.item_doubleclick)

		##############################
		#	4- LABEL DEFINITION	   	 #
		##############################

		self.LBL_INVERT_WORD = QtGui.QLabel('Definition :', self)
		self.LBL_INVERT_WORD.setGeometry(QtCore.QRect(10, 360, 441, 200))
		self.LBL_INVERT_WORD.setFont(font)
		self.LBL_INVERT_WORD.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
		self.LBL_INVERT_WORD.setWordWrap(True)


		######################################################
		#													 #
		#				TOOLBAR FUNCTIONS	   				 #
		#													 #
		######################################################

		# All the following is for creating the toolbar, and link the buttons to the functions they should use.

		##################
		#	1- SEARCH	 #
		##################

		# We create a Search button on the toolbar, with a shortcut, and linked to searchWord function, which is used
		# to show or hide the appropriates items needed for the search feature
		BT_SEARCH = QtGui.QAction(QtGui.QIcon('Images/Functions/Search.png'), 'Search', self)
		BT_SEARCH.setShortcut('Ctrl+T')
		BT_SEARCH.triggered.connect(self.searchWord)
		self.toolbar = self.addToolBar('Search')
		self.toolbar.addAction(BT_SEARCH)

		##############
		#	2- ADD	 #
		##############

		# We create a Add button on the toolbar, with a shortcut, and linked to addWord function, which is used
		# to show or hide the appropriates items needed for the add feature
		BT_ADD = QtGui.QAction(QtGui.QIcon('Images/Functions/Add.png'), 'Add/Modify', self)
		BT_ADD.setShortcut('Ctrl+N')
		BT_ADD.triggered.connect(self.addWord)
		self.toolbar = self.addToolBar('Add/Modify')
		self.toolbar.addAction(BT_ADD)

		##############################
		#	3- INVERTED DICTIONARY	 #
		##############################

		# We create a Invert button on the toolbar, with a shortcut, and linked to invert function, which is used
		# to show or hide the appropriates items needed for the invert feature
		BT_INVERT = QtGui.QAction(QtGui.QIcon('Images/Functions/Invert.png'), 'Invert', self)
		BT_INVERT.setShortcut('Ctrl+I')
		BT_INVERT.triggered.connect(self.invert)
		self.toolbar = self.addToolBar('Invert')
		self.toolbar.addAction(BT_INVERT)

		##################
		#	4- FAVORITE	 #
		##################

		# We create a Favorite button on the toolbar, with a shortcut, and linked to display_Favorite function,
		# which is used for displaying favourites on the appropriate List view
		BT_FAV = QtGui.QAction(QtGui.QIcon('Images/Functions/Fav.png'), 'Favorite', self)
		BT_FAV.setShortcut('Ctrl+L')
		BT_FAV.triggered.connect(self.displayFavorite_Correspondence)
		self.toolbar = self.addToolBar('Favorite')
		self.toolbar.addAction(BT_FAV)

		##################
		#	5- DELETE	 #
		##################

		# We create a Delete button on the toolbar, with a shortcut, and linked to delete function, which is used
		# to delete a word selected from the database
		BT_DELETE = QtGui.QAction(QtGui.QIcon('Images/Functions/Delete.png'), 'Delete', self)
		BT_DELETE.setShortcut('Ctrl+D')
		BT_DELETE.triggered.connect(self.deleteWord_Correspondence)
		self.toolbar = self.addToolBar('Delete')
		self.toolbar.addAction(BT_DELETE)

		##########################
		#	6- FIRST DISPLAY	 #
		##########################

		# We set for all of the variables (labels, textfield...) if they are shown or not on the first display.
		self.LW_SEARCH_DEFINITION.show()
		self.TF_SEARCH_WORD.show()
		self.LBL_SEARCH_DEFINITION.show()
		self.LBL_ADD_WORD.hide()
		self.TF_ADD_WORD.hide()
		self.LBL_ADD_TYPE.hide()
		self.CB_ADD_TYPE.hide()
		self.LBL_ADD_DEFINITION.hide()
		self.TF_ADD_DEFINITION.hide()
		self.BT_ADD_OK.hide()
		self.LBL_ADD_COUNT.hide()
		self.LBL_ADDEDIT.hide()
		self.TF_INVERT_SEARCH.hide()
		self.LW_INVERT_WORD.hide()
		self.LBL_INVERT_WORD.hide()
		self.LBL_INVERT_SEARCH.hide()




		##############################
		#	7- WINDOW PROPERTIES	 #
		##############################

		# We set the window properties, the size, which is not resizable and the title.
		self.setFixedSize(621, 600)
		self.setWindowTitle('PioupiouWord')
		self.show()
		
		
		
		
####################################################################################################################
#																												   #
#													FUNCTIONS													   #
#																												   #
####################################################################################################################

## LET'S DO IT ##

######################################################
#													 #
#						LANGUAGES	   				 #
#													 #
######################################################

		##################
		#	1- ENGLISH	 #
		##################

	# We set, for when the language selected is english the english() function, which will change the text in the labels
	# to their english translation, and check the english language in the menu idem for all the other languages

	def english(self):
		self.LBL_BIENVENUE.setText('Welcome on our dictionary young pioupiou !')
		self.LANGUAGE = 'English'
		self.LBL_SEARCH_SEARCH.setText("Research :")
		self.LBL_FAV.setText("Favorite :")
		self.LBL_SEARCH_DEFINITION.setText("Definition :")
		self.LBL_ADD_WORD.setText("Word :")
		self.LBL_ADD_TYPE.setText("Type :")
		self.LBL_ADD_DEFINITION.setText("Definition :")
		self.LBL_INVERT_SEARCH.setText("Inverted Search :")
		self.LBL_ADDEDIT.setGeometry(QtCore.QRect(150, 452, 100, 35))
		self.LBL_ADDEDIT.setText("Add :")
		self.LBL_FAV_EXP.setText("Double-click to delete a word from your favorites")
		self.LBL_SEARCH_EXP.setText("Double-click to add a word to your favorites")
		self.french.setChecked(False)
		self.english.setChecked(True)
		self.german.setChecked(False)
		self.spanish.setChecked(False)
		self.LBL_FLAG1.setPixmap(QtGui.QPixmap('Images/Countries/England.png'))
		self.LBL_FLAG2.setPixmap(QtGui.QPixmap('Images/Countries/England.png'))
		self.LBL_ADD_COUNT.setText("0/500 characters")
		self.cleanAdd(self)
		self.cleanSearch(self)
		self.cleanInvert(self)
		self.cleanFavorite(self)

		##################
		#	2- FRENCH	 #
		##################

	def french(self):
		self.LBL_BIENVENUE.setText('Bienvenue jeune pipiou dans notre dictionnaire !')
		self.LANGUAGE = 'Francais'
		self.LBL_SEARCH_SEARCH.setText("Recherche :")
		self.LBL_FAV.setText("Favoris :")
		self.LBL_SEARCH_DEFINITION.setText("Definition :")
		self.LBL_ADD_WORD.setText("Mot :")
		self.LBL_ADD_TYPE.setText("Type :")
		self.LBL_ADD_DEFINITION.setText("Definition :")
		self.LBL_INVERT_SEARCH.setText("Recherche Inversée :")
		self.LBL_ADDEDIT.setGeometry(QtCore.QRect(130, 452, 100, 35))
		self.LBL_ADDEDIT.setText("Ajouter :")
		self.LBL_FAV_EXP.setText("Double-cliquez pour supprimer un mot de vos favoris")
		self.LBL_SEARCH_EXP.setText("Double-cliquez pour ajouter un mot dans vos favoris")
		self.french.setChecked(True)
		self.english.setChecked(False)
		self.german.setChecked(False)
		self.spanish.setChecked(False)
		self.LBL_FLAG1.setPixmap(QtGui.QPixmap('Images/Countries/France.png'))
		self.LBL_FLAG2.setPixmap(QtGui.QPixmap('Images/Countries/France.png'))
		self.LBL_ADD_COUNT.setText("0/500 lettres")
		cleanAdd(self)
		cleanSearch(self)
		cleanInvert(self)
		cleanFavorite(self)

		##################
		#	3- GERMAN	 #
		##################

	def german(self):
		self.LBL_BIENVENUE.setText('Willkommen auf unserem Worterbuch junger pioupiou !')
		self.LANGUAGE = 'German'
		self.LBL_SEARCH_SEARCH.setText("Suche :")
		self.LBL_FAV.setText("Favoriten :")
		self.LBL_SEARCH_DEFINITION.setText("Definition :")
		self.LBL_ADD_WORD.setText("Wort :")
		self.LBL_ADD_TYPE.setText("Typ :")
		self.LBL_ADD_DEFINITION.setText("Definition :")
		self.LBL_ADDEDIT.setGeometry(QtCore.QRect(105, 452, 100, 35))
		self.LBL_ADDEDIT.setText("Hinzufugen :")
		self.LBL_INVERT_SEARCH.setText("Ruckwartssuche :")
		self.LBL_FAV_EXP.setText("Doppelklicken Sie auf ein Wort aus Ihren Favoriten loschen")
		self.LBL_SEARCH_EXP.setText("Doppelklicken Sie auf ein Wort zu Ihren Favoriten hinzufugen")
		self.french.setChecked(False)
		self.english.setChecked(False)
		self.german.setChecked(True)
		self.spanish.setChecked(False)
		self.LBL_FLAG1.setPixmap(QtGui.QPixmap('Images/Countries/Germany.png'))
		self.LBL_FLAG2.setPixmap(QtGui.QPixmap('Images/Countries/Germany.png'))
		self.LBL_ADD_COUNT.setText("0/500 buchstaben")
		cleanAdd(self)
		cleanSearch(self)
		cleanInvert(self)
		cleanFavorite(self)

		##################
		#	4- SPANISH	 #
		##################

	def spanish(self):
		self.LBL_BIENVENUE.setText('Bienvenidos a nuestro diccionario joven pioupiou !')
		self.LANGUAGE = 'Spanish'
		self.LBL_SEARCH_SEARCH.setText("Busqueda :")
		self.LBL_FAV.setText("Favoritos :")
		self.LBL_SEARCH_DEFINITION.setText("Definicion :")
		self.LBL_ADD_WORD.setText("Palabra :")
		self.LBL_ADD_TYPE.setText("Tipo :")
		self.LBL_ADD_DEFINITION.setText("Definicion :")
		self.LBL_INVERT_SEARCH.setText("Invertada Busqueda :")
		self.LBL_ADDEDIT.setGeometry(QtCore.QRect(130, 452, 100, 35))
		self.LBL_ADDEDIT.setText("Anadir :")
		self.LBL_FAV_EXP.setText("Haga doble clic para eliminar una palabra de sus favoritos")
		self.LBL_SEARCH_EXP.setText("Haga doble clic para anadir una palabra a sus favoritos")
		self.french.setChecked(False)
		self.english.setChecked(False)
		self.german.setChecked(False)
		self.spanish.setChecked(True)
		self.LBL_FLAG1.setPixmap(QtGui.QPixmap('Images/Countries/Spain.png'))
		self.LBL_FLAG2.setPixmap(QtGui.QPixmap('Images/Countries/Spain.png'))
		self.LBL_INVERT_WORD.setText("Definicion :")
		self.LBL_ADD_COUNT.setText("0/500 letras")
		cleanAdd(self)
		cleanSearch(self)
		cleanInvert(self)
		cleanFavorite(self)

##########################################################
#														 #
#						HIDE AND SHOW	   				 #
#														 #
##########################################################

# For the following functions, we just set the differents objects to visible or not depending on the feature selected by the user.

	##########################
	#	1- BUTTON SEARCH	 #
	##########################

	def searchWord(self):
		self.LW_SEARCH_DEFINITION.show()
		self.TF_SEARCH_WORD.show()
		self.LBL_SEARCH_DEFINITION.show()
		self.LBL_SEARCH_SEARCH.show()
		self.LBL_SEARCH_EXP.show()
		self.LBL_ADD_WORD.hide()
		self.TF_ADD_WORD.hide()
		self.LBL_ADD_TYPE.hide()
		self.CB_ADD_TYPE.hide()
		self.LBL_ADD_DEFINITION.hide()
		self.LBL_ADD_COUNT.hide()
		self.TF_ADD_DEFINITION.hide()
		self.BT_ADD_OK.hide()
		self.LBL_ADDEDIT.hide()
		self.TF_INVERT_SEARCH.hide()
		self.LW_INVERT_WORD.hide()
		self.LBL_INVERT_WORD.hide()
		self.LBL_INVERT_SEARCH.hide()

	######################
	#	2- BUTTON ADD	 #
	######################

	def addWord(self):
		self.LW_SEARCH_DEFINITION.hide()
		self.TF_SEARCH_WORD.hide()
		self.LBL_SEARCH_DEFINITION.hide()
		self.LBL_SEARCH_SEARCH.hide()
		self.LBL_SEARCH_EXP.hide()
		self.LBL_ADD_WORD.show()
		self.TF_ADD_WORD.show()
		self.LBL_ADD_TYPE.show()
		self.CB_ADD_TYPE.show()
		self.LBL_ADD_DEFINITION.show()
		self.TF_ADD_DEFINITION.show()
		self.BT_ADD_OK.show()
		self.LBL_ADD_COUNT.show()
		self.LBL_ADDEDIT.show()
		self.TF_INVERT_SEARCH.hide()
		self.LW_INVERT_WORD.hide()
		self.LBL_INVERT_WORD.hide()
		self.LBL_INVERT_SEARCH.hide()

	##########################
	#	3- BUTTON INVERT	 #
	##########################

	def invert(self):
		self.LW_SEARCH_DEFINITION.hide()
		self.TF_SEARCH_WORD.hide()
		self.LBL_SEARCH_DEFINITION.hide()
		self.LBL_SEARCH_SEARCH.show()
		self.LBL_SEARCH_EXP.show()
		self.LBL_SEARCH_SEARCH.hide()
		self.LBL_ADD_WORD.hide()
		self.TF_ADD_WORD.hide()
		self.LBL_ADD_TYPE.hide()
		self.CB_ADD_TYPE.hide()
		self.LBL_ADD_DEFINITION.hide()
		self.TF_ADD_DEFINITION.hide()
		self.BT_ADD_OK.hide()
		self.LBL_ADD_COUNT.hide()
		self.LBL_ADDEDIT.hide()
		self.TF_INVERT_SEARCH.show()
		self.LW_INVERT_WORD.show()
		self.LBL_INVERT_WORD.show()
		self.LBL_INVERT_SEARCH.show()


#############################################################################
#													 						 #
#						ACCESS TO DATABASE WITH MODEL FILE	   				 #
#													 						 #
##############################################################################

##################################
#								 #
#		SEARCH FUNCTIONS	   	 #
#								 #
##################################

	##################################################
	#	1- DISPLAY WORD BEGINING WITH THE LETTER...	 #
	##################################################

	# This function is called each time something is taped on the textedit for searching a word
	# First we clear the list view results for not display twice or more the result 
	# Then take value of country (global value) and text (taped on the searching) case to use them as arguments.
	# The function text_changed_search is in our model and return an array wich contains our results (words beginning with inputText)
	# With the loop for, we add each row as an item on our list view
	def text_changed_search_Correspondence(self):
		self.LW_SEARCH_DEFINITION.clear()
		self.LBL_SEARCH_DEFINITION.setText("Definition :")
		inputText = self.TF_SEARCH_WORD.text()
		country = str(self.LANGUAGE)
		if inputText == "":
			self.LW_SEARCH_DEFINITION.clear()
			if self.LANGUAGE == 'Francais':
				self.LBL_SEARCH_DEFINITION.setText("Définition :")
			if self.LANGUAGE == 'English':
				self.LBL_SEARCH_DEFINITION.setText("Definition :")
			if self.LANGUAGE == 'Spanish':
				self.LBL_SEARCH_DEFINITION.setText("Definicion :")
			if self.LANGUAGE == 'German':
				self.LBL_SEARCH_DEFINITION.setText("Definition :")
			self.LBL_SEARCH_DEFINITION.setText("Definition :")
		else:
			result = self.model.text_changed_search(country, inputText)
			for row in result:
				self.LW_SEARCH_DEFINITION.addItem("%s" % row)

	######################################################
	#	2- DISPLAY DEFINITION WHEN YOU CLICK ON THE WORD #
	######################################################

	# Once again we take the value of the country using global value self.LANGUAGE
	# item.text() take the value of the item you click on
	# If we want put utf8 char, we have to unicode the word en then encode it in 'utf8'
	# Then we give array the value of the return value of item_click placed in our model taking as argument word and country
	# Depending of the query in the model, the first column(0) of array will represent type and the second(1) the defintion
	# Now we juste display it as the text of our label
	def item_click_Correspondence(self, item):
		inputText = item.text()
		self.item = inputText
		country = str(self.LANGUAGE)
		word = unicode(self.item)
		word.encode('utf8')
		array = self.model.item_click(word, country)
		type = array[0]
		definition = array[1]
		definition = definition.replace("()","'")
		self.LBL_SEARCH_DEFINITION.setText("Definition : " + type + ".  " + definition)
		
		
		
		
##############################
#							 #
#		ADD FUNCTIONS	   	 #
#							 #
##############################

	#########################################################
	#	1- KNOW IF A WORD IS ALREADY ON OUR DATABASE OR NOT #
	#########################################################

	# This function is called each time you change the word you want to add
	# Each time the textedit where you will write your definition is first clear in order to clear 
	# the definition of a word that you changed
	# Definition will take the value of return value of text_changed_add placed on our model taking 
	# the arguments country and inputText.
	# If definition is None (no return value = no def in our database), then global value ADDETIT 
	# take value 0 (for adding) and our label will be "add' depending of the language
	# Else ADDEDIT take value 1 (for edit). We have to encode the return value as latin-1 for accent
	# because definition is stocked in database with ascii char
	# and the we have to replace "()" by " ' " because we can't use " ' ' in sql request, we decided
	# to replace each of this " ' ' by "()" before using our database and replace in the other way
	#  "()" by " ' " for displaying

	def text_changed_add_Correspondence(self):
		self.TF_ADD_DEFINITION.clear()
		inputText = self.TF_ADD_WORD.text()
		country = str(self.LANGUAGE)
		definition = ""
		if inputText == "":
			self.TF_ADD_DEFINITION.clear()
		else:
			definition = self.model.text_changed_add(country, inputText)
			if definition == None:
				self.ADDEDIT = 0
				if self.LANGUAGE == "English":
					self.LBL_ADDEDIT.setText("Add :")
				elif self.LANGUAGE == "German":
					self.LBL_ADDEDIT.setText("Hinzufugen :")
				elif self.LANGUAGE == "Francais":
					self.LBL_ADDEDIT.setText("Ajouter :")
				elif self.LANGUAGE == "Spanish":
					self.LBL_ADDEDIT.setText("Anadir :")
			else:
				self.ADDEDIT = 1
				definition = ''.join(definition).encode('latin-1')
				definition = definition.replace("()", "'")
				self.TF_ADD_DEFINITION.setText("%s" % definition)
				if self.LANGUAGE == "English":
					self.LBL_ADDEDIT.setText("Edit :")
				elif self.LANGUAGE == "German":
					self.LBL_ADDEDIT.setText("Bearbeiten :")
				elif self.LANGUAGE == "Francais":
					self.LBL_ADDEDIT.setText("Editer :")
				elif self.LANGUAGE == "Spanish":
					self.LBL_ADDEDIT.setText("Editar :")

	##############################
	#	2- NEW WORD IN DATABASE	 #
	##############################

	# Once again we take value of country (global value LANGUAGE), word and definition put in our text edit. This time we take
	#the value of our combobox too.
	# We use unicode and encode in order to be able to use utf8 char
	# Then as it explains on textchanged_add, we replace " ' " by "()" because query do not accept " ' "
	# If definition is empty, we show an alert message
	# And we delete white spaces in word eg "Hos pital    " -> "Hospital"
	# Depending of the value of ADDEDIT, we insert all our datas in database (add)
	# or update it (edit)

	def okAdd(self):
		conn = sqlite3.connect('Dictionary.db')
		c = conn.cursor()
		word = unicode(self.TF_ADD_WORD.text())
		definition = unicode(self.TF_ADD_DEFINITION.toPlainText())
		word.encode('utf8')
		definition.encode('utf8')
		definition = definition.replace("'", "()")
		word = word.replace(" ", "")
		type = str(self.CB_ADD_TYPE.currentText())
		country = self.LANGUAGE
		if definition == "":
			self.msg = QMessageBox()
			self.msg.setIcon(QMessageBox.Warning)
			self.msg.setText("Definition is empty")
			self.msg.setWindowTitle("Alert !")
			self.msg.setStandardButtons(QMessageBox.Ok)
			self.msg.setDefaultButton(QMessageBox.Ok)
			self.msg.show()
		else:
			if self.ADDEDIT == 0:  
				c.execute(''' INSERT INTO Correspondence (Word, Definition, Type, Country) VALUES(?,?,?,?) ''', (word, definition, type, country))
				print(word + " added");
			else:
				c.execute(" UPDATE Correspondence SET Definition = '%s', Type = '%s' WHERE Word = '%s' " % (definition, type, word))
				print(word + " modified");
		conn.commit()
		conn.close()

	##############################
	#	3- LIMITE NUMBER OF CHAR #
	##############################

	# Use for block number of char put in your definition (cause if you want to display it well it can't be to long)
	# The function is called each time definition change and count take value of len of our definition 
	# Then we just enable or not our button edit/add and set color of our label depending of the value of count 
	# (less/more than 500)
	def text_changed_add_definition(self):
		count = len(self.TF_ADD_DEFINITION.toPlainText())
		if self.LANGUAGE == 'Francais':
			self.LBL_ADD_COUNT.setText(str(count)+'/500 lettres')
		if self.LANGUAGE == 'English':
			self.LBL_ADD_COUNT.setText(str(count)+'/500 characters')
		if self.LANGUAGE == 'Spanish':
			self.LBL_ADD_COUNT.setText(str(count)+'/500 letras')
		if self.LANGUAGE == 'German':
			self.LBL_ADD_COUNT.setText(str(count)+'/500 buchstaben')
		if count <= 500:
			self.BT_ADD_OK.setEnabled(True)
			self.LBL_ADD_COUNT.setStyleSheet('color: black')
		else:
			self.BT_ADD_OK.setEnabled(False)
			self.LBL_ADD_COUNT.setStyleSheet('color: red')
			
					
			
					
##################################
#								 #
#		INVERT FUNCTIONS	   	 #
#								 #
##################################


	###########################################################################
	#	1- DISPLAY WORDS THAT CONTAINS IN THEIR DEFINITION THE WORD YOU TAPED #
	###########################################################################

	# Invert functions are just working as search function but we inverse return value 
	# Only the query is different but it is on the model file. 
	def text_changed_invert_Correspondence(self):
		self.LW_INVERT_WORD.clear()
		self.LBL_INVERT_WORD.setText("Definition :")
		inputText = self.TF_INVERT_SEARCH.text()
		country = str(self.LANGUAGE)
		if inputText == "":
			self.LW_INVERT_WORD.clear()
			self.LBL_INVERT_WORD.setText("Definition :")
		else:
			result = self.model.text_changed_invert(country, inputText)
			for row in result:
				self.LW_INVERT_WORD.addItem("%s" % row)

	#########################################################
	#	2- DISPLAY DEFINITION OF THE WORD YOU CLICKED ON	#
	#########################################################

	def item_click_invert_Correspondence(self, item):
		inputText = item.text()
		self.item = inputText
		country = str(self.LANGUAGE)
		word = unicode(self.item)
		word.encode('utf8')
		print (word)
		#print (word.encode('utf-8'));
		array = self.model.item_click_invert(word, country)
		type = array[0]
		definition = array[1]
		definition = definition.replace("()","'")
		self.LBL_INVERT_WORD.setText("Definition : " + type + ".  " + definition);
		
		
		
		
##################################
#								 #
#		DELETE FUNCTIONS	   	 #
#								 #
##################################

	####################
	#	1- DELETE WORD #
	####################

	def deleteWord_Correspondence(self):
	# First we give vardelete an integer value corresponding of the row you selected in your search list view
	# Then you take off the item selected using function takeItem of the row vardelete
	# As the rest of the functions, delete word call function in model using arguments
	# This time nothing is returned cause the model function is just deleting a word from database. 
		vardelete = self.LW_SEARCH_DEFINITION.currentRow()
		self.LW_SEARCH_DEFINITION.takeItem(vardelete)
		inputText = self.item
		inputText = unicode(inputText)
		inputText.encode('utf8')
		country = str(self.LANGUAGE)
		self.model.deleteWord(inputText, country)
		
		
		
		
##################################
#								 #
#		FAVORITE FUNCTIONS	   	 #
#								 #
##################################

	########################################
	#	1- DISPLAY ALL YOUR FAVORITE WORDS #
	########################################

	# Works as search, we clear list view and then adding item with loop for using a tab thanks to return value
	def displayFavorite_Correspondence(self):
		self.LW_FAV.clear()
		array = self.model.displayFavorite(self.LANGUAGE)
		for r in array:
			self.LW_FAV.addItem("%s" % r)

	##########################################
	#	2- DELETE A WORD FROM YOUR FAVORITES #
	##########################################

	# Same thing, no return value because just set favorite to 0
	def item_doubleclick_Fav_Correspondence(self, item):
		vardelete = self.LW_FAV.currentRow()
		self.LW_FAV.takeItem(vardelete)
		inputText = item.text()
		inputText = unicode(inputText)
		inputText.encode('utf8')
		#self.item = inputText
		country = str(self.LANGUAGE)
		self.model.item_doubleclick_fav(inputText, country)

	##########################
	#	3- ADD TO FAVORITES	 #
	##########################

	# Same way, we unicode and encode in order to have utf8 char
	# Then we give valu of favorite 1 (true) where word = selected word using item.
	def item_doubleclick(self, item):
		conn = sqlite3.connect('Dictionary.db')
		c = conn.cursor()
		inputText = item.text()
		inputText = unicode(inputText)
		inputText.encode('utf8')
		c.execute(" SELECT COUNT(*) FROM Correspondence WHERE Word = '%s' AND Favorite = 1 " % inputText)
		for row in c:
			number = row[0]
		if (number == 0):
			c.execute(" UPDATE Correspondence SET Favorite = 1 WHERE Word = '%s' " % inputText)
			c.execute(" SELECT Word FROM Correspondence WHERE Favorite = 1 AND Word = '%s' " % inputText)
			result = c.fetchone()
			favoris = unicode(result[0])
			self.LW_FAV.addItem(favoris)
			print(inputText + " added in your favorites");
		else:
			self.msg = QMessageBox()
			self.msg.setIcon(QMessageBox.Warning)
			self.msg.setText("This word is already in your favorites")
			self.msg.setWindowTitle("Alert !")
			self.msg.setStandardButtons(QMessageBox.Ok)
			self.msg.setDefaultButton(QMessageBox.Ok)
			self.msg.show()
		conn.commit()
		conn.close()

		
		
		
##############################################################################
#													 						 #
#									HELP FILE				   				 #
#													 						 #
##############################################################################
	
	def helpme(self):
	# Call pioupiouWord.pdf file depending of OS
		file = 'PioupiouWord.pdf'
		if sys.platform == 'linux2':
			subprocess.call(["xdg-open", file])
		if sys.platform == 'win32' or sys.platform == 'win64':
			os.startfile(file)
		else:
			subprocess.Popen("open PioupiouWord.pdf", shell=True)
			
			
			
##################################################################################
#														 						 #
#									CLEAN FUNCTIONS	 			  				 #
#													 							 #
##################################################################################

	#def cleanSearch(self):
	#	self.TF_SEARCH_WORD.setText('')
	#	self.LW_SEARCH_DEFINITION.clear()
	#	self.LBL_SEARCH_DEFINITION.setText('')
	#def cleanAdd(self):
	#	self.TF_ADD_WORD.setText('')
	#	self.TF_ADD_DEFINITION.plainText('')
	#def cleanInvert(self):
	#	self.TF_INVERT_SEARCH.setText('')
	#	self.LW_INVERT_WORD.clear()
	#	self.LBL_INVERT_WORD.setText('')
	#def cleanFavorite(self):
	#	self.LW_FAV.clear()	

#########################################################################################################################


##############################################################################
#													 						 #
#						FUNCTIONS FOR DEVELOPPER			   				 #
#													 						 #
##############################################################################


	def createDatabase(self):
		conn = sqlite3.connect('Dictionary.db')
		c = conn.cursor()
		c.execute('''CREATE TABLE Correspondence(Word TEXT, Type TEXT, Definition TEXT, Country TEXT, Favorite bool)''')
		conn.commit()
		conn.close()
	## Correspondence ##	
	 # Word (text)    #	
	 # Type (text)    #
	 #Definition(text)#
	 # Country (text) #
	 # Favorite (bool)#

	def deleteData(self):
		conn = sqlite3.connect('Dictionary.db')
		c = conn.cursor()
		c.execute(" DELETE FROM Correspondence ")
		print("No more Data");
		conn.commit()
		conn.close()


#########################################################################################################################




## MAIN PREMIERE FONCTION APPELLEE LORS DE L EXECUTION DU PROGRAMME ##
def main():
	app = QtGui.QApplication(sys.argv)
	model = Model() #Call MODEL
	dictionary = ViewController(model)
	#dictionary.deleteData()
    #dictionary.createDatabase()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()