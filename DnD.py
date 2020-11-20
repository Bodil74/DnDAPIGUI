import json
import requests
import random
import tkinter as tk
import PIL
from PIL import ImageTk, Image
import os
import io


if __name__ == '__main__':
	print('Run the GUI.py file')


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

######################### Available links #############################
'''
spells/ 7 pages
monsters/ 22 pages
documents/
backgrounds/
planes/
sections/ 1 page
feats/
conditions/
races/
classes/ 1 page
magicitems/ 5 pages
weapons/
search/
'''

def load_image(character):
	loaded_image = Image.open(f'{os.getcwd()}\\images\\Class Icon - {character}.png')
	loaded_image = loaded_image.resize((300, 300), Image.ANTIALIAS)

	final_image = ImageTk.PhotoImage(loaded_image)

	return final_image

def load_data(address):
	req = requests.get(address)
	load_data = json.loads(req.text)

	return load_data

def search_for(data, search_term):
	for i in data:
		for j in range(len(i['results'])):
			if i['results'][j]['name'].lower() == search_term.lower():
				return i['results'][j]

	return 'Not Found'

############################## Class Data ###############################

class ClassData():
	def __init__(self):
		self.loaded = False
		self.class_dict = {}

	def load_class_data(self):
		self.loaded = True
		self.data = load_data('https://api.open5e.com/classes/?format=json')

		for i in range(len(self.data['results'])):
			self.class_dict[self.data['results'][i]['name']] = i

	def get_classes(self):
		_list = []

		for i in range(len(self.data['results'])):
			_list.append(self.data['results'][i]['name'])
		
		return _list

	def get_class_data(self, character, info, title):
		output = ''

		if not title:
			for i in info:
				output = output + self.data['results'][character][i]

		else:
			for i in info:
				output = output + i.replace('_', ' ').title() + ' : ' + self.data['results'][character][i] + '\n\n'

		return output

############################# Spell Data #############################

class SpellData():
	def __init__(self):
		self.loaded = False

	def load_spell_data(self):
		self.loaded = True

		self.data = []

		for i in range(7):
			self.data.append(load_data(f'https://api.open5e.com/spells/?format=json&page={i + 1}'))

	def get_spell_data(self, *args, spell):
		output = ''

		if spell == 'random':
			self.x = random.randint(0, len(self.data) - 1)
			random_spell = self.data[self.x]['results'][random.randint(0, len(self.data[self.x]['results']) - 1)]
			for i in args:
				try:
					output = output + i.replace('_', ' ').title() + ' : ' + random_spell[i] + '\n\n'

				except:
					output = output + i.replace('_', ' ').title() + ' : ' + 'N/A' + '\n\n'
					continue

		elif spell != 'Not Found':
			for i in args:
				output = output + i.replace('_', ' ').title() + ' : ' + spell[i] + '\n\n'

		else:
			return self.get_spell_data('name', 'desc', 'level', 'duration', 'casting_time', 'range', 'dnd_class', 'school', 'components', 'material', 'ritual', spell = 'random')
			print('Not Found')

		return output

############################ Magic Item Data ##############################

class MagicItemData():
	def __init__(self):
		self.loaded = False

	def load_magic_item_data(self):
		self.loaded = True

		self.data = []

		for i in range(5):
			self.data.append(load_data(f'https://api.open5e.com/magicitems/?format=json&page={i + 1}'))

	def get_magic_item_data(self, *args, magic_item):
		output = ''

		if magic_item == 'random':
			self.x = random.randint(0, len(self.data) - 1)
			random_magic_item = self.data[self.x]['results'][random.randint(0, len(self.data[self.x]['results']) - 1)]
			for i in args:
				try:
					output = output + i.replace('_', ' ').title() + ' : ' + random_magic_item[i] + '\n\n'

				except:
					output = output + i.replace('_', ' ').title() + ' : ' + 'N/A' + '\n\n'
 
		elif magic_item != 'Not Found':
			for i in args:
				output = output + i.replace('_', ' ').title() + ' : ' + magic_item[i] + '\n\n'
		
		else:
			return self.get_magic_item_data('name', 'type', 'rarity', 'desc', 'requires_attunement', magic_item = 'random')
			print('Not Found')

		return output

############################ Sections Data ##############################

class SectionData():
	def __init__(self):
		self.loaded = False
		self.section_dict = {'Pick A Section' : random.randint(0, 26)}

	def load_section_data(self):
		self.loaded = True
		self.data = load_data('https://api.open5e.com/sections/?format=json')

		for i in range(len(self.data['results'])):
			self.section_dict[self.data['results'][i]['name']] = i

	def get_section_data(self, section):
		return self.data['results'][self.section_dict[section]]['desc']

	def get_sections(self):
		_list = []

		for i in range(len(self.data['results'])):
			_list.append(self.data['results'][i]['name'])

		return _list

class_data = ClassData()
spell_data = SpellData()
magic_item_data = MagicItemData()
section_data = SectionData()
