import numpy as np
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn import metrics

def handle_arguments():
    # Create the parser and add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('inputFiles',
                        metavar='inputFiles',
                        type=Path,
                        nargs='+',
                        help='saved numpy array trace representations'
                        )

    # Parse and print the results
    args = parser.parse_args()
    return args.inputFiles


def correlate(numpy_arrays):
    print(numpy_arrays)
    confusion_matrix = np.array([[8,  89], [101, 802]])
    cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=[False, True])

    cm_display.plot()
    plt.show()


def main():
    numpy_arrays = list()
    input_files = handle_arguments()
    for input_file in input_files:
        input_path = Path(input_file).resolve()
        if not input_path.exists():
            print("ERROR: " + str(input_path) + "does not exist")
        input_file_name = input_path.name
        numpy_arrays.append(np.load(input_file_name))

    correlate(numpy_arrays)


if __name__ == '__main__':
    main()


