Summary:	An X Window System image editing or paint program
Name:		xpaint
Version:	2.8.7.3
Release:	%mkrel 1
License:        MIT
Group:		Graphics
BuildRequires: 	xpm-devel jpeg-devel png-devel libxp-devel
BuildRequires:	tiff-devel zlib-devel bison flex 
BuildRequires:  Xaw3d-devel imake gccmakedep
Source0:	http://prdownloads.sourceforge.net/sf-xpaint/xpaint-%{version}.tar.bz2
Source1:	icons-%{name}.tar.bz2
URL:            https://sourceforge.net/projects/sf-xpaint
BuildRoot:	%{_tmppath}/xpaint-root

%description
XPaint is an X Window System color image editing program which supports
many standard paint program operations. XPaint also supports advanced
features like image processing algorithms, scripting and batch jobs.  
XPaint allows you to edit multiple images simultaneously and supports
a large variety of image formats, including PNG, JPEG, TIFF, XPM, PPM, 
XBM, PS, etc.

Install this package if you need a simple paint program for X.

Recent versions of XPaint add new optional editing features based 
on programmable filters and user defined procedures written as scripts 
in plain C. The package includes a substantial list of examples and 
some support for batch processing.

%prep
%setup -q 

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

