# TODO:
# - ask atlassian for permission to redistribute it.
# - ERROR: Class version could not be extracted from /home/z/tmp/jira-enterprise-3.13.3-root-z/usr/share/jira/WEB-INF/classes/com/atlassian/jira/servlet/CaptchaService.class
%include	/usr/lib/rpm/macros.java
Summary:	JIRA bug and issue tracker
Name:		jira-enterprise
Version:	3.13.3
Release:	0.2
License:	Proprietary, not distributable
Group:		Networking/Daemons/Java/Servlets
Source0:	http://www.atlassian.com/software/jira/downloads/binary/atlassian-%{name}-%{version}.tar.gz
# NoSource0-md5:	9810796dcf4331218c3874174c9dbbee
NoSource:	0
Source1:	http://www.atlassian.com/software/jira/docs/servers/jars/v1/jira-jars-tomcat5.zip
# NoSource1-md5:	0c1184bc77a55cb09c3cd1a66ca06b4f
NoSource:	1
Source2:	%{name}-context.xml
Source3:	%{name}-README.PLD
Patch0:		%{name}-log4j-properties.patch
URL:		http://www.atlassian.com/software/jira/default.jsp
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
Requires:	tomcat
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JIRA lets you prioritise, assign, track, report and audit your
'issues,' whatever they may be - from software bugs and help-desk
tickets to project tasks and change requests.

More than just an issue tracker, JIRA is an extensible platform that
you can customise to match to your business processes.

%prep
%setup -q -n atlassian-%{name}-%{version} -a1
%patch0 -p1

cp %{SOURCE3} README.PLD

%build
%ant compile

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},/var/log/jira}
install -d $RPM_BUILD_ROOT%{_sharedstatedir}/jira/{jiradb,index,attachments,backups}
cp -a tmp/build/war $RPM_BUILD_ROOT%{_datadir}/jira

# configuration
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jira,%{_sharedstatedir}/tomcat/conf/Catalina/localhost}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/jira/tomcat-context.xml
ln -s %{_sysconfdir}/jira/tomcat-context.xml $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/jira.xml 
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/log4j.properties $RPM_BUILD_ROOT%{_sysconfdir}/jira/log4j.properties
ln -s %{_sysconfdir}/jira/log4j.properties $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/log4j.properties

# libraries missing in tomcat 5.5
install -d $RPM_BUILD_ROOT%{_datadir}/tomcat/common/lib
cp -a jira-jars-tomcat5/* $RPM_BUILD_ROOT%{_datadir}/tomcat/common/lib

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
# do not make this file writeable by tomcat. We do not want to allow user to
# undeploy this app via tomcat manager.
%{_datadir}/jira
%dir %{_sysconfdir}/jira
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jira/log4j.properties
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jira/tomcat-context.xml
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira/jiradb
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira/index
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira/attachments
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira/backups
%attr(2775,root,servlet) %dir /var/log/jira
%{_datadir}/tomcat/common/lib/*.jar
%doc licenses/csv.license README.PLD
