Summary:	An X Window System image editing or paint program
Name:		xpaint
Version:	2.7.8.1
Release:	%mkrel 5
License:        MIT
Group:		Graphics
BuildRequires: 	X11-devel xpm-devel jpeg-devel png-devel 
BuildRequires:	tiff-devel zlib-devel bison flex xorg-x11
BuildRequires:  Xaw3d-devel imake gccmakedep
Source0:	http://prdownloads.sourceforge.net/sf-xpaint/xpaint-%{version}.tar.bz2
Source1:	icons-%{name}.tar.bz2
Patch0:		xpaint-2.7.8.1-new-X.patch
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
%patch0 -p1 -b .new-X

%build
xmkmf -a
perl -p -i -e "s|CXXDEBUGFLAGS = .*|CXXDEBUGFLAGS = $RPM_OPT_FLAGS|" Makefile
perl -p -i -e "s|CDEBUGFLAGS = .*|CDEBUGFLAGS = $RPM_OPT_FLAGS|" Makefile
make CDEBUGFLAGS="$RPM_OPT_FLAGS" xaw

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
StartupNotify=true
Categories=X-MandrivaLinux-Multimedia-Graphics;Graphics;
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
%{_bindir}/xpaint
%{_mandir}/man1/xpaint.1x*
%dir %{_datadir}/xpaint
%{_datadir}/xpaint/*.xpm
%dir %{_datadir}/xpaint/c_scripts
%dir %{_datadir}/xpaint/c_scripts/3d_curves
%dir %{_datadir}/xpaint/c_scripts/3d_surfaces
%dir %{_datadir}/xpaint/c_scripts/filters
%dir %{_datadir}/xpaint/c_scripts/images
%dir %{_datadir}/xpaint/c_scripts/layers
%dir %{_datadir}/xpaint/c_scripts/procedures
%{_datadir}/xpaint/c_scripts/3d_curves/*
%{_datadir}/xpaint/c_scripts/3d_surfaces/*
%{_datadir}/xpaint/c_scripts/filters/*
%{_datadir}/xpaint/c_scripts/images/*
%{_datadir}/xpaint/c_scripts/layers/*
%{_datadir}/xpaint/c_scripts/procedures/*
%dir %{_datadir}/xpaint/help
%{_datadir}/xpaint/help/*
%dir %{_datadir}/xpaint/messages
%{_datadir}/xpaint/messages/*
%dir %{_datadir}/xpaint/include
%{_datadir}/xpaint/include/*
%config(noreplace) %{_sysconfdir}/X11/app-defaults/XPaint*
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/*.png
%{_iconsdir}/*/*.png

