//TODO write a description for this script
//@author 
//@category _NEW_
//@keybinding 
//@menupath 
//@toolbar 

import ghidra.app.script.GhidraScript;
import ghidra.program.model.lang.protorules.*;
import ghidra.program.model.mem.*;
import ghidra.program.model.lang.*;
import ghidra.program.model.pcode.*;
import ghidra.program.model.data.ISF.*;
import ghidra.program.model.util.*;
import ghidra.program.model.reloc.*;
import ghidra.program.model.data.*;
import ghidra.program.model.block.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.scalar.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.address.*;
import ghidra.program.model.scalar.Scalar;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class DetectAPIHashing extends GhidraScript {

    @Override
    public void run() throws Exception {
		
         String filePath = "C:\\Users\\vboxuser\\Desktop\\HashingData.txt";
        
        // Leer el archivo y almacenar los hashes en un mapa
        Map<Long, String> hashMap = new HashMap<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = br.readLine()) != null) {
                // Suponiendo que el formato es: modulo_hash ! funcion_hash ----HASH---> hash ----SUM----> suma
                String[] parts = line.split("  ");
                long suma =  Long.parseLong(parts[4].substring(2), 16);
                hashMap.put(suma, parts[0]);

               // long moduloHash = Long.parseLong(parts[0], 16);
                //long funcionHash = Long.parseLong(parts[2], 16);
                //long suma = Long.parseLong(parts[6], 16);
                //hashMap.put(suma, moduloHash + funcionHash);
            }
        } catch (IOException e) {
            println("Error al leer el archivo: " + e.getMessage());
            return;
        }
	//for(Map.Entry<Long, String> entry : hashMap.entrySet()){
	//println("Clave: " + entry.getKey() + ", Valor: " + entry.getValue());
//}
        Listing listing = currentProgram.getListing();
        InstructionIterator instructions = listing.getInstructions(true);

        while (instructions.hasNext() && !monitor.isCancelled()) {
            Instruction instruction = instructions.next();

            if (instruction.getMnemonicString().equals("PUSH")) {
                Instruction nextInstruction = instruction.getNext();
                if (nextInstruction != null && nextInstruction.getMnemonicString().equals("CALL") &&
                    nextInstruction.getDefaultOperandRepresentation(0).equals("EBP")) {

                    // Extraer el valor del PUSH
                    Scalar pushValue = (Scalar) instruction.getOpObjects(0)[0];
                    long hashValue = pushValue.getValue();

                   if(hashMap.containsKey(hashValue)){
                    String address = instruction.getAddress().toString();
					
                    println("Address: " + address +"  HashValue: " + Long.toHexString(hashValue) + "Nombre de la funcion " + hashMap.get(hashValue));
                   instruction.setComment(CodeUnit.EOL_COMMENT, hashMap.get(hashValue));

                    // Si coincide, agrega un comentario
                    //String comment = "Match found: " + Long.toHexString(hashValue);
                    //instruction.setComment(CodeUnit.EOL_COMMENT, comment);
	}
                }
            }
        }
    }
}