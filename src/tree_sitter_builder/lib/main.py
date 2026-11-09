import logging
import pathlib
import platform
import tempfile

from setuptools._distutils.ccompiler import new_compiler
from setuptools._distutils.unixccompiler import UnixCCompiler

from .. import subr

logger = logging.getLogger(__name__)


def build_library(output_path: pathlib.Path, repo_path: pathlib.Path):
    src_path = repo_path / "src"
    source_paths = [src_path / "parser.c"]
    cpp = False
    if (src_path / "scanner.cc").exists():
        cpp = True
        source_paths.append(src_path / "scanner.cc")
    elif (src_path / "scanner.c").exists():
        source_paths.append(src_path / "scanner.c")

    compiler = new_compiler()
    if isinstance(compiler, UnixCCompiler):
        compiler.set_executables(compiler_cxx="c++")

    with tempfile.TemporaryDirectory(suffix="tree_sitter_language") as out_dir:
        object_paths = []
        for source_path in source_paths:
            flags = None
            if platform.system() != "Windows":
                flags = ["-fPIC"]
                if source_path.suffix == ".c":
                    flags.append("-std=c11")
            object_paths.append(
                compiler.compile(
                    [str(source_path)],
                    output_dir=out_dir,
                    include_dirs=[str(src_path)],
                    extra_preargs=flags,
                )[0]
            )
        compiler.link_shared_object(
            object_paths,
            str(output_path),
            target_lang="c++" if cpp else "c",
        )


def build(repository: str, repo_dir: pathlib.Path, build_dir: pathlib.Path):
    clone_dir_name = subr.git.get_repo_name(repository)
    target_file = build_dir / (clone_dir_name + ".so")

    logger.info(f'Build tree-sitter module: {str(target_file)}')
    target_file.unlink(missing_ok=True)
    build_library(target_file, repo_dir / clone_dir_name)
