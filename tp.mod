# Conjuntos
set EVENTOS;
set JORNADA;
set DEPORTES;

param CALIDAD {e in EVENTOS};
param INICIO {e in EVENTOS};
param FIN {e in EVENTOS};
param HORA {j in JORNADA};
param INTERCALABLE {e in EVENTOS};
param DEPORTE_EVENTO {d in DEPORTES, e in EVENTOS};
param BONO_FINAL {e in EVENTOS};
param ES_FINAL {e in EVENTOS};

var tr{e in EVENTOS} >= 0, binary;
var y{e in EVENTOS, j in JORNADA} >= 0, binary;

maximize z: sum{e in EVENTOS} tr[e] * ( CALIDAD[e] + BONO_FINAL[e] );

# Demandas.
s.t. inicio {e in EVENTOS, j in JORNADA}: HORA[j] >= INICIO[e] * y[e, j];
s.t. fin {e in EVENTOS, j in JORNADA}: FIN[e] >= (HORA[j] + 1) * y[e, j];
s.t. y_inf {e in EVENTOS}: sum{j in JORNADA} y[e, j] >= (FIN[e] - INICIO[e]) * tr[e];
s.t. y_sup {e in EVENTOS}: sum{j in JORNADA} y[e, j] <= (FIN[e] - INICIO[e]) * tr[e];
s.t. evento_hora {j in JORNADA}: sum{e in EVENTOS} y[e, j] * INTERCALABLE[e] <= 2;
s.t. transmision_final {d in DEPORTES}: sum{e in EVENTOS} tr[e] * DEPORTE_EVENTO[d, e] * (1 - ES_FINAL[e]) >= sum{e in EVENTOS} tr[e] * DEPORTE_EVENTO[d, e] * ES_FINAL[e];

# Data Section
data;
set EVENTOS 	:=  ARQ1 ARQ2 ATL1 ATL2 BAD1 BAD2;
set DEPORTES 	:=  ARQ ATL BAD;
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


param BONO_FINAL		:=
ARQ1									0
ARQ2									10
ATL1									0
ATL2									15
BAD1									0
BAD2									20;

param ES_FINAL				:=
ARQ1									0
ARQ2									1
ATL1									0
ATL2									1
BAD1									0
BAD2									1;

param DEPORTE_EVENTO:	ARQ1	ARQ2	ATL1	ATL2	BAD1	BAD2 :=
ARQ 									1			1			0			0			0			0
ATL 									0			0			1			1			0			0
BAD 									0			0			0			0			1			1;


