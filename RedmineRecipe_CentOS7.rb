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

#%w(httpd httpd-devel httpd-tools ImageMagick ImageMagick-devel subversion mercurial).each do |pkg|
#  package pkg do
#    action :install
#  end
#end

#execute "svn co http://svn.redmine.org/redmine/branches/3.0-stable /var/lib/redmine" do
#  not_if "test -e /var/lib/redmine"
#end

#gem_package "passenger" do
#   version '5.0.7'
#end

#gem_package "bundler"

execute "createUser_Redmine" do
   user "postgres"
   command "psql -c \"CREATE ROLE redmine LOGIN ENCRYPTED PASSWORD 'redmine' NOINHERIT VALID UNTIL 'infinity';\""
   not_if "psql -c \"select usename from pg_user where usename = 'redmine';\""
end
