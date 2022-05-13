collatz(N, N).
collatz(N0, N) :-
    0 is mod(N0, 2),
    N1 is N0 / 2,
    collatz(N1, N).
collatz(N0, N) :-
    1 is mod(N0, 2),
    N1 is 3 * N0 + 1,
    collatz(N1, N ).

% Example query:
% ?- collatz(10, L).