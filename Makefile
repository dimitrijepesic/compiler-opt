PYTHON ?= python3
TECTONIC ?= tectonic
AUDIT_IMAGE ?= cgym-causal:0.2.5
EXAMPLE_OUT ?= tmp/reproduce-example

.PHONY: verify numbers figures paper image reproduce-example
verify:
	$(PYTHON) scripts/build_paper_artifact.py --check
	$(PYTHON) scripts/verify_causal_baseline_audit.py > /dev/null && \
	  echo "Verified causal-audit provenance, hashes and totals."

numbers:
	$(PYTHON) scripts/build_paper_artifact.py

figures:
	$(PYTHON) scripts/build_paper_artifact.py --figure

paper: verify
	cd paper && $(TECTONIC) --keep-logs main.tex

image:
	sh scripts/build_audit_image.sh

reproduce-example:
	docker run --rm --platform linux/amd64 -e PYTHONWARNINGS=ignore \
	  -v "$(CURDIR):/work" -w /work $(AUDIT_IMAGE) \
	  python scripts/reproduce_baseline_example.py --out /work/$(EXAMPLE_OUT)
