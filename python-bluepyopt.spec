# versioneer is used, so no tags for patch versions
# use git tar since pypi does not include examples that are needed for tests.
%global commit 4024a233c6475e7e757d82e522dfca11089ada6a
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%bcond_without tests

%global pypi_name bluepyopt
%global pretty_name BluePyOpt

Name: python-%{pypi_name}
Version: 1.9.48
Release: 1%{?dist}
Summary: Bluebrain Python Optimisation Library (bluepyopt)

License: LGPLv3
URL: https://github.com/BlueBrain/BluePyOpt
Source0: %{url}/archive/%{commit}/%{pretty_name}-%{shortcommit}.tar.gz
# use _version file from pypi tar to trick versioneer
Source1: %{pypi_name}-%{version}_version.py

BuildArch: noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

# To run tests
%if %{with tests}
BuildRequires:  %{py3_dist future}
BuildRequires:  %{py3_dist deap}
BuildRequires:  %{py3_dist efel}
BuildRequires:  %{py3_dist ipyparallel}
BuildRequires:  %{py3_dist jinja2}
BuildRequires:  python3-jupyter-client
BuildRequires:  python3-nbconvert
BuildRequires:  %{py3_dist mock}
BuildRequires:  python3-neuron
BuildRequires:  neuron-devel
BuildRequires:  %{py3_dist nose}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist pandas}
BuildRequires:  %{py3_dist pebble}
BuildRequires:  %{py3_dist pickleshare}
%endif


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

# Only need to list ones not listed in setup.py
Requires: neuron-devel
Requires: python3-neuron
Requires: python3dist(setuptools)


# For Fedora 32/31, not needed for F33+
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -n %{pretty_name}-%{commit}
# Optional dependency, remove so that automatic dep generator does not pick it up
sed -i '/scoop/ d' setup.py

# For tests, we install jupyter as BuildRequires
# remove all Makefile deps on the jupyter target
# need to check this for each update, in case the makefile changes
sed -i 's/^\(.*:.*\)jupyter$/\1/' Makefile

mv -v %{SOURCE1} "%{pypi_name}/_version.py"

%build
%py3_build

%install
%py3_install

%check
%if %{with tests}
# Prepare for tests
# Refer to: https://github.com/BlueBrain/BluePyOpt/blob/master/tox.ini
# and https://github.com/BlueBrain/BluePyOpt/blob/master/Makefile
make stochkv_prepare l5pc_prepare sc_prepare meta_prepare
# one erring test, and one failing test disabled: both eFEL related
PYTHONPATH=$RPM_BUILD_ROOT/%{python3_sitelib} nosetests-%{python3_version} -a unit -e test_eFELFeature_string_settings -e test_eFELFeature
PYTHONPATH=$RPM_BUILD_ROOT/%{python3_sitelib} nosetests-%{python3_version} -a !unit
%endif

%files -n python3-%{pypi_name}
%license LICENSE.txt LGPL.txt
%doc README.md

%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
%{_bindir}/bpopt_tasksdb

%changelog
* Mon Jul 06 2020 Anil Tuncel <tuncel.manil@gmail.com> - 1.9.48-1
- Move neuron requirement to subpackage
- Enable tests
- Use github tar since pypi tar does not include examples

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
