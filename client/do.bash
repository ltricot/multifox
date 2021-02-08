function main() {
	if ! dpkg -s supercollider >/dev/null; then
		sudo apt install -y supercollider
	fi

	python3 -m pip install FoxDot janus
	python3 main.py
}

main
