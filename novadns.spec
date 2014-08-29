#
# Example spec file for cdplayer app...
#
Summary: novadns
Name: novadns
Version: 0.2.1
Release: 1 
License: GPL
Group: Applications/System
#Source: https://github.com/curtisgithub/novadns
Packager: curtis <curtis@serverascode.com>

BuildRoot:      %{_tmppath}/%{real_name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

%define git_repo https://github.com/curtisgithub/novadns

Requires: python-jinja2
Requires: python-novaclient

%description
Create /etc/hosts from openstack 

%prep
rm -rf ./%{name}
git clone %{git_repo} %{name}
#pushd %{name}
#        # Note the v in front of version
#        git checkout v%{cybera_version}
#popd

%build

%install

cd novadns
pwd
ls
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/novadns
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/etc/init

sed -i 's|NOVADNS_HOME = "/home/centos/novadns"|NOVADNS_HOME = "/etc/novadns"|g' ./novadns.py
sed -i 's|exec /home/centos/novadns/novadns.py|exec /usr/sbin/novadns|g' ./novadns.upstart
head ./novadns.py
tail ./novadns.upstart
cp ./novadns.py $RPM_BUILD_ROOT/usr/sbin/novadns
cp ./novadns.upstart $RPM_BUILD_ROOT/etc/init/novadns.conf
cp ./novadns.conf.example $RPM_BUILD_ROOT/etc/novadns/novadns.conf.example
cp ./novadns.template $RPM_BUILD_ROOT/etc/novadns/novadns.template

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/sbin/novadns
/etc/novadns
# /etc/novadns/nova.conf is not included, just an example conf file
/etc/init/novadns.conf


%changelog
* Tue Dec 17 2012 curtis@serverascode.com
- added /etc/vcl/sites/*/conf.php and specific site code into $share-web
