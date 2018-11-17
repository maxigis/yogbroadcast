# CONJUNTOS

set DIAS;
set CANALES;
set HORAS;
set DEPORTES;
set SEDES;
set PERIODISTAS;
set EVENTOS;

# Definicion de Parametros

# Parametro Auxiliar
param BLOQUES {h in HORAS}

# Parametros por deporte
param INTERCALABLE {d in DEPORTES};
param CALIDAD {d in DEPORTES};
param AUMENTO_ESPECIAL {d in DEPORTES};
param AUMENTO_FINAL {d in DEPORTES};
param PUEDE_CUBRIR {p in PERIODISTAS, d in DEPORTES};
param ESPECIALISTA {p in PERIODISTAS, d in DEPORTES};

# Parametros por eventos
param COMIENZO {e in EVENTOS};
param FIN {e in EVENTOS};
param DUR {e in EVENTOS};
param ES_FINAL {e in EVENTOS};
param ES_SEDE {e in EVENTOS, s in SEDES};
param DEP_EVENTO {e in EVENTOS, d in DEPORTES};
