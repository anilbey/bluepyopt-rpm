# versioneer is used, so no tags for patch versions
# use git tar since pypi does not include examples that are needed for tests.
%global commit cc5448730d73311150421a4bec0930315d39cf9b
%global shortcommit %(c=%{commit}; echo ${c:0:7})

# Tests use deprecated nose, so are currently disabled
# We run these in mock to test for the time being
# Asked upstream to stop using nose for tests
# https://github.com/BlueBrain/BluePyOpt/issues/358
%bcond_with tests

%global pypi_name bluepyopt
%global pretty_name BluePyOpt

%global _description %{expand:
The Blue Brain Python Optimisation Library (BluePyOpt) is an extensible
framework for data-driven model parameter optimisation that wraps and
standardises several existing open-source tools. It simplifies the task of
creating and sharing these optimisations, and the associated techniques and
knowledge. This is achieved by abstracting the optimisation and evaluation
tasks into various reusable and flexible discrete elements according to
established best-practices.}

Name: python-%{pypi_name}
Version: 1.9.149
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
# Required to compile neuron based models
BuildRequires:  neuron-devel
BuildRequires:  gcc-c++
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel

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

%description %_description

%package -n python3-%{pypi_name}
Summary:        %{summary}

# Only need to list ones not listed in setup.py
Requires: neuron-devel
Requires: python3-neuron
Requires: python3dist(setuptools)

# Not needed for F33+
%py_provides python3-%{srcname}

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
pushd bluepyopt/tests/
    # One tests fails
    PYTHONPATH=$RPM_BUILD_ROOT/%{python3_sitelib} nosetests-%{python3_version} -a 'unit' -s -v -x -e test_metaparameter
    PYTHONPATH=$RPM_BUILD_ROOT/%{python3_sitelib} nosetests-%{python3_version} -a '!unit' -s -v -x
popd
%endif

%files -n python3-%{pypi_name}
%license LICENSE.txt LGPL.txt
%doc README.rst

%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
%{_bindir}/bpopt_tasksdb

%changelog
* Sun Apr 11 2021 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.9.149-1
- Update to latest release

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
