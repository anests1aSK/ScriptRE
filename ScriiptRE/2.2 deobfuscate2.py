import sys
import re


cleanJunk = lambda lines: [ line for line in lines if not line.endswith(" & @SEC") ]

# Clean junk perfix from varaible names
cleanVarNames = lambda lines: [line.replace("$g932193107bewuoee", "$") for line in lines]
	

def revStrings(lines):
 
	myRev = lambda match: "\"" + match.group(0).split("\"")[1][::-1] + "\""
	
	return [ re.sub(r'_stringreverse\(".*?"\)', myRev, line) for line in lines ]

def replaceStrings(lines):
	# name:value dictionary of variables
	variables = {}
	res = []
	
	# Extract simple definitions of string variables	
	lines_step2 = []
	for line in lines:	
		var_def = re.search('^\s*(\$[0-9a-z]*?) = (\"[^ ]*?\")$', line)
		if var_def:
			variables[var_def.group(1)] = var_def.group(2)
			continue
		lines_step2.append(line)

	lines_step3 = []
	for line in lines_step2:
		# Replace string variables
		for v in sorted(variables, key = len, reverse = True):
			if v in line: line = line.replace(v, variables[v])
		lines_step3.append(line)

	# Concatenate strings
	return [ line.replace('" & "', '') for line in lines_step3 ]
	
if __name__ == "__main__":
	
	lines = [ l.rstrip() for l in open( sys.argv[1]).readlines() ]
	clean_lines = revStrings(cleanVarNames(cleanJunk(lines)))

	#for _ in range(10):
	clean_lines = replaceStrings(clean_lines)
		
	print('\n'.join(clean_lines)) 