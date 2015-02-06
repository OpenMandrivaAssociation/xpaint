Summary:	An X Window System image editing or paint program
Name:		xpaint
Version:	2.9.8.3
Release:	2
License:	MIT
Group:		Graphics
URL:		https://sourceforge.net/projects/sf-xpaint
Source0:	http://prdownloads.sourceforge.net/sf-xpaint/xpaint-%{version}.tar.bz2
Source1:	icons-%{name}.tar.bz2
Patch0:		xpaint-build_against_system_libraries.patch
BuildRequires:	bison
BuildRequires:	chrpath
BuildRequires:	flex
BuildRequires:	gccmakedep
BuildRequires:	imake
BuildRequires:	pkgconfig(libopenjpeg1)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xp)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	jpeg-devel
BuildRequires:	Xaw3d-devel
BuildRequires:	xaw3dxft-devel

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
%patch0 -p0 -b .syslib

%build
# adapted fixes from Fedora
sed -i -e "s/\(XCOMM CDEBUGFLAGS =\)/CDEBUGFLAGS = %{optflags}\nCXXDEBUGFLAGS = %{optflags}/g" Local.config
sed -i -e 's|-lXpm|-lXpm -lX11 -lm -lXmu -lXt -lXext|g' Local.config
sed -i -e 's|-lpng -lz|-lpng|g' Local.config
sed -i -e 's|/lib |/%{_lib} |g' Local.config
sed -i -e 's|@XPMDIR@|%{_prefix}|g' Local.config
sed -i -e 's|JP2K_INCLUDE =|JP2K_INCLUDE = -I%{_includedir}/openjpeg-1.5|g' Local.config
sed -i -e 's|/usr/lib|%{_libdir}|g' configure
sed -i -e 's|install -c -s pdfconcat|install -c pdfconcat|g' Imakefile
#sed -i -e 's|CFLAGS="-O3 -s -DNDEBUG=1"|CFLAGS=%{optflags}|g' pdfconcat.c
for f in ChangeLog README; do
    iconv -f iso-8859-1 -t utf-8 $f > $f.utf8
    touch -r $f $f.utf8
    mv $f.utf8 $f
done

#build against system libraries
rm -rf xaw3dxft/
rm -rf Xaw3dxft/
rm -rf X11/

#%%configure or %%configure2_5x brokes the build
./configure xaw3dxft.so

#%%make brokes the build
make LOCAL_LDFLAGS="%{ldflags}"

%install
%makeinstall_std install.man

#use upstream .desktop file
install -Dpm0644 %{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

#mdk icon
install -d %{buildroot}%{_iconsdir}
tar jxf %{SOURCE1} -C %{buildroot}%{_iconsdir}

# rpath
chrpath -d %{buildroot}%{_bindir}/xpaint

# symlink on /etc
rm -rf %{buildroot}/usr/lib/X11/app-defaults

%files
%doc ChangeLog README* TODO Doc/*.doc Doc/sample.Xdefaults
%config(noreplace) %{_sysconfdir}/X11/app-defaults/*
%{_bindir}/*
%{_mandir}/man1/xpaint.*
%{_datadir}/xpaint
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/*.png
%{_iconsdir}/*/*.png

