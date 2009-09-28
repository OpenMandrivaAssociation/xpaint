Summary:	An X Window System image editing or paint program
Name:		xpaint
Version:	2.8.0
Release:	%mkrel 1
License:        MIT
Group:		Graphics
BuildRequires: 	xpm-devel jpeg-devel png-devel libxp-devel
BuildRequires:	tiff-devel zlib-devel bison flex 
BuildRequires:  Xaw3d-devel imake gccmakedep
Source0:	http://prdownloads.sourceforge.net/sf-xpaint/xpaint-%{version}.tar.bz2
Source1:	icons-%{name}.tar.bz2
# (fc) 2.8.0-1mdv fix format string error
Patch0:		xpaint-2.8.0-fmt_string.patch
# (fc) 2.8.0-1mdv fix build with xaw3d
Patch1:		xpaint-2.8.0-xaw3d.patch
URL:            https://sourceforge.net/projects/sf-xpaint
BuildRoot:	%{_tmppath}/xpaint-root

%description
XPaint is an X Window System color image editing program which supports
most standard paint program options.  XPaint also supports advanced
features like image processing algorithms.  XPaint allows you to edit
multiple images simultaneously and supports a variety of image formats,
including PPM, XBM, TIFF, JPEG, etc.

Install the xpaint package if you need a paint program for X.

Xpaint now uses the Xaw95 widget set for a bit nicer look, as well as
adding some new editing features including user filters. Some example
filter code is included. 

%prep
%setup -q 
%patch0 -p1 -b .fmt_string
%patch1 -p1 -b .xaw3d

%build
sed -i -e "s/\(XCOMM CDEBUGFLAGS =\)/CDEBUGFLAGS = $RPM_OPT_FLAGS\nCXXDEBUGFLAGS = $RPM_OPT_FLAGS/g" Local.config
./configure

%make xaw3d

%install
rm -rf $RPM_BUILD_ROOT

make \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_bindir} \
	MANDIR=%{_mandir}/man1 install install.man

# (sb) fix the include path in the built in scripting filter examples
#perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_datadir}/xpaint/filters/*.c

#mdk menu entry

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Xpaint
Comment=Paint program
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Graphics;
EOF

#mdk icon
install -d $RPM_BUILD_ROOT%{_iconsdir}
tar jxf %{SOURCE1} -C $RPM_BUILD_ROOT%{_iconsdir}

# symlink on /etc
rm -f $RPM_BUILD_ROOT/usr/lib/X11/app-defaults

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog README README.PNG TODO Doc
%{_bindir}/*
%{_mandir}/man1/xpaint.1x*
%{_datadir}/xpaint
%config(noreplace) %{_sysconfdir}/X11/app-defaults/XPaint*
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/*.png
%{_iconsdir}/*/*.png

