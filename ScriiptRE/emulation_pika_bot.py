from dumpulator import Dumpulator

aux_tres = [{'start': 4985289, 'end': 4985347, 'offset_var': -496, 'xmm': 0}, {'start': 4985347, 'end': 4985479, 'offset_var': -920, 'xmm': 0}, {'start': 4985479, 'end': 4985547, 'offset_var': -512, 'xmm': 0}, {'start': 4985547, 'end': 4985592, 'offset_var': -400, 'xmm': 0}, {'start': 4985592, 'end': 4985647, 'offset_var': -584, 'xmm': 0}, {'start': 4985647, 'end': 4985752, 'offset_var': -648, 'xmm': 0}, {'start': 4985752, 'end': 4985813, 'offset_var': -560, 'xmm': 0}, {'start': 4985813, 'end': 4985858, 'offset_var': -412, 'xmm': 0}, {'start': 4985858, 'end': 4986443, 'offset_var': -1364, 'xmm': 0}, {'start': 4986443, 'end': 4986580, 'offset_var': -1000, 'xmm': 0}, {'start': 4986580, 'end': 4986686, 'offset_var': -840, 'xmm': 0}, {'start': 4986686, 'end': 4986784, 'offset_var': -776, 'xmm': 0}, {'start': 4986784, 'end': 4986891, 'offset_var': -712, 'xmm': 0}, {'start': 4986891, 'end': 4986971, 'offset_var': -136, 'xmm': 0}, {'start': 4986971, 'end': 4987016, 'offset_var': -76, 'xmm': 0}, {'start': 4987016, 'end': 4987076, 'offset_var': -20, 'xmm': 0}, {'start': 4987076, 'end': 4987132, 'offset_var': -64, 'xmm': 0}, {'start': 4987132, 'end': 4987295, 'offset_var': -308, 'xmm': 0}, {'start': 4987295, 'end': 4987365, 'offset_var': -544, 'xmm': 0}, {'start': 4987564, 'end': 4987630, 'offset_var': -528, 'xmm': 0}, {'start': 4987630, 'end': 4987699, 'offset_var': -192, 'xmm': 0}, {'start': 4987699, 'end': 4987780, 'offset_var': -16908, 'xmm': 1}, {'start': 4987780, 'end': 4987852, 'offset_var': -12952, 'xmm': 1}, {'start': 4987852, 'end': 4987921, 'offset_var': -48, 'xmm': 0}]

def emulate():
    dp = Dumpulator("C:\\Users\\anests1a\\Desktop\\minidump_pika.dmp", quiet=True)  
    xmm = 0
    dp.start(0x004C11C9, end=0x004C1203)
    
    if xmm == 1:
        eax_len = dp.regs.eax
        out = dp.read(dp.regs.ebp + offset, eax_len * 2)
        out = dp.replace(b'\x00', b'')
        
    else:
        ecx_len = dp.regs.ecx

        if ecx_len > 2:
            if dp.read(dp.regs.ebp + offset, 2)[1] == 0:
                out = dp.read(dp.regs.ebp + offset, ecx_len * 2)
                out = dp.replace(b'\x00', b'')
            else:
                out = dp.read(dp.regs.ebp + offset, ecx_len)                
        else:
            out = dp.read(dp.regs.ebp + offset, ecx_len)

    return out
    

emulate()
#labels = {}
#for block in aux_tres:
   
#    if block.get('xmm') == 0:        
#        out = emulate(block.get('start'), block.get('end'), block.get('offset_var'), block.get('xmm'))
#        labels[bloc.get('start')] = out.decode('utf-8')
                
#    elif block.get('xmm') == 1:
#        out = emulate(block.get('start'), block.get('end'), block.get('offset_var'), block.get('xmm'))
#        labels[bloc.get('start')] = out.decode('utf-8')
    

   

#print(labels)