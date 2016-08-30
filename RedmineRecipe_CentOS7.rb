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

#execute "Development Tools"do
#   command "yum -y groupinstall \"Development Tools\" "
#end

#%w(openssl-devel readline-devel zlib-devel curl-devel libyaml-devel libffi-devel).each do |pkg|
#  package pkg do
#    action :install
#  end
#end

#%w(postgresql-server postgresql-devel).each do |pkg|
#  package pkg do
#    action :install
#  end
#end

#Apache
#%w(httpd httpd-devel).each do |pkg|
#  package pkg do
#    action :install
#  end
#end

#ImageMagick
#%w(ImageMagick ImageMagick-devel ipa-pgothic-fonts).each do |pkg|
#  package pkg do
#    action :install
#  end
#end

#execute "bundler install" do
#   command "gem install bundler --no-rdoc --no-ri"
#   not_if "gem list | grep 'bundler'"
#end

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

#%w(subversion).each do |pkg|
#  package pkg do
#    action :install
#  end
#end

#execute "install redmine" do
#  command <<-EOF
#     export LC_CTYPE=ja_JP.utf8
#     svn co http://svn.redmine.org/redmine/branches/3.2-stable /var/lib/redmine
#  EOF
#  not_if "test -e /var/lib/redmine"
#end

#     export http_proxy=http://proxy.nttd-wave.com:15080/
#execute "generate_secret" do
#   cwd "/var/lib/redmine"
#   command <<-EOF
#     bundle install --without development test
#     bundle exec rake generate_secret_token
#     RAILS_ENV=production bundle exec rake db:migrate
#     RAILS_ENV=production REDMINE_LANG=ja bundle exec rake redmine:load_default_data
#   EOF
#end

#execute "passenger install" do
#  command "gem install -r -p http://proxy.nttd-wave.com:15080 passenger --no-rdoc --no-ri"
#  command "gem install passenger --no-rdoc --no-ri"
#  not_if "gem list | grep 'passenger'"
#end

execute "passenger-install-apache2-module" do
   user "root"
   command "/opt/rbenv/versions/2.2.3/bin/passenger-install-apache2-module --auto"
end

#execute "chown redmine directory" do
#  command "chown -R apache:apache /var/lib/redmine"
#end

