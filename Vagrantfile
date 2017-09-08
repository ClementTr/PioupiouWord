# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure(2) do |config|
  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  
  config.vm.box = "npalm/mint17-amd64-cinnamon"
  #config.vm.box = "box-cutter/ubuntu1404-desktop"
  
  config.ssh.username = "vagrant"
  config.ssh.password = "vagrant" 
  config.ssh.insert_key = false

  config.vm.network "forwarded_port", guest: 10, host: 1010


  config.vm.synced_folder "Project/", "/home/vagrant/Desktop/Project/"

  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    vb.gui = true
  end

  # Execute shell which will configure our environment.
  config.vm.provision "shell", inline: "bash -x /vagrant/vagrant-setup.sh"
  
end