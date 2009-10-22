# TODO:
# - ask atlassian for permission to redistribute it.
# - ERROR: Class version could not be extracted from /home/z/tmp/jira-enterprise-3.13.3-root-z/usr/share/jira/WEB-INF/classes/com/atlassian/jira/servlet/CaptchaService.class
# NOTE:
# - It does not work. Tomcat6 is unable to compile these JSPs. Prints some
#   JDT-related errors. See catalina.out for details.  Use TOMCAT-5_5 branch,
#   with tomcat 5.5.

%include	/usr/lib/rpm/macros.java
Summary:	JIRA bug and issue tracker
Name:		jira-enterprise
Version:	4.0
Release:	1
License:	Proprietary, not distributable
Group:		Networking/Daemons/Java/Servlets
# Sources:
# http://www.atlassian.com/software/jira/downloads/binary/atlassian-%{name}-%{version}.tar.gz
# http://www.atlassian.com/software/jira/docs/servers/jars/v1/jira-jars-tomcat5.zip
Source0:	atlassian-%{name}-%{version}.tar.gz
# NoSource0-md5:	173689228807247d9be56a0a0e8e1590
NoSource:	0
Source1:	jira-jars-tomcat5.zip
# NoSource1-md5:	0c1184bc77a55cb09c3cd1a66ca06b4f
NoSource:	1
Source2:	%{name}-context.xml
Source3:	%{name}-entityengine.xml
Source4:	%{name}-application.properties
Source5:	%{name}-README.PLD
Patch0:		%{name}-log4j-properties.patch
URL:		http://www.atlassian.com/software/jira/default.jsp
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
Requires:	tomcat >= 0:6.0.20-3
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

cp %{SOURCE3} edit-webapp/WEB-INF/classes/entityengine.xml
cp %{SOURCE4} edit-webapp/WEB-INF/classes/jira-application.properties
cp %{SOURCE5} README.PLD

%build
%ant compile

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},/var/log/jira}
install -d $RPM_BUILD_ROOT%{_sharedstatedir}/jira/{jiradb,index,attachments,backups}
cp -a tmp/build/war $RPM_BUILD_ROOT%{_datadir}/jira

# configuration
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jira,%{_sharedstatedir}/tomcat/conf/Catalina/localhost}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/jira.xml
ln -s %{_sharedstatedir}/tomcat/conf/Catalina/localhost/jira.xml $RPM_BUILD_ROOT%{_sysconfdir}/jira/tomcat-context.xml
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/jira-application.properties $RPM_BUILD_ROOT%{_sysconfdir}/jira/jira-application.properties
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/log4j.properties $RPM_BUILD_ROOT%{_sysconfdir}/jira/log4j.properties
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/entityengine.xml $RPM_BUILD_ROOT%{_sysconfdir}/jira/entityengine.xml
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/osuser.xml $RPM_BUILD_ROOT%{_sysconfdir}/jira/osuser.xml
ln -s %{_sysconfdir}/jira/jira-application.properties $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/jira-application.properties
ln -s %{_sysconfdir}/jira/log4j.properties $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/log4j.properties
ln -s %{_sysconfdir}/jira/entityengine.xml $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/entityengine.xml
ln -s %{_sysconfdir}/jira/osuser.xml $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/osuser.xml

# some additional libraries
install -d $RPM_BUILD_ROOT%{_datadir}/tomcat/lib
cp -a jira-jars-tomcat5/* $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/lib
ln -s %{_datadir}/jira/WEB-INF/lib/hsqldb-*.jar $RPM_BUILD_ROOT%{_datadir}/tomcat/lib/hsqldb.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
# do not make this file writeable by tomcat. We do not want to allow user to
# undeploy this app via tomcat manager.
%{_datadir}/jira
%dir %{_sysconfdir}/jira
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jira/jira-application.properties
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jira/log4j.properties
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jira/entityengine.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jira/osuser.xml
%{_sysconfdir}/jira/tomcat-context.xml
%config(noreplace) %verify(not md5 mtime size) %attr(2775,root,tomcat) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/jira.xml
%{_datadir}/tomcat/lib/*jar
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira/jiradb
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira/index
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira/attachments
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira/backups
%attr(2775,root,servlet) %dir /var/log/jira
%doc licenses/csv.license README.PLD
