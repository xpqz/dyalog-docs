# Dyalog APL documentation

> **Note** This is the source repository for the documentation for Dyalog APL. If you are looking for the actual published documentation, visit the [help section](https://help.dyalog.com/) on Dyalog's website instead. This repository is intended for documentation authors, not users.

If you want to contribute content to Dyalog's documentation, see the file [CONTRIBUTE.md](CONTRIBUTE.md) for an outline of the process we use.

## Organisation

This is a mkdocs monorepo, using the Spotify [monorepo](https://github.com/backstage/mkdocs-monorepo-plugin) plugin. The top-level site is defined by the file `mkdocs.yml` in the root, and the `docs/` directory. The other directories are the respective sub-sites included in the `nav` section in `mkdocs.yml`.

## Tools

The `tools/` directory contains a `docker compose` configuration that can be used to preview our documentation documents in their rendered form. See its [README](tools/README.md) file for instructions on how to use the tooling.
   
## Publish

[For the person responsible for publishing]

```
mike set-default --push [--remote github] 20.0  # only needed once
mike deploy --push [--remote github] 20.0
```
