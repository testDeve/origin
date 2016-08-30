# SELinuxをoffに
#execute "sudo setenforce 0" do
#  not_if "getenforce | grep Disabled"
#end

#file "/etc/selinux/config" do
#  action :edit
#  block do |content|
#    next if content =~ /^SELINUX=disabled/
#    content.gsub!(/^SELINUX=.*/, "SELINUX=disabled")
#  end
#end

%w(httpd httpd-devel httpd-tools ImageMagick ImageMagick-devel subversion mercurial libcurl-devel).each do |pkg|
  package pkg do
    action :install
  end
end

execute "svn co http://svn.redmine.org/redmine/branches/3.0-stable /var/lib/redmine" do
  not_if "test -e /var/lib/redmine"
end

execute "passenger install" do
  command "gem install -r -p http://proxy.nttd-wave.com:15080 passenger -v 5.0.7 "
  #command "gem install passenger -v 5.0.7"
  not_if "gem list | grep 'passenger'"
end

execute "passenger-install-apache2-module" do
   user "root"
   command "/opt/rbenv/versions/2.2.2/bin/passenger-install-apache2-module --auto"
end

#execute "createUser_Redmine" do
#   user "postgres"
#   command "psql -c \"CREATE ROLE redmine LOGIN ENCRYPTED PASSWORD 'redmine' NOINHERIT VALID UNTIL 'infinity';\""
#   not_if "psql -c \"select usename from pg_user where usename='redmine'\" | grep 'redmine'"
#end

#execute "createDB_Redmine" do
#   user "postgres"
#   command "createdb -E UTF-8 -l ja_JP.UTF-8 -O redmine -T template0 redmine"
#   not_if "psql -l | grep 'redmine'"
#end

#execute "chown redmine directory" do
#  command "chown -R apache:apache /var/lib/redmine"
#end

#execute "bundle install" do
#   cwd "/var/lib/redmine"
#   command <<-CMD
#     export http_proxy=http://proxy.nttd-wave.com:15080/
#     bundle install --without development test 
#     rake generate_secret_token
#     RAILS_ENV=production rake db:migrate
#   CMD
#end
