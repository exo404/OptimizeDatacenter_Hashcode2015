def read_input(file_path_opt, file_path_greedy):
    opt = 0
    greedy = 0
    with open(file_path_opt, 'r') as o:
        opt = int(o.readlines()[0])
    with open(file_path_greedy, 'r') as g:
        greedy = int(g.readlines()[0])
    return opt, greedy

def gap_calc(opt, greedy):
    gap = (opt - greedy) / opt * 100
    return gap

opt, greedy = read_input('input_output/score_opt.txt', 'input_output/score_greedy.txt')
gap = int(gap_calc(opt, greedy))
print(f"Gap: {gap}%")
      
