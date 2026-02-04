.PHONY: bootstrap check test plan policy docflow clean-artifacts

bootstrap:
	@./scripts/bootstrap.sh

check:
	@./scripts/checks.sh

test:
	@mise exec -- python -m pytest

plan:
	@./scripts/plan_snapshot.sh

policy:
	@mise exec -- python scripts/policy_check.py --workflows

docflow:
	@mise exec -- python -m gabion docflow-audit --root . --fail-on-violations

clean-artifacts:
	@./scripts/clean_artifacts.sh
