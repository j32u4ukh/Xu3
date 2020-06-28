class Config:
    def __init__(self, dictionary):
        self.__dict__.update(dictionary)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return self.__dict__.__str__()

    __repr__ = __str__

    def items(self):
        for key, value in self.__dict__.items():
            yield key, value


if __name__ == "__main__":
    d = dict(a=123, b=456)
    config = Config(d)
    print("config.a:", config.a)
    print("config.b:", config.b)
    config.c = 789
    print("config.c:", config.c)
    del config.b
    print(config)

    for key, value in config.items():
        print(key, value)
