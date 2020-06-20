import os


def modifyPickle4Windows(_origin_path, _new_path):
    """
    錯誤訊息:
    _pickle.UnpicklingError: the STRING opcode argument must be quoted

    說明：
    換行符號切換 for windows user: \r\n -> \n
    """
    with open(_origin_path, "rb") as input_file:
        lines = input_file.readlines()

        with open(_new_path, "wb") as output_file:
            for line in lines:
                line = line.replace(b'\r', b'').replace(b'\n', b'')
                output_file.write(line + b'\n')

    print("[dos2Unix done] {} -> {}".format(os.path.basename(_origin_path),
                                            os.path.basename(_new_path)))


def moduleNotFoundAfterRunSetup():
    """
    錯誤訊息:
    ModuleNotFoundError: No module named 'XXX'

    說明：
    在執行 python setup.py build_ext --inplace 後，PyCharm 當中的 module 連結出現異常導致無法 import。

    參考來源：
    無
    """
    print("""我將原專案移出，PyCharm 會先出現 VCS 錯誤，因為原本有透過 git 在進行管理。
    將該錯誤排除後，再次將原專案移入，讓 PyCharm 重新產生 module 的連結便可正常運行。
    
    專案移出後我有在其他資料夾下再次開啟，確定可以正常運作後才移回原資料夾。""")


if __name__ == "__main__":
    origin_path = r"D:\PycharmProjects\NeuralNetwork\OpenEyes\FastObjectLocalization\Data\CLASSES.pkl"
    new_path = r"D:\PycharmProjects\NeuralNetwork\OpenEyes\FastObjectLocalization\Data\AdjClasses.pkl"
    modifyPickle4Windows(origin_path, new_path)
