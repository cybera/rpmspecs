# TODO:
# DONE - Split into 2+ packages
# - Example vcl.conf for apache?
# DONE - each package has it's own requires

Name:           vcl
Version:        2.2.1  
Release:        2%{?dist}
Summary:        An open-source system used to dynamically provision and broker remote access to a dedicated compute environment for an end-user 

Group:         Applications/System
License:       Apache 2.0 
URL:           https://cwiki.apache.org/VCL 
Source0:       apache-VCL-%{version}-incubating.tar.bz2
Patch0:       utils_virtual_undefined.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: 	mysql-server

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
Requires: xmlsec1-openssl
Requires: perl-Object-InsideOut


%description
VCL is an open-source system used to dynamically provision and broker remote access to a dedicated compute environment for an end-user. The provisioned computers are typically housed in a data center and may be physical blade servers, traditional rack mounted servers, or virtual machines. VCL can also broker access to standalone machines such as a lab computers on a university campus.

%description web
VCL Web GUI

%description managementnode
VCL Managment Node

%prep
%setup -n apache-VCL-%{version}-incubating
pushd web/.ht-inc
# patch does not like spaces in front of it!
%patch0 -p0
popd

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT/etc/%{name}
mkdir -p $RPM_BUILD_ROOT/etc/init.d

# These two VMWare modules are not supplied, as one would expect given how they are used 
# in VCL, by VCL. But the rpmbuild process picks it up as a requirement.
# It could be solved by simply adding it as a requirement during the install process like
# other cpan modules, but right now the official install docs don't ask to install these
# modules, so I'm guessing it's never used and am commenting them out. -- curtis
pushd ./managementnode/lib/VCL/Module/Provisioning/VMware
	sed -i 's|use VMware::Vix::Simple;|#use VMware::Vix::Simple;|' VIX_API.pm
	sed -i 's|use VMware::Vix::API::Constants;|#use VMware::Vix::API::Constants;|' VIX_API.pm
popd

# We are installing vcld in a different location than /usr/local/vcl/bin so the init script
# needs to be altered. -- curtis
pushd ./managementnode/bin
	sed -i 's|DAEMON_PATH=/usr/local/vcl/bin|DAEMON_PATH=/usr/share/vcl-managementnode/bin|' S99vcld.linux
popd

#
# Begin copying files..
#
cp -r ./mysql/* $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/
cp -r ./web $RPM_BUILD_ROOT/usr/share/%{name}-web

# Move the init file to the right spot
mv ./managementnode/bin/S99vcld.linux $RPM_BUILD_ROOT/etc/init.d/vcld
# Move vcld.conf to /etc/vcl...
cp ./managementnode/etc/vcl/vcld.conf $RPM_BUILD_ROOT/etc/%{name}/
# Keep the original vcld.conf file but rename it
mv ./managementnode/etc/vcl/vcld.conf ./managementnode/etc/vcl/vcld.conf.orig
# Now copy everything else
cp -r ./managementnode $RPM_BUILD_ROOT/usr/share/%{name}-managementnode

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/share/doc/%{name}-%{version}

%files web
/usr/share/%{name}-web
%attr(755,apache,root) /usr/share/vcl-web/.ht-inc/maintenance

%files managementnode
/usr/share/%{name}-managementnode
%config(noreplace) /etc/vcl/vcld.conf
/etc/init.d/vcld

%changelog
* Mon Jun 25 2012 curtis@serverascode.com
- comment out VMware::Vix::Simple and VMware::Vix::API::Constants in VIX_API.pm because that library is not provided nor asked for in the official docs. 
* Fri Jun 22 2012 curtis@serverascode.com
- initial rpm
