# -*- coding: utf-8 -*-


import os, sys
import sqlite3

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QCoreApplication, Qt
from PyQt4.QtGui import QListWidget, QListWidgetItem, QApplication
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Model():

	##	FAVORITES	##
# DISPLAY #
	def displayFavorite(self, country):
	# Return an array 'arr' of all words where favorite = 1
	# result take all results and they are stocked in a tab arr with a loop foor that is returned after connection has been closed.
		conn = sqlite3.connect('Dictionary.db')
		c = conn.cursor()
		c.execute(" SELECT Word FROM Correspondence WHERE Favorite = 1 AND Country = '%s' " % country)
		result = c.fetchall()
		arr = []
		for row in result:
			arr.append(row)
		print ("Favorite diplayed");
		conn.commit()
		conn.close()
		return arr
# DELETE FROM FAV #
	# Just set favorite = 0 (false) without delete the word with command delete
	def item_doubleclick_fav(self, inputText, country):	
		conn = sqlite3.connect('Dictionary.db')
		c = conn.cursor()
		c.execute(" UPDATE Correspondence SET Favorite = 0 WHERE Word = '%s' "  % (inputText))
		favoris = unicode(inputText)
		print (inputText + " deleted from favorites.");
		conn.commit()
		conn.close()
		self.displayFavorite(country)
		
		
		
		
		
	##	FUNCTION ADD	##	
# TEXT CHANGED #
	# Return one result (definition of a word where Country = country)
	def text_changed_add(self, country, inputText):
		conn = sqlite3.connect('Dictionary.db')
		c = conn.cursor()
		c.execute(" SELECT Definition FROM Correspondence WHERE Word = '%s' AND Country = '%s' " %(inputText, country))
		result = c.fetchone()
		definition = result
		conn.commit()
		conn.close()
		return definition	
		
		

		
		
	##	FUNCTION SEARCH	##
# TEXT CHANGED #
	def text_changed_search(self, country, inputText):
		# Return all words in an array 'arr' that begin with inputText argument thanks to LIKE '%%s%'
		conn = sqlite3.connect('Dictionary.db')
		c = conn.cursor()
		c.execute(" SELECT Word FROM Correspondence WHERE Word Like '%s%%' AND Country = '%s' ORDER BY Word " %(inputText, country))
		result = c.fetchall()
		arr = []
		for row in result:
			arr.append(row)
		conn.commit()
		conn.close()
		return arr
# CLICK #
	def item_click(self, inputText, country):
	# Return one result for query (fetchone()) but stocked in an array cause two row are asked (Type and Definition)
	# Return the array. Do not forget the unicode if you want use utf8 
		conn = sqlite3.connect('Dictionary.db')
		c = conn.cursor()
		inputText = unicode(inputText)
		c.execute(''' SELECT Type, Definition FROM Correspondence WHERE Word = ? AND Country = ? ''', (inputText, country))
		result = c.fetchone()
		type = str(result[0])
		definition = unicode(result[1])
		array = []
		array.append(type)
		array.append(definition) 
		conn.commit()
		conn.close()
		return array





	##	FUNCTION INVERT	##
# TEXT CHANGED #
	# Same than search
	def text_changed_invert(self, country, inputText):	
		conn = sqlite3.connect('Dictionary.db')
		c = conn.cursor()
		inputText = unicode(inputText)
		c.execute("SELECT Word FROM Correspondence WHERE Definition Like '%%%s%%' AND Country = '%s' ORDER BY Word " %(inputText, country))
		result = c.fetchall()
		arr = []
		for row in result:
			arr.append(row)
		conn.commit()
		conn.close()
		return arr	
# CLICK #
	def item_click_invert(self, inputText, country):
		conn = sqlite3.connect('Dictionary.db')
		c = conn.cursor()
		inputText = unicode(inputText)
		c.execute(''' SELECT Type, Definition FROM Correspondence WHERE Word = ? AND Country = ? ''', (inputText, country))
		result = c.fetchone()
		type = str(result[0])
		definition = unicode(result[1])
		array = []
		array.append(type)
		array.append(definition) 
		conn.commit()
		conn.close()
		return array
			
		
		
		
		
	##	DELETE WORD	##
	# Delete from database, cannot be refund after
	def deleteWord(self, inputText, country):
		conn = sqlite3.connect('Dictionary.db')
		c = conn.cursor()
		c.execute(''' DELETE FROM Correspondence WHERE Word = ? AND Country = ? ''', (inputText, country))
		print(inputText + " deleted");
		conn.commit()
		conn.close()
			
