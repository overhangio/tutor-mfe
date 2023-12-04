- [Bugfix] Support MFE remotes that are not on GitHub. (by @gabor-boros and @regisb)
- 💥[Bugfix] Bypass rate-limiting when checking for upstream git changes. To achieve that, we use the `ADD --keep-git-dir` option, which is only compatible with BuildKit 0.11, from January 2023. Also, we get rid of the `get_github_refs_path` function. (by @gabor-boros and @regisb)

