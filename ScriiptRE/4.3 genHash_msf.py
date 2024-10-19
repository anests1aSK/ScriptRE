import pefile

def ror(val, r_bits, max_bits):
    return ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

libs = ["kernel32", "ntdll", "wininet"]
basePath = "c:\\Windows\\System32\\"

def hash_mod(name):
	chars = [list(c) + list(chr(0)) for c in list((name+".dll").upper()) + list(chr(0))]
	chars_uni = [val for _ in chars for val in _]
	
	h = 0
	# Add string terminator to hash calculation
	for c in chars_uni:
		h = ror(h, 13, 32)
		h += ord(c)
	return h

def hash_func(modName, funcName):
	h_mod = hash_mod(modName)
	
	h_func = 0
	# Add string terminator to hash calculation
	for c in list(funcName) + list(chr(0)):
		h_func = ror(h_func, 13, 32)
		h_func += ord(c)
		
	return (h_func + h_mod) & (2**32 - 1)

if __name__ == "__main__":
	for lib in libs:
		f = open(lib + "_msf.h", "w")
		f.write("typedef enum " + lib.upper() + "\n{\n")
		
		pe = pefile.PE(basePath + lib + ".dll")
		for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
			if exp.name:
				f.write("\t%s_%s = 0x%08X,\n" % (lib.upper(), exp.name, hash_func(lib, exp.name)))
		f.write("\t%s_END = 0xDEADBEEF\n" % lib.upper())
		f.write("};\n")
		f.close()