# include<iostream>
# include<algorithm>
# include<stdlib.h>

#define bSIZE 3
#define tSIZE 2
using namespace std;

class fd {
	public:
		string L;
		char R;
		void load(string Lin, char Rin) {
			L = Lin;
			R = Rin;
		}
};

class relation {
	public:
		string attr_set;
		int keylimiter;
		string getKey() {
			return attr_set.substr(0,keylimiter);
		}
		string getnonKey() {
			if(keylimiter==attr_set.length())
				return "";
			return attr_set.substr(keylimiter);
		}
		void keyLoad(string key) {
			attr_set = key;
			keylimiter = key.length();
		}
		void nonkeyLoad(char c) {
			attr_set.append(1,c);
		}
		void simpleDisplay() {
			cout<<getKey()<<" "<<getnonKey()<<endl;
		}
};

 //UTILITY - Returns 1 if s1 is a subset of s2, otherwise 0
int strIsSubset(string s1, string s2) {
	for(int i=0;i<s1.length();i++)
		if(s2.find(s1.at(i))==string::npos)
			return 0;
	return 1;
}

void strUnion(string &s1, string s2) //UTILITY - Inserts fresh characters into sorted string s1 from s2
{
	for(int i=0;i<s2.length();i++)
	{
		//char c = s2.at(i);
		if(s1.find(s2.at(i))==string::npos)
			s1.append(1,s2.at(i));
	}
	sort(s1.begin(),s1.end());
}

void strUnion(string &s1, char c) //UTILITY - Single character eqvt for String Union
{
	string s2;
	s2.append(1,c);
	strUnion(s1,s2);
}

void fdsCopier(fd fdsrc[],fd fdst[],int sSIZE) //UTILITY - Copies contents of FD Set fdsrc to fdst
{
	for(int i=0;i<sSIZE;i++)
	{
		fdst[i].L = fdsrc[i].L;
		fdst[i].R = fdsrc[i].R;
	}
}

void crHelper(fd fds[], fd fdcr[], int SIZE, int fdnum) //UTILITY - Copies all FDs from fds to fdcr except the one stored at index fdnum
{
	int k = 0;
	for(int i=0;i<SIZE;i++)
		if(fdnum!=i)
		{
			fdcr[k].L = fds[i].L;
			fdcr[k].R = fds[i].R;
			k++;
		}
}

string allAttributes(fd fds[],int SIZE) //UTILITY - Returns list of all attributes in an FD Set
{
	string attr_set;
	for(int i=0;i<SIZE;i++)
	{
		strUnion(attr_set, fds[i].L);
		strUnion(attr_set, fds[i].R);
	}
	return attr_set;
}

int bulkInput(fd fds[], int SIZE, string promptL = "\nInput LHS: ", string promptR = "Input RHS: ") //INPUT - Mass FD Input from stdin into cannonical FD Set, and returns size of resultant FD Set
{
	int j = 0;
	string Lin, Rin;
	for(int i=0;i<SIZE;i++)
	{
		cout<<promptL;
		cin>>Lin;
		cout<<promptR;
		cin>>Rin;
		sort(Lin.begin(),Lin.end());
		Lin.erase(std::unique(Lin.begin(), Lin.end()), Lin.end());
		for(int k=0;k<Rin.length();k++)
		{
			fds[j].load(Lin,Rin[k]);
			j++;
		}
	}
	return j;
}

string closure(fd fds[], string fplus, int SIZE) //Returns closure of fplus in FD set fds
{
	string ofplus;
	do
	{
		ofplus = fplus;
		for(int i=0;i<SIZE;i++)
			if(strIsSubset(fds[i].L,fplus)==1)
				strUnion(fplus,fds[i].R);
	}
	while(fplus.compare(ofplus)!=0);
	return fplus;
}

string keyFinder(fd fds[], int SIZE) //Returns a minimal key for FD set fds
{
	string key, attr_set, keycr;
	key = attr_set = allAttributes(fds, SIZE);
	int i = 0;
	while(i<key.length())
	{
		if(key.length()>1)
		{
			keycr = key;
			keycr.erase(i,1);
			if(attr_set.compare(closure(fds,keycr,SIZE))==0)
				key = keycr;
			else
				i++;
		}
		else
			return key;
	}
	return key;
}

int fdCover(fd fds1[], fd fds2[], int SIZE1, int SIZE2) //Returns 1 if FD Set fds1 covers fds2, otherwise 0
{
	for(int i=0;i<SIZE2;i++)
		if(closure(fds1,fds2[i].L,SIZE1).find(fds2[i].R)==string::npos)
			return 0;
	return 1;
}

int equivalence(fd fds1[], fd fds2[], int SIZE1, int SIZE2) //Returns 1 if FD Set fds1 is equivalent to fds2, otherwise 0
{
	return(fdCover(fds1,fds2,SIZE1,SIZE2) && fdCover(fds2,fds1,SIZE2,SIZE1));
}

int minCover(fd fds[], int SIZE) //Reduces FD Set fds to it's minimal cover, and returns the new size
{
	int j;
	fd fdcr[bSIZE];
	for(int i=0;i<SIZE;i++)
	{
		j=0;
		while(j<fds[i].L.length())
		{
			if(fds[i].L.length()>1)
			{
				fdsCopier(fds,fdcr,SIZE);
				fdcr[i].L.erase(j,1);
				if(equivalence(fds,fdcr,SIZE,SIZE)==1)
					fdsCopier(fdcr,fds,SIZE);
				else
					j++;
			}
			else
				break;
		}
	}

	j=0;
	while(j<SIZE)
	{
		crHelper(fds,fdcr,SIZE,j);
		if(equivalence(fds,fdcr,SIZE,SIZE-1)==1)
		{
			fdsCopier(fdcr,fds,SIZE-1);
			SIZE-=1;
		}
		else
			j++;
	}
	return SIZE;
}

int NF3(fd fds[], int &SIZE, relation rset[]) //Stores decomposed 3NF relations of fds in rset. Returns number of relations.
{
	int rSIZE = 0;
	string key = keyFinder(fds, SIZE);
	SIZE = minCover(fds, SIZE); //1. Reduce FD Set to Minimal Cover.
	for(int i=0;i<SIZE;i++) //2. Put FDs into relations GROUP BY LHS and set KEY = LHS.
	{
		int j;
		for(j=0;j<rSIZE;j++)
			if(fds[i].L.compare(rset[j].getKey())==0)
			{
				rset[j].nonkeyLoad(fds[i].R);
				break;
			}

		if(j==rSIZE)
		{
			rset[j].keyLoad(fds[i].L);
			rset[j].nonkeyLoad(fds[i].R);
			rSIZE++;
		}
	}
	//At this stage, 3NF is complete but may be lossy.
	for(int i=0;i<rSIZE;i++) //3. Test if Relation Set possibly requires fixing for Lossless Design.
	{
		if(strIsSubset(key,rset[i].attr_set)==1)
			return rSIZE;
	}

	for(int i=0;i<rSIZE;i++) //4. Ensure Lossless property by adding new 'key-only' relation.
	{
		if(strIsSubset(rset[i].attr_set,key)==1)
		{
			rset[i].keyLoad(key);
			return rSIZE;
		}
	}
	rset[rSIZE].keyLoad(key);
	return rSIZE+1;
}
/* Returns 1 if given relations and FDs are in BCNF, 0 otherwise */
int isBCNF(relation rset[], fd fds[], int rSIZE, int fSIZE)
{
	for(int i=0;i<fSIZE;i++)
		for(int j=0;j<rSIZE;j++)
		{
			if((strIsSubset(fds[i].L,rset[j].attr_set)==1) && (rset[j].attr_set.find(fds[i].R)!=string::npos))
				if(strIsSubset(rset[j].attr_set,closure(fds,fds[i].L,fSIZE))!=1)
					return 0;
		}
	return 1;
}

int main() {
	fd fds1[bSIZE], fds2[bSIZE];
	relation rset[bSIZE];
	int n1,rs1, nFd;
	cout << "Enter number of FDs: ";
	cin >> nFd;
	n1 = bulkInput(fds1,nFd);
	cout<<"\n-----\n";
	cout<<"Canonical Form FDs\n\n";
	for(int i=0;i<n1;i++)
		cout<<fds1[i].L<<" "<<fds1[i].R<<"\n";
	cout<<"\n-----\n";
	cout<<"3NF Set (Key Others)\n\n";
	rs1 = NF3(fds1, n1, rset);
	for(int i=0;i<rs1;i++)
		rset[i].simpleDisplay();
	if(isBCNF(rset,fds1,rs1,n1))
		cout<<"isBCNF?: YES";
	else
		cout<<"isBCNF?: NO";
	cout<<"\n-----\n";
	cout<<"keyFinder finds: "<<keyFinder(fds1,n1);
	cout<<"\n-----\n";
}