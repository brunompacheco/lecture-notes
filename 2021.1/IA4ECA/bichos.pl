% Premissas
cores(amarelo).

pele(X) :- animal(X).

animal(X) :- peixe(X).
animal(X) :- passaro(X).
animal(X) :- mamifero(X).

nadadeiras(X) :- peixe(X).
nadar(X) :- peixe(X).

asas(X) :- passaro(X).
voar(X) :- passaro(X), \+ avestruz(X).

ovos(X) :- peixe(X), \+ tubarao(X).
ovos(X) :- passaro(X).
% \+ ovos(X) :- mamifero(X).

andar(X) :- mamifero(X), \+ morcego(X).

peixe(X) :- tubarao(X).
peixe(X) :- salmao(X).

passaro(X) :- canario(X).
passaro(X) :- avestruz(X).

mamifero(X) :- vaca(X).
mamifero(X) :- morcego(X).

delicia(X) :- salmao(X).
cor(X, amarelo) :- canario(X).
andar(X) :- avestruz(X).
leite(X) :- vaca(X).
carne(X) :- vaca(X).
voar(X) :- morcego(X).

% Específicas
canario(piupiu).
peixe(nemo).
tubarao(tutu).
vaca(mimosa).
morcego(vamp).
avestruz(xica).
salmao(alfred).

% Perguntas
?- voar(piupiu).
?- cor(piupiu, X).
?- voar(xica).
?- asas(xica).
?- voar(vamp).
?- asas(vamp).
?- ovos(vamp).
?- ovos(X), animal(X).
?- carne(X), animal(X).
?- andar(X), animal(X).
?- nadar(X), \+ ovos(X), animal(X).