execute "sudo setenforce 0" do
  user "root"
  not_if "getenforce | grep Disabled"
end

execute "yum update" do
  user "root"
  command "yum update -y"
end

include_recipe "../Postgresql/PostgresqlRecipe_AWSLinux.rb"

execute "Development Tools"do
   user "root"
   command "yum -y groupinstall \"Development Tools\" "
end

%w(ruby23 ruby23-devel).each do |pkg|
  package "ruby23 ruby23-devel" do
    user "root"
    action :install
  end
end

execute "ruby20 erase" do
   user "root"
   command "yum -y erase ruby20"
end

execute "gem install io-console bundler" do
   user "root"
   command <<-EOF 
     gem install io-console
     gem install bundler --no-rdoc --no-ri
   EOF
end

execute "createUser_Redmine" do
   user "postgres"
   command "psql -c \"CREATE ROLE redmine LOGIN ENCRYPTED PASSWORD 'redmine' NOINHERIT VALID UNTIL 'infinity';\""
   not_if "psql -c \"select usename from pg_user where usename='redmine'\" | grep 'redmine'"
end

execute "createDB_Redmine" do
   user "postgres"
   command "createdb -E UTF-8 -l ja_JP.UTF-8 -O redmine -T template0 redmine"
   not_if "psql -l | grep 'redmine'"
end

#Apache
%w(httpd httpd-devel).each do |pkg|
  package pkg do
    action :install
  end
end

%w(make gcc gcc-c++ automake autoconf libcurl-devel apr-devel apr-util-devel).each do |pkg|
  package pkg do
    action :install
  end
end

%w(openssl-devel readline-devel zlib-devel curl-devel libyaml-devel libffi-devel ImageMagick ImageMagick ImageMagick-devel ipa-gothic-fonts).each do |pkg|
  package pkg do
    action :install
  end
end

package "subversion" do
   action :install
end

execute "install redmine" do
  command <<-EOF
     export LC_CTYPE=ja_JP.utf8
     svn co http://svn.redmine.org/redmine/branches/3.2-stable /var/lib/redmine
  EOF
  not_if "test -e /var/lib/redmine"
end

%w(database.yml configuration.yml).each do |fileName|
   remote_file "/var/lib/redmine/config/#{fileName}" do
      owner  "root"
      group  "root"
      source "AWS/var/lib/redmine/config/#{fileName}"
   end

   execute "chmod #{fileName}" do
      user "root"
      command "chmod 644 /var/lib/redmine/config/#{fileName}"
   end
end

remote_file "/var/lib/pgsql9/data/pg_hba.conf" do
   owner "postgres"
   group "postgres"
   source "AWS/var/lib/pgsql9/data/pg_hba.conf"
end

execute "pg_hba.conf reload" do
   user "postgres"
   command "pg_ctl -D /var/lib/pgsql9/data reload"
end

execute "development" do
   user "root"
   cwd "/var/lib/redmine"
   command "/usr/local/share/ruby/gems/2.3/gems/bundler-1.12.5/exe/bundle install --without development test"
end 

execute "generate_secret" do
   user "root"
   cwd "/var/lib/redmine"
   command <<-EOF
     /usr/local/share/ruby/gems/2.3/gems/bundler-1.12.5/exe/bundle exec /usr/local/share/ruby/gems/2.3/gems/rake-11.2.2/exe/rake generate_secret_token
     RAILS_ENV=production /usr/local/share/ruby/gems/2.3/gems/bundler-1.12.5/exe/bundle exec /usr/local/share/ruby/gems/2.3/gems/rake-11.2.2/exe/rake db:migrate
     RAILS_ENV=production REDMINE_LANG=ja /usr/local/share/ruby/gems/2.3/gems/bundler-1.12.5/exe/bundle exec /usr/local/share/ruby/gems/2.3/gems/rake-11.2.2/exe/rake redmine:load_default_data
   EOF
end

execute "passenger install" do
  command "gem install passenger --no-rdoc --no-ri"
  not_if "gem list | grep 'passenger'"
end

execute "rake" do
  command "gem install rake"
end

execute "mkswap" do
   user "root"
   command <<-EOF
     dd if=/dev/zero of=/swap bs=1M count=1024
     mkswap /swap
     swapon /swap
   EOF
end

execute "passenger-install-apache2-module" do
   user "root"
   command "/usr/local/share/ruby/gems/2.3/gems/passenger-5.0.30/bin/passenger-install-apache2-module --auto"
end

remote_file "/etc/httpd/conf.d/redmine.conf" do
   owner "root"
   group "root"
   source "AWS/etc/httpd/conf.d/redmine.conf"
end

execute "chmod redmine.conf" do
   user "root"
   command "chmod 644 /etc/httpd/conf.d/redmine.conf"
end

execute "chown redmine directory" do
  command "chown -R apache:apache /var/lib/redmine"
end

execute "create link" do
  command "ln -s /var/lib/redmine/public /var/www/html/redmine"
end

execute "chkconfig" do
   user "root"
   command "chkconfig httpd on"
end

execute "httpd service config" do
   user "root"
   command "service httpd configtest"
end

execute "httpd service start" do
   user "root"
   command "service httpd start"
end

