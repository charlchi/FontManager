
import ctypes
from ctypes import *

xlib = cdll.LoadLibrary('libX11.so')

def get_fonts():
	XOpenDisplay = xlib.XOpenDisplay
	XOpenDisplay.argtypes = [c_char_p]
	XOpenDisplay.restype = c_void_p
	display = XOpenDisplay(b"")
	
	XListFonts = xlib.XListFonts
	XListFonts.argtypes = [c_void_p, c_char_p, c_int, POINTER(c_int)]
	XListFonts.restype = POINTER(c_char * 0)
	
	ret_res = c_int(0)
	
	fontList = XListFonts(
		display,
		b'*',
		0,
		ctypes.byref(ret_res)
	)
	return fontList
