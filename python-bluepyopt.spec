%global pypi_name bluepyopt

Name:           python-%{pypi_name}
Version:        1.9.48
Release:        1%{?dist}
Summary:        Bluebrain Python Optimisation Library (bluepyopt)

License:        LGPLv3
URL:            https://github.com/BlueBrain/BluePyOpt
Source0:        https://files.pythonhosted.org/packages/source/b/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
The Blue Brain Python Optimisation Library (BluePyOpt) is an extensible
framework for data-driven model parameter optimisation that wraps and
standardises several existing open-source tools. It simplifies the task of
creating and sharing these optimisations, and the associated techniques and
knowledge. This is achieved by abstracting the optimisation and evaluation
tasks into various reusable...

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Requires:       python3-neuron
Requires:       python3dist(deap)
Requires:       python3dist(efel) >= 2.13
Requires:       python3dist(future)
Requires:       python3dist(ipyparallel)
Requires:       python3dist(jinja2) >= 2.8
Requires:       python3dist(numpy) >= 1.6
Requires:       python3dist(pandas) >= 0.18
Requires:       python3dist(pickleshare) >= 0.7.3
Requires:       python3dist(setuptools)
%description -n python3-%{pypi_name}
The Blue Brain Python Optimisation Library (BluePyOpt) is an extensible
framework for data-driven model parameter optimisation that wraps and
standardises several existing open-source tools. It simplifies the task of
creating and sharing these optimisations, and the associated techniques and
knowledge. This is achieved by abstracting the optimisation and evaluation
tasks into various reusable...


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%doc README.md
%{_bindir}/bpopt_tasksdb
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Sun Jul 07 2019 Luis M. Segundo <blackfile@fedoraproject.org> - 1.8.38-1
- Initial package.
