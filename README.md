# FluxCD GitOps Repository

This branch uses an environment-first FluxCD layout for the `production` cluster.

```text
clusters/production/                 # Flux reconciliation entrypoint
  flux-system/                       # Flux-generated bootstrap manifests only
  infrastructure.yaml                # Reconciles infrastructure before apps
  apps.yaml                          # Reconciles application overlays
infrastructure/controllers/cert-manager/
  base/                              # Shared cert-manager resources
  production/                        # Production overlay
apps/<application>/
  base/                              # Application manifests
  production/                        # Environment-specific overlay
```

## Applications

The following application folders are ready for their manifests:

- `ykp-dashboard`
- `ykp-auth`
- `ykp-catalog`
- `ykp-shell`
- `ykp-api`

Add Kubernetes resources to an application's `base/` directory and list them in its `base/kustomization.yaml`. Put environment-specific patches and configuration in its `production/` directory.

## Flux source

Flux syncs the `ykp-dev` branch from `https://github.com/su-mangale/fluxcd.git`. The production root Kustomization applies Flux itself, then cert-manager, then the application layer through the explicit `dependsOn` relationship.

## Certificate issuance

The retained Let's Encrypt issuers use Traefik for HTTP-01 challenges. Install/configure an ingress controller using the `traefik` ingress class, or update the issuer solver before requesting certificates.