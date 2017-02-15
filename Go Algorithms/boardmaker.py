#This program produces a dictionary in a text file that is copied across to board9.py. 
#This dictionary maps each position to a dictionary of its player and neighbours.

#Open a text file
f=open("board9.txt","w")

#Labels for the rows and columns 
alphabet="abcdefghi"
number="123456789"

#loop through every column and row
for i in alphabet:
    for j in number:
	#add to the file a string consisting of, for example '    "a1":{"player:None, "neighbours":["a2", "b1",] }
        f.write('"'+i+j+'":{"player":None, "neighbours":[')
        if i!="a":
            f.write('"' + alphabet[alphabet.index(i) - 1] + j + '", ')
        if i!="i":
            f.write('"' + alphabet[alphabet.index(i) + 1] + j + '", ')
        if j!="1":
            f.write('"' + i + number[number.index(j) - 1]  + '", ')
        if j!="9":
            f.write('"' + i + number[number.index(j) + 1]  + '", ')
        f.write(']} ')

