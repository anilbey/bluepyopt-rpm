%define name bluepyopt
%define version 1.9.48
%define unmangled_version 1.9.48
%define unmangled_version 1.9.48
%define release 1

BuildRequires:  python3dist(setuptools)

Summary: Bluebrain Python Optimisation Library (bluepyopt)
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: LGPLv3
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: BlueBrain Project, EPFL <werner.vangeit@epfl.ch>
Url: https://github.com/BlueBrain/BluePyOpt

Requires:	python3-neuron
Requires:       python3dist(deap)
Requires:       python3dist(efel) >= 2.13
Requires:       python3dist(future)
Requires:       python3dist(ipyparallel)
Requires:       python3dist(jinja2) >= 2.8
Requires:       python3dist(numpy) >= 1.6
Requires:       python3dist(pandas) >= 0.18
Requires:       python3dist(pickleshare) >= 0.7.3
# Requires:       python3dist(scoop) >= 0.7
Requires:       python3dist(setuptools)
Requires:	python3dist(pebble) >= 4.3.10

%description
The Blue Brain Python Optimisation Library (BluePyOpt) is an extensible framework for data-driven model parameter optimisation that wraps and standardises several existing open-source tools. It simplifies the task of creating and sharing these optimisations, and the associated techniques and knowledge. This is achieved by abstracting the optimisation and evaluation tasks into various reusable and flexible discrete elements according to established best-practices.

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python3 setup.py build

%install
python3 setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
