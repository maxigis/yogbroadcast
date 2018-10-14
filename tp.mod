# Conjuntos
set EVENTOS;
set JORNADA;

param CALIDAD {e in EVENTOS};
param INICIO {e in EVENTOS};
param FIN {e in EVENTOS};
param HORA {j in JORNADA};
param INTERCALABLE {e in EVENTOS};

var tr{e in EVENTOS} >= 0, binary;
var y{e in EVENTOS, j in JORNADA} >= 0, binary;

maximize z: sum{e in EVENTOS} CALIDAD[e] * tr[e];

# Demandas.
s.t. inicio {e in EVENTOS, j in JORNADA}: HORA[j] >= INICIO[e] * y[e, j];
s.t. fin {e in EVENTOS, j in JORNADA}: FIN[e] >= (HORA[j] + 1) * y[e, j];
s.t. y_inf {e in EVENTOS}: sum{j in JORNADA} y[e, j] >= (FIN[e] - INICIO[e]) * tr[e];
s.t. y_sup {e in EVENTOS}: sum{j in JORNADA} y[e, j] <= (FIN[e] - INICIO[e]) * tr[e];
s.t. evento_hora {j in JORNADA}: sum{e in EVENTOS} y[e, j] * INTERCALABLE[e] <= 2;

# Data Section
data;
set EVENTOS 	:=  ARQ1 ARQ2 ATL1 ATL2 BAD1 BAD2;
set JORNADA 	:=  1 2 3 4 5 6 7 8 9;

param CALIDAD :=
ARQ1					40
ARQ2					20
ATL1					60
ATL2					50
BAD1					30
BAD2					20;

param INICIO	:=
ARQ1					1
ARQ2					6
ATL1					1
ATL2					6
BAD1					4
BAD2					8;

param FIN			:=
ARQ1					4
ARQ2					9
ATL1					5
ATL2					10
BAD1					6
BAD2					10;

param HORA		:=
1							1
2							2
3							3
4							4
5							5
6							6
7							7
8							8
9							9;

param INTERCALABLE		:=
ARQ1									1
ARQ2									1
ATL1									1
ATL2									1
BAD1									2
BAD2									2;
