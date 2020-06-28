def decorator(func):
    def inner():
        print("func: {}".format(func.__name__))
        func()

    return inner


def check_value(check_type="bigger"):
    def decorator(func):
        def parameters(val1, val2):
            if check_type == "bigger":
                assert val1 > val2, "val1 should bigger than val2."
            elif check_type == "smaller":
                assert val1 > val2, "val1 should smaller than val2."

            exec_func = func(val1, val2)
            return exec_func

        return parameters

    return decorator


@check_value()
def func1(val1, val2):
    print(f"func1: {val1}, {val2}")


@decorator
def func2():
    print("decorator test")


class Decorator:
    def __init__(self):
        self.message = "decorator of class method."
        self.num = 0
        self.mode = "bigger"

    def decorator_test(func):
        def decorator(self, *args, **kwargs):
            print(self.message)
            func(self, *args, **kwargs)

        return decorator

    @decorator_test
    def test(self, plus):
        self.num += plus
        print(f"self.num: {self.num}")

    def decorator_test2(func):
        def decorator(self, val1, val2):
            # print(self.message)
            if self.mode == "bigger" and (val1 < val2):
                print("val1 should bigger than val2.")

            func(self, val1, val2)

        return decorator

    @decorator_test2
    def test2(self, val1, val2):
        print(f"mode: {self.mode}, val1: {val1}, val2: {val2}")


if __name__ == "__main__":

    func1(5, 49)
    func2()
    doctor = Decorator()
    for i in range(5):
        for j in range(5):
            doctor.test2(i, j)
