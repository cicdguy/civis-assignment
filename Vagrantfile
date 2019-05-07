VAGRANTFILE_API_VERSION = "2"

vm_name = 'app'
vm_env = 'dev'
app_dir_on_vm = '/home/vagrant/app'

ENV['ANSIBLE_CONFIG'] = "ansible/ansible.cfg"
ENV['ANSIBLE_DIR'] = "ansible/"

vagrant_ip = "192.168.52.101"

boxes = {
 "centos7" => "centos/7",
}

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  boxes.each do |distribution, box|
    config.vbguest.auto_update = false
    config.ssh.insert_key = false
    config.ssh.forward_agent = true

    config.vm.provision "file", source: "app/", destination: app_dir_on_vm

    config.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--cpus", "2"]
      vb.customize ["modifyvm", :id, "--memory", "4096"]
      vb.customize ["modifyvm", :id, "--natdnsproxy1", "off"]
      vb.customize ["modifyvm", :id, "--nictype1", "virtio" ]
      vb.customize ["modifyvm", :id, "--nictype2", "virtio" ]
    end

    config.vm.define "#{distribution}-#{vm_name}" do |host|
      host.vm.hostname = vm_name
      host.vm.box = box
      host.vm.network :private_network, ip: vagrant_ip
      host.vm.provision "ansible" do |ansible|
        ansible.verbose = "v"
        ansible.limit = "all"
        ansible.extra_vars = {
          ENV: vm_env,
          mount_point: app_dir_on_vm,
          vagrant_vm_ip: 'localhost',
        }
        ansible.playbook = "ansible/configure.yml"
        ansible.compatibility_mode = "2.0"
        ansible.groups = {
          "#{vm_name}-#{vm_env}" => [ "#{distribution}-#{vm_name}" ]
        }
      end
    end
  end
end
