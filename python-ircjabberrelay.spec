%global libname ircjabberrelay
Name:           python-%{libname}
Version:        0.0.1
Release:        1%{?dist}
Summary:        Relay between IRC and Jabber

Group:          System Environment/Daemons
License:        Public Domain
URL:            https://github.com/atorkhov/ircjabberrelay
Source0:        %{libname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel python-setuptools
Requires:       python-twisted-core python-twisted-names python-wokkel-muc

%if 0%{?fedora}
BuildRequires:  systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%else
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
%endif

%description
Relay between IRC and Jabber


%prep
%setup -q -c -n %{libname}-%{version}


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

mkdir -p %{buildroot}/%{_sysconfdir}/%{libname}
mv %{buildroot}/%{python_sitelib}/%{libname}/config.py %{buildroot}/%{_sysconfdir}/%{libname}
ln -s %{_sysconfdir}/%{libname}/config.py %{buildroot}/%{python_sitelib}/%{libname}/config.py

%if 0%{?fedora}
mkdir -p %{buildroot}/%{_unitdir}
cp %{libname}.service %{buildroot}/%{_unitdir}
%else
mkdir -p %{buildroot}/%{_initddir}
cp %{libname}.init %{buildroot}/%{_initddir}/%{libname}
%endif


%if 0%{?fedora}
%post
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable ircjabberrelay.service > /dev/null 2>&1 || :
    /bin/systemctl stop ircjabberrelay.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart ircjabberrelay.service >/dev/null 2>&1 || :
fi
%else
%post
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add ircjabberrelay

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service ircjabberrelay stop >/dev/null 2>&1
    /sbin/chkconfig --del ircjabberrelay
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service ircjabberrelay condrestart >/dev/null 2>&1 || :
fi
%endif


%files
%defattr(-,root,root,-)
%doc README
%dir %{_sysconfdir}/%{libname}
%config(noreplace) %{_sysconfdir}/%{libname}/*
%{_bindir}/%{libname}.tac
%{python_sitelib}/%{libname}
%{python_sitelib}/%{libname}-%{version}-py*.egg-info
%if 0%{?fedora}
%{_unitdir}/*
%else
%{_initddir}/*
%endif

%changelog
* Thu Jun 14 2012 Alexey Torkhov <atorkhov@gmail.com> - 0.0.1-1
- Initial package
