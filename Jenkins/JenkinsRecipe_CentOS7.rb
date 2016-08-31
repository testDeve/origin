%w( wget java-1.8.0-openjdk ).each do |pkg|
  package pkg do
    action :install
  end
end

execute "download repo" do
  user "root"
  command "wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat/jenkins.repo"
  not_if "test -e /etc/yum.repos.d/jenkins.repo"
end

execute "import jenkins key" do
  user "root"
  #command "rpm --import http://pkg.jenkins-ci.org/redhat/jenkins-ci.org.key"
  command "rpm --httpproxy http://proxy.nttd-wave.com --httpport 15080 --import http://pkg.jenkins-ci.org/redhat/jenkins-ci.org.key"
end

package "jenkins" do
  user "root"
  action :install
end

[:enable,:restart].each do |act|
  service "jenkins" do
    action act
  end
end

execute "firewall port open" do
  command "firewall-cmd --add-port=8080/tcp --zone=public --permanent"
  not_if "grep -c 8080 /etc/firewalld/zones/public.xml"
end

execute "firewall reload" do
  command "firewall-cmd --reload"
end
