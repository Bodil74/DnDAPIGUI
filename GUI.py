import tkinter as tk
import time
import os
import DnD


class UI_Main(tk.Tk):
	def __init__(self):
		super().__init__()
		
		self.winfo_toplevel().title('DnD')
		self.childWindows = []

		# Setup

		self._canvas = tk.Canvas(self, width = 200, height = 200)
		self._canvas.pack()
		self._main_frame = tk.Frame(self._canvas, bd = 5)
		self._main_frame.place(relx = 0.05, rely = 0.05, relwidth = 0.9, relheight = 0.9, anchor = 'nw')

	# Visuals

	def _make_buttons(self):
		self._select_button = tk.Button(self._main_frame, text = 'Select', command = lambda : self._make_character_window())
		self._select_button.place(relx = 0.35, rely = 0.12, relwidth = 0.3, relheight = 0.1)

		self._spells_button = tk.Button(self._main_frame, text = 'Spells', command = lambda : self._make_spell_window())
		self._spells_button.place(relx = 0, rely = 0.35, relwidth = 0.5, relheight = 0.3)

		self._magic_items_button = tk.Button(self._main_frame, text = 'Magic Items', command = lambda : self._make_magic_item_window())
		self._magic_items_button.place(relx = 0.5, rely = 0.35, relwidth = 0.5, relheight = 0.3)

		self._sections_button = tk.Button(self._main_frame, text = 'Sections', command = lambda : self._make_section_window())
		self._sections_button.place(relx = 0, rely = 0.65, relwidth = 0.5, relheight = 0.3)

	def _make_menus(self):
		self._pick_class_var = tk.StringVar()
		self._pick_class_var.set('Pick A Class')
		self._option_menu = tk.OptionMenu(self._main_frame, self._pick_class_var, *DnD.class_data.get_classes())
		self._option_menu.place(relwidth = 0.65, relheight = 0.12, relx = 0.175, rely = 0)

	def _make_character_window(self):
		try:
			self.childWindows.append(UI_Character_Menu(self._pick_class_var.get()))
			self.childWindows[-1].start()

		except:
			pass

	def _make_spell_window(self):
		if not DnD.spell_data.loaded:
			DnD.spell_data.load_spell_data()

		self.childWindows.append(UI_Spell_Menu())
		self.childWindows[-1].start()

	def _make_magic_item_window(self):
		if not DnD.magic_item_data.loaded:
			DnD.magic_item_data.load_magic_item_data()

		self.childWindows.append(UI_Magic_Item_Menu())
		self.childWindows[-1].start()

	def _make_section_window(self):
		if not DnD.section_data.loaded:
			DnD.section_data.load_section_data()

		self.childWindows.append(UI_Section_Menu())
		self.childWindows[-1].start()
		
	def main(self):
		self._make_buttons()
		self._make_menus()
		self.mainloop()


class UI_Character_Menu(tk.Toplevel):
	def __init__(self, character):
		super().__init__()

		self.character = character
		try:
			self.image = DnD.load_image(self.character)
		except:
			self.image = 'not loaded'
		self.fonts = []

		# Setup

		self._canvas = tk.Canvas(self, width = 1200, height = 700)
		self._canvas.pack()
		self._main_frame = tk.Frame(self._canvas, bd = 5)
		self._main_frame.place(relwidth = 1, relheight = 1, anchor = 'nw')
		self.winfo_toplevel().title('Class Info')

	def _change_text(self, *args, title = False):
		self._text.delete('1.0', tk.END)
		self._text.insert(tk.END, DnD.class_data.get_class_data(DnD.class_data.class_dict[self.character], args, title = title))

	# Visuals

	def _make_text_box(self):
		self._scrollbar = tk.Scrollbar(self._main_frame)
		self._scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

		self._text = tk.Text(self._main_frame, wrap = tk.WORD, width = 100)
		self._text.place(relx = 0.3, relwidth = 0.685, relheight = 1)
		self._change_text('desc')

		self._scrollbar.config(command = self._text.yview)

	def _add_image(self):
		self._class_image_label = tk.Label(self._main_frame)
		self._class_image_label.place(relx = 0.03, rely = 0.03)
		try:
			self._class_image_label.image = self.image
			self._class_image_label.config(image = self._class_image_label.image)
		except:
			self._class_image_label.config(text = 'Image didn\'t Load')

	def _make_buttons(self):
		self._level_table_button = tk.Button(self._main_frame, text = 'Level Table', command = lambda : self._change_text('table'))
		self._level_table_button.place(relx = 0, rely = 0.7, relwidth = 0.1, relheight = 0.07)

		self._desc_button = tk.Button(self._main_frame, text = 'Description', command = lambda : self._change_text('desc'))
		self._desc_button.place(relx = 0, rely = 0.77, relwidth = 0.1, relheight = 0.07)

		self._level_one_button = tk.Button(self._main_frame, text = 'Level One', command = lambda : self._change_text('hit_dice', 'hp_at_1st_level', 'hp_at_higher_levels', 'prof_armor', 'prof_weapons', 'prof_tools', 'prof_saving_throws', 'prof_skills', title = True))
		self._level_one_button.place(relx = 0, rely = 0.84, relwidth = 0.1, relheight = 0.07)

	def start(self):
		self._make_text_box()
		self._make_buttons()
		self._add_image()


