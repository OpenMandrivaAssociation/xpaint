Summary:	An X Window System image editing or paint program
Name:		xpaint
Version:	2.9.1.4
Release:	%mkrel 1
License:	MIT
Group:		Graphics
BuildRequires:	xpm-devel jpeg-devel png-devel libxp-devel
BuildRequires:	tiff-devel zlib-devel bison flex 
BuildRequires:	Xaw3d-devel xaw3dxft-devel imake gccmakedep
BuildRequires:	libxft-devel chrpath
Source0:	http://prdownloads.sourceforge.net/sf-xpaint/xpaint-%{version}.tar.bz2
Source1:	icons-%{name}.tar.bz2
Patch0:		xpaint-2.8.18-use_system_Xaw3dxft.patch
URL:		https://sourceforge.net/projects/sf-xpaint
BuildRoot:	%{_tmppath}/xpaint-root
# Menus uses Liberation fonts
Requires:	fonts-ttf-liberation

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
%patch0 -p1

%build
# adapted fixes from Fedora
sed -i -e "s/\(XCOMM CDEBUGFLAGS =\)/CDEBUGFLAGS = $RPM_OPT_FLAGS\nCXXDEBUGFLAGS = $RPM_OPT_FLAGS/g" Local.config
sed -i -e 's|-lXpm|-lXpm -lX11 -lm -lXmu -lXt -lXext|g' Local.config
sed -i -e 's|-lpng -lz|-lpng|g' Local.config
sed -i -e 's|/lib |/%{_lib} |g' Local.config
sed -i -e 's|@XPMDIR@|%{_prefix}|g' Local.config
sed -i -e 's|/usr/lib|%{_libdir}|g' configure
sed -i -e 's|install -c -s pdfconcat|install -c pdfconcat|g' Imakefile
sed -i -e 's|CFLAGS="-O3 -s -DNDEBUG=1"|CFLAGS=$RPM_OPT_FLAGS|g' pdfconcat.c
for f in ChangeLog README; do
    iconv -f iso-8859-1 -t utf-8 $f > $f.utf8
    touch -r $f $f.utf8
    mv $f.utf8 $f
done

#%%configure or %%configure2_5x brokes the build
./configure xaw3dxft.so

#%%make brokes the build
make

%install
rm -rf %{buildroot}

%makeinstall_std install.man

#mdk menu entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Xpaint
Comment=Paint program
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Graphics;
EOF

#mdk icon
install -d %{buildroot}%{_iconsdir}
tar jxf %{SOURCE1} -C %{buildroot}%{_iconsdir}

# rpath
chrpath -d %{buildroot}%{_bindir}/xpaint

# symlink on /etc
rm -rf %{buildroot}/usr/lib/X11/app-defaults

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog README* TODO Doc/*.doc Doc/sample.Xdefaults
%{_bindir}/*
%{_mandir}/man1/xpaint.1x*
%{_datadir}/xpaint
%config(noreplace) %{_sysconfdir}/X11/app-defaults/*
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/*.png
%{_iconsdir}/*/*.png
