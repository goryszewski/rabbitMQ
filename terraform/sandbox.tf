module "node" {

  for_each = var.hosts
  source   = "github.com/goryszewski/terraform_module/libvirt/domain"
  domain   = var.domain
  hostname = each.key
  tags     = each.value["tags"]
  memoryMB = each.value["memoryMB"]
  network  = module.network.id
  public_network = var.public_network
  template = var.template
}
provider "libvirt" {
  uri = var.qemu_url
}
