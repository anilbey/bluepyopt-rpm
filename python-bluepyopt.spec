%global pypi_name bluepyopt

Summary: Bluebrain Python Optimisation Library (bluepyopt)
Name: python-%{pypi_name}
Version: 1.9.48
Release: 1%{?dist}
Source0: %{pypi_source}
License: LGPLv3
BuildRoot: %{_tmppath}/%{pypi_name}-%{version}-%{release}-buildroot
BuildArch: noarch
Url: https://github.com/BlueBrain/BluePyOpt

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

# Only need to list ones not listed in setup.py
Requires: python3-neuron
Requires: python3dist(setuptools)

%description
The Blue Brain Python Optimisation Library (BluePyOpt) is an extensible framework for data-driven model parameter optimisation that wraps and standardises several existing open-source tools. It simplifies the task of creating and sharing these optimisations, and the associated techniques and knowledge. This is achieved by abstracting the optimisation and evaluation tasks into various reusable and flexible discrete elements according to established best-practices.

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

%check
%if %{with tests}
%{__python3} setup.py test
%endif

%files -n python-%{pypi_name}
%license LICENSE.txt LGPL.txt
%doc README.md

%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
/usr/bin/bpopt_tasksdb

%changelog
* 17 June 2020 Anil Tuncel <tuncel.manil@gmail.com>
- Initial package generated using python setup.py bdist --formats=rpm
* 25 June 2020 Anil Tuncel <tuncel.manil@gmail.com>
- Removed INSTALLED_FILES method
- Updated file checks
- Added check to run tests
- Removed the %clean tag
- use autosetup, py3_build, py3_install
- use pypi_source macro
- removed deprecated release, vengor and group tags

%defattr(-,root,root)
