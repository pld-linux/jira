# TODO:
# - ask atlassian for permission to redistribute it.
# - package plugin-timesheet as separate spec?
# - apply security patches:
#   http://jira.atlassian.com/browse/JRA-20995
#   http://jira.atlassian.com/browse/JRA-20994

%include	/usr/lib/rpm/macros.java

%define		plugintimesheetver	1.9
%define		pluginsubversionver	0.10.5.2
%define		pluginjetiver		1.8

Summary:	JIRA bug and issue tracker
Name:		jira-enterprise
Version:	4.1.1
Release:	1
License:	Proprietary, not distributable
Group:		Networking/Daemons/Java/Servlets
# Sources:
# wget -c http://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-enterprise-4.1.1.tar.gz
# wget -c http://www.atlassian.com/software/jira/docs/servers/jars/v1/jira-jars-tomcat5.zip
# wget -c https://studio.plugins.atlassian.com/svn/TIME/jars/atlassian-jira-plugin-timesheet-1.9.jar
# wget -c http://maven.atlassian.com/contrib/com/atlassian/jira/plugin/ext/subversion/atlassian-jira-subversion-plugin/0.10.5.2/atlassian-jira-subversion-plugin-0.10.5.2-distribution.zip
# wget -c https://studio.plugins.atlassian.com/wiki/download/attachments/2261441/email-this-issue-plugin-1.8.jar
Source0:	atlassian-%{name}-%{version}.tar.gz
# NoSource0-md5:	b23e25ec407f657cbff786b98973605a
NoSource:	0
Source1:	jira-jars-tomcat5.zip
# NoSource1-md5:	0c1184bc77a55cb09c3cd1a66ca06b4f
NoSource:	1
Source2:	%{name}-context.xml
Source3:	%{name}-entityengine.xml
Source4:	%{name}-application.properties
Source5:	%{name}-README.PLD
# Most of jira plugins are distributable (or even BSD licensed), but it make
# no sense to store them in DF unles Source0 and Source1 are distributable.
Source10:	atlassian-jira-plugin-timesheet-%{plugintimesheetver}.jar
# NoSource10-md5:	38d2c943b72c4d7bb3d2eba514d1df39
NoSource:	10
Source11:	atlassian-jira-subversion-plugin-%{pluginsubversionver}-distribution.zip
# NoSource11-md5:	5e220049093be0f732a174e7955aa13d
NoSource:	11
Source12:	email-this-issue-plugin-%{pluginjetiver}.jar
# NoSource12-md5:	9290b62d79d257c58b5661b74dbbc4b0
NoSource:	12
URL:		http://www.atlassian.com/software/jira/default.jsp
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
Requires:	jre-X11
Requires:	tomcat >= 0:6.0.20-4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JIRA lets you prioritise, assign, track, report and audit your
'issues,' whatever they may be - from software bugs and help-desk
tickets to project tasks and change requests.

More than just an issue tracker, JIRA is an extensible platform that
you can customise to match to your business processes.

%package plugin-timesheet
Summary:	JIRA Timesheet report and portlet
License:	BSD
Group:		Libraries/Java
URL:		http://confluence.atlassian.com/display/JIRAEXT/Timesheet+report+and+portlet
Requires:	%{name} = %{version}-%{release}

%description plugin-timesheet
JIRA Timesheet report and portlet.

%package plugin-subversion
Summary:	JIRA Subversion Plugin
License:	BSD
Group:		Libraries/Java
URL:		http://confluence.atlassian.com/display/JIRAEXT/JIRA+Subversion+plugin
Requires:	%{name} = %{version}-%{release}

%description plugin-subversion
A plugin to integrate JIRA with Subversion.This plugin displays
Subversion commit info in a tab on the associated JIRA issue. To link
a commit to a JIRA issue, the commit's text must contain the issue key
(eg. "This commit fixes TST-123").

%package plugin-email-this-issue
Summary:	JIRA "Email this issue" plugin
License:	BSD
Group:		Libraries/Java
URL:		https://plugins.atlassian.com/plugin/details/4977
Requires:	%{name} = %{version}-%{release}

%description plugin-email-this-issue
This plugin contains an issue operation component that allows users to
compose an email and send the issue to arbitrary recipients.

Most important features are:

- send email with issue details to email addresses outside JIRA,
  assignee, reporter and watchers.
- attach issue attachments to email
- control who can invoke the operation through a project role
- text and html email format are supported, email body understands
  Confluence wiki markup
- email template can be customized per project and issue type
- a comment is created reflecting the event of sending an email (body,
  recipients, etc) - see below
- i18n-enabled, the plugin can be translated, it is currently
  available in English, German, French, Polish and Hungarian.
- you have options like "CC to me" and "Reply to me" to receive a copy
  of the email or to receive replies to the email.
