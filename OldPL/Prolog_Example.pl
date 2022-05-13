% Prolog code to accompany PL_Documentation.pdf

% Here we define our facts.
male(sawyer).
male(michael).
female(rachel).
female(naomi).
child(sawyer, michael).
child(sawyer, rachel).
child(rachel, naomi).
always_true.

% Here we define our rules.
parent(A, B) :- child(B, A).
mother(A, B) :- female(A), parent(A, B).

ancestor(A, B) :- parent(A, B).
ancestor(A, B) :- parent(A, C), ancestor(C, B).

count(A, A).
count(A, C) :- B is A + 1, count(B, C).

write_var(A) :- A is 6 + 2, write(A).

write_var2(A) :- A is 6 + 2, write(A), fail.