import torch as t
import numpy as np


def main():
    # pytorch_corrcoef()
    # numpy_correlate()
    # numpy_correlate_random()
    numpy_fft2()


def pytorch_corrcoef():
    device = "cuda:0" if t.cuda.is_available() else "cpu"

    print(device)
    tensor1 = t.Tensor([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10.0, 0.0])
    tensor2 = t.Tensor([0.0, -5.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    tensor1 = tensor1.to(device)
    tensor2 = tensor2.to(device)
    tensor3 = t.stack((tensor1, tensor2))

    print(tensor3.device)
    print(tensor3.data)

    result = t.corrcoef(tensor3)

    print(result.device)
    print(result.data)


def numpy_correlate():
    array1 = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10.0, 0.0])
    array2 = np.array([0.0, -5.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    result = np.correlate(array1, array2, mode="full")

    print(result)


def numpy_correlate_random():
    array1 = np.random.rand(100)
    array2 = np.random.rand(100)

    result = np.correlate(array1, array2, mode="full")

    print(result)


def numpy_fft2():
    array1 = np.load("traces/rsa_GCC_funroll-all-loops_trace.npy")
    array2 = np.load("traces/rsa_GCC_O0_trace.npy")

    result1 = np.fft.fft2(array1)

    for what in array1:
        print(what)
    print(array1)
    print(result1)

if __name__ == '__main__':
    main()
