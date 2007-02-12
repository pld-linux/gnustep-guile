Summary:	GNUstep Guile interface
Summary(pl.UTF-8):   Interfejs Guile do GNUstepa
Name:		gnustep-guile
Version:	1.1.4
Release:	4
License:	LGPL/GPL
Group:		Libraries
Source0:	ftp://ftp.gnustep.org/pub/gnustep/libs/%{name}-%{version}.tar.gz
# Source0-md5:	f20d84b0edcbefe2929063f74d170701
Patch0:		%{name}-paths.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-pass-arguments.patch
URL:		http://www.gnustep.org/
BuildRequires:	autoconf
BuildRequires:	gnustep-base-devel >= 1.7.3
#BuildRequires:	gnustep-db-devel >= ? (gdl2? -lgnustep-db2 -lgnustep-db2control)
BuildRequires:	gnustep-gui-devel >= 0.8.8-2
BuildRequires:	gnustep-make-devel >= 1.7.3
BuildRequires:	guile-devel >= 1.6
Requires(post,postun):	/sbin/ldconfig
Requires:	gnustep-make >= 1.7.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gsdir		/usr/%{_lib}/GNUstep

%define		libcombo	gnu-gnu-gnu
%define		gsos		linux-gnu
%ifarch %{ix86}
%define		gscpu		ix86
%else
# also s/alpha.*/alpha/, but we use only "alpha" arch for now
%define		gscpu		%(echo %{_target_cpu} | sed -e 's/amd64/x86_64/;s/ppc/powerpc/')
%endif

%description
The GNUstep Guile Interface lets you use (and extend) the GNUstep
libraries from within Guile. This effectively provides you with
scripting language for GNUstep and an interactive system for
developing GNUstep applications.

%description -l pl.UTF-8
Interfejs Guile do GNUstepa pozwala na używanie (i rozszerzanie)
bibliotek GNUstepa z poziomu Guile. Efektywnie udostępnia to język
skryptowy dla GNUstepa i interaktywny system do rozwijania aplikacji
GNUstepowych.

%package devel
Summary:	GNUstep guile headers
Summary(pl.UTF-8):   Pliki nagłówkowe GNUstep guile
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gnustep-base-devel >= 1.7.3
Requires:	guile-devel >= 1.6

%description devel
Header files for GNUstep Guile interface.

%description devel -l pl.UTF-8
Pliki nagłówkowe interfejsu Guile do GNUstepa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__autoconf}
cd Greg
cp -f %{_gsdir}/System/Library/Makefiles/config.* .
%{__autoconf}
cd ../ScriptKit
%{__autoconf}
cd ..
. %{_gsdir}/System/Library/Makefiles/GNUstep.sh
%configure

%{__make} \
	messages=yes

%{__make} -C Documentation

%install
rm -rf $RPM_BUILD_ROOT
. %{_gsdir}/System/Library/Makefiles/GNUstep.sh
%{__make} install \
	INSTALL_ROOT_DIR=$RPM_BUILD_ROOT \
	GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{_gsdir}/System

%{__make} -C Documentation install \
	GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{_gsdir}/System
# not (yet?) supported by rpm-compress-doc
find $RPM_BUILD_ROOT%{_gsdir}/System/Library/Documentation \
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
%docdir %{_prefix}/System/Library/Documentation
%dir %{_gsdir}/System/Library/Documentation/Developer/Guile
%{_gsdir}/System/Library/Documentation/Developer/Guile/ReleaseNotes

%{_gsdir}/System/Library/Libraries/Guile
%attr(755,root,root) %{_gsdir}/System/Library/Libraries/%{gscpu}/%{gsos}/%{libcombo}/lib*.so.*

%attr(755,root,root) %{_gsdir}/System/Tools/%{gscpu}/%{gsos}/%{libcombo}/*

%files devel
%defattr(644,root,root,755)
# UNIX world
%attr(755,root,root) %{_libdir}/libgreg.so
%{_libdir}/libgreg.la
# static?
#%%{_libdir}/libgreg.a

# GNUstep world
%docdir %{_prefix}/System/Library/Documentation
%{_gsdir}/System/Library/Documentation/Developer/Guile/Manual
%{_gsdir}/System/Library/Documentation/info/*.info*
%{_gsdir}/System/Library/Headers/%{libcombo}/GNUstepGuile
%{_gsdir}/System/Library/Headers/%{libcombo}/ScriptKit
%{_gsdir}/System/Library/Headers/%{libcombo}/gnustep/guile
%{_gsdir}/System/Library/Libraries/%{gscpu}/%{gsos}/%{libcombo}/lib*.so
%{_gsdir}/System/Library/Makefiles/Additional/guile.make
