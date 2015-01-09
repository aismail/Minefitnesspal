def makearrayfromprint(s):
  	arr = []
  	for val in s:
  		if val != "[" and val != " " and val!="]":
  			arr.append(val)
  	return arr