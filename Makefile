.PHONY: setup run dev clean help docker

# Default target
all: setup run

# Setup virtual environment and install dependencies
setup:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

	@echo "Configuring supervisord..."
	# Supervisord
	#apt-get update
	sudo apt-get install -y supervisor
	#rm -rf /var/lib/apt/lists/*
	mkdir -p /etc/supervisor/conf.d
	COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
	supervisord -c /etc/supervisor/conf.d/supervisord.conf


# Run the server
run:
	@echo "Starting server..."
	python server.py



# Start mode (setup and run)
start: setup run

# Clean up virtual environment
clean:
	@echo "Cleaning up..."
	rm -rf venv
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +;

# Help
help:
	@echo "Available commands:"
	@echo "  make       - Setup environment and run server"
	@echo "  make setup - Setup virtual environment and install dependencies"
	@echo "  make run   - Run the server"
	@echo "  make start - Setup and run"
	@echo "  make clean - Clean up virtual environment and cache files"
