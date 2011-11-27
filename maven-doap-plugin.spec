Name:           maven-doap-plugin
Version:        1.0
Release:        6
Summary:        Plugins which generate a DOAP file from information in a POM

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-doap-plugin/
# svn export http://svn.apache.org/repos/asf/maven/plugins/tags/maven-doap-plugin-1.0/
# tar jcf maven-doap-plugin-1.0.tar.gz maven-doap-plugin-1.0/
Source0:        %{name}-%{version}.tar.bz2
Patch0:        %{name}-pom.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: java-devel >= 0:1.6.0
BuildRequires: plexus-utils
BuildRequires: ant-nodeps
BuildRequires: maven2
BuildRequires: maven-install-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-maven-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-plugin-testing-harness
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: jpackage-utils
Requires: ant-nodeps
Requires: maven2
Requires: jpackage-utils
Requires: java
Requires(post): jpackage-utils
Requires(postun): jpackage-utils 

Obsoletes: maven2-plugin-doap <= 0:2.0.8
Provides: maven2-plugin-doap = 1:%{version}-%{release}

%description
Maven 2 DOAP Plugin is used to generate compliant Description 
of a Project (DOAP) file from a POM. The main goal is to 
be able to provide DOAP files for Semantic Web systems that 
use them as primary input but that would also alleviate 
the burden of maintaining two sets of metadata.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires: jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}
%patch0 -b .sav

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository

mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap org.apache.maven.plugins %{name} %{version} JPP %{name}

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

