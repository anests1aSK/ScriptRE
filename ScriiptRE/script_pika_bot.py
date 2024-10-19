import idc
import idautils
import idaapi
import ctypes

def get_offset_var(value):
    op_offset = idc.get_operand_value(value, 0)
    return ctypes.c_int(op_offset).value

#print(hex(get_offset_var(idc.get_operand_value(ea, 0))))
#print(function_ea)

def block_funct(fn):
    
    out_aux_emulation = []
    f = ida_funcs.get_func(fn)
    fchart = list(idaapi.FlowChart(f, flags=idaapi.FC_PREDS)) 
    
    for block in range(len(fchart)):
        #print(block)
        current_block = fchart[block]    
        #print(f"Block Address: {hex(current_block.start_ea)}")
        #print(f"{hex(current_block.end_ea)}")
        #print(f" {hex(idc.prev_head(current_block.end_ea))}")
        
        prev_inst = idc.prev_head(current_block.end_ea)
        if idc.print_insn_mnem(prev_inst) == 'jl':
            prev_block_set_hash_var = fchart[block - 1]
            #print(f"Prev_Block : {hex(prev_block_set_hash_var.start_ea)}")
            #loop dechiper block
            jl_ins_ptr = prev_inst
            end_block_jl = current_block.end_ea
            start_previous_block = prev_block_set_hash_var.start_ea
            
            #>= start to end, find offset ebp+ecx+offset
            while jl_ins_ptr >= current_block.start_ea:
                #print(f"{hex(jl_ins_ptr)}") 
                #print(f"__prev: {hex(idc.prev_head(jl_ins_ptr))}")
                jl_ins_ptr = idc.prev_head(jl_ins_ptr)
                
                if idc.print_insn_mnem(jl_ins_ptr) == "mov":
                    get_offset = get_offset_var(jl_ins_ptr)
                    #print(f"{hex(get_offset)}")
                    out_aux_emulation.append({'start' : start_previous_block,
                                'end' : end_block_jl,
                                'offset_var' : get_offset})
                    break
    return out_aux_emulation

aux_string = []

for function in idautils.Functions():
        out = block_funct(function)
        aux_string += out
   

print(aux_string)