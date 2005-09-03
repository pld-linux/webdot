Summary:	A CGI graph server script that uses tcldot utility
Summary(pl):	Skrypt serwerowy CGI do grafów u¿ywaj±cy narzêdzia tcldot
Name:		webdot
Version:	2.6
Release:	1
Group:		Applications/Graphics
License:	BSD-like
Source0:	http://www.graphviz.org/pub/graphviz/ARCHIVE/%{name}-%{version}.tar.gz
# Source0-md5:	dbf6712c9a5fd069defeeb58d081ee86
Patch0:		%{name}-status.patch
URL:		http://www.graphviz.org/
Requires:	FHS >= 2.3-12
# it wants to open "Times" font by filename
Requires:	fonts-TTF-microsoft
Requires:	graphviz-tcl
Requires:	ghostscript
Requires:	tcl
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		appdir		%{_datadir}/webdot
%define		cgibindir	%{_prefix}/lib/cgi-bin
%define		cachedir	/var/cache/webdot
%define		tcldotlib	/usr/%{_lib}/graphviz/libtcldot.so

%description
A cgi-bin program that produces clickable graphs in web pages when
provided with an href to a .dot file. Uses Tcldot from the
graphviz-tcl package.

%description -l pl
webdot to program CGI tworz±cy klikalne grafy na stronach WWW kiedy
href wskazuje na plik .dot. U¿ywa Tcldot z pakietu graphviz-tcl.

%prep
%setup -q
%patch -p1

find . -type d -name CVS | xargs rm -rf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{cgibindir},%{appdir},%{cachedir}}
cp -r html/webdot/* $RPM_BUILD_ROOT%{appdir}

cat > $RPM_BUILD_ROOT%{cgibindir}/webdot <<'EOF'
#!/usr/bin/tclsh
set LIBTCLDOT %{tcldotlib}
set CACHE_ROOT %{cachedir}
set GS /usr/bin/gs
set PS2EPSI /usr/bin/ps2epsi
set LOCALHOSTONLY 1
EOF
cat cgi-bin/webdot >> $RPM_BUILD_ROOT%{cgibindir}/webdot

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES COPYING README
%attr(755,root,root) %{cgibindir}/webdot
%{appdir}
%attr(770,root,http) %{cachedir}
