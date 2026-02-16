VENV = .venv
BIN = $(VENV)/bin

.PHONY: init run clean

# initialize the project by creating a virtual environment and installing dependencies
init: $(VENV)
	@cp -n .env.example .env || true
	$(BIN)/pip install -r requirements.txt
	@echo "✅ Listo. Usa 'make run'"

$(VENV):
	python3 -m venv $(VENV)

# run api with hot reload
run:
	$(BIN)/uvicorn app.main:app --reload

# clean virtual environment and pycache
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +