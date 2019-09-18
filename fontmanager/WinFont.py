
import ctypes
from ctypes import *
from ctypes.wintypes import *

# ctypes doesn't import constants, from wingdi.h
DEFAULT_PITCH	= 0
FIXED_PITCH		= 1
VARIABLE_PITCH	= 2
FF_DONTCARE  	= (0<<4)  # Don't care or don't know.
FF_ROMAN     	= (1<<4)  # Variable stroke width, serifed.
FF_SWISS     	= (2<<4)  # Variable stroke width, sans-serifed.
FF_MODERN    	= (3<<4)  # Constant stroke width, serifed or sans-serifed.
FF_SCRIPT    	= (4<<4)  # Cursive, etc.
FF_DECORATIVE	= (5<<4)  # Old English, etc. 

LF_FACESIZE   = 32

class LOGFONT(ctypes.Structure):
	_fields_ = [( "lfHeight", LONG ),
				( "lfWidth", LONG ),
				( "lfEscapement", LONG ),
				( "lfOrientation", LONG ),
				( "lfWeight", LONG ),
				( "lfItalic", BYTE ),
				( "lfUnderline", BYTE ),
				( "lfStrikeOut", BYTE ),
				( "lfCharSet", BYTE ),
				( "lfOutPrecision", BYTE ),
				( "lfClipPrecision", BYTE ),
				( "lfQuality", BYTE ),
				( "lfPitchAndFamily", BYTE ),
				( "lfFaceName", CHAR * LF_FACESIZE)]

get_create_cda_func = windll.gdi32.CreateDCA
get_create_cda_func.argtypes = [LPCSTR, LPCSTR, LPCSTR, c_void_p]
get_create_cda_func.restype = HDC

get_font_families_func = windll.gdi32.EnumFontFamiliesExA
get_font_families_func.argtypes = [HDC, LOGFONT, c_void_p, LPARAM, DWORD]
get_font_families_func.restype = INT


windowsFontList = []

# callback to handle list of fonts
@CFUNCTYPE(INT, LOGFONT, c_void_p, DWORD, LPARAM)
def handle_font_func(font, phys_font, type, param):
	
	if font.lfPitchAndFamily != FF_MODERN | FIXED_PITCH:
		return 1

	windowsFontList.append(font.lfFaceName.decode('ascii'))
	return 1

def get_fonts():

	windowsFontList.clear()

	# windows
	lf = LOGFONT()
	lf.lfCharSet = 0
	lf.lfPitchAndFamily = FF_MODERN | FIXED_PITCH # potentially modifiable
	lf.lfFaceName = b"\0"

	ctx = get_create_cda_func(b"DISPLAY", b"", b"", 0)
	get_font_families_func(ctx, lf, handle_font_func, 0, 0)

	windowsFontList.sort()
	#print(fontList)
	return windowsFontList
