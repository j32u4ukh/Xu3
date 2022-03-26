class Base62:
    B62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, base10):
        self.value = Base62.base10To62(base10=base10)

    @classmethod
    def base10To62(cls, base10):
        if base10 == 0:
            return "0"

        sign = "" if base10 >= 0 else "-"
        value = ""
        base10 = abs(base10)

        while base10 != 0:
            base10, r = divmod(base10, 62)
            val = cls._base10To62(b10=r)
            value = val + value

        return sign + value

    @classmethod
    def _base10To62(cls, b10):
        assert 0 <= b10 <= 61, "idx should between 0 and 61"
        return cls.B62[b10]

    @classmethod
    def base62To10(cls, base62):
        is_negative = base62.startswith("-")

        if is_negative:
            base62 = base62[1:]

        base62 = base62[::-1]
        base10 = 0
        multiple = 1

        for b in base62:
            base10 += cls._base62To10(b62=b) * multiple
            multiple *= 62

        if is_negative:
            base10 *= -1

        return base10

    @classmethod
    def _base62To10(cls, b62):
        assert b62 in cls.B62, "b62 should in 0-9 or a-z or A-Z"
        return cls.B62.index(b62)

    def __str__(self):
        return self.value

    __repr__ = __str__

    def __eq__(self, other):
        return self.value == other.value

    # 加法
    def __add__(self, other):
        value = Base62.base62To10(base62=self.value)
        other_value = Base62.base62To10(base62=other.value)

        return Base62(base10=value + other_value)

    # 減法
    def __sub__(self, other):
        value = Base62.base62To10(base62=self.value)
        other_value = Base62.base62To10(base62=other.value)

        return Base62(base10=value - other_value)

    # 乘法
    def __mul__(self, other):
        value = Base62.base62To10(base62=self.value)
        other_value = Base62.base62To10(base62=other.value)

        return Base62(base10=int(value * other_value))

    # 除法
    def __truediv__(self, other):
        value = Base62.base62To10(base62=self.value)
        other_value = Base62.base62To10(base62=other.value)

        return Base62(base10=int(value / other_value))


if __name__ == "__main__":
    def fullTest():
        print("Start testing")

        for a in range(100):
            for b in range(100):
                if (Base62(a) + Base62(b)) != Base62(a + b):
                    print(a, b, Base62(a), Base62(b), Base62(a) + Base62(b), Base62(a + b))

        print("End testing")

    fullTest()
