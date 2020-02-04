import os


def modifyPickle4Windows(_origin_path, _new_path):
    """換行符號切換 \r\n -> \n for windows

    錯誤訊息:
    _pickle.UnpicklingError: the STRING opcode argument must be quoted"""
    with open(_origin_path, "rb") as input_file:
        lines = input_file.readlines()

        with open(_new_path, "wb") as output_file:
            for line in lines:
                line = line.replace(b'\r', b'').replace(b'\n', b'')
                output_file.write(line + b'\n')

    print("[dos2Unix done] {} -> {}".format(os.path.basename(_origin_path),
                                            os.path.basename(_new_path)))


if __name__ == "__main__":
    origin_path = r"D:\PycharmProjects\NeuralNetwork\OpenEyes\FastObjectLocalization\Data\CLASSES.pkl"
    new_path = r"D:\PycharmProjects\NeuralNetwork\OpenEyes\FastObjectLocalization\Data\AdjClasses.pkl"
    modifyPickle4Windows(origin_path, new_path)
