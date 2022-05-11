
% simple flight-planning system

% airport(City,Code)
% ------------------
% matches a city name with an airport code, e.g. "nanaimo" with "ycd"
airport('Nanaimo', 'YCD').
airport('Vancouver', 'YVR').
airport('Victoria', 'YYJ').
airport('Calgary', 'YYC').
airport('Lethbridge', 'YQL').
airport('Kamloops', 'YKA').

% flight(DeptAC, ArrAC)
% ---------------------
% as a fact, states there is a direct flight between the
%    departure airport and arrival airport,
% under the given flight code (e.g. "AC123")
flight('YCD', 'YYC').
flight('YCD', 'YVR').
flight('YKA', 'YQL').
flight('YKA', 'YYC').
flight('YQL', 'YKA').
flight('YQL', 'YVR').
flight('YQL', 'YYC').
flight('YYJ', 'YVR').
flight('YYJ', 'YYC').
flight('YVR', 'YYC').
flight('YVR', 'YQL').
flight('YVR','YCD').
flight('YVR','YYJ').
flight('YYC', 'YQL').
flight('YYC', 'YKA').
flight('YYC','YCD').
flight('YYC', 'YYJ').
flight('YYC', 'YVR').

% flights(DeptAC, ArrAC)
% ----------------------
% as a rule, finds a sequence (list) of flights connecting
%    the departure airport to the arrival airport

% direct flight
flights(D,A) :- airport(Dname,D), airport(Aname,A),
   flight(D,A), format("Direct flight ~w(~w) to ~w(~w)~n",[Dname,D,Aname,A]).

% one-stop
flights(D,A) :-
   flight(D,I), I \= A, flight(I,A), airport(Dname,D), airport(Iname,I), airport(Aname,A),
   format("Flight ~w(~w) to ~w(~w) via ~w(~w)~n", [Dname,D,Aname,A,Iname,I]).

% two-stop
flights(D,A) :-
   flight(D,I), I \= A, flight(I,J), J \= A, J \= D, flight(J,A), airport(Dname,D),
   airport(Aname,A), airport(Iname,I), airport(Jname,J),
   format("Flight ~w(~w) to ~w(~w) via ~w(~w) and ~w(~w)~n", [Dname,D,Aname,A,Iname,I,Jname,J]).

% flights(DeptCity, ArrCity)
% --------------------------
% run a flights query, but starting with the city name (translate to airport codes)
flights(DC,AC) :- airport(DC,D), airport(AC,A), flights(D,A).
