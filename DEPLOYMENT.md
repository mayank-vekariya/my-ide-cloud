# Deployment

## Public showcase: GitHub Pages

This repository's `docs/` directory is a static HTML/CSS/JavaScript site. It has no build dependencies and does not run the application.

1. Run `python scripts/check_showcase.py` from the repository root.
2. In GitHub **Settings → Pages**, choose **Deploy from a branch**, branch **main**, folder **/docs**.
3. The public URL is [Code Server](https://mayank-vekariya.github.io/my-ide-cloud/).
4. Push subsequent showcase changes to `main`; check the Pages deployment status before sharing the URL.

The `showcase-check.yml` workflow validates the static page and tests the local liveness endpoint. It does not deploy cloud resources or claim end-to-end application coverage. A Pages deployment may require repository-admin setup; workflow success alone does not prove publishing is enabled.

## Local preview

```sh
python -m http.server 4173 --bind 127.0.0.1 --directory docs
```

## Application hosting

Only the static showcase is ready for public GitHub Pages hosting. Do not deploy the Flask control plane or unauthenticated code-server container publicly as-is. First resolve authentication/authorization, shell input handling, CSRF and persistent workspace storage. Configure project, region and image through a reviewed configuration layer; use least-privilege credentials and private Cloud Run access. Cloud deployment can incur charges and is not performed by these instructions.

## Publishing checklist

- [ ] HTML/CSS/JavaScript and image references pass the local check.
- [ ] The public page clearly distinguishes illustrations from application output.
- [ ] Project and documentation links resolve.
- [ ] No credentials, private uploads, database files or model weights are included in `docs/`.
- [ ] The Pages deployment finishes successfully.

## Updating and rollback

Keep changes in normal Git commits. To roll back a published showcase, revert only the relevant showcase commit and push the reviewed revert; do not reset unrelated project history. Preserve the résumé's GitHub repository link so visitors can reach both source and showcase.
