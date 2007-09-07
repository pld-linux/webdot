Summary:	A CGI graph server script that uses tcldot utility
Summary(pl.UTF-8):	Skrypt serwerowy CGI do grafów używający narzędzia tcldot
Name:		webdot
Version:	2.10
Release:	1
Group:		Applications/Graphics
License:	BSD-like
Source0:	http://www.graphviz.org/pub/graphviz/ARCHIVE/%{name}-%{version}.tar.gz
# Source0-md5:	8a5e8a039f8e40603a9971d527892442
Patch0:		%{name}-status.patch
URL:		http://www.graphviz.org/
Requires:	filesystem >= 3.0-11
# it wants to open "Times" font by filename
Requires:	fonts-TTF-microsoft
Requires:	graphviz-tcl >= 2.10
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

%description -l pl.UTF-8
webdot to program CGI tworzący klikalne grafy na stronach WWW kiedy
href wskazuje na plik .dot. Używa Tcldot z pakietu graphviz-tcl.

%prep
%setup -q
%patch0 -p1

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
