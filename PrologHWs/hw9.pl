% Sawyer Redstone

% Question 1
% Yes, E is true. A and B are facts, which means that C is true. D is also a fact. Because of this, C AND D => E makes E true.

% Question 2
% (a) a = True
% (b) c = True
% (c) h = False
% (d) d = False
% (e) k = True
% (f) e = False
% (g) j = False

% Question 8
inboth(A, B, X) :- member(X, A), member(X, B).

% Question 9
increment_all([], X) :- X = [].
increment_all([H|T], X) :- Y is H + 1, increment_all(T, Z), X = [Y|Z].

% Question 10
merge(A, [], A).
merge([], B, B).
merge([H1|T1], [H2|T2], X) :- H1 < H2, merge(T1, [H2|T2], Z), X = [H1|Z].
merge([H1|T1], [H2|T2], X) :- H1 >= H2, merge([H1|T1], T2, Z), X = [H2|Z].

% Question 11
% Yes, this will unify. X1 = d. X3 = a. X4 = f(b). X5 = [c, d].
% Y1 = [a, f(b), c, d].

% Question 12
all_diff([]).
all_diff([H|T]) :- not(member(H, T)), all_diff(T).

% Question 13
splitAt(Pos, List, FirstPart, SecondPart) :- append(FirstPart, SecondPart, List), length(FirstPart, Pos).

collatz(N, N ).
collatz(N0, N ) :-
    0 is mod(N0, 2),
    N1 is N0 / 2,
    collatz(N1, N ).
collatz(N0, N ) :-
    1 is mod( N0 , 2),
    N1 is 3 * N0 + 1,
collatz(N1, N ).

