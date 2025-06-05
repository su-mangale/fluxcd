# FluxCD GitOps Repository

This repository implements a scalable, multi-environment GitOps workflow using FluxCD. It is organized for production-grade Kubernetes platform and application management, supporting overlays for production and staging, and grouping resources by application and infrastructure component.

## Repository Structure

```
repo-root/
├── apps/
│   ├── base/           # Base manifests for each application (HelmRelease, Kustomization, etc.)
│   ├── production/     # Production overlays (patches, env-specific config)
│   └── staging/        # Staging overlays
├── infrastructure/
│   ├── base/           # Base manifests for infra components (ingress, sources, etc.)
│   ├── production/     # Production overlays (patches, env-specific config)
│   └── staging/        # Staging overlays
├── clusters/
│   ├── production/     # Kustomization for production cluster (references overlays)
│   └── staging/        # Kustomization for staging cluster
├── helm/               # Helm charts for custom or third-party apps
└── README.md           # This file
```

## Onboarding Instructions

### 1. Prerequisites
- FluxCD installed on your Kubernetes cluster
- Access to this Git repository
- `kubectl` access to your cluster

### 2. Push the Repository
Initialize and push this repository to your remote:

```bash
git init
git add .
git commit -m "Initial commit for FluxCD GitOps setup"
git remote add origin <your-repo-url>
git push -u origin main
```

### 3. Add the Repository as a FluxCD Source
Apply the `GitRepository` manifest (see `infrastructure/base/sources/gitrepo.yaml`) or create your own:

```bash
kubectl apply -f infrastructure/base/sources/gitrepo.yaml
```

Or manually:

```bash
cat <<EOF | kubectl apply -f -
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: fluxcd
  namespace: flux-system
spec:
  interval: 1m0s
  url: <REPO_URL>
  ref:
    branch: main
EOF
```

### 4. Deploy Cluster Kustomizations
Apply the Kustomization for your environment (production or staging):

```bash
kubectl apply -k clusters/production
# or for staging
kubectl apply -k clusters/staging
```

### 5. Verify FluxCD Sync
Check that resources are being reconciled:

```bash
kubectl get kustomizations -A
kubectl get helmreleases -A
```

---

## Notes
- All application and infrastructure manifests are grouped by component under `apps/base/` and `infrastructure/base/`.
- Overlays for production and staging allow for environment-specific configuration and patches.
- Only Kustomization manifests should exist in `clusters/production` and `clusters/staging`.
- Secrets (e.g., GitHub PAT) should be managed securely and never committed to the repo.

For more details, see the comments in each directory and manifest.