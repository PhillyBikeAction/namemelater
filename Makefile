default:
	@echo "Call a specific subcommand:"
	@echo
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null\
	| awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}'\
	| sort\
	| egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
	@echo
	@exit 1

lint:
	tox -e black
	tox -e ruff

reformat:
	tox -e reformat

serve:
	docker compose up

migrate:
	docker compose run --rm namemelater aerich migrate $(filter-out $@,$(MAKECMDGOALS))

db-upgrade:
	docker compose run --rm namemelater aerich upgrade

dbshell:
	docker-compose exec db psql -U postgres postgres
