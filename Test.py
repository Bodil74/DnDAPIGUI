if __name__ == '__main__':
	print('Run GUI.py')
'''
import json
import requests

def load_data(address):
	req = requests.get(address)
	load_data = json.loads(req.text)

	return load_data

def search_for(data, search_term):
	for i in data:
		for j in range(len(i['results'])):
			print(i['results'][j]['name'])
			if i['results'][j]['name'].lower() == search_term.lower():
				return i['results'][j]

	return 'Nothing'


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

spell_data = SpellData()

spell_data.load_spell_data()
search_for(spell_data.data, 'fffff')
'''