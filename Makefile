# Variables
APP_NAME := Shakestory
MAIN_FILE := main.py
BINARY_NAME := shakestory
BINARY_PATH := ./bin/$(BINARY_NAME)
BUILD_DIR := ./bin
SRC_DIR := ./app

# Activate virtual environment
venv:
	@echo "Activating virtual environment..."
	@source venv/bin/activate

# Build the application
build:
	@echo "Building $(APP_NAME)..."
	@python -m compileall $(SRC_DIR)
	@echo "#!/usr/bin/env python" > $(BINARY_PATH)
	@cat $(SRC_DIR)/$(MAIN_FILE) >> $(BINARY_PATH)
	@chmod +x $(BINARY_PATH)

# Run the application with uvicorn and auto-reload
run:
	@echo "Running $(APP_NAME) with uvicorn and auto-reload..."
	@uvicorn app.main:app --reload

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf $(BUILD_DIR)

# Install dependencies (assuming you're using pipenv or virtualenv)
deps:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt

# Format the code (assuming you're using black or autopep8)
fmt:
	@echo "Formatting code..."
	@black $(SRC_DIR)
	@echo "Formatting completed."

# Help target to display available make commands
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  venv        Activate virtual environment"
	@echo "  build       Build the application"
	@echo "  run         Run the application with uvicorn and auto-reload"
	@echo "  clean       Clean build artifacts"
	@echo "  deps        Install dependencies"
	@echo "  fmt         Format the code"
	@echo "  help        Display this help message"

# Default target
.DEFAULT_GOAL := help