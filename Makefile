.PHONY: bootstrap check test plan snapshot policy docflow badges clean-artifacts

bootstrap:
	@./scripts/bootstrap.sh

check:
	@./scripts/checks.sh

test:
	@mise exec -- python -m pytest

plan:
	@./scripts/plan_snapshot.sh

snapshot:
	@./scripts/snapshot.sh

policy:
	@mise exec -- python scripts/policy_check.py --workflows

docflow:
	@mise exec -- python scripts/docflow_audit.py --root . --fail-on-violations

badges:
	@./scripts/update_badges.sh

clean-artifacts:
	@./scripts/clean_artifacts.sh
