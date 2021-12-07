# Interface Read the Docs and GitHub Actions

[![Docs](https://github.com/dfm/rtds-action/workflows/Docs/badge.svg)](https://github.com/dfm/rtds-action/actions?query=workflow%3ADocs)
[![Documentation Status](https://readthedocs.org/projects/rtds-action/badge/?version=latest)](https://rtds-action.readthedocs.io/en/latest/?badge=latest)

I like to use [Read the Docs](https://readthedocs.org/) to build (and version!) my
docs, but I _also_ like to use [Jupyter notebooks](https://jupyter.org/) to
write tutorials. Unfortunately, even though
[notebooks can be executed on Read the Docs](https://docs.readthedocs.io/en/stable/guides/jupyter.html),
some of them take a very long time to run or
need special Docker environments to execute,
which goes beyond what the platform supports. In these cases I needed to check
executed notebooks (often with large images) into my git repository, causing
huge amounts of bloat. Futhermore, the executed notebooks would often get out of
sync with the development of the code. **No more!!**

_This library avoids these issues by executing code on [GitHub
Actions](https://github.com/features/actions), uploading build artifacts (in
this case, executed Jupter notebooks), and then (only then!) triggering a
Read the Docs build that can download the executed notebooks._

There is still some work required to set up this workflow, but this library has
three pieces that make it a bit easier:

1. A GitHub action that can be used to trigger a build for the current branch on
   Read the Docs.
2. A Sphinx extension that interfaces with the GitHub API to download the
   artifact produced for the target commit hash.
3. Some documentation that shows you how to set all this up!

## Usage

The following gives the detailed steps of the process of setting up a project
using this workflow. But you can also see a fully functional example in this
repository. The documentation source is the `docs` directory and the
`.github/workflows` directory includes a workflow that is executed to build the
docs using this package. The rendered page is available at
[rtds-action.readthedocs.io](https://rtds-action.readthedocs.io).

### 1. Set up Read the Docs

1. First, you'll need to import your project as usual. If you've already done
   that, don't worry: this will also work with existing Read the Docs projects.
2. Next, go to the admin page for your project on Read the Docs, click on
   `Integrations` (the URL is something like
   `https://readthedocs.org/dashboard/YOUR_PROJECT_NAME/integrations/`).
3. Click `Add integration` and select `Generic API incoming webhook`.
4. Take note of the webhook `URL` and `token` on this page for use later.

You should also edit your webhook settings on GitHub by going to
`https://github.com/USERNAME/REPONAME/settings/hooks` and clicking "Edit"
next to the Read the Docs hook. On that page, you should un-check the `Pushes`
option.

### 2. Set up GitHub Actions workflow

In this example, we'll assume that we have tutorials written as Jupyter
notebooks, saved as Python scripts using
[Jupytext](https://jupytext.readthedocs.io/en/latest/introduction.html) (because
that's probably what you should be doing anyways!) in a directory called
`docs/tutorials`.

First, you'll need to add the Read the Docs webhook URL and token that you
recorded above as "secrets" for your GitHub project by going to the URL
`https://github.com/USERNAME/REPONAME/settings/secrets`. I'll call them
`RTDS_WEBHOOK_URL` (include the `https`!) and `RTDS_WEBHOOK_TOKEN` respectively.

For this use case, we can create the workflow `.github/workflows/docs.yml` as
follows:

```yaml
name: Docs
on: [push, release]

jobs:
  notebooks:
    name: "Build the notebooks for the docs"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Install dependencies
        run: |
          python -m pip install -U pip
          python -m pip install -r .github/workflows/requirements.txt

      - name: Execute the notebooks
        run: |
          jupytext --to ipynb --execute docs/tutorials/*.py

      - uses: actions/upload-artifact@v2
        with:
          name: notebooks-for-${{ github.sha }}
          path: docs/tutorials

      - name: Trigger RTDs build
        uses: dfm/rtds-action@v1
        with:
          webhook_url: ${{ secrets.RTDS_WEBHOOK_URL }}
          webhook_token: ${{ secrets.RTDS_WEBHOOK_TOKEN }}
          commit_ref: ${{ github.ref }}
```

Here, we're also assuming that we've added a `pip` requirements file at
`.github/workflows/requirements.txt` with the dependencies required to execute
the notebooks. Also note that in the `upload-artifact` step we give our artifact
that depends on the hash of the current commit. This is crucial! We also need to
take note of the `notebooks-for-` prefix because we'll use that later.

It's worth emphasizing here that the only "special" steps in this workflow are
the last two. You can do whatever you want to generate your artifact in the
previous steps (for example, you could use `conda` instead of `pip`) because
this workflow is not picky about how you get there!

### 3. Set up Sphinx

Finally, you can edit the `conf.py` for your Sphinx documentation to add support
for fetching the artifact produced by your action. Here is a minimal example:

```python
import os

extensions = [... "rtds_action"]

# The name of your GitHub repository
rtds_action_github_repo = "USERNAME/REPONAME"

# The path where the artifact should be extracted
# Note: this is relative to the conf.py file!
rtds_action_path = "tutorials"

# The "prefix" used in the `upload-artifact` step of the action
rtds_action_artifact_prefix = "notebooks-for-"

# A GitHub personal access token is required, more info below
rtds_action_github_token = os.environ["GITHUB_TOKEN"]

# Whether or not to raise an error on Read the Docs if the
# artifact containing the notebooks can't be downloaded (optional)
rtds_action_error_if_missing = False
```

Where we have added the custom extension and set the required configuration
parameters.

You'll need to provide Read the Docs with a GitHub personal access token (it only
needs the `public_repo` scope if your repo is public). You can generate a new
token by going to [your GitHub settings
page](https://github.com/settings/tokens). Then, save it as an environment
variable (called `GITHUB_TOKEN` in this case) on Read the Docs.

## Development

For now, just a note: if you edit `src/js/index.js`, you _must_ run `npm run package` to generate the compiled action source.
