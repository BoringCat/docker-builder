
%global commit_sha a07fcc03264915c624f0e4818993c5b4df3fa703

Name:    unixbench
Version: 5.1.3
Release: 1%{?dist}
Summary: The original BYTE UNIX benchmark suite
License: GNU,GPLv2
URL:     https://github.com/kdlucas/byte-unixbench
Source0: https://github.com/kdlucas/byte-unixbench/archive/%{commit_sha}.tar.gz
Source1: ubench
Patch00: no-make.patch

BuildRequires: /usr/bin/gcc
Requires:      /usr/bin/perl
Requires:      /usr/bin/grep
Requires:      /bin/sh

%description
UnixBench is the original BYTE UNIX benchmark suite, updated and revised by many people over the years.

The purpose of UnixBench is to provide a basic indicator of the performance of a Unix-like system; hence, multiple 
tests are used to test various aspects of the system's performance. These test results are then compared to the 
scores from a baseline system to produce an index value, which is generally easier to handle than the raw scores. 
The entire set of index values is then combined to make an overall index for the system.

Some very simple graphics tests are included to measure the 2D and 3D graphics performance of the system.

Multi-CPU systems are handled. If your system has multiple CPUs, the default behaviour is to run the selected tests 
twice -- once with one copy of each test program running at a time, and once with N copies, where N is the number of 
CPUs. This is designed to allow you to assess:

the performance of your system when running a single task
the performance of your system when running multiple tasks
the gain from your system's implementation of parallel processing

Do be aware that this is a system benchmark, not a CPU, RAM or disk benchmark. The results will depend not only on 
your hardware, but on your operating system, libraries, and even compiler.

%prep
%setup -q -n byte-%{name}-%{commit_sha}
cd UnixBench/
%patch00 -p1

%build
cd UnixBench/
make %{?_smp_mflags} all

%install
cd UnixBench/
install -d %{buildroot}/opt/%{name}
install -d %{buildroot}/usr/bin
cp -rv pgms results testdir tmp Run %{buildroot}/opt/%{name}/
cp %{_sourcedir}/ubench %{buildroot}/usr/bin/ubench
chmod 755 %{buildroot}/usr/bin/ubench
chmod 755 %{buildroot}/opt/%{name}/Run
chmod ugoa+w %{buildroot}/opt/%{name}/{results,testdir,tmp}

%files
%defattr (-,root,root,0755)
%dir /opt/%{name}
%dir /opt/%{name}/pgms
%attr(0755, root, root) /opt/%{name}/pgms/arithoh*
%attr(0755, root, root) /opt/%{name}/pgms/context1*
%attr(0755, root, root) /opt/%{name}/pgms/dhry2*
%attr(0755, root, root) /opt/%{name}/pgms/dhry2reg*
%attr(0755, root, root) /opt/%{name}/pgms/double*
%attr(0755, root, root) /opt/%{name}/pgms/execl*
%attr(0755, root, root) /opt/%{name}/pgms/float*
%attr(0755, root, root) /opt/%{name}/pgms/fstime*
%attr(0755, root, root) /opt/%{name}/pgms/gfx-x11*
%attr(0755, root, root) /opt/%{name}/pgms/hanoi*
%attr(0644, root, root) /opt/%{name}/pgms/index.base
%attr(0755, root, root) /opt/%{name}/pgms/int*
%attr(0755, root, root) /opt/%{name}/pgms/long*
%attr(0755, root, root) /opt/%{name}/pgms/looper*
%attr(0755, root, root) /opt/%{name}/pgms/multi.sh*
%attr(0755, root, root) /opt/%{name}/pgms/pipe*
%attr(0755, root, root) /opt/%{name}/pgms/register*
%attr(0755, root, root) /opt/%{name}/pgms/short*
%attr(0755, root, root) /opt/%{name}/pgms/spawn*
%attr(0755, root, root) /opt/%{name}/pgms/syscall*
%attr(0755, root, root) /opt/%{name}/pgms/tst.sh*
%attr(0644, root, root) /opt/%{name}/pgms/unixbench.logo
%attr(0755, root, root) /opt/%{name}/pgms/whetstone-double
%attr(0644, root, root) /opt/%{name}/testdir/cctest.c
%attr(0644, root, root) /opt/%{name}/testdir/dc.dat
%attr(0644, root, root) /opt/%{name}/testdir/large.txt
%attr(0644, root, root) /opt/%{name}/testdir/sort.src

%dir %attr(0777, root, root) /opt/%{name}/results
%dir %attr(0777, root, root) /opt/%{name}/testdir
%dir %attr(0777, root, root) /opt/%{name}/tmp
%attr(0755, root, root) /usr/bin/ubench
%attr(0755, root, root) /opt/%{name}/Run

