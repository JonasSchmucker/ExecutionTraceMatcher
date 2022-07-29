import numpy as np
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
from numpy import number
from sklearn import metrics
import scipy
import scipy.signal as signal
import progressbar

mode_dict = {
    1: "Comparing function traces based on scipy.correlate()",
    2: "Comparing function traces based on scipy two-dimensional Fourier transform",
    3: "Comparing function traces elementwise",
}


def handle_arguments():
    # Create the parser and add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('inputFiles',
                        metavar='inputFiles',
                        type=Path,
                        nargs='*',
                        help='saved numpy array trace representations'
                        )

    parser.add_argument('-r',
                        "--inputdir",
                        metavar='input_directory',
                        type=Path,
                        nargs='?',
                        default='./traces',
                        help='directory containing saved numpy array trace representations'
                        )

    parser.add_argument('-m',
                        "--mode",
                        metavar='mode',
                        type=int,
                        nargs='?',
                        default=1,
                        help='determines which mode will be used to correlate the function traces. '
                             'Valid modes are ' + str(list(mode_dict.keys()))
                        )

    # Parse and print the results
    args = parser.parse_args()
    return args.inputFiles, args.inputdir, args.mode


def correlate(numpy_arrays, mode):
    print("Loading chosen mode...  ", end="")
    print(mode_dict.get(mode, "mode " + str(mode) + " is invalid. "
                                                    "Valid modes are " + str(list(mode_dict.keys()))))
    if mode == 1:
        return correlate_scipy_correlate(numpy_arrays)
    elif mode == 2:
        return correlate_scipy_fft2(numpy_arrays)
    elif mode == 3:
        return correlate_numpy_equal(numpy_arrays)
    else:
        return np.zeros((len(numpy_arrays), len(numpy_arrays)))


def correlate_numpy_equal(numpy_arrays):
    bar = progressbar.ProgressBar(maxval=len(numpy_arrays) * len(numpy_arrays)).start()

    cm = np.zeros((len(numpy_arrays), len(numpy_arrays)))
    progress = 0
    for (i, array_a) in enumerate(numpy_arrays):
        for (o, array_b) in enumerate(numpy_arrays):
            if i < o:
                cm[i][o] = cm[o][i] = 1 if np.array_equal(array_a, array_b) else 0
            progress += 1
            bar.update(progress)
    print()
    return cm


def correlate_scipy_fft2(numpy_arrays):
    max_cols = 0
    max_rows = numpy_arrays[0].shape[1]
    for array in numpy_arrays:
        if max_cols < array.shape[0]:
            max_cols = array.shape[0]

    bar = progressbar.ProgressBar(maxval=len(numpy_arrays)).start()

    progress = 0
    numpy_arrays_fourier_transforms = list()
    for array in numpy_arrays:
        numpy_arrays_fourier_transforms.append(
            scipy.fft.fft2(array, s=(max_cols, max_rows), axes=(-2, -1))
        )
        progress += 1
        bar.update(progress)
    print()

    print(numpy_arrays_fourier_transforms[0])

    bar = progressbar.ProgressBar(maxval=len(numpy_arrays) * len(numpy_arrays)).start()
    progress = 0
    cm = np.zeros((len(numpy_arrays), len(numpy_arrays)))

    debug_string = ""

    for (i, array_a) in enumerate(numpy_arrays_fourier_transforms):
        for (o, array_b) in enumerate(numpy_arrays_fourier_transforms):
            if i < o:
                if i == 0 and o == 1:
                    array_c = array_a - array_b
                # TODO switch absolute average
                average = np.average(array_a - array_b)
                absolute_average = np.absolute(average)
                inverse = 1.0 / absolute_average
                cm[i][o] = cm[o][i] = inverse
                debug_string += ("i: " + str(i) + "\to: " + str(o) + "\tinverse: " + str(inverse) + "\n")
            progress += 1
            bar.update(progress)
    print()
    print(debug_string)
    print(array_c)
    return cm


def correlate_scipy_correlate(numpy_arrays):
    bar = progressbar.ProgressBar(maxval=len(numpy_arrays) * len(numpy_arrays)).start()

    cm = np.zeros((len(numpy_arrays), len(numpy_arrays)))
    progress = 0
    for (i, array_a) in enumerate(numpy_arrays):
        for (o, array_b) in enumerate(numpy_arrays):
            if i < o:
                cm[i][o] = cm[o][i] = np.average(signal.correlate(array_a, array_b, mode="full"))
            progress += 1
            bar.update(progress)
    print()
    return cm


def load_numpy_arrays() -> (list, list):
    numpy_arrays = list()
    numpy_arrays_names = list()
    input_files, input_directory, mode = handle_arguments()
    for input_file in input_files:
        input_path = Path(input_file).resolve()
        if not input_path.exists():
            print("ERROR: " + str(input_path) + "does not exist")
            break
        if not input_path.match("*.npy"):
            print("ERROR: " + str(input_path) + "is not a numpy array file")
            break
        input_file_name = input_path.name
        numpy_arrays.append(np.load(input_file_name))
        numpy_arrays_names.append(input_file_name)

    input_directory_path = Path(input_directory).resolve()
    if not input_directory_path.exists():
        print("ERROR: " + str(input_directory_path) + "does not exist")
    else:
        print("Loading directory " + input_directory_path.name)
        for input_path in input_directory_path.iterdir():
            if not input_path.match("*.npy"):
                print("ERROR: " + str(input_path) + " is not a numpy array file")
                break
            input_file_name = input_path.name
            numpy_arrays.append(np.load(input_directory_path.name + "/" + input_file_name))
            numpy_arrays_names.append(input_file_name)

    return numpy_arrays, numpy_arrays_names, mode


def main():
    numpy_arrays, numpy_arrays_names, mode = load_numpy_arrays()
    if len(numpy_arrays) == 0:
        print("ERROR: No Function Traces could be loaded")
        return

    for trace in numpy_arrays:
        print(trace.shape)

    cm = correlate(numpy_arrays, mode)
    print("Generating Heatmap")
    cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=numpy_arrays_names)

    cm_display.plot(xticks_rotation=45.0)
    plt.show()


if __name__ == '__main__':
    main()
