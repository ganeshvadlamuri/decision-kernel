.PHONY: demo-ros2 test lint typecheck all

demo-ros2:
	python -m demos.ros2_hello_world.run

test:
	pytest tests/ -v

lint:
	ruff check . --fix

typecheck:
	mypy brain/ cli/ adapters/ --ignore-missing-imports

all: lint typecheck test
