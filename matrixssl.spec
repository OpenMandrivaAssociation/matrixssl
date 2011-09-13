%define	major 3
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Embedded SSL implementation
Name:		matrixssl
Version:	3.2.1
Release:	%mkrel 1
License:	GPLv2
Group:		System/Libraries
URL:		http://www.matrixssl.org/
Source0:	%{name}-3-2-1-open.tgz
Patch0:		matrixssl-3.2.1-no_strip.diff
Patch2:		matrixssl-3.2.1-soname.diff
BuildRequires:	dietlibc-devel >= 0.32
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PeerSec MatrixSSL is an embedded SSL implementation designed for 
small footprint devices and applications requiring low overhead per 
connection. The library is less than 50K on disk with cipher suites.

It includes SSL client and SSL server support, session resumption, 
and implementations of RSA, 3DES, ARC4, SHA1, and MD5. The source is
well documented and contains portability layers for additional 
operating systems, cipher suites, and cryptography providers. 

%package -n	%{libname}
Summary:	Embedded SSL implementation
Group:          System/Libraries

%description -n	%{libname}
PeerSec MatrixSSL is an embedded SSL implementation designed for 
small footprint devices and applications requiring low overhead per 
connection. The library is less than 50K on disk with cipher suites.

It includes SSL client and SSL server support, session resumption, 
and implementations of RSA, 3DES, ARC4, SHA1, and MD5. The source is
well documented and contains portability layers for additional 
operating systems, cipher suites, and cryptography providers. 

%package -n	%{develname}
Summary:	Static library and header files for the %{name} library
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	dietlibc-devel >= 0.32
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel
Obsoletes:	%{mklibname matrixssl -d 1}

%description -n	%{develname}
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

%setup -q -n %{name}-3-2-1-open
%patch0 -p0

# prepare for dietlibc
mkdir -p dietlibc
cp -rp core crypto matrixssl Makefile dietlibc/

%build

# first make the standard glibc stuff...
make DFLAGS="%{optflags} -fPIC" MAJOR="%{major}"

# now make the dietlibc static library
make -C dietlibc CC="diet -Os gcc" \
    DFLAGS="" \
    LDFLAGS="-nostdlib" \
    libmatrixssl.a

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_prefix}/lib/dietlibc/{lib,include}
install -d %{buildroot}%{_includedir}/matrixssl/core
install -d %{buildroot}%{_includedir}/matrixssl/crypto/{digest,keyformat,math,pubkey,symmetric}

# install the glibc version
install -m0755 lib%{name}.so %{buildroot}%{_libdir}/lib%{name}.so.%{version}
ln -snf lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so.%{major}
ln -snf lib%{name}.so.%{major} %{buildroot}%{_libdir}/lib%{name}.so
install -m0644 lib%{name}.a %{buildroot}%{_libdir}/

# install the headers
install -m0644 core/*.h %{buildroot}%{_includedir}/matrixssl/core/
install -m0644 crypto/*.h %{buildroot}%{_includedir}/matrixssl/crypto/
install -m0644 crypto/digest/*.h %{buildroot}%{_includedir}/matrixssl/crypto/digest/
install -m0644 crypto/keyformat/*.h %{buildroot}%{_includedir}/matrixssl/crypto/keyformat/
install -m0644 crypto/math/*.h %{buildroot}%{_includedir}/matrixssl/crypto/math/
install -m0644 crypto/pubkey/*.h %{buildroot}%{_includedir}/matrixssl/crypto/pubkey/
install -m0644 crypto/symmetric/*.h %{buildroot}%{_includedir}/matrixssl/crypto/symmetric/
install -m0644 matrixssl/matrixsslApi.h %{buildroot}%{_includedir}/matrixssl/
install -m0644 matrixssl/matrixsslConfig.h %{buildroot}%{_includedir}/matrixssl/
install -m0644 matrixssl/matrixssllib.h %{buildroot}%{_includedir}/matrixssl/

# install the dietlibc version
install -m0644 dietlibc/lib%{name}.a %{buildroot}%{_prefix}/lib/dietlibc/lib/

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc doc/*.pdf
%{_includedir}/matrixssl
%{_libdir}/*.so
%{_libdir}/*.a
%{_prefix}/lib/dietlibc/lib/*.a
