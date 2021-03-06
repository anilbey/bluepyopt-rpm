# Tests currently disabled
# pebble is missing a build for rawhide:
# https://bugzilla.redhat.com/show_bug.cgi?id=1851120
%bcond_with tests

%global pypi_name bluepyopt

Name: python-%{pypi_name}
Version: 1.9.48
Release: 1%{?dist}
Summary: Bluebrain Python Optimisation Library (bluepyopt)

License: LGPLv3
URL: https://github.com/BlueBrain/BluePyOpt
Source0: %{pypi_source}

BuildArch: noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

BuildRequires:  python3-neuron


# Only need to list ones not listed in setup.py
Requires: python3-neuron
Requires: python3dist(setuptools)

%global _description %{expand:
The Blue Brain Python Optimisation Library (BluePyOpt) is an extensible
framework for data-driven model parameter optimisation that wraps and
standardises several existing open-source tools. It simplifies the task of
creating and sharing these optimisations, and the associated techniques and
knowledge. This is achieved by abstracting the optimisation and evaluation
tasks into various reusable and flexible discrete elements according to
established best-practices.}

%description %_description

%package -n python3-%{pypi_name}
Summary:        %{summary}

# For Fedora 32/31, not needed for F33+
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -n %{pypi_name}-%{version}
# Optional dependency, remove so that automatic dep generator does not pick it up
sed -i '/scoop/ d' setup.py


%build
%py3_build

%install
%py3_install

%check
%if %{with tests}
%{__python3} setup.py test
%endif

%files -n python3-%{pypi_name}
%license LICENSE.txt LGPL.txt
%doc README.md

%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
%{_bindir}/bpopt_tasksdb

%changelog
* Thu Jun 25 2020 Anil Tuncel <tuncel.manil@gmail.com> - 1.9.48-1
- Removed INSTALLED_FILES method
- Updated file checks
- Added check to run tests
- Removed the %%clean tag
- use autosetup, py3_build, py3_install
- use pypi_source macro
- removed deprecated release, vengor and group tags

* Wed Jun 17 2020 Anil Tuncel <tuncel.manil@gmail.com> - 1.9.48-1
- Initial package generated using python setup.py bdist --formats=rpm
