execute "yum update" do
  user "root"
  command "yum update -y"
end

execute "yum libxslt" do
  user "root"
  command "yum install -y libxslt.i686"
end

%w(postgresql postgresql-contrib postgresql-devel postgresql-libs postgresql-server).each do |pkg|
  user "root"
  package pkg do
    action :install
  end
end

execute "initdb" do
  command "PGSETUP_INITDB_OPTIONS='--encoding UTF8 --no-locale' sudo /sbin/service postgresql initdb"
  not_if "test -e /var/lib/pgsql9/data/postgresql.conf"
end

execute "postgreSQL auto start" do
  user "root"
  command "/sbin/chkconfig postgresql on"
end

[:enable,:restart].each do |act|
  service "postgresql" do
    action act
  end
end

