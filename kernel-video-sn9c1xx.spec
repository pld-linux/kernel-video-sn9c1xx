#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%define		rel		0.1
%define		pname	sn9c1xx
Summary:	Video4Linux2 driver for SN9C1xx PC Camera Controllers
Name:		%{pname}%{_alt_kernel}
Version:	1.48
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Group:		Base/Kernel
Source0:	http://www.linux-projects.org/downloads/%{pname}-%{version}.tar.gz
# Source0-md5:	d5af6f1b1c2807787ca19ba79e49201a
URL:		http://www.linux-projects.org/modules/mydownloads/viewcat.php?cid=2
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Video4Linux2 driver for SN9C101, SN9C102, SN9C103, SN9C105, SN9C120 PC
Camera Controllers.

%prep
%setup -q -n %{pname}-%{version}

%build
%if %{with kernel}
%build_kernel_modules -m sn9c102
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with kernel}
%install_kernel_modules -m sn9c102 -d kernel/misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%if %{with kernel}
%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*
%endif
