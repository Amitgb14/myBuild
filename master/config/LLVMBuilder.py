
import buildbot
from buildbot.plugins import util, steps
from buildbot.steps.shell import Configure, ShellCommand
from buildbot.steps.shell import WarningCountingShellCommand
from buildbot.process.properties import WithProperties

def getLLVMCMakeBuildFactory(
    clean            = True,
    test             = True,
    install          = None,
    make             = 'make',
    jobs             = 2,
    defaultBranch    = 'trunk',     # Branch to build.
    config_name      = 'Release',
    env              = {},
    extra_cmake_args = []):

    llvm_srcdir = "llvm.src"
    llvm_objdir = "llvm.obj"

    f = util.BuildFactory()

    # Determine the build directory.
    f.addStep(
        buildbot.steps.shell.SetProperty(
            name        = "get_builddir",
            command     = ["pwd"],
            property    = "builddir",
            description = "set build dir",
            workdir     = ".",
            env = env))



    # Checkout sources.
    f.addStep(
        steps.SVN(
            name = 'svn-llvm',
            mode = 'incremental',
            repourl ='http://llvm.org/svn/llvm-project/llvm/trunk',
            workdir = llvm_srcdir))

    f.addStep(
        steps.SVN(
            name = 'svn-clang',
            mode = 'incremental',
            repourl = 'http://llvm.org/svn/llvm-project/cfe/trunk',
            workdir = '%s/tools/clang' % llvm_srcdir))

    f.addStep(
        steps.SVN(
            name = 'svn-clang-tools-extra',
            mode = 'incremental',
            repourl = 'http://llvm.org/svn/llvm-project/clang-tools-extra/trunk',
            workdir = '%s/tools/clang/tools/extra' % llvm_srcdir))

    f.addStep(
        steps.SVN(
            name = 'svn-compiler-rt',
            mode = 'incremental',
            repourl = 'http://llvm.org/svn/llvm-project/compiler-rt/trunk',
            workdir = '%s/projects/compiler-rt' % llvm_srcdir))

    f.addStep(
        steps.SVN(
            name = 'svn-lld',
            mode = 'incremental',
            repourl = 'http://llvm.org/svn/llvm-project/lld/trunk',
            workdir = '%s/tools/lld' % llvm_srcdir))

    f.addStep(
        steps.SVN(
            name = 'svn-polly',
            mode = 'incremental',
            repourl = 'http://llvm.org/svn/llvm-project/polly/trunk',
            workdir = '%s/tools/polly' % llvm_srcdir))

    f.addStep(
        steps.SVN(
            name = 'svn-libcxx',
            mode = 'incremental',
            repourl = 'http://llvm.org/svn/llvm-project/libcxx/trunk',
            workdir = '%s/projects/libcxx' % llvm_srcdir))

    f.addStep(
        steps.SVN(
            name = 'svn-libcxxabi',
            mode = 'incremental',
            repourl = 'http://llvm.org/svn/llvm-project/libcxxabi/trunk',
            workdir = '%s/projects/libcxxabi' % llvm_srcdir))

    f.addStep(
        steps.SVN(
            name = 'svn-test-suite',
            mode = 'incremental',
            repourl = 'http://llvm.org/svn/llvm-project/test-suite/trunk',
            workdir = '%s/projects/test-suite' % llvm_srcdir))


    cmake_args = {}
    if install:
        cmake_args["CMAKE_INSTALL_PREFIX"] = install
    cmake_args["CMAKE_BUILD_TYPE"] = config_name
    for args in extra_cmake_args:
        if "-D" in args:
            args = args.replace("-D", "")
        key, value = args.split("=")
        cmake_args[key] = value

    f.addStep(
        steps.CMake(
            generator       = 'Ninja',
            definitions     = cmake_args,
            options         = ["../" + llvm_srcdir],
            description     = ['configuring', config_name],
            descriptionDone = ['configure',   config_name],
            workdir         = llvm_objdir,
            env             = env))
    if clean:
        f.addStep(
            WarningCountingShellCommand(
                name            = "clean-llvm",
                command         = [make, 'clean'],
                haltOnFailure   = True,
                description     = "cleaning llvm",
                descriptionDone = "clean llvm",
                workdir         = llvm_objdir,
                env             = env))

    f.addStep(
        WarningCountingShellCommand(
            name            = "compile",
            command         = ['ninja-build', WithProperties("-j %s" % jobs)],
            haltOnFailure   = True,
            description     = "compiling llvm",
            descriptionDone = "compile llvm",
            workdir         = llvm_objdir,
            env             = env))

    if install:
        f.addStep(
            WarningCountingShellCommand(
                name            = "install",
                command         = ['ninja-build', 'install'],
                haltOnFailure   = True,
                description     = "installing llvm",
                descriptionDone = "install llvm",
                workdir         = llvm_objdir))
    if test:
        f.addStep(
            ShellCommand(
                name            = "test-llvm",
                command         = ["ninja-build", "check-all"],
                description     = "testing llvm",
                descriptionDone = "test llvm",
                workdir         = llvm_objdir))
    return f

