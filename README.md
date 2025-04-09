Template repository for Python projects
===



# Versioning Recommendations


Think of a software as a series of increments called features. Feature should ideally be a small portion of the code that can be tested and merged independently. Merging of feature is done through pull request which code is reviewed by someone else. After successful review, the code is merged to the `main` branch and the feature branch is deleted. The git allows for multiple branches to be opened at the same time so once the code is submitted for code review, another feature can be worked on in a different branch - even if it's dependent on the previous feature. This way, the `main` branch of the code is stable and reviewed so it's clear which piece of code works and which doesn't.

Keep track of significant changes in the code by tagging the commits with short description  

**Key-takeaways:**

- Use branches while implementing new features `git checkout -b feature/feature_name`
- Commit small portions of the code and add messages `git commit -m "short description of the change"`- Keep the feature size manageable (two weeks of work can be reviewed/merged in a reasonable time while two months worth work is not)
- Request pull/merge with `main` via [pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) and assign your supervisor as a reviewer
- Use tags for major updates `git tag -a "works end2end" -m "This version can run the whole pipeline"`
- Format your code before committing to avoid marking whitespace changes in GH code review. Use either `ruff check --fix .` or a combination of `black` and `isort`.
- Don't put .ipynb to the repository as the code is not versioned properly (it's been ignored - see `.gignore` file).
- Use `.gitignore` for your data and outputs. 
- Should you need to version your data, consider using HuggingFace instead of github.


# Code

- Use english in code as well as in docstring, comments and readme
- Add support for CLI with proper `--help` when appropriate (see `app.py`)
- Don't use print for debugging, use logging instead
- Consider using type hints and docstrings at least for high level code
- The code should be installable library (see `pyproject.toml`)
- Make sure that `README.md` is up-to-date with your code (installation instruction)
- Always log exceptions with stacktrace `logger.exception(e)` where `e` is the exception caught


# Utility

- Use `jupyter lab` instead of jupyter notebook
  - Make the virtual environment available in jupyter lab by activating the virtual environment and running `python -m ipykernel install --user --name=myenv` (see [ipykernel docs](https://ipython.readthedocs.io/en/stable/install/kernel_install.html))
