"""Python3 Relational Database Normalization Library
Author : R Mukesh ( IIITDM, Kancheepuram )
"""

#__VERBOSE__ = True : Indicates that ALL VIOLATIONS and INTERMEDIATES will be printed
__VERBOSE__=True


def verbose(verbose_level):
	"""Change the output verbosity level for the module."""
	global __VERBOSE__
	__VERBOSE__=verbose_level

class database:
	"""A hood for attributes, FDs, keys and related operations on a relation."""
	def read_attributes(self,sep=' '):
		"""Reads attributes from user into a set.
		
		Keyword arguments:
		sep -- the seperator between attributes (default <space>)	
		"""
		print("Enter the attributes in the form A",sep,"B",sep,"C",sep='')
		#flat file (set) of all atrributes
		self.attributes=set(input().strip().split(sep))

	def read_FDs(self,fd_sep=';',side_sep='->',attr_sep=','):
		"""Read FDs from user.
		
		Keyword arguments:
		fd_sep -- delimiter between FDs (default ';')
		side_sep -- seperator between LHS and RHS in a FD (default '->')
		attr_sep -- seperator between attributes in LHS/RHS of a FD (default ',')
		"""

		print("\nEnter FDs in the form A",attr_sep,"B",side_sep,"C",attr_sep,"D",attr_sep,"E",fd_sep,"X",side_sep,"Y",attr_sep,"Z",sep='')
		self.FDs=input().strip().split(fd_sep)
		self.FDs=[x.strip().split(side_sep) for x in self.FDs]
		self.FDs=[[set(x[0].strip().split(attr_sep)),set(x[1].strip().split(attr_sep))] for x in self.FDs]
	
	#NOT NECCESSARY : module computes candidate keys from given attributes, FDs
	def read_candidateKeys(self,key_sep=';',attr_sep=','):
		"""Reads 'all' candidate key(s) of the relation from user and generates prime attributes set.
		
		Keyword arguments:
		key_sep -- delimiter between candidate keys (default ';')
		attr_sep -- seperator between attributes in a candidate key (default ',')	
		"""
		print("\nEnter the Candidate keys in the form A",attr_sep,"B",key_sep,"C",attr_sep,"D",attr_sep,"E",key_sep,"F")
		self.candidate_keys=[set(keys.strip().split(attr_sep)) for keys in input().strip().split(key_sep)]
			
		#generating prime attributes (TODO: can be made seperate function)
		self.primes=set()
		for keys in self.candidate_keys:
			for attr in keys:
				self.primes.add(attr)

	def print_attributes(self,seperator=' '):
		"""Prints the attributes.
		
		Keyword arguments:
		seperator -- seperator between the attributes (default <space>)
		"""
		print(*self.attributes,sep=seperator)

	def print_FDs(self,fd_sep='\n',side_sep=" => ",attr_sep=","):
		"""Prints the FDs.

		Keyword arguments:
		fd_sep -- delimiter between FDs (default <newline>)
		side_sep -- seperator between LHS and RHS in a FD (default '=>')
		attr_sep -- seperator between attributes in LHS/RHS of a FD (default ',')
		"""
		for FD in self.FDs:
			print(*FD[0],sep=attr_sep,end="")
			print(side_sep,end="")
			print(*FD[1],sep=attr_sep,end="")
			print(fd_sep,end="")

	def print_cKeys(self,key_sep='\n',attr_sep=','):
		"""Prints 'all' the candidate keys of a relation.
		
		Keyword arguments:
		key_sep -- delimiter between candidate keys (default <newline>)
		attr_sep -- seperator between attributes in a candidate key (default ',') 
		"""
		for ckey in self.candidate_keys:
			print(*ckey,sep=attr_sep,end=key_sep)

	#prints all fields of a database
	def print_all(self):
		"""Prints the attributes, FDs and Candidate keys (with default seperators)"""
		print("\nAttributes : ",end="")
		self.print_attributes()

		print("\nFDs")
		self.print_FDs()

		print("\nCANDIDATE KEYS")
		self.print_cKeys()


	def __init__(self,init_attributes=None,init_fds=None):
		"""initialises a database object with attributes, FDs (converted to minimal cover) and corresponding candidate keys.
		
		Keyword arguments:
		init_attributes -- initialising value of 'attributes' field (default <None> - reads attributes from user)
		init_fds -- initialising value of 'FDs' field (default <None> - reads FDs from user)
		"""
		if init_attributes is None:
			self.read_attributes()
		else:
			self.attributes=init_attributes

		if init_fds is None:
			self.read_FDs()
		else:
			self.FDs=init_fds

		#convert FDs to minimal Cover
		self.FDs=self.minimalCover()

		#self.read_candidateKeys()
		self.generate_ckeys()

	#generate minimal cover of the given FDs
	def minimalCover(self):
		"""Returns Minimal Cover(Canonical Form) of 'FDs' of the database object."""
		global __VERBOSE__

		new_FDs=[]
		#decompose RHS of all FDs : canonical form
		for FD in self.FDs:
			for element in FD[1]:
				new_FDs.append([FD[0],{element}])

		#eliminate redundant FDs
		reduced_FDs=new_FDs.copy()

		for cur_FD in new_FDs:
			temp_FD=reduced_FDs.copy()
			temp_FD.remove(cur_FD)

			#if closure of LHS of cur_FD using temp_FD contains RHS; remove cur_FD
			if cur_FD[1].issubset(closure(temp_FD,cur_FD[0].copy())):
				if __VERBOSE__==True:
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
						if __VERBOSE__==True:
							print("# removing redundant attribute ",attributes,"from ",cur_FD)
						cur_FD[0].difference_update({attributes})

		#TODO: may recombine LHS if neccessary
		return reduced_FDs
	
	#TODO: decomposition into 2NF satifying relations

	#dependency preserving and lossless join decomposition	
	def dep_los_3NFdecompose(self):
		"""Performs 'dependency preserving' 'lossless join' decomposition of a database object.
		
		Note: Original database object remains intact.
		The list of decomposed relations is created as a field 'DECOMPOSED_3NF_RELN' in the original database object.
		"""
		global __VERBOSE__

		LHS_values=[]

		self.DECOMPOSED_3NF_RELN=[]

		for FD in self.FDs:
			if LHS_values.__contains__(FD[0])==False:
				LHS_values.append(FD[0])

				decompose_attr=FD[0].copy()
				decompose_fd=[]

				for fd_element in self.FDs:
					if fd_element[0].__eq__(FD[0]):
						decompose_attr.update(fd_element[1])
						decompose_fd.append(fd_element)

				self.DECOMPOSED_3NF_RELN.append(database(decompose_attr,decompose_fd))
		
		#check if decomposed relations has any ckey in atleat one decomposed relations
		DcontainsKey=0
		for keys in self.candidate_keys:
			for relations in self.DECOMPOSED_3NF_RELN:
				if keys.issubset(relations.attributes):
					DcontainsKey=1
					break

		if DcontainsKey==0:
			
			if __VERBOSE__==True:
				print("No KEY found in decomposed relations D")

			self.candidate_keys.sort(key=len)
			self.DECOMPOSED_3NF_RELN.append(database(self.candidate_keys[0],[]))

		del LHS_values

		length=len(self.DECOMPOSED_3NF_RELN)
		i=0
		#remove redundant relations
		while i<length-1:
			j=i+1
			while j<length:

				if (self.DECOMPOSED_3NF_RELN[i].attributes).issubset(self.DECOMPOSED_3NF_RELN[j].attributes):

					#merge FDs of DECOMPOSED_3NF_RELN of i into j
					for fds in self.DECOMPOSED_3NF_RELN[i].FDs:
						self.DECOMPOSED_3NF_RELN[j].FDs.append(fds)

					self.DECOMPOSED_3NF_RELN.pop(i)
					i=i-1
					length=length-1
					break
				j=j+1
			i=i+1


		if __VERBOSE__==True:
			print("\n\n 3NF DECOMPOSED RELATIONS")
			print("+------------------------+\n")

		for num in range(len(self.DECOMPOSED_3NF_RELN)):
			self.DECOMPOSED_3NF_RELN[num].generate_ckeys()
			
			if __VERBOSE__==True:
				print("RELATION ",num+1)
				self.DECOMPOSED_3NF_RELN[num].print_all()
				print("-------------------------------------------------------")

			self.DECOMPOSED_3NF_RELN[num].primes=set()
			for keys in self.DECOMPOSED_3NF_RELN[num].candidate_keys:
				for attr in keys:
					self.DECOMPOSED_3NF_RELN[num].primes.add(attr)

	#TODO: decomposition into 3NF satisfying relations.
	
	#generate all candidate keys
	def generate_ckeys(self):
		"""Generates the candidate key(s) set and prime attributes set of a database object."""
		#generate all that have not appeared in RHS of any FD : set A
		#generate all that appear on RHS, but not LHS 	      : set B
		LHS_values=set()
		RHS_values=set()

		for FD in self.FDs:
			LHS_values.update(FD[0])
			RHS_values.update(FD[1])

		self.candidate_keys=[]

		L=LHS_values.difference(RHS_values)
		R=RHS_values.difference(LHS_values)
		B=LHS_values.intersection(RHS_values)

		cur_attrs=B.union(L,R)
		left_out=self.attributes.difference(cur_attrs)

		#if LHS values is not empty and closure(L)=R
		if closure(self.FDs,L.copy()).__eq__(cur_attrs):
			self.candidate_keys.append(L)

		else:	
			#these attributes may be ckeys if augument with more attributes from B
			key_violate_attr=set()
			#these attributes augument with L are cKeys
			key_satisfy_attr=set()

			for b in B:
				if(closure(self.FDs,L.union({b})).__eq__(cur_attrs)):
					key_satisfy_attr.add(b)
					self.candidate_keys.append(L.union({b}))

				else:
					key_violate_attr.add(b)
			
			#candidate keys set with possible super_key outliers
			ckeys_w_spkey=[]

			for violate_attr in key_violate_attr:

				#attributes under consideration in subset formation
				check_attrs=B.difference({violate_attr}.union(key_satisfy_attr))
				subsets=_powerset(check_attrs)

				#print("\nkey violation : ",L.union({violate_attr}))
				for s in subsets:
					#cur_key_check : set of attributes being checked if it is c_key
					cur_key_check=s.union(L,{violate_attr})
					#print("key check : ",cur_key_check)
					if closure(self.FDs,cur_key_check.copy()).__eq__(cur_attrs):

						#check if 'cur_key_check' is a superset of some already existing c_key
						is_ckey=1

						for key in ckeys_w_spkey:
							if(key.issubset(cur_key_check)):
								is_ckey=0
								break

						if is_ckey==1:
							#print("is candid key")
							ckeys_w_spkey.append(cur_key_check)

			to_eliminate=[]

			for i in range(len(ckeys_w_spkey)-1):
				for j in range(i+1,len(ckeys_w_spkey)):

					if ckeys_w_spkey[i].issubset(ckeys_w_spkey[j]):
						to_eliminate.append(ckeys_w_spkey[j])

					elif ckeys_w_spkey[i].issuperset(ckeys_w_spkey[j]):
						to_eliminate.append(ckeys_w_spkey[i])

			for super_keys in to_eliminate:
				ckeys_w_spkey.remove(super_keys)

			self.candidate_keys.extend(ckeys_w_spkey)

		for key in self.candidate_keys:
			key.update(left_out)			

		#generating prime attributes
		self.primes=set()
		for keys in self.candidate_keys:
			for attr in keys:
				self.primes.add(attr)	
	
	
	#is a given set of attributes : a partial dependency
	def isPartialKey(self,attr_set):
		"""Checks if given atrribute(s) set is a part (i.e., proper subset) of a candidate key.
		
		Keyword arguments:
		attr_set -- given attribute(s) set
		"""
		isPartkey=False
		for keys in self.candidate_keys:
			#attribute set a proper subset of candidate keys
			if attr_set.issubset(keys) and attr_set.__eq__(keys)==False:
				isPartkey=True
				break

		return isPartkey

	#helper function
	def isSuperKey(self,attr_set):
		"""Checks if any candidate key is a part or whole (i.e., subset) of the given attribute(s) set.
		
		Keyword arguments:
		attr_set -- given attribute(s) set
		"""
		isSKey=False
		for keys in self.candidate_keys:
			if keys.issubset(attr_set):
				isSKey=True
				break

		return isSKey

	#test using general definition of 2NF : returns True if is in 2NF
	def test2NFRelation(self):
		"""Checks if the database object is in Second Normal Form and prints the 2NF violations."""	
		global __VERBOSE__

		#RHS is non-prime attribute -> LHS is not a partial dependency
		is2NF=True
		#if RHS not in primes
		for FD in self.FDs:
			if FD[1].issubset(self.primes)==False and self.isPartialKey(FD[0]):
					if __VERBOSE__==True:
						print(FD[0],"->",FD[1],"violates 2NF")
					is2NF=False

		return is2NF

	#test using general definition of 3NF : returns True if is in 3NF
	def test3NFRelation(self):
		"""Checks if the database object is in Third Normal Form and prints the 3NF violations."""
		global __VERBOSE__
		#X->A : X is superkey or A is prime attribute
		is3NF=True
		for FD in self.FDs:
			if self.isSuperKey(FD[0]) or FD[1].issubset(self.primes):
				pass

			else:
				if __VERBOSE__==True:
					print(FD[0],"->",FD[1],"violates 3NF")
				is3NF=False
		return is3NF

	#test using general definition of BCNF : returns True if is in BCNF
	def testBCNFRelation(self):
		"""Checks if the database object is in Boyce-Codd Normal Form and prints the BCNF violations."""
		global __VERBOSE__
		isBCNF=True
		for FD in self.FDs:
			if self.isSuperKey(FD[0]):
				pass
			else:
				if __VERBOSE__==True:
					print(FD[0],"->",FD[1],"violates BCNF")
				isBCNF=False
		return isBCNF
	
	#TODO: test for fourth,fifth normal form violations
	
	def test_all_NFs(self):
		"""Checks and summarises the compliance with 2NF,3NF,BCNF."""
		global __VERBOSE__
		init_verbose=__VERBOSE__

		verbose(False)
		is2NF=self.test2NFRelation()
		is3NF=self.test3NFRelation()
		isBCNF=self.testBCNFRelation()

		print("\nCHECK ALL NORMAL FORMS")

		print("2NF  : ","YES" if is2NF==True else "NO")
		print("3NF  : ","YES" if is3NF==True else "NO")
		print("BCNF : ","YES" if isBCNF==True else "NO")
		print()

		#set back verbose level to initial state
		verbose(init_verbose)

''' ************* start of helper function ************** '''

#generate all powersets of the given set : PRIVATE FUNCTION
def _powerset(given_set):
	"""Returns list of all powersets of  given set except empty set.
	
	Keyword arguments:
	given_set -- the set for which powerset is computed
	"""
	result = [set()]
	for x in given_set:
		result.extend([subset.union({x}) for subset in result])
	result.pop(0)
	return result

#Note a part of class : Closure is computed for attributes on modified 'FDs'
def closure(FDs,given_attr):
	"""Computes closure of given attribute(s) set from given 'FDs'.
		
	Keyword arguments:
	FDs -- FDs from which closure is computed
	given_attr -- attribute(s) set for which closure is computed 	
	"""
	newlyAdded=True
	while(newlyAdded!=False):
		newlyAdded=False
		for cur_FD in FDs:
			#if LHS of FD is subset of given
			if cur_FD[0].issubset(given_attr) and not cur_FD[1].issubset(given_attr):
				given_attr.update(cur_FD[1])
				#print(given)
				newlyAdded=True


	return given_attr

''' ************* end of helper function ************** '''
