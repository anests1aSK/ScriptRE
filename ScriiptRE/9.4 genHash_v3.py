import pefile
import ctypes 

libs = ["kernel32", "ntdll"]
basePath = "c:\\Windows\\System32\\"

hashLib = ctypes.CDLL("genHash.dll") 
hashLib.genHash.argtypes = [ctypes.c_char_p] 
hashLib.genHash.restype = ctypes.c_uint32

for lib in libs:
	pe = pefile.PE(basePath + lib + ".dll")
	symbols_all = map(lambda s: s.name,  pe.DIRECTORY_ENTRY_EXPORT.symbols)
	symbols = filter(None, symbols_all)
	enum = map(lambda s: "\t%s_%s = 0x%08X,\n" % (lib.upper(), s, hashLib.genHash(s)), symbols)
	open(lib + ".h", "w").write("typedef enum " + lib.upper() + "\n{\n" + "".join(enum) + "};\n")