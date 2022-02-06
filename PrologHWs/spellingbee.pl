test1 :-
    Letters = [r,a,b,o,t,l,y],
    doSpellingBee(Letters, Word),
    atom_chars(AtomWord,Word),write(AtomWord),nl,
    fail.

test2 :-
    Letters = [t,e,v,o,q,m,n],
    doSpellingBee(Letters, Word),
    atom_chars(AtomWord,Word),write(AtomWord),nl,
    fail.

readWord(InStream,W):-
     get_char(InStream,Char),
     checkCharAndReadRest(Char,W,InStream).

checkCharAndReadRest('\n',[],_):- !.
checkCharAndReadRest(' ',[],_):- !.
checkCharAndReadRest(end_of_file,[],_):- !.
checkCharAndReadRest(Char,[Char|Chars],InStream):-
     get_char(InStream,NextChar),
     checkCharAndReadRest(NextChar,Chars,InStream).

readWordStream(Str,[]) :- at_end_of_stream(Str), !.
readWordStream(Str,[Word|Words]) :- readWord(Str,Word), readWordStream(Str,Words).

readDict(Words) :-
         open('spellingbee.txt',read,Str),
         readWordStream(Str,Words),
         close(Str).

doSpellingBee([H|T], GoodWord) :- readDict(AllWords), member(GoodWord, AllWords), length(GoodWord, X), X > 3, memberchk(H, GoodWord), legalWord(GoodWord, [H|T]).

% Given a word with the correct middle letter, check if all other letters are legal.
legalWord([], _Letters).
legalWord([H|T], Letters) :- memberchk(H, Letters), legalWord(T, Letters), !.
