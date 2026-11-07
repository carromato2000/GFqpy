.PHONY: test, clean

clean:
	rm -rf __pycache__ src/__pycache__ src/test/__pycache__

test:
	python3 -m unittest discover -s src/test -p "test*.py"

testPoly:
	python3 -m unittest discover -s src/test -p "testPolynomial.py"

testPrimeField:
	python3 -m unittest discover -s src/test -p "testPrimeField.py"