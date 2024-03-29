import sublime
import sublime_plugin
import ctypes
import platform

HOST_OS = platform.system()

if HOST_OS == "Windows":
	from .fontmanager.WinFont import (get_fonts)
else:
	from .fontmanager.UnixFont import (get_fonts)

class FontManagerCommand(sublime_plugin.WindowCommand):
	
	PREFS_FILE = 'Preferences.sublime-settings'
	
	prefs = None
	fonts = None
	current = None

	def run(self):

		self.prefs = sublime.load_settings(self.PREFS_FILE)
		self.fonts = get_fonts()

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
