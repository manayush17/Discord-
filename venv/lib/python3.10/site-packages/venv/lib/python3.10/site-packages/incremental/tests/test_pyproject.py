# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""Test handling of ``pyproject.toml`` configuration"""

import os
from typing import cast, Optional, Union
from pathlib import Path
from twisted.trial.unittest import TestCase

from incremental import _load_pyproject_toml, _IncrementalConfig


class VerifyPyprojectDotTomlTests(TestCase):
    """Test the `_load_pyproject_toml` helper function"""

    def _loadToml(
        self, toml: str, *, path: Union[Path, str, None] = None
    ) -> Optional[_IncrementalConfig]:
        """
        Read a TOML snipped from a temporary file with `_load_pyproject_toml`

        @param toml: TOML content of the temporary file

        @param path: Path to which the TOML is written
        """
        path_: str
        if path is None:
            path_ = self.mktemp()  # type: ignore
        else:
            path_ = str(path)

        with open(path_, "w") as f:
            f.write(toml)

        try:
            return _load_pyproject_toml(path_)
        except Exception as e:
            if hasattr(e, "add_note"):
                e.add_note(  # type: ignore[attr-defined]
                    f"While loading:\n\n{toml}"
                )  # pragma: no coverage
            raise

    def test_fileNotFound(self):
        """
        An absent ``pyproject.toml`` file produces no result
        """
        path = os.path.join(cast(str, self.mktemp()), "pyproject.toml")
        self.assertIsNone(_load_pyproject_toml(path))

    def test_configMissing(self):
        """
        A ``pyproject.toml`` that exists but provides no relevant configuration
        is ignored.
        """
        for toml in [
            "\n",
            "[tool.notincremental]\n",
            "[project]\n",
        ]:
            self.assertIsNone(self._loadToml(toml))

    def test_nameMissing(self):
        """
        `ValueError` is raised when ``[tool.incremental]`` is present but
        the project name isn't available.
        """
        for toml in [
            "[tool.incremental]\n",
            "[project]\n[tool.incremental]\n",
        ]:
            self.assertRaises(ValueError, self._loadToml, toml)

    def test_nameInvalid(self):
        """
        `TypeError` is raised when the project name isn't a string.
        """
        for toml in [
            "[tool.incremental]\nname = -1\n",
            "[tool.incremental]\n[project]\nname = 1.0\n",
        ]:
            self.assertRaises(TypeError, self._loadToml, toml)

    def test_toolIncrementalInvalid(self):
        """
        `ValueError` is raised when the ``[tool]`` or ``[tool.incremental]``
        isn't a table.
        """
        for toml in [
            "tool = false\n",
            "[tool]\nincremental = false\n",
            "[tool]\nincremental = 123\n",
            "[tool]\nincremental = null\n",
        ]:
            self.assertRaises(ValueError, self._loadToml, toml)

    def test_toolIncrementalUnexpecteKeys(self):
        """
        Raise `ValueError` when the ``[tool.incremental]`` section contains
        keys other than ``"name"``
        """
        for toml in [
            "[tool.incremental]\nfoo = false\n",
            '[tool.incremental]\nname = "OK"\nother = false\n',
        ]:
            self.assertRaises(ValueError, self._loadToml, toml)

    def test_setuptoolsOptIn(self):
        """
        The package has opted-in to Incremental version management when
        the ``[tool.incremental]`` section is a dict. The project name
        is taken from ``[tool.incremental] name`` or ``[project] name``.
        """
        root = Path(self.mktemp())
        pkg = root / "src" / "foo"
        pkg.mkdir(parents=True)

        for toml in [
            '[project]\nname = "Foo"\n[tool.incremental]\n',
            '[tool.incremental]\nname = "Foo"\n',
        ]:
            config = self._loadToml(toml, path=root / "pyproject.toml")

            self.assertEqual(
                config,
                _IncrementalConfig(
                    has_tool_incremental=True,
                    package="Foo",
                    path=str(pkg),
                ),
            )

    def test_noToolIncrementalSection(self):
        """
        The ``has_tool_incremental`` flag is false when there
        isn't a ``[tool.incremental]`` section.
        """
        root = Path(self.mktemp())
        pkg = root / "foo"
        pkg.mkdir(parents=True)

        config = self._loadToml(
            '[project]\nname = "foo"\n',
            path=root / "pyproject.toml",
        )

        self.assertEqual(
            config,
            _IncrementalConfig(
                has_tool_incremental=False,
                package="foo",
                path=str(pkg),
            ),
        )
