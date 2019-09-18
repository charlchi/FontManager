import sublime
import sublime_plugin
import ctypes
import platform

from .fontmanager.WinFont import (get_windows_fonts)

print(0 << 4)
print(1 << 4)
print(2 << 4)
print(3 << 4)
print(4 << 4)
print(5 << 4)


class FontManagerCommand(sublime_plugin.WindowCommand):
	
	PREFS_FILE = 'Preferences.sublime-settings'
	
	prefs = None
	fonts = None
	current = None

	def run(self):

		self.prefs = sublime.load_settings(self.PREFS_FILE)
		if platform.system() == "Windows":
			self.fonts = get_windows_fonts()
		else:
			self.fonts = []

		self.current = -1
		initial_highlight = -1
		for i, v in enumerate(self.fonts):
			if v == self.prefs.get("font_face"):
				initial_highlight = i
				self.current = i

		self.window.show_quick_panel(
			self.fonts,
			self.on_done,
			sublime.KEEP_OPEN_ON_FOCUS_LOST | sublime.MONOSPACE_FONT,
			initial_highlight,
			self.on_highlighted
		)

	def on_done(self, index):
		saveIndex = index if index > -1 else self.current
		if index > -1:
			self.prefs.set("font_face", self.fonts[saveIndex])
		print(index)

	def on_highlighted(self, index):
		if index > -1:
			self.prefs.set("font_face", self.fonts[index])
		print(index)
