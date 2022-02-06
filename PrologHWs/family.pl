male(bob).
male(john).
male(ben).
male(martin).
male(edmund).
male(david).
male(isidore).
male(william).
male(ferdinand).
male(morris).
male(alphonse).
male(jiri).
female(kathryn).
female(beatrice).
female(rachel).
female(lillian).
female(alice).
female(rosa).
female(marjorie).
female(emma).
female(nellie).
female(eva).
female(bertha).
female(fergie).

% A is the child of B
child(bob, john).
child(bob, kathryn).

child(beatrice, john).
child(beatrice, kathryn).

child(john, ben).
child(john, rachel).
child(lillian, ben).
child(lillian, rachel).

child(kathryn, rosa).
child(kathryn, martin).
child(alice, martin).
child(alice, rosa).
child(ferdinand, martin).
child(ferdinand, fergie).

child(marjorie, edmund).
child(marjorie, lillian).
child(david, lillian).
child(david, edmund).

child(ben, isidore).
child(ben, bertha).
child(william, isidore).
child(william, bertha).
child(emma, isidore).
child(emma, bertha).

child(morris, alphonse).
child(morris, emma).
child(nellie, alphonse).
child(nellie, emma).
child(eva, alphonse).
child(eva, emma).
child(jiri, alphonse).
child(jiri, emma).

% Sawyer added
parent(A, B) :- child(B, A).

% Question 3
father(A, B) :- male(A), parent(A, B).
mother(A, B) :- female(A), parent(A, B).

% Question 4
sibling(A, B) :- parent(X, A), parent(X, B), A \= B.

% Question 5
uncle(A, B) :- parent(X, B), sibling(A, X), male(A).
aunt(A, B) :- parent(X, B), sibling(A, X), female(A).

% Question 6
ancestor(A, B) :- parent(A, B).
ancestor(A, B) :- parent(A, X), ancestor(X, B).

% Question 7
first_cousin(A, B) :- parent(X, A), sibling(Y, X), parent(Y, B).
