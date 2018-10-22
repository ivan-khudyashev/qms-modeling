all:
	echo "<all> target in development ..."

install: prerequest python_install

prerequest: python_install
	python -m pip install numpy scipy matplotlib ipython jupyter pandas sympy nose

python_install:
	echo "<python_install> target in development ..."
