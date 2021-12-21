import numpy as np

input_file = 'test.input'
# input_file = 'inputs/day_20.input'

hotmap = {
    '#': 1,
    '.': 0,
}

def parse(Niter):
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')

    code = np.array(list(map(hotmap.get, data[0].strip())))

    body = [x.strip() for x in data[2:]]

    # todo
    # convert body to correct size image
    sz = len(body) + 2*(Niter+1), len(body[0]) + 2*(Niter+1)
    image = np.zeros(sz)


    image[Niter+1:len(body)+Niter+1, Niter+1:len(body[0])+Niter+1] = np.array([list(map(hotmap.get, x)) for x in body])

    return code, image

kernel = np.array([2**i for i in reversed(range(9))])
def pix(A, i, j):
    M, N = np.shape(A)
    s = np.array([
        A[i-1, j-1], A[i-1, j  ], A[i-1, (j+1)%N],
        A[i  , j-1], A[i  , j  ], A[i  , (j+1)%N],
        A[(i+1)%M, j-1], A[(i+1)%M, j  ], A[(i+1)%M, (j+1)%N],
    ])
    return (kernel @ s).astype(int)

# def kernel(N):
#     kernel = np.zeros(2*N+3)
#     kernel[:3] = [1, 2, 4]
#     kernel[N:N+3] = [8, 16, 32]
#     kernel[2*N:2*N+3] = [64, 128, 256]
#     return kernel

# def rep_c(i, c):
#     z0 = c[0]
#     z1 = c[-1]
#     return z0 * (1 - (z1 > 0) * (i%2))

# def next_A(A, c, k, i, N, Niter):
#     z = c[np.convolve(A, k, 'same').astype(int)].reshape((-1, N+2*(Niter+1)))
#     nA = np.ones_like(z) * rep_c(i, c)
#     nA[Niter-i:-(Niter-i), Niter-i:-(Niter-i)] = z[Niter-i:-(Niter-i), Niter-i:-(Niter-i)]
#     return nA.flatten()

def next_A(A, c):
    M, N = A.shape
    z = np.array([[pix(A, i, j) for j in range(N)] for i in range(M)]).flatten()
    return c[z].reshape((M, N))

def pprint(A):
    for row in A:
        print(''.join(['#' if x else '.' for x in row]))
    print()

def part_a():
    Niter = 2
    c, A = parse(Niter)

    for i in range(Niter):
        # pprint(A)
        A = next_A(A, c)

    # pprint(A)

    return A.sum()

def part_b():
    Niter = 50
    c, A = parse(Niter)

    for i in range(Niter):
        # pprint(A)
        A = next_A(A, c)

    # pprint(A)

    return A.sum()


if __name__ == "__main__":
    print(part_a())
    print(part_b())