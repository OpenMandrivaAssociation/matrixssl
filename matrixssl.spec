%define	major	1
%define libname	%mklibname %{name} %{major}

Summary:	MatrixSSL is an embedded SSL implementation
Name:		matrixssl
Version:	1.8.3
Release:	%mkrel 1
License:	GPL
Group:		System/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.matrixssl.org/
Source0:	%{name}-1-8-3-open.tar.gz
Patch0:		matrixssl-shared_and_static.diff
Patch1:		matrixssl-1.8.1-debian.diff
BuildRequires:	dietlibc-devel >= 0.20
BuildRequires:	dos2unix

%description
PeerSec MatrixSSL is an embedded SSL implementation designed for 
small footprint devices and applications requiring low overhead per 
connection. The library is less than 50K on disk with cipher suites.

It includes SSL client and SSL server support, session resumption, 
and implementations of RSA, 3DES, ARC4, SHA1, and MD5. The source is
well documented and contains portability layers for additional 
operating systems, cipher suites, and cryptography providers. 

%package -n	%{libname}
Summary:	MatrixSSL is an embedded SSL implementation
Group:          System/Libraries

%description -n	%{libname}
PeerSec MatrixSSL is an embedded SSL implementation designed for 
small footprint devices and applications requiring low overhead per 
connection. The library is less than 50K on disk with cipher suites.

It includes SSL client and SSL server support, session resumption, 
and implementations of RSA, 3DES, ARC4, SHA1, and MD5. The source is
well documented and contains portability layers for additional 
operating systems, cipher suites, and cryptography providers. 

%package -n	%{libname}-devel
Summary:	Static library and header files for the %{name} library
Group:		Development/C
Obsoletes:	%{name}-devel lib%{name}-devel
Provides:	%{name}-devel lib%{name}-devel
Requires:	%{libname} = %{version}
Requires:	dietlibc-devel >= 0.20

%description -n	%{libname}-devel
PeerSec MatrixSSL is an embedded SSL implementation designed for 
small footprint devices and applications requiring low overhead per 
connection. The library is less than 50K on disk with cipher suites.

It includes SSL client and SSL server support, session resumption, 
and implementations of RSA, 3DES, ARC4, SHA1, and MD5. The source is
well documented and contains portability layers for additional 
operating systems, cipher suites, and cryptography providers. 

This package contains the static libraries and headers for both
glibc and dietlibc.

%prep

%setup -q -n %{name}-1-8-3-open
%patch0 -p0
%patch1 -p1

# prepare for dietlibc
mkdir -p dietlibc
cp -rp src dietlibc/
cp matrixSsl.h matrixCommon.h dietlibc/

# strip away annoying ^M
find -type f -exec dos2unix -U {} \;

%build

# first make the standard glibc stuff...
make -C src DFLAGS="%{optflags} -fPIC"

# now make the dietlibc static library
make -C dietlibc/src CC="diet -Os gcc" \
    LDFLAGS="-nostdlib" \
    static

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_prefix}/lib/dietlibc/{lib,include}

# fix headers
perl -pi -e "s|src/matrixConfig\.h|matrixConfig\.h|g" matrixCommon.h dietlibc/matrixCommon.h

# install the glibc version
install -m0755 src/lib%{name}.so %{buildroot}%{_libdir}/lib%{name}.so.%{version}
ln -snf lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so.%{major}
ln -snf lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so
install -m0644 src/lib%{name}.a %{buildroot}%{_libdir}/
install -m0644 matrixSsl.h %{buildroot}%{_includedir}/
install -m0644 matrixCommon.h %{buildroot}%{_includedir}/
install -m0644 src/matrixConfig.h %{buildroot}%{_includedir}/

# install the dietlibc version
install -m0644 dietlibc/src/lib%{name}.a %{buildroot}%{_prefix}/lib/dietlibc/lib/
install -m0644 dietlibc/matrixSsl.h %{buildroot}%{_prefix}/lib/dietlibc/include/
install -m0644 dietlibc/matrixCommon.h %{buildroot}%{_prefix}/lib/dietlibc/include/
install -m0644 dietlibc/src/matrixConfig.h %{buildroot}%{_prefix}/lib/dietlibc/include/

# cleanup the examples directory
rm -f examples/*.sln
rm -f examples/*.vcproj
rm -f examples/*.pem
rm -f examples/*.p12

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc doc/*.pdf examples
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_prefix}/lib/dietlibc/include/*
%{_prefix}/lib/dietlibc/lib/*.a


