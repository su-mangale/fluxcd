# FluxCD GitOps Repository

This repository manages the production Kubernetes cluster with FluxCD.

```text
apps/
  base/                 # Shared application manifests, one directory per app
  production/           # Production application aggregation and patches
infrastructure/
  base/                 # Shared namespaces and Flux image automation
  production/           # Production infrastructure aggregation
clusters/
  production/           # Flux bootstrap and production reconciliation entrypoint
```

## Applications

- `ykp-dashboard`
- `ykp-auth`
- `ykp-catalog`
- `ykp-shell`
- `ykp-api`

Application manifests live in `apps/base/<application>/`. Add production-specific changes in `apps/production/`.

Infrastructure is shared from `infrastructure/base/` and enabled for production from `infrastructure/production/`.

Flux syncs the `ykp-dev` branch from `https://github.com/su-mangale/fluxcd.git` and starts at `clusters/production/`.

## Image automation

Flux scans the YKP images in GHCR and commits selected image updates to `ykp-dev`. Application image fields must retain their inline `$imagepolicy` marker.