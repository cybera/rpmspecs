# TODO:
# DONE - Split into 2+ packages
# - Example vcl.conf for apache?
# DONE - each package has it's own requires

Name:   vcl-cybera
%define real_name vcl
%define cybera_version 0.4
Version:        2.3
Release:        4%{?dist}
Summary:        An open-source system used to dynamically provision and broker remote access to a dedicated compute environment for an end-user 

Group:         Applications/System
License:       Apache 2.0 
URL:           https://cwiki.apache.org/VCL 
#Source0:       apache-VCL-%{version}.tar.bz2

%define git_repo git@github.com:cybera/VCL.git

BuildRoot:      %{_tmppath}/%{real_name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: 	mysql-server
BuildArch:  noarch

%package web
Summary: VCL Web Interface
Group: Application/Internet
#
# Web Node
# 
Requires: httpd
Requires: mod_ssl
Requires: php
# Epel
Requires: libmcrypt
Requires: php-gd
Requires: php-json
# Epel
Requires: php-mcrypt
Requires: php-mysql
Requires: php-openssl
#php-sysvsem
# sysvsem is in php-process
Requires: php-process
Requires: php-xml
Requires: php-xmlrpc
Requires: php-ldap 

%package managementnode
Summary: VCL Management Node
Group: Application/System
#
# Management Node
# 
Requires: dhcp
Requires: sendmail
Requires: expat
Requires: expat-devel
Requires: gcc
Requires: krb5-libs
Requires: krb5-devel
Requires: libxml2
Requires: libxml2-devel
Requires: nmap
Requires: openssl
Requires: openssl-devel
Requires: perl-CPAN
Requires: perl-DBD-MySQL
Requires: perl-DBI
Requires: perl-Digest-SHA1
Requires: perl-MailTools
Requires: perl-Net-Jabber
Requires: perl-RPC-XML
Requires: perl-YAML
Requires: perl-Regexp-Common
Requires: perl-WWW-Curl
Requires: xmlsec1-openssl
Requires: perl-Object-InsideOut
# Only in cybera version
Requires: perl-Net-Amazon-EC2


%description
VCL is an open-source system used to dynamically provision and broker remote access to a dedicated compute environment for an end-user. The provisioned computers are typically housed in a data center and may be physical blade servers, traditional rack mounted servers, or virtual machines. VCL can also broker access to standalone machines such as a lab computers on a university campus.

%description web
VCL Web GUI

%description managementnode
VCL Managment Node

%prep
#%setup -n apache-VCL-%{version}
rm -rf ./%{real_name}
git clone %{git_repo} %{real_name}
pushd %{real_name}
        # Note the v in front of version
        git checkout v%{cybera_version}
        # Strip .svn
        find . -name .svn -type d -print0 | xargs -0 rm -rf 
popd


%build

%install
cd vcl
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/%{real_name}
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{real_name}-%{version}
mkdir -p $RPM_BUILD_ROOT/etc/%{real_name}
mkdir -p $RPM_BUILD_ROOT/etc/init.d

# Drop into trunk now
pushd trunk

# We are installing vcld in a different location than /usr/local/vcl/bin so the init script
# needs to be altered. -- curtis
pushd ./managementnode/bin
	sed -i 's|DAEMON_PATH=/usr/local/vcl/bin|DAEMON_PATH=/usr/share/vcl-managementnode/bin|' S99vcld.linux
popd

#
# Begin copying files..
#
cp -r ./mysql/* $RPM_BUILD_ROOT/usr/share/doc/%{real_name}-%{version}/
cp -r ./web $RPM_BUILD_ROOT/usr/share/%{real_name}-web
# Themes is one level up from trunk
cp -r ../themes/* $RPM_BUILD_ROOT/usr/share/%{real_name}-web/themes/
cp -r ../sites $RPM_BUILD_ROOT/usr/share/%{real_name}-web/
cp -r ../utils $RPM_BUILD_ROOT/usr/share/%{real_name}
cp -r ../image-resources $RPM_BUILD_ROOT/usr/share/%{real_name}

# Move the init file to the right spot
mv ./managementnode/bin/S99vcld.linux $RPM_BUILD_ROOT/etc/init.d/vcld
# Move vcld.conf to /etc/vcl...
cp ./managementnode/etc/vcl/vcld.conf $RPM_BUILD_ROOT/etc/%{real_name}/
# Keep the original vcld.conf file but rereal_name it
mv ./managementnode/etc/vcl/vcld.conf ./managementnode/etc/vcl/vcld.conf.orig
# Remove ec2 code for now
# - it requires Amazon::EC2::Client for which there is no RPM that I know off
#   and anyways it's not being used
rm -rf ./managementnode/lib/VCL/Module/Provisioning/EC2
# Now copy everything else
cp -r ./managementnode $RPM_BUILD_ROOT/usr/share/%{real_name}-managementnode
# remove ec2 code

popd #from trunk

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/share/doc/%{real_name}-%{version}
/usr/share/%{real_name}

%files web
/usr/share/%{real_name}-web
%attr(755,apache,root) /usr/share/vcl-web/.ht-inc/maintenance

%files managementnode
/usr/share/%{real_name}-managementnode
%config(noreplace) /etc/vcl/vcld.conf
/etc/init.d/vcld

%changelog
* Mon Aug 13 2012 curtis@serverascode.com
- added sites
* Fri Aug 10 2012 curtis@serverascode.com
- initial rpm based on vcl.spec
