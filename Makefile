# Whole modeling -> serving pipeline (exluding evaluation)
.PHONY: all
all: database preprocess train serve


# Create local SQL database with docker
.PHONY: database
database:
	@cd src/database && $(MAKE) -s

# Run preprocessing job
.PHONY: preprocess
preprocess:
	@cd src/preprocess && $(MAKE) -s

# Train model
.PHONY: train
train:
	@cd src/train && $(MAKE) -s

# Evaluate results
.PHONY: evaluate
evaluate:
	@cd src/evaluate && $(MAKE) -s

# Serve model
.PHONY: serve
serve:
	@cd src/serve && $(MAKE) -s
