# FluxCD GitOps Repository

This repository implements a scalable, production-ready GitOps workflow using FluxCD. It is organized for Kubernetes platform and application management, supporting overlays for production, and grouping resources by application and infrastructure component.

## Repository Structure

```
repo-root/
├── apps/
│   ├── base/           # Base manifests for each application (HelmRelease, Kustomization, etc.)
│   └── production/     # Production overlays (patches, env-specific config)
├── infrastructure/
│   ├── base/           # Base manifests for infra components (ingress, sources, etc.)
│   └── production/     # Production overlays (patches, env-specific config)
├── clusters/
│   └── production/     # Kustomization for production cluster (references overlays)
├── helm/               # Helm charts for custom or third-party apps
└── README.md           # This file
```

## Onboarding Instructions

### 1. Prerequisites
- FluxCD installed on your Kubernetes cluster
# FluxCD GitOps Repository

This repository implements a GitOps workflow using FluxCD. It groups infrastructure and applications by component and uses per-component Kustomizations so Flux can reconcile resources in a controlled order.

## What changed (recent updates)
- Issuers for cert-manager moved into their own overlay: `infrastructure/base/cert-manager/issuers/*`.
- cert-manager is reconciled via a dedicated Kustomization: `clusters/production/flux-system/cert-manager-kustomization.yaml`.
- Issuers are applied from `clusters/production/flux-system/cert-manager-issuers-kustomization.yaml` and depend on `cert-manager`.
- Traefik has a per-component Kustomization: `clusters/production/flux-system/traefik-kustomization.yaml` and depends on cert-manager + issuers.
- Applications are managed individually (example: `fast-api`): `clusters/production/flux-system/fast-api-kustomization.yaml` (depends on Traefik and cert-manager-issuers).
- Alertmanager (prometheus-community/alertmanager v1.27.1) added as a HelmRelease with its own kustomizations and a `helm-repos` Kustomization to ensure the HelmRepository is applied first.
- Root/infrastructure and monolithic `apps` kustomizations were removed in favor of per-component Kustomizations to enable correct ordering via Flux `dependsOn`.

## Key concepts used here
- Per-component Kustomizations: each infra/app component has a Kustomization CR under `clusters/production/flux-system/` that points at the overlay in the repo. This gives Flux stable objects to reference with `dependsOn`.
- Ordering with dependsOn: use `spec.dependsOn` in a Kustomization to make Flux wait for another Kustomization to be Ready before reconciling.
- wait + health checks: Kustomizations use `wait: true` and (optionally) `healthChecks`/`healthCheckExprs` (CEL) to express readiness requirements for complex resources like Certificate issuance and Traefik availability.
- HelmRepository ordering: HelmRepository resources must exist before HelmReleases try to fetch charts. We apply repository manifests via a dedicated `helm-repos` Kustomization and make HelmRelease Kustomizations depend on it.

## How to use this repository (bootstrapping)

1) Choose the branch you want Flux to use for bootstrapping (this repo contains a working branch named `cert-manager-issuers` used for the staged changes in this repo). Example bootstrap command:

```bash
flux bootstrap github \
  --token-auth \
  --owner=su-mangale \
  --repository=fluxcd \
  --branch=cert-manager-issuers \
  --path=clusters/production
```

2) The bootstrap command will apply Flux system components and then the Kustomizations in `clusters/production/flux-system/`.

3) Kustomizations are reconciled independently. Check status with:

```bash
kubectl -n flux-system get kustomizations.kustomize.toolkit.fluxcd.io
kubectl -n flux-system describe kustomization <name>
```

4) Verify HelmReleases and charts (e.g., Alertmanager):

```bash
kubectl -n monitoring get helmreleases
kubectl -n monitoring describe helmrelease alertmanager
```

## How ordering is implemented (examples)
- cert-manager Kustomization (installs HelmRelease with installCRDs: true)
- cert-manager-issuers Kustomization dependsOn cert-manager and waits for cert-manager to be ready before applying ClusterIssuer objects
- traefik Kustomization dependsOn cert-manager and cert-manager-issuers so Traefik only reconciles after certificate infrastructure is available
- fast-api Kustomization dependsOn traefik and cert-manager-issuers; it also includes CEL health checks to ensure Traefik and issuers are ready before declaring the app healthy
- alertmanager Kustomization dependsOn helm-repos (so HelmRepository is present) and cert-manager/traefik as configured

## Adding a new component or application
1. Create the component overlay under `infrastructure/base/<component>` (or `apps/base/<app>`).
2. Add a `kustomization.yaml` in the overlay listing resources.
3. Add a production overlay under `infrastructure/production/<component>` that references the base overlay.
4. Add a Kustomization CR in `clusters/production/flux-system/` named e.g. `<component>-kustomization.yaml` with:

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: <component>
  namespace: flux-system
spec:
  path: "./infrastructure/production/<component>"
  wait: true
  prune: true
  dependsOn:
    - name: other-component
      namespace: flux-system
```

5. Add the new Kustomization filename to `clusters/production/flux-system/kustomization.yaml` resources list so the overlay includes it.

## Health checks (CEL)
- Use `spec.healthChecks` (resource references) and `spec.healthCheckExprs` (CEL expressions) inside a Kustomization CR to define what "Ready" means for that component.
- Example (we use this for `fast-api`): ensure ClusterIssuer exists and Traefik deployment has available replicas. CEL expressions evaluate status fields and allow precise definitions of readiness.

## Troubleshooting tips
- If a HelmRelease fails with `HelmRepository not found`, ensure the HelmRepository resource is reconciled first — we use a `helm-repos` Kustomization for this and make HelmRelease Kustomizations depend on it.
- Use `kubectl -n flux-system describe kustomization <name>` to inspect conditions, events and health-check output.
- For HelmRelease issues: `kubectl -n <target-namespace> describe helmrelease <name>` and check `helm-controller` logs.
- If CRDs are missing for a component (e.g., cert-manager): ensure the cert-manager HelmRelease was applied with `installCRDs: true` and that the cert-manager Kustomization reached Ready before resources that depend on its CRDs are applied.

## Repo changes made in this branch (summary)
- Moved ClusterIssuer manifests to: `infrastructure/base/cert-manager/issuers/`
- Added per-component Kustomizations under: `clusters/production/flux-system/` — `cert-manager`, `cert-manager-issuers`, `traefik`, `fast-api`, `alertmanager`, `helm-repos`
- Added Alertmanager HelmRelease and HelmRepository under `infrastructure/base/monitoring/alertmanager/` and production overlay under `infrastructure/production/alertmanager/`

## Final notes
- This repo uses FluxCD v2 concepts (Kustomization CRs, HelmRelease, HelmRepository). Keep the `clusters/production/flux-system` overlay as the single place Flux reads for cluster-scoped reconciliation. Use `dependsOn` and `wait` to control ordering rather than relying on file ordering.
- If you want, I can open a PR with these changes and a checklist for reviewers, or revert/adjust any of the per-component timeouts or health checks.

---

If you'd like the README to also include quick-start commands for local testing (kind/minikube) or a diagram, tell me which and I'll add it.