class UI_Spell_Menu(tk.Toplevel):
	def __init__(self):
		super().__init__()

		# Setup

		self._canvas = tk.Canvas(self, width = 500, height = 410)
		self._canvas.pack()
		self._main_frame = tk.Frame(self._canvas, bd = 5)
		self._main_frame.place(relwidth = 1, relheight = 1, anchor = 'nw')
		self.winfo_toplevel().title('Spell Info')

	def _change_text(self, spell):
		self._text.delete('1.0', tk.END)
		self._text.insert(tk.END, DnD.spell_data.get_spell_data('name', 'desc', 'level', 'duration', 'casting_time', 'range', 'dnd_class', 'school', 'components', 'material', 'ritual', spell = spell))

	# Visuals

	def _make_buttons(self):
		self._enter_button = tk.Button(self._main_frame, text = 'Search', command = lambda : self._change_text(DnD.search_for(DnD.spell_data.data, self._text_entry.get())))
		self._enter_button.place(relx = 0.82, rely = 0, relwidth = 0.16, relheight = 0.05)

	def _make_text_box(self):
		self._text = tk.Text(self._main_frame, wrap = tk.WORD, width = 100)
		self._text.place(relx = 0, rely = 0.055, relwidth = 1, relheight = 0.95, anchor = 'nw')
		self._change_text('random')

	def _make_search_bar(self):
		self._text_entry = tk.Entry(self._main_frame)
		self._text_entry.place(relx = 0, rely = 0, relwidth = 0.8, relheight = 0.05)

	def start(self):
		self._make_buttons()
		self._make_text_box()
		self._make_search_bar()


class UI_Magic_Item_Menu(tk.Toplevel):
	def __init__(self):
		super().__init__()

		# Setup

		self._canvas = tk.Canvas(self, width = 500, height = 410)
		self._canvas.pack()
		self._main_frame = tk.Frame(self._canvas, bd = 5)
		self._main_frame.place(relwidth = 1, relheight = 1)
		self.winfo_toplevel().title('Magic Item Info')

	def _change_text(self, magic_item):
		self._text.delete('1.0', tk.END)
		self._text.insert(tk.END, DnD.magic_item_data.get_magic_item_data('name', 'type', 'rarity', 'desc', 'requires_attunement', magic_item = magic_item))

	# Visuals

	def _make_buttons(self):
		self._enter_button = tk.Button(self._main_frame, text = 'Search', command = lambda : self._change_text(DnD.search_for(DnD.magic_item_data.data, self._text_entry.get())))
		self._enter_button.place(relx = 0.82, rely = 0, relwidth = 0.16, relheight = 0.05)

	def _make_text_box(self):
		self._text = tk.Text(self._main_frame, wrap = tk.WORD, width = 100)
		self._text.place(relx = 0, rely = 0.055, relwidth = 1, relheight = 0.95, anchor = 'nw')
		self._change_text('random')

	def _make_search_bar(self):
		self._text_entry = tk.Entry(self._main_frame)
		self._text_entry.place(relx = 0, rely = 0, relwidth = 0.8, relheight = 0.05)

	def start(self):
		self._make_buttons()
		self._make_text_box()
		self._make_search_bar()


class UI_Section_Menu(tk.Toplevel):
	def __init__(self):
		super().__init__()

		# Setup

		self._canvas = tk.Canvas(self, width = 550, height = 560)
		self._canvas.pack()
		self._main_frame = tk.Frame(self._canvas, bd = 5)
		self._main_frame.place(relwidth = 1, relheight = 1)
		self.winfo_toplevel().title('Section Info')

	def _change_text(self):
		self._text.delete('1.0', tk.END)
		self._text.insert(tk.END, DnD.section_data.get_section_data(self._pick_section_var.get()))

	# Visuals

	def _make_buttons(self):
		self._select_button = tk.Button(self._main_frame, text = 'Select', command = lambda : self._change_text())
		self._select_button.place(relx = 0.8, rely = 0, relwidth = 0.2, relheight = 0.05)

	def _make_text_box(self):
		self._text = tk.Text(self._main_frame, wrap = tk.WORD, width = 100)
		self._text.place(relx = 0, rely = 0.06, relwidth = 1, relheight = 0.95)
		self._change_text()

	def _make_menus(self):
		self._pick_section_var = tk.StringVar()
		self._pick_section_var.set('Pick A Section')
		self._option_menu = tk.OptionMenu(self._main_frame, self._pick_section_var, *DnD.section_data.get_sections())
		self._option_menu.place(relwidth = 0.8, relheight = 0.055, relx = 0, rely = 0)

	def start(self):
		self._make_menus()
		self._make_buttons()
		self._make_text_box()

################################ Startup ###############################

if __name__ == '__main__':
	if not DnD.class_data.loaded:
			DnD.class_data.load_class_data()

	UI = UI_Main()
	UI.main()
