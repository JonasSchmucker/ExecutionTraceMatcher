import numpy as np
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn import metrics
import scipy.signal as signal
import progressbar


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

    # Parse and print the results
    args = parser.parse_args()
    return args.inputFiles, args.inputdir


def conv(array_a: np.array, array_b: np.array) -> float:
    return np.average(signal.correlate(array_a, array_b, mode="full"))


def correlate(numpy_arrays):

    bar = progressbar.ProgressBar(maxval=len(numpy_arrays) * len(numpy_arrays)).start()

    cm = np.zeros((len(numpy_arrays), len(numpy_arrays)))
    progress = 0
    for (i, array_a) in enumerate(numpy_arrays):
        for (o, array_b) in enumerate(numpy_arrays):
            if array_a is not array_b:
                cm[i][o] = conv(array_a, array_b)
            progress += 1
            bar.update(progress)
    return cm


def load_numpy_arrays() -> (list, list):
    numpy_arrays = list()
    numpy_arrays_names = list()
    input_files, input_directory = handle_arguments()
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

    return numpy_arrays, numpy_arrays_names


def main():
    numpy_arrays, numpy_arrays_names = load_numpy_arrays()
    cm = correlate(numpy_arrays)

    cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=numpy_arrays_names)

    cm_display.plot(xticks_rotation=45.0)
    plt.show()


if __name__ == '__main__':
    main()


