Summary:	GNUstep Guile interface
Summary(pl):	Interfejs Guile do GNUstepa
Name:		gnustep-guile
Version:	1.0.3
Release:	1
License:	LGPL/GPL
Group:		Libraries
Source0:	ftp://ftp.gnustep.org/pub/gnustep/libs/%{name}-%{version}.tar.gz
Patch0:		%{name}-update.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-link.patch
URL:		http://www.gnustep.org/
BuildRequires:	gnustep-base-devel >= 1.3.0
BuildRequires:	gnustep-gui-devel
BuildRequires:	gnustep-make-devel >= 1.3.0
BuildRequires:	guile-devel >= 1.4
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gsdir		/usr/lib/GNUstep

%define		libcombo	gnu-gnu-gnu
%define		gsos		linux-gnu
%ifarch %{ix86}
%define		gscpu		ix86
%else
# also s/alpha.*/alpha/, but we use only "alpha" arch for now
%define		gscpu		%{_target_cpu}
%endif

%description
The GNUstep Guile Interface lets you use (and extend) the GNUstep
libraries from within Guile. This effectively provides you with
scripting language for GNUstep and an interactive system for
developing GNUstep applications.

%description -l pl
Interfejs Guile do GNUstepa pozwala na u¿ywanie (i rozszerzanie)
bibliotek GNUstepa z poziomu Guile. Efektywnie udostêpnia to jêzyk
skryptowy dla GNUstepa i interaktywny system do rozwijania aplikacji
GNUstepowych.

%package devel
Summary:	GNUstep guile headers
Summary(pl):	Pliki nag³ówkowe GNUstep guile
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	gnustep-base-devel
Requires:	guile-devel

%description devel
Header files for GNUstep Guile interface.

%description devel -l pl
Pliki nag³ówkowe interfejsu Guile do GNUstepa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__autoconf}
cd Greg
cp -f %{_gsdir}/System/Makefiles/config.* .
%{__autoconf}
cd ../ScriptKit
%{__autoconf}
cd ..
. %{_gsdir}/System/Makefiles/GNUstep.sh
%configure

%{__make} \
	messages=yes

%{__make} -C Documentation

%install
rm -rf $RPM_BUILD_ROOT
. %{_gsdir}/System/Makefiles/GNUstep.sh
%{__make} install \
	INSTALL_ROOT_DIR=$RPM_BUILD_ROOT \
	GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{_gsdir}/System

%{__make} -C Documentation install \
	GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{_gsdir}/System
# not (yet?) supported by rpm-compress-doc
find $RPM_BUILD_ROOT%{_gsdir}/System/Documentation \
	-type f -a ! -name '*.html' | xargs gzip -9nf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc ChangeLog*

# UNIX world
%attr(755,root,root) %{_bindir}/greg
%attr(755,root,root) %{_libdir}/libgreg.so.*.*
%{_datadir}/guile/*/ice-9/*.scm
%{_mandir}/man1/greg.1*
%{_infodir}/greg.info*

# GNUstep world
%dir %{_gsdir}/System/Applications/*.app
%{_gsdir}/System/Applications/*.app/Resources
%dir %{_gsdir}/System/Applications/*.app/%{gscpu}
%dir %{_gsdir}/System/Applications/*.app/%{gscpu}/%{gsos}
%dir %{_gsdir}/System/Applications/*.app/%{gscpu}/%{gsos}/%{libcombo}
%{_gsdir}/System/Applications/*.app/%{gscpu}/%{gsos}/%{libcombo}/*.openapp
%attr(755,root,root) %{_gsdir}/System/Applications/gui.app/gui
%attr(755,root,root) %{_gsdir}/System/Applications/gui.app/%{gscpu}/%{gsos}/%{libcombo}/gui
%attr(755,root,root) %{_gsdir}/System/Applications/guile-gui.app/guile-gui
%attr(755,root,root) %{_gsdir}/System/Applications/guile-gui.app/%{gscpu}/%{gsos}/%{libcombo}/guile-gui

%docdir %{_prefix}/System/Documentation
%{_gsdir}/System/Documentation/Developer/Guile
%{_gsdir}/System/Documentation/info/*.info*

%attr(755,root,root) %{_gsdir}/System/Libraries/%{gscpu}/%{gsos}/%{libcombo}/lib*.so.*

%attr(755,root,root) %{_gsdir}/System/Tools/%{gscpu}/%{gsos}/%{libcombo}/*

%files devel
%defattr(644,root,root,755)
# UNIX world
%attr(755,root,root) %{_libdir}/libgreg.so
%{_libdir}/libgreg.la
# static?
#%{_libdir}/libgreg.a

# GNUstep world
%{_gsdir}/System/Headers/ScriptKit
%{_gsdir}/System/Headers/gnustep/guile
%{_gsdir}/System/Libraries/%{gscpu}/%{gsos}/%{libcombo}/lib*.so
%{_gsdir}/System/Makefiles/Additional/guile.make
