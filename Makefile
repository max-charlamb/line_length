
default:
	pyinstaller --onefile line_length.py
	chmod +x ./dist/line_length
	sudo ln -s /Users/maxcharlamb/Documents/GitHub/line_length/dist/line_length /usr/local/bin

clean:
	sudo rm /usr/local/bin/line_length
	rm -rf __pycache__ build dist line_length.spec