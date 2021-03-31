# luhn algorithm

def luhn(x):

	*digits, check = list(x)

	s = 0

	for i, digit in enumerate(digits[::-1]):

		if not i % 2: digit = str(int(digit) * 2)

		if len(digit) > 1: digit = sum(map(int, digit))

		s += int(digit)

	s += int(check)

	return s % 10 == 0