- email recipients are added to watchers on demand
- recipients from custom fields and groups/project roles can be added
- email options may be reused, i.e. there is no need to check all your
  options every time you send an email

%prep
%setup -q -n atlassian-%{name}-%{version} -a1 -a11

mv atlassian-jira-subversion-plugin-*/README.txt README-plugin-subversion.txt

# set paths for logs
sed -i 's,^\(log4j\.appender\.[a-z]*\.File\)=\(.*\)$,\1=/var/log/jira/\2,' webapp/WEB-INF/classes/log4j.properties

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
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/jira/tomcat-context.xml
ln -s %{_sysconfdir}/jira/tomcat-context.xml $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/jira.xml
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/jira-application.properties $RPM_BUILD_ROOT%{_sysconfdir}/jira/jira-application.properties
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/log4j.properties $RPM_BUILD_ROOT%{_sysconfdir}/jira/log4j.properties
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/entityengine.xml $RPM_BUILD_ROOT%{_sysconfdir}/jira/entityengine.xml
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/osuser.xml $RPM_BUILD_ROOT%{_sysconfdir}/jira/osuser.xml
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/seraph-config.xml $RPM_BUILD_ROOT%{_sysconfdir}/jira/seraph-config.xml
mv $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/actions.xml $RPM_BUILD_ROOT%{_sysconfdir}/jira/actions.xml
ln -s %{_sysconfdir}/jira/jira-application.properties $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/jira-application.properties
ln -s %{_sysconfdir}/jira/log4j.properties $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/log4j.properties
ln -s %{_sysconfdir}/jira/entityengine.xml $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/entityengine.xml
ln -s %{_sysconfdir}/jira/osuser.xml $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/osuser.xml
ln -s %{_sysconfdir}/jira/seraph-config.xml $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/seraph-config.xml
ln -s %{_sysconfdir}/jira/actions.xml $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/actions.xml

# some additional libraries
install -d $RPM_BUILD_ROOT%{_datadir}/tomcat/lib
cp -a jira-jars-tomcat5/* $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/lib
hsqldbfilename=$(basename $(ls $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/lib/hsql*jar))
ln -s %{_datadir}/jira/WEB-INF/lib/$hsqldbfilename $RPM_BUILD_ROOT%{_datadir}/tomcat/lib/hsqldb.jar

# plugins
cp %{SOURCE10} $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/lib/atlassian-jira-plugin-timesheet-%{plugintimesheetver}.jar

cp atlassian-jira-subversion-plugin-*/subversion-jira-plugin.properties $RPM_BUILD_ROOT%{_sysconfdir}/jira/subversion-jira-plugin.properties
cp atlassian-jira-subversion-plugin-*/lib/* $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/lib
ln -s %{_sysconfdir}/jira/subversion-jira-plugin.properties $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/classes/subversion-jira-plugin.properties
cp %{SOURCE12} $RPM_BUILD_ROOT%{_datadir}/jira/WEB-INF/lib/email-this-issue-plugin-%{pluginjetiver}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc licenses/csv.license README.PLD
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

#plugins
%exclude %{_datadir}/jira/WEB-INF/lib/atlassian-jira-plugin-timesheet-%{plugintimesheetver}.jar
%exclude %{_datadir}/jira/WEB-INF/lib/atlassian-jira-subversion-plugin-%{pluginsubversionver}.jar
%exclude %{_datadir}/jira/WEB-INF/lib/svnkit-1.2.1.5297.jar
%exclude %{_datadir}/jira/WEB-INF/lib/trilead-ssh2-build213-svnkit-1.2-patch.jar
%exclude %{_datadir}/jira/WEB-INF/lib/email-this-issue-plugin-%{pluginjetiver}.jar
%exclude %{_datadir}/jira/WEB-INF/classes/subversion-jira-plugin.properties
%exclude %{_sysconfdir}/jira/subversion-jira-plugin.properties

%files plugin-timesheet
%defattr(644,root,root,755)
%{_datadir}/jira/WEB-INF/lib/atlassian-jira-plugin-timesheet-%{plugintimesheetver}.jar

%files plugin-subversion
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,tomcat) %{_sysconfdir}/jira/subversion-jira-plugin.properties
%{_datadir}/jira/WEB-INF/classes/subversion-jira-plugin.properties
%{_datadir}/jira/WEB-INF/lib/atlassian-jira-subversion-plugin-%{pluginsubversionver}.jar
%{_datadir}/jira/WEB-INF/lib/svnkit-1.2.1.5297.jar
%{_datadir}/jira/WEB-INF/lib/trilead-ssh2-build213-svnkit-1.2-patch.jar

%files plugin-email-this-issue
%defattr(644,root,root,755)
%{_datadir}/jira/WEB-INF/lib/email-this-issue-plugin-%{pluginjetiver}.jar
