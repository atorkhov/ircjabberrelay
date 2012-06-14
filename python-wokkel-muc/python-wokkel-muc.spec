%global libname wokkel
Name:           python-%{libname}-muc
Version:        0.4.0
Release:        1%{?dist}
Summary:        Enhancements to the Twisted XMPP protocol implementation

Group:          Development/Languages
License:        MIT
URL:            http://wokkel.ik.nu
Source0:        %{libname}-muc-%{version}.tar.gz
Patch0:         %{libname}.diff

BuildArch:      noarch
BuildRequires:  python-devel, python-setuptools, python-twisted-words, python-twisted-names
Requires:       python-twisted-words, python-twisted-names

Provides:       python-%{libname} = %{version}

%description
Wokkel is collection of enhancements on top of the Twisted networking
framework, written in Python. It mostly provides a testing ground
for enhancements to the Jabber/XMPP protocol implementation as found
in Twisted Words, that are meant to eventually move there.

Currently, Wokkel provides the following enhancements
on top of Twisted Words:

* A mechanism for easier implementation of XMPP Enhancement Protocols (XEPs)
  as so-called subprotocols.
* XMPP Client and server-side component support, that eases development
  and supports subprotocols.
* Subprotocol implementations for:
  o Generic presence, roster and message handling.
  o Service Discovery (XEP-0030), service side.
  o Publish-Subscribe (XEP-0060), client and service side.
  o Software Version (XEP-0092), service side. 
* Data format implementations for:
  o Data Forms (XEP-0004)
  o User Tune (XEP-0118)
  o User Mood (XEP-0107) 


%prep
%setup -q -n %{libname}-muc
%patch0 -p0


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%check
PYTHONPATH=`pwd` %{__python} wokkel/test/test_*.py
 

%files
%defattr(-,root,root,-)
%doc LICENSE NEWS README
%{python_sitelib}/%{libname}
%{python_sitelib}/%{libname}-%{version}-py*.egg-info

%changelog
* Thu Jun 14 2012 Alexey Torkhov <atorkhov@gmail.com> - 0.4.0-1
- Packaging wokkel-muc-client-support-24 branch
