#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	frozenlist
Summary:	A list-like structure which implements collections.abc.MutableSequence
Summary(pl.UTF-8):	Podobna do listy struktura implementująca collections.abc.MutableSequence
Name:		python3-%{module}
Version:	1.5.1
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/frozenlist/
# Source0:	https://files.pythonhosted.org/packages/source/f/frozenlist/%{module}-%{version}.tar.gz
Source0:	https://github.com/aio-libs/frozenlist/archive/57ce23807c0d08651106c9de0b78e525838f3fac.zip
# Source0-md5:	1b50afd47f8eb56e34efdde796207b2b
Patch0:		disable-towncrier.patch
URL:		https://pypi.org/project/frozenlist/
BuildRequires:	python3-Cython >= 3.0.12
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-expandvars
BuildRequires:	python3-installer
BuildRequires:	python3-setuptools >= 1:47
%if %{_ver_lt "%py3_ver" 3.11}
BuildRequires:	python3-tomli
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-aiohttp_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
frozenlist.FrozenList is a list-like structure which implements
collections.abc.MutableSequence. The list is mutable until
FrozenList.freeze is called, after which list modifications
raise RuntimeError.

%description -l pl.UTF-8
frozenlist.FrozenList to podobna do listy struktura implementująca
collections.abc.MutableSequence. Lista jest modyfikowalna do czasu
wywołania FrozenList.freeze, po którym próby modyfikacji rzucą
wyjątek RuntimeError.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
#%%setup -q -n %{module}-%{version}
%setup -q -n %{module}-57ce23807c0d08651106c9de0b78e525838f3fac
%patch -P0 -p1

# keep *.c files so debuginfo will pick it up
sed -i -e 's#build_inplace: bool = False,#build_inplace: bool = True,#g' -e 's#build_inplace=False#build_inplace=True#g' packaging/pep517_backend/_backend.py

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst CONTRIBUTORS.txt README.rst
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/*.pyi
%{py3_sitedir}/%{module}/*.pyx
%{py3_sitedir}/%{module}/py.typed
%attr(755,root,root) %{py3_sitedir}/%{module}/*.so
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/%{module}-%{version}*.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
