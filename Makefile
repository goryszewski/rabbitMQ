HOSTS={ "master01" : { memoryMB: "8192" , "tags" : ["rabbit"] }}

Terraform_VARS= -var 'template=debian12' -var 'hosts=$(HOSTS)'

terraform_init:
	@echo "[MAKE] Terraform Init"
	# cd ./terraform && terraform init $(Terraform_VARS)

terraform_plan: terraform_init
	@echo "[MAKE] Terraform Plan"
	cd ./terraform && terraform plan  $(Terraform_VARS)

terraform_apply: terraform_plan
	@echo "[MAKE] Terraform Apply"
	cd ./terraform && terraform apply --auto-approve $(Terraform_VARS)

## 

v:
	source ./venv/bin/activate

send: 
	flask --app send run 

recv: 
	python3 ./receive.py

docker1:
	docker compose up -d

test:
	curl -XPOST 127.0.0.1:5000/name -H "Content-Type: application/json" -d '{"data":1}'

looptest:
	python3 ./loop_rest.py

format:
	black --config ./pyproject.toml  lib/*.py ./*.py
# https://raw.githubusercontent.com/jbryer/CompStats/refs/heads/master/Data/titanic3.csv