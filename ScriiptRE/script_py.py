import pefile
namesModule = ['\\Kernel32.dll', '\\wininet.dll']
nameModule = "KERNEL32.DLL\0".encode('utf-16-le')
winModule = "WININET.DLL\0".encode('utf-16-le')
nameFunct = 'LoadLibraryA\0'.encode('ascii')
dll_path =  r'C:\Windows\System32'
dll_path2 =  r'C:\Windows\System32\Kernel32.dll'
import pefile
namesModule = ['\\Kernel32.dll', '\\wininet.dll']
nameModule = "KERNEL32.DLL\0".encode('utf-16-le')
winModule = "WININET.DLL\0".encode('utf-16-le')
nameFunct = 'LoadLibraryA\0'.encode('ascii')
dll_path =  r'C:\Windows\System32'
dll_path2 =  r'C:\Windows\System32\Kernel32.dll'

def get_exported_functions(dll_path):
    pe = pefile.PE(dll_path)
    exported_functions = []

    if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
        for export in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            if export.name:
                exported_functions.append(export.name + b'\x00')
    return exported_functions

def ror13_hash(unhash):
    result = 0
    for b in unhash:       
        result = ((result >> 13) | (result << (32 - 13))) & 0xffffffff
        result = (result + b) & 0xffffffff    
        #print(hex(result))
        
    return hex(result)
#functions = get_exported_functions(dll_path2)
#print(hex((int(ror13_hash(functions[968]), 16) + int(ror13_hash(nameModule), 16)& 0xffffffff)))

for module in namesModule:
    functions = get_exported_functions(r"".join([dll_path , module])) 
    upperModule = module[1:].upper().encode('utf-16-le') + (b'\x00'*2)    
    hash_upper_module_hex = ror13_hash(upperModule)    
    print(module[1:], '  ----HASH---->  ', hash_upper_module_hex)
    for func in functions:
        hash_funct_hex = ror13_hash(func)
        print(module[1:], "!", func.decode('utf-8'), "  ----HASH--->  ", 
              hash_funct_hex, "  ----SUM---->  ", 
              hex((int(hash_upper_module_hex, 16) +  int(hash_funct_hex, 16)) & 0xffffffff))
        with open(r"C:\Users\vboxuser\Desktop\HashingData.txt", "a") as archivo:
            str_result = module[1:] + "!" + func.decode('utf-8') + "  ----HASH--->  " + hash_funct_hex + "  ----SUM---->  " + hex((int(hash_upper_module_hex, 16) +  int(hash_funct_hex, 16)) & 0xffffffff) + "\n"  
            archivo.write(str_result)


#index = 0
#for func in functions:
#    print(index, "  ", func)
#    index+=1
#print(functions[968])
