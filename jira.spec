# TODO:
# - convert to "-installer" type package?

# NOTE:
# Do not remove NoSource tags. Make sure DistFiles won't fetch JIRA sources.
#
# Todd Revolt from Atlassian told that:
#   * We are free to integrate Atlassian products into PLD. So we can write
#     installer scripts, create nosrc packages etc.
#   * We are not permitted to redistribute their products. That mean during
#     installation each user has to download JIRA from atlassian web page.
#
# See Atlassian_EULA_3.0.pdf for more details.

# RELEASE INFO:
# This version was released 06 Oct 2009

%if 0
# Download sources manually:
wget -c http://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-enterprise-4.0.tar.gz
wget -c http://www.atlassian.com/about/licensing/Atlassian_EULA_3.0.pdf
wget -c http://www.atlassian.com/software/jira/docs/servers/jars/v1/jira-jars-tomcat5.zip
%endif

%include	/usr/lib/rpm/macros.java

Summary:	JIRA bug and issue tracker
Name:		jira
Version:	4.0
Release:	1.1
License:	Proprietary, not distributable
Group:		Networking/Daemons/Java/Servlets
Source0:	atlassian-%{name}-enterprise-%{version}.tar.gz
# NoSource0-md5:	d17425350cf1bbef6ca93c178f16a04f
NoSource:	0
Source1:	Atlassian_EULA_3.0.pdf
# NoSource1-md5:	9e87088024e3c5ee2e63a72a3e99a6cb
NoSource:	1
Source2:	%{name}-jars-tomcat5.zip
# NoSource2-md5:	0c1184bc77a55cb09c3cd1a66ca06b4f
NoSource:	2
Source3:	context.xml
Source4:	entityengine.xml
Source5:	application.properties
Source6:	README.PLD
URL:		http://www.atlassian.com/software/jira/default.jsp
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	unzip
Requires:	jpackage-utils
Requires:	jre-X11
Requires:	tomcat >= 6.0.26-8
Obsoletes:	jira-enterprise
Conflicts:	confluence >= 3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		pluginsdir	%{_datadir}/jira/plugins
%description
JIRA lets you prioritise, assign, track, report and audit your
'issues,' whatever they may be - from software bugs and help-desk
tickets to project tasks and change requests.

More than just an issue tracker, JIRA is an extensible platform that
you can customise to match to your business processes.

%prep
%setup -q -n atlassian-%{name}-enterprise-%{version} -a2

cp %{SOURCE1} .

# http://confluence.atlassian.com/pages/viewpage.action?pageId=208962752
find -name 'org.apache.felix.main*.jar' | xargs rm
cp %{SOURCE7} webapp/WEB-INF/lib

# set paths for logs
sed -i 's,^\(log4j\.appender\.[a-z]*\.File\)=\(.*\)$,\1=/var/log/jira/\2,' webapp/WEB-INF/classes/log4j.properties

cp %{SOURCE4} edit-webapp/WEB-INF/classes/entityengine.xml
cp %{SOURCE5} edit-webapp/WEB-INF/classes/jira-application.properties
cp %{SOURCE6} README.PLD

%build
%ant compile

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{pluginsdir},/var/log/jira}
install -d $RPM_BUILD_ROOT%{_sharedstatedir}/jira/{jiradb,index,attachments,backups}
cp -a tmp/build/war/* $RPM_BUILD_ROOT%{_datadir}/jira

# configuration
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jira,%{_sharedstatedir}/tomcat/conf/Catalina/localhost}
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/jira/tomcat-context.xml
ln -s %{_sysconfdir}/jira/tomcat-context.xml $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/jira.xml
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/jira-application.properties $RPM_BUILD_ROOT%{_sysconfdir}/jira/jira-application.properties
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/log4j.properties $RPM_BUILD_ROOT%{_sysconfdir}/jira/log4j.properties
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/entityengine.xml $RPM_BUILD_ROOT%{_sysconfdir}/jira/entityengine.xml
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/osuser.xml $RPM_BUILD_ROOT%{_sysconfdir}/jira/osuser.xml
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/seraph-config.xml $RPM_BUILD_ROOT%{_sysconfdir}/jira/seraph-config.xml
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/actions.xml $RPM_BUILD_ROOT%{_sysconfdir}/jira/actions.xml
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/crowd-ehcache.xml $RPM_BUILD_ROOT%{_sysconfdir}/jira/crowd-ehcache.xml
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/crowd.properties $RPM_BUILD_ROOT%{_sysconfdir}/jira/crowd.properties
ln -s %{_sysconfdir}/jira/jira-application.properties $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/jira-application.properties
ln -s %{_sysconfdir}/jira/log4j.properties $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/log4j.properties
ln -s %{_sysconfdir}/jira/entityengine.xml $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/entityengine.xml
ln -s %{_sysconfdir}/jira/osuser.xml $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/osuser.xml
ln -s %{_sysconfdir}/jira/seraph-config.xml $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/seraph-config.xml
ln -s %{_sysconfdir}/jira/actions.xml $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/actions.xml
ln -s %{_sysconfdir}/jira/crowd-ehcache.xml $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/crowd-ehcache.xml
ln -s %{_sysconfdir}/jira/crowd.properties $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/crowd.properties

# some additional libraries
install -d $RPM_BUILD_ROOT%{_datadir}/tomcat/lib
cp -a jira-jars-tomcat5/* $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/lib
hsqldbfilename=$(basename $(ls $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/lib/hsql*jar))
ln -s %{_datadir}/jira/WEB-INF/lib/$hsqldbfilename $RPM_BUILD_ROOT%{_datadir}/tomcat/lib/hsqldb.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc licenses/csv.license README.PLD Atlassian_EULA_3.0.pdf
%{_datadir}/jira
%dir %attr(750,root,tomcat) %{_sysconfdir}/jira
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,tomcat) %{_sysconfdir}/jira/*
%{_sharedstatedir}/tomcat/conf/Catalina/localhost/jira.xml
%{_datadir}/tomcat/lib/*jar
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira/jiradb
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira/index
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira/attachments
%attr(2775,root,servlet) %dir %{_sharedstatedir}/jira/backups
%attr(2775,root,servlet) %dir /var/log/jira
