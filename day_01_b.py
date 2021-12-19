input_file = "inputs/day_1.input"

def num_times_increasing(depth_list):
    count = 0
    a = sum(depth_list[:3])
    for i in range(1, len(depth_list) - 2):
        b = sum(depth_list[i:i+3])
        count += int(b > a)
        a = b
    return count


if __name__ == "__main__":
    with open(input_file, 'r') as fp:
        data = fp.read().strip()

    depth_list = [int(x) for x in data.split()]
    print(num_times_increasing(depth_list))