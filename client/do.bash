function main() {
	if ! dpkg -s supercollider >/dev/null; then
		sudo apt install -y supercollider
	fi

	if ! grep FoxDot < <(pip freeze) >/dev/null; then
		python3 -m pip install FoxDot
	fi

	python3 main.py
}

main
