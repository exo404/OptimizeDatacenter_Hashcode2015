import pulp

def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    #Legge il file di input e restituisce il numero di righe di slot, gli slot non disponibili, il numero di pool e il numero di server da allocare
    R, S, U, P, M = map(int, lines[0].strip().split())
    unavailable_slots = []

    #Legge gli slot non disponibili
    for i in range(1, U + 1):
        unavailable_slots.append(tuple(map(int, lines[i].strip().split())))

    #Legge i server
    servers = []
    for i in range(U + 1, U + 1 + M):
        servers.append(tuple(map(int, lines[i].strip().split())))
    
    return R, S, U, P, M, unavailable_slots, servers

def solve_optimization(R, S, U, P, M, unavailable_slots, servers):
    # Crea il problema di PLI
    prob = pulp.LpProblem("MaximizeGuaranteedCapacity", pulp.LpMaximize)

    # Variabili decisionali:
    # x[i][r][s] = 1 se il server i è piazzato alla riga r e slot s
    x = pulp.LpVariable.dicts("x", (range(M), range(R), range(S)), 0, 1, pulp.LpBinary)

    # y[i][p] = 1 se il server i è assegnato il pool p
    y = pulp.LpVariable.dicts("y", (range(M), range(P)), 0, 1, pulp.LpBinary)

    # min_guaranteed_capacity[p] per rappresentare la minima capacità garantita del pool p
    min_guaranteed_capacity = pulp.LpVariable.dicts("min_guaranteed_capacity", (range(P)), lowBound=0)
    
    # Vincoli: 
    # Ogni server deve essere assegnato a un solo slot e un solo pool
    for i in range(M):
        prob += pulp.lpSum(x[i][r][s] for r in range(R) for s in range(S)) == 1
        prob += pulp.lpSum(y[i][p] for p in range(P)) == 1

    # Ogni server deve essere assegnato a uno slot disponibile e deve essere piazzato in una riga con spazio sufficiente
    for r, s in unavailable_slots:
        for i in range(M):
            prob += x[i][r][s] == 0

    for i, (size, _) in enumerate(servers):
        for r in range(R):
            for s in range(S):
                if s + size > S: 
                    for offset in range(size):
                        if s + offset < S:
                            prob += x[i][r][s + offset] == 0

    # Ogni slot può contenere al massimo un server
    for r in range(R):
        for s in range(S):
            prob += pulp.lpSum(x[i][r][s] for i in range(M)) <= 1

    # Funzione: Massimizza la capacità minima garantita su ogni pool
    for p in range(P):
        total_capacity = pulp.lpSum(servers[i][1] * y[i][p] for i in range(M))
        for r in range(R):
            if y[i][p] == 1:
                row_capacity = pulp.lpSum(servers[i][1] * x[i][r][s] for i in range(M) for s in range(S))
            prob += min_guaranteed_capacity[p] <= total_capacity - row_capacity
    prob += pulp.lpSum(min_guaranteed_capacity[p] for p in range(P))

    # Risolvi il problema
    prob.solve()

    # Output
    allocation = []
    for i in range(M):
        assigned = False
        for r in range(R):
            for s in range(S):
                if pulp.value(x[i][r][s]) == 1:
                    for p in range(P):
                        if pulp.value(y[i][p]) == 1:
                            allocation.append((r, s, p))
                            assigned = True
                            break
                if assigned:
                    break
            if assigned:
                break
        if not assigned:
            allocation.append('x')
    return allocation

def write_output(allocation, file_path):
    with open(file_path, 'w') as f:
        for item in allocation:
            if item == 'x':
                f.write('x\n')
            else:
                f.write(f"{item[0]} {item[1]} {item[2]}\n")

def main(input_file, output_file):
    R, S, U, P, M, unavailable_slots, servers = read_input(input_file)
    allocation= solve_optimization(R, S, U, P, M, unavailable_slots, servers)
    write_output(allocation, output_file)

input_file = './input.in'
output_file = './hashcode_2015_qualification_round.out'
main(input_file, output_file)
