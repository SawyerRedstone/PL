arc(g,h).
arc(g,d).
arc(e,d).
arc(h,f).
arc(e,f).
arc(a,e).
arc(a,b).
arc(b,f).
arc(b,c).
arc(f,c).


path(X, X, Path, NewPath) :- append(Path, [X], NewPath).
path(X, Y, OldPath, NewPath) :- arc(X, Z), append(OldPath, [Z], NewPath), path(Z, Y, NewPath, _).

