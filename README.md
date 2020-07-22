# Interface GitHub Actions and ReadTheDocs

I like to use [ReadTheDocs](https://readthedocs.org/) to build (and version!) my
docs, but I _also_ like to use [Jupyter notebooks](https://jupyter.org/) to
write tutorials. Unfortunately, this has always meant that I needed to check
executed notebooks (often with large images) into my git repository, causing
huge amounts of bloat. Futhermore, the executed notebooks would often get out of
sync with the development of the code. **No more!!**

_This library avoids these issues by executing code on [GitHub
Actions](https://github.com/features/actions), uploading build artifacts (in
this case, executed Jupter notebooks), and then (only then!) triggering a
ReadTheDocs build that can download the executed notebooks._
