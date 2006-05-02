%define product ERP5Form
%define version 0.11
%define release 7

%define zope_home %{_prefix}/lib/zope
%define software_home %{zope_home}/lib/python

Summary:   A Zope product that add easy to use form to ERP5
Name:      zope-%{product}
Version:   %{version}
Release:   %mkrel %{release}
License:   GPL
Group:     System/Servers
URL:       http://www.erp5.org
Source0:   %{product}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-rootdir
BuildArch: noarch
Conflicts: ERP5Form
Requires:  erp5-zope erp5-Formulator pdftk pychart

#----------------------------------------------------------------------
%description
ERP5Form extends Zope Formulator and provides a very fast way to
create forms. ERP5Form forms can be designe with a web user interface
and rendered automatically by page template. Context variables (here,
form...) are provided to each field at rendering time. Together with
ERP5Type, ERP5Form defines a fast rapid application environment.

#----------------------------------------------------------------------
%prep
%setup -c

%build


%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}/%{software_home}/Products
%{__cp} -a * %{buildroot}%{software_home}/Products/


%clean
%{__rm} -rf %{buildroot}

%post
if [ "`%{_prefix}/bin/zopectl status`" != "daemon manager not running" ] ; then
  service zope restart
fi

%postun
if [ -f "%{_prefix}/bin/zopectl" ] && [ "`%{_prefix}/bin/zopectl status`" != "daemon manager not running" ] ; then
  service zope restart
fi

%files
%defattr(0644, zope, zope, 0755)
%doc %{product}/VERSION.txt %{product}/TODO.txt
%{software_home}/Products/*

#----------------------------------------------------------------------
%changelog
* Tue Apr 04 2006 Kevin Deldycke <kevin@nexedi.com> 0.11-7mdk
- New build from the SVN repository

* Wed Feb 01 2006 Kevin Deldycke <kevin@nexedi.com> 0.11-6mdk
- Give ownership to zope
- New build from the CVS

* Wed Feb 01 2006 Kevin Deldycke <kevin@nexedi.com> 0.11-5mdk
- Give ownership to zope
- New build from the CVS

* Tue Jan 31 2006 Kevin Deldycke <kevin@nexedi.com> 0.11-4mdk
- pdftk is required to let ERP5Form handle PDF files

* Mon Jan 30 2006 Kevin Deldycke <kevin@nexedi.com> 0.11-3mdk
- New build from the CVS

* Fri Jan 27 2006 Kevin Deldycke <kevin@nexedi.com> 0.11-2mdk
- New build from the CVS

* Thu Jan 26 2006 Kevin Deldycke <kevin@nexedi.com> 0.11-1mdk
- Update to version 0.11

* Wed Jan 18 2006 Kevin Deldycke <kevin@nexedi.com> 0.10-1mdk
- Update to version 0.10

* Mon Jan 16 2006 Kevin Deldycke <kevin@nexedi.com> 0.9.20060116-1mdk
- New build from the CVS

* Tue Jan 10 2006 Kevin Deldycke <kevin@nexedi.com> 0.9.20060110-1mdk
- New release for Mandriva 2006
- Spec file updated

* Tue Sep 01 2004 Sebastien Robin <seb@nexedi.com> 0.8-1mdk
- Final relase for Mandrake 10.1

* Thu Jun 10 2004 Sebastien Robin <seb@nexedi.com> 0.1-5mdk
- New Release for Mandrake 10.1

* Tue Jan 10 2004 Sebastien Robin <seb@nexedi.com> 0.1-4mdk
- Added the dependency : ZGDChart

* Mon Sep 08 2003 Sebastien Robin <seb@nexedi.com> 0.1-3mdk
- Changed permissions on files

* Wed Sep 05 2003 Sebastien Robin <seb@nexedi.com> 0.1-2mdk
- Update spec in order to follows Mandrake Rules

* Mon May 12 2003 Sebastien Robin <seb@nexedi.com> 0.1-1nxd
- Create the spec file
