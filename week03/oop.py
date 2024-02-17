# neg / add / sub / mul
class Polynomial(object):

    def __init__(self, poly):
        self._poly = tuple(poly)

    # use a getter for private fields.
    def terms(self):
        return self._poly

    def __neg__(self):
        return Polynomial([(-i[0], i[1]) for i in self.terms()])

    def __add__(self, other):
        return Polynomial(self.terms() + other.terms())

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        return Polynomial([(i[0] * j[0], i[1] + j[1]) for i in self.terms() for j in other.terms()])

    def __call__(self, x):
        return sum([v1 * (x ** v2) for (v1, v2) in self._poly])

    def __str__(self):
        is_first_string = True
        final_string = ""
        for curr_tuple in self._poly:
            if is_first_string:
                if curr_tuple[0] < 0:
                    sign = '-'
                else:
                    sign = ''
                final_string = sign + self.convert(curr_tuple[0], curr_tuple[1])
                is_first_string = False
            else:
                if curr_tuple[0] < 0:
                    sign = ' -'
                else:
                    sign = ' +'
                term = " " + self.convert(curr_tuple[0], curr_tuple[1])
                final_string = final_string + sign + term
        return final_string

    def simplify(self):
        dictionary = {0: 0}
        for curr_tuple in self._poly:
            if curr_tuple[1] not in dictionary:
                dictionary[curr_tuple[1]] = curr_tuple[0]
            else:
                dictionary[curr_tuple[1]] = dictionary[curr_tuple[1]] + curr_tuple[0]
            modified_list = [(dictionary[key], key) for key in dictionary if dictionary[key] != 0]
            modified_list.sort(key=lambda y: y[1], reverse=True)
        if len(modified_list) == 0:
            self._poly = ((0, 0),)
        else:
            self._poly = tuple(modified_list)

    def convert(self, input1, input2):
        input1 = abs(input1)
        input1_string = str(input1)
        input2_string = "^" + str(input2)
        helper_string = "x"
        if input2 == 0:
            helper_string = ""
            input2_string = ""
            return input1_string + helper_string + input2_string
        if input2 == 1:
            helper_string = "x"
            input2_string = ""
        if input1 == 1:
            input1_string = ""
            helper_string = "x"
        return input1_string + helper_string + input2_string


# call
p = Polynomial([(2, 1), (1, 0)])
print([p(x) for x in range(5)])
# [1, 3, 5, 7, 9]
#
# simplify
p = Polynomial([(2, 1), (1, 0)])
q = -p + (p * p)
print(q.terms())
# ((-2, 1), (-1, 0), (4, 2), (2, 1), (2, 1), (1, 0))
q.simplify()
print(q.terms())
# ((4, 2), (2, 1))
#
# str
p = Polynomial([(1, 1), (1, 0)])
qs = (p, p + p, -p, -p - p, p * p)
for q in qs:
    q.simplify()
    print(q)
# ...
# 'x + 1'
# '2x + 2'
# '-x - 1'
# '-2x - 2'
# 'xˆ2 + 2x + 1'
# ...

p = Polynomial([(0, 1), (2, 3)])
print(p)
print(p * p)
print(-p * p)
# '0x + 2xˆ3'
# '0xˆ2 + 0xˆ4 + 0xˆ4 + 4xˆ6'
# '0xˆ2 + 0xˆ4 + 0xˆ4 - 4xˆ6'
