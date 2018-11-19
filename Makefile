IBM_PATH = '/opt/ibm/ILOG/CPLEX_Studio128/cplex/bin/x86-64_linux/cplex'
MODEL = src/tp.mod
DATA = src/tp.dat
CPLEX_MODEL = /tmp/tp.lp
CPLEX_OUTPUT = /tmp/cplex.sol
GLPK = glpsol

check:
	$(GLPK) --check --model $(MODEL)

migrate:
	$(GLPK) --check --model $(MODEL) --data $(DATA) --wlp $(CPLEX_MODEL)

cplex:
	rm -f $(CPLEX_OUTPUT)
	$(IBM_PATH) -c "read $(CPLEX_MODEL)" "optimize" "write $(CPLEX_OUTPUT)"
	rm -f cplex.log

.PHONY: check
