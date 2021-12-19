input_file = "inputs/day_1.input"

def num_times_increasing(depth_list):
    count = 0
    for a, b in zip(depth_list[:-1], depth_list[1:]):
        count += int(b > a)
    return count

if __name__ == "__main__":
    with open(input_file, 'r') as fp:
        data = fp.read().strip()

    depth_list = [int(x) for x in data.split()]
    print(num_times_increasing(depth_list))