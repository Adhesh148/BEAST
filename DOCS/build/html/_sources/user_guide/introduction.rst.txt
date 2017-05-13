Introduction
============

RDMS Normalization Library is a library for NORMALIZATION of RELATIONAL DATABASES in `Python <https://www.python.org>`__,
through a pythonic and object-oriented interface.

The library is designed with the philosophy that it should serving as a one-stop for all 
database design activities (From conception  to realization): 

* Finding Minimal Cover ( Canonical form ) of FDs

* Finding closure of set of attributes

* Generating all Candidate Keys

* Testing for Normal Forms - 2NF, 3NF, BCNF

* Decomposition of Relations that violate NORMAL FORMS

Many more in the phase of development. All of these with verbose step-by-step explanation.

Motivation
**********

It was recently, when we were doing our PROJECT `COMPLAINT MANAGEMENT SYSTEM <https://github.com/guptaanmol184/Database-Project-Files>`__
as a part of the DBMS course, that I first attempted this heavy lifting, mind numbing, fearful nightmare ... task of manually normalizing
A BUNCH OF FDs. A little too much of exaggeration, isn't it? 

However, it was the perfect thing for a computer to do, and never the right thing for humans. So, I decided to put the bones in place,
so people after me can fill in the flesh and blood. It is rather obvious that this BEAST,  with its heart of the pythonic stuff, will expeditiously grow and evolve over time.

The library is intended for direct python3 CLI use or for use in other modules and applications (Web and Desktop), in any form that may benifit the community at large.

The author is eagerly looking for collaborators and developers who are willing to built upon the BEAST.
