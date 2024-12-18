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
