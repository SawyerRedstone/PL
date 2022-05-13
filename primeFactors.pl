% Determine the prime factors of a given positive integer.
 
% N is the number to be factored, L is a list of the prime factors.
prime_factors(N, L) :- N > 0,  prime_factors(N, L, 2). 


% F is the smallest prime factor of N.
prime_factors(1, [], _) :- !.               % 1 has no prime factors.          
prime_factors(N, [F|L], F) :-               % N is a multiple of F
    R is N // F, N =:= R * F, !, prime_factors(R, L, F).
prime_factors(N,L,F) :-                     % N is not a multiple of F
    next_factor(N,F,NF), prime_factors(N,L,NF).        
   
next_factor(_,2,3) :- !.
next_factor(N,F,NF) :- F * F < N, !, NF is F + 2.
next_factor(N,_,N).                          % F > sqrt(N)