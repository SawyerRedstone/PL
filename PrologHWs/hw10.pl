someTree(X) :-
	X = t("t1",
		t("t2a",
			t("t3a", nil, nil),
			t("t3b", nil, nil)),
		t("t2b",
			t("t3c", nil, nil),
			t("t3d", nil, nil))).

% Question 1
flipTree(nil, nil).
flipTree(t(V, L, R), X) :- flipTree(L, L2), flipTree(R, R2), X = t(V, R2, L2).

% Question 2
inorderTraversalSpatial(nil, []).
inorderTraversalSpatial(t(V, L, R), X) :- inorderTraversalSpatial(L, X1), append(X1, [V], X2), inorderTraversalSpatial(R, X3), append(X2, X3, X).

% Question 3
inorderTraversalTemporal(t(_V, L, _R), X) :- inorderTraversalTemporal(L, X).
inorderTraversalTemporal(t(V, _L, _R), V).
inorderTraversalTemporal(t(_V, _L, R), X) :- inorderTraversalTemporal(R, X).

% Question 4
sublist(A, B) :- append(A, _, B).  % Append is checking if B starts with A.
sublist(A, [_|T]) :- sublist(A, T).

% Question 5
sublist_cut(A, B) :- append(A, _, B), !.
sublist_cut(A, [_|T]) :- sublist_cut(A, T).

% Question 6
% a) X = 14.
% b) X = 14, X = 24.
% c) false.
% d) false.

% Question 7
bad_sort(X, Y) :- permutation(X, Y), isSorted(Y), !.

isSorted([_]).
isSorted([H1, H2|T]) :- H1 =< H2, isSorted([H2|T]).

% Question 8
lookup(K, L, V) :- member(K-V, L), !.

% Question 9
graph1([n1-n2, n2-n5, n1-n3, n1-n4, n4-n6, n6-n7, n6-n8]).
graph2([n1-n2, n2-n5, n1-n3, n1-n4, n4-n6, n6-n7, n7-n1, n7-n8]).
graph3([n4-n5, n1-n2, n1-n3, n1-n4, n4-n9, n9-10, n9-n11, n9-n12, n12-n9]).

hasCycle(G) :- member(X-Y, G), getChain([X], Y, G), !.

getChain(Reached, Next, _G) :- memberchk(Next, Reached), !.
getChain(Reached, Next, G) :- member(Next-X, G), append(Reached, [Next], NewReached), getChain(NewReached, X, G), !.


