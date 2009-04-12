# TODO
# - ask atlassian for permission to redistribute it.
%include	/usr/lib/rpm/macros.java
Summary:	JIRA bug and issue tracker
Name:		jira-enterprise
Version:	3.13.3
Release:	0.1
License:	Proprietary, not distributable
Group:          Networking/Daemons/Java/Servlets
Source0:	http://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-enterprise-3.13.3.tar.gz
# NoSource0-md5:	9810796dcf4331218c3874174c9dbbee
NoSource:	0
Source1:	%{name}-context.xml
URL:		http://www.atlassian.com/software/jira/default.jsp
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	group(servlet)
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JIRA lets you prioritise, assign, track, report and audit your 'issues,'
whatever they may be — from software bugs and help-desk tickets to project
tasks and change requests.

More than just an issue tracker, JIRA is an extensible platform that you can
customise to match to your business processes.

%prep
%setup -n atlassian-%{name}-%{version}

%build
%ant compile

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jira,%{_datadir}/jira,%{_sharedstatedir}/{jira,tomcat/conf/Catalina/localhost}}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/jira.xml
cp -a tmp/build/war $RPM_BUILD_ROOT%{_datadir}/jira

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/jira
# do not make this file writeable by tomcat. We do not want to allow user to
# undeploy this app via tomcat manager.
%config(noreplace) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/jira.xml
%{_datadir}/jira
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira
