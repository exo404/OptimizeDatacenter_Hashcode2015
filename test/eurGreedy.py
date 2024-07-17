import math

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

path = "hashcode_2015_qualification_round.in"
#path = "input.in"

class Server(object):

    def __init__(self, number, size, capacity):
        self.number = number
        self.size = size
        self.capacity = capacity
        self.slot = -1
        self.row = -1
        self.pool = -1

    def __str__(self):
        return 'size: %d, cap: %d, ratio: %.02f, (%d,%d), pool=%d' % (
            self.size, self.capacity, self.ratio, self.slot, self.row,
            self.pool)

    @property
    def ratio(self):
        return float(self.capacity) / float(self.size)


class DataCenter(object):

    def __init__(self, R, S, unavailable_slots, P, M, servers):
        self.R = R
        self.S = S
        self.unavailable_slots = unavailable_slots
        self.P = P
        self.M = M
        self.grid = [[0 for _ in range(S)] for _ in range(R)]
        self.servers = servers
        self.servers.sort(key=lambda x: x.ratio, reverse=True)
        self.pools_capacity = [0 for _ in range(P)]

    def init_grid(self):
        for r, s in self.unavailable_slots:
            self.grid[r][s] = -1
    def put_servers(self):
        for i in range(self.M):
            for r in range(self.R):
                for s in range(self.S):
                    if self.servers[i].row != -1:
                        break
                    if self.grid[r][s] != 0:
                        continue
                    if s + self.servers[i].size > self.S:
                        continue
                    can_place = True
                    for offset in range(self.servers[i].size):
                        if self.grid[r][s + offset] != 0:
                            can_place = False
                            break
                    if not can_place:
                        continue
                    print(f"Server {i} with ratio {self.servers[i].ratio} allocated at ({r},{s})")
                    self.servers[i].row = r
                    self.servers[i].slot = s
                    for offset in range(self.servers[i].size):
                        self.grid[r][s + offset] = 1  
                    break
    def server_to_pools(self):
        min_capacity = 1000
        for i in range(self.M):
            if self.servers[i].pool != -1:
                    break
            for p in range(self.P):
                if self.pools_capacity[p] <= min_capacity:
                    min_pool = p
                    min_capacity = self.pools_capacity[p] + servers[i].capacity
            self.servers[i].pool = min_pool
            self.pools_capacity[min_pool] += self.servers[i].capacity
            print(f"Server {i} allocated at pool {min_pool}")
    def minimum_guaranteed_capacity(self):
        z = [0 for p in range(self.P)]
        for p in range (self.P):
            c_tot = sum(servers[i].capacity for i in range(self.M) if servers[i].pool == p)
            for r in range(self.R):
                c_row = sum(servers[i].capacity for i in range(self.M) if servers[i].pool == p and servers[i].row == r)
            z[p] = c_tot - c_row
            print(f"Pool {p} has minimum guaranteed capacity {z[p]}")
                
                    

R, S, U, P, M, unavailable_slots, serversData = read_input(path)
servers = [Server(i, size, capacity) for i, (size, capacity) in enumerate(serversData)]
datacenter = DataCenter(R, S, unavailable_slots, P, M, servers)
datacenter.init_grid()
datacenter.put_servers()
datacenter.server_to_pools()
for p in range(P):
    print(f"Pool {p} has capacity {datacenter.pools_capacity[p]}")
datacenter.minimum_guaranteed_capacity()           

def write_output(allocation, file_path):
    with open(file_path, 'w') as f:
        for item in allocation:
            if item == 'x':
                f.write('x\n')
            else:
                f.write(f"{item[0]} {item[1]} {item[2]}\n")
                