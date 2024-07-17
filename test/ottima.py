import gurobipy as gp
from gurobipy import GRB

def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    R, S, U, P, M = map(int, lines[0].strip().split())
    unavailable_slots = []

    for i in range(1, U + 1):
        unavailable_slots.append(tuple(map(int, lines[i].strip().split())))

    servers = []
    for i in range(U + 1, U + 1 + M):
        servers.append(tuple(map(int, lines[i].strip().split())))

    return R, S, U, P, M, unavailable_slots, servers

#path = "hashcode_2015_qualification_round.in"
path = "input.txt"

R, S, U, P, M, unavailable_slots, servers = read_input(path)

#Creo un modello
model = gp.Model("hashcode_pli")

# Creo le variabili di decisione
x = model.addVars(M, R, S, vtype=GRB.BINARY, name="x")
y = model.addVars(M, P, vtype=GRB.BINARY, name="y")
z = model.addVars(P, vtype=GRB.CONTINUOUS, name="z")

# Aggiungo i vincoli
model.addConstrs(gp.quicksum(x[i, r, s] for r in range(R) for s in range(S)) == 1 for i in range(M))

model.addConstrs(gp.quicksum(x[i, r, s] for i in range(M)) <= 1 for r in range(R) for s in range(S))

model.addConstrs(gp.quicksum(y[i, p] for p in range(P)) == 1 for i in range(M))

for r, s in unavailable_slots:
    for i in range(M):
        model.addConstr(x[i, r, s] == 0, f"unavailable_{i}_{r}_{s}")

for i, (size, budget) in enumerate(servers):
    for r in range(R):
        for s in range(S):
            if (s + size > S):
                for offset in range(size):
                    if (s + offset < S):
                        model.addConstr(x[i, r, s + offset] == 0, f"space_{i}_{r}_{s}")

for p in range(P):
    c_tot = gp.quicksum(servers[i][1] * y[i, p] for i in range(M))
    
    for r in range(R):
        c_row = gp.quicksum(servers[i][1] * x[i, r, s] * y[i,p] for i in range(M) for s in range(S))
        model.addConstr(z[p] <= c_tot - c_row, name="z_constr")

# Funzione obiettivo
model.setParam('OutputFlag', 1)
model.setObjective(gp.quicksum(z[p] for p in range(P)), GRB.MAXIMIZE)
model.optimize()

if model.status == GRB.OPTIMAL:
    for p in range(P):
        print(f"Capacità minima garantita per il pool {p}: {z[p].X}")
        
        
Xvals = model.getAttr('X', x)
Yvals = model.getAttr('X', y)
                
allocation = []

for i in range(M):
    assigned = False
        
    for r in range(R):
        for s in range(S):
            if Xvals[i,r,s] == 1:
                for p in range(P):
                    if Yvals[i,p] == 1:
                        allocation.append((r, s, p))
                        assigned = True
                        break
            if assigned:
                break
        if assigned:
            break
    if not assigned:
        allocation.append('x')

def write_output(allocation, file_path):
    with open(file_path, 'w') as f:
        for item in allocation:
            if item == 'x':
                f.write('x\n')
            else:
                f.write(f"{item[0]} {item[1]} {item[2]}\n")
                
write_output(allocation, "output.txt")