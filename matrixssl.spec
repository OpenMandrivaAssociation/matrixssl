%define	major 3
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Embedded SSL implementation
Name:		matrixssl
Version:	3.4.1
Release:	1
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


%changelog
* Tue Sep 13 2011 Oden Eriksson <oeriksson@mandriva.com> 3.2.1-1mdv2012.0
+ Revision: 699642
- 3.2.1
- really *use* soname (wtf?)

* Fri Jan 14 2011 Oden Eriksson <oeriksson@mandriva.com> 3.1.4-1
+ Revision: 631035
- 3.1.4

* Mon Sep 06 2010 Sandro Cazzaniga <kharec@mandriva.org> 3.1.3-1mdv2011.0
+ Revision: 576259
- update to 3.1.3

* Sat Apr 24 2010 Sandro Cazzaniga <kharec@mandriva.org> 3.1.1-1mdv2010.1
+ Revision: 538435
- rediff one patch
- drop p1, applied upstream
- fix %%file, %%install
- new version 3.1.1

* Fri Mar 12 2010 Oden Eriksson <oeriksson@mandriva.com> 3.1-1mdv2010.1
+ Revision: 518386
- 3.1

* Wed Nov 11 2009 Oden Eriksson <oeriksson@mandriva.com> 1.8.8-1mdv2010.1
+ Revision: 464623
- 1.8.8 (disables in-session renegotiation)

* Thu Aug 13 2009 Oden Eriksson <oeriksson@mandriva.com> 1.8.7d-1mdv2010.0
+ Revision: 416026
- 1.8.7d
- fix P1

* Thu Sep 11 2008 Oden Eriksson <oeriksson@mandriva.com> 1.8.6-1mdv2009.0
+ Revision: 283671
- 1.8.6
- rediffed P0

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 1.8.5-4mdv2009.0
+ Revision: 268137
- rebuild early 2009.0 package (before pixel changes)

* Tue Jun 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1.8.5-3mdv2009.0
+ Revision: 217533
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Jun 08 2008 Oden Eriksson <oeriksson@mandriva.com> 1.8.5-2mdv2009.0
+ Revision: 216901
- rebuilt against dietlibc-0.32

* Tue May 13 2008 Oden Eriksson <oeriksson@mandriva.com> 1.8.5-1mdv2009.0
+ Revision: 206562
- 1.8.5
- fix devel package naming

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.8.3-2mdv2008.1
+ Revision: 170978
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- fix no-buildroot-tag
- kill re-definition of %%buildroot on Pixel's request


* Sat Feb 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.8.3-1mdv2007.0
+ Revision: 118708
- 1.8.3
- rediffed the shared patch

* Tue Dec 19 2006 Oden Eriksson <oeriksson@mandriva.com> 1.8.2-1mdv2007.1
+ Revision: 100298
- Import matrixssl

* Tue Dec 19 2006 Oden Eriksson <oeriksson@mandriva.com> 1.8.2-1mdv2007.1
- 1.8.2

* Fri Jul 14 2006 Oden Eriksson <oeriksson@mandriva.com> 1.8.1-1mdv2007.0
- 1.8.1 (Minor feature enhancements)
- rediffed P1

* Sat Feb 04 2006 Oden Eriksson <oeriksson@mandriva.com> 1.8-1mdk
- 1.8 (Minor feature enhancements)
- rediffed P0,P1

* Sat Feb 04 2006 Oden Eriksson <oeriksson@mandriva.com> 1.7.3-1mdk
- 1.7.3

* Thu Oct 20 2005 Oden Eriksson <oeriksson@mandriva.com> 1.7.1-2mdk
- fix headers

* Sat Sep 17 2005 Oden Eriksson <oeriksson@mandriva.com> 1.7.1-1mdk
- 1.7.1
- rediffed P0

* Wed May 11 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.5-3mdk
- oops! another silly lib64 fix :)

* Wed May 11 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.5-2mdk
- really 1.2.5 (duh!)
- rediff P1 (fixes x86_64 build)
- fix common dietlibc location
- rpmlint fixes

* Fri Apr 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2.5-1mdk
- 1.2.5
- use the %%mkrel macro

* Fri Feb 25 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2.4-1mdk
- 1.2.4

* Fri Dec 31 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2.2-3mdk
- revert latest "lib64 fixes"

* Tue Dec 28 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2.2-2mdk
- lib64 fixes

* Fri Oct 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2.2-1mdk
- 1.2.2

* Thu Aug 05 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2-1mdk
- initial mandrake package

