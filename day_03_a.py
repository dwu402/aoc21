input_file = 'inputs/day_3.input'

def count(nums, counts):
    for i, bit in enumerate(nums):
        counts[i][int(bit)] += 1
    
def count_cols(data):
    counts = [{0: 0, 1: 0} for _ in data[0]]
    for line in data:
        count(line, counts)
    return counts

def gamma_epsilon(count_dict):
    if count_dict[0] > count_dict[1]:
        return 0, 1
    
    return 1, 0

def bin2dec(bin_list):
    val = 0
    for i, bit in enumerate(bin_list[::-1]):
        val += 2**i * bit
    return val

def get_ge(data):
    counts = count_cols(data)
    ges = [gamma_epsilon(cd) for cd in counts]
    gammas, epsilons = zip(*ges)
    gamma = bin2dec(gammas)
    epsilon = bin2dec(epsilons)

    return gamma, epsilon

if __name__ == '__main__':
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')
    gamma, epsilon = get_ge(data)
    print(gamma*epsilon)