import sys
sys.path.append("../SRC/")

import normalization

print(normalization.__doc__)

'''Start of main program'''
company=normalization.database()

company.print_all()

company.test_all_NFs()

print("\n2NF Violations")
is2NF=company.test2NFRelation()

print("\n3NF Violations")
is3NF=company.test3NFRelation()

print("\nBCNF Violations")
isBCNF=company.testBCNFRelation()

if is3NF==0: 
	company.dep_los_3NFdecompose()

else:
	print("\nNO 2NF and 3NF Violations")
'''End of main program'''
