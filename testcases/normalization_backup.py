class database:

	def read_attributes(self):
		print("Enter the attributes")
		#flat file (set) of all atrributes
		self.attributes=[set(input().strip().split(' '))]

	def read_FDs(self):
		print("\nEnter FDs in the form A,B->C,D,E;X->Y,Z")
		self.FDs=input().strip().split(';')
		self.FDs=[x.strip().split('->') for x in self.FDs]
		self.FDs=[[set(x[0].strip().split(',')),set(x[1].strip().split(','))] for x in self.FDs]

	def __init__(self):
		self.read_attributes()
		self.read_FDs()

		#convert FDs to minimal Cover
		self.FDs=minimalCover(self.FDs)

	
def minimalCover(FDs):
	new_FDs=[]
	#decompose RHS of all FDs
	for FD in FDs:
		for element in FD[1]:
			new_FDs.append([FD[0],{element}])

	#eliminate redundant FDs
	reduced_FDs=new_FDs.copy()

	for cur_FD in new_FDs:
		temp_FD=reduced_FDs.copy()
		temp_FD.remove(cur_FD)

		#if closure of LHS of cur_FD using temp_FD contains RHS; remove cur_FD
		if cur_FD[1].issubset(closure(temp_FD,cur_FD[0].copy())):
			print("# Removing : ",cur_FD)
			reduced_FDs.remove(cur_FD)

	#now eliminate redundant attributes in LHS of reduced FDs
	for cur_FD in reduced_FDs:
		if(len(cur_FD[0])==1):
			pass
		
		else:
			LHS=cur_FD[0].copy()
			for attributes in LHS:
				if({attributes}.issubset(closure(reduced_FDs,cur_FD[0].difference({attributes})))):
					print("# removing redundant attribute ",attributes,"from ",cur_FD)
					cur_FD[0].difference_update({attributes})

	#may recombine LHS if neccessary
	return reduced_FDs


def closure(FDs,given):
	
	newlyAdded=1
	while(newlyAdded!=0):
		newlyAdded=0
		for cur_FD in FDs:
			#if LHS of FD is subset of given
			if cur_FD[0].issubset(given) and not cur_FD[1].issubset(given):
				given.update(cur_FD[1])
				#print(given)
				newlyAdded=1

	return given


company=database()