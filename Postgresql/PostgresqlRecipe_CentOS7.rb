package "wget"do
  action :install
  not_if "yum list installed | grep 'wget'"
end

package "wget https://download.postgresql.org/pub/repos/yum/9.5/redhat/rhel-7-x86_64/pgdg-centos95-9.5-2.noarch.rpm" do
  not_if "rpm -q pgdg-centos95-9.5-2.noarch"
end

%w(postgresql95 postgresql95-contrib postgresql95-devel postgresql95-libs postgresql95-server).each do |pkg|
  package pkg do
    action :install
  end
end

execute "initdb" do
  command "PGSETUP_INITDB_OPTIONS='--encoding UTF8 --no-locale' /usr/pgsql-9.5/bin/postgresql95-setup initdb"
  not_if "test -e /var/lib/pgsql/9.5/data/postgresql.conf"
end

[:enable,:restart].each do |act|
  service "postgresql-9.5" do
    action act
  end
end

execute "firewall port open" do
  command "firewall-cmd --add-port=5432/tcp --zone=public --permanent"
  not_if "grep -c 5432 /etc/firewalld/zones/public.xml"
end

execute "firewall reload" do
  command "firewall-cmd --reload"
end
