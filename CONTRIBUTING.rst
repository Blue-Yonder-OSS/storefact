============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Bug reports
===========

When reporting a bug please include:

    * Your operating system name and version.
    * Any details about your local setup that might be helpful in troubleshooting.
    * Detailed steps to reproduce the bug.

Documentation improvements
==========================

Store factory for simplekv could always use more documentation, whether as part of the
official Store factory for simplekv docs, in docstrings, or even on the web in blog posts,
articles, and such.

Feature requests and feedback
=============================

If you are proposing a feature:

    * Explain in detail how it would work.
    * Keep the scope as narrow as possible, to make it easier to implement.
    * Remember that this is a volunteer-driven project, and that contributions are welcome :)

Development
===========

Pull Request Guidelines
-----------------------

If you need some code review or feedback while you're developing the code just make the pull request.

For merging, you should:

1. Include passing tests (run ``tox``).
2. Update documentation when there's new API, functionality etc. 
3. Add a note to ``CHANGELOG.rst`` about the changes.
4. Add yourself to ``AUTHORS.rst``.

Tips
----

To run a subset of tests::

    tox -e envname -- py.test -k test_myfeature

To run all the test environments in *parallel* (you need to ``pip install detox``)::

    detox