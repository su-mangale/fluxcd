# FluxCD GitRepository Source Setup

This guide explains how to add this repository as a Git source in FluxCD on your Kubernetes cluster.

## Prerequisites
- FluxCD installed on your Kubernetes cluster
- Access to this Git repository (clone URL)
- `kubectl` access to your cluster

## 1. Create a GitRepository Source

Replace `<REPO_URL>` with your repository's HTTPS or SSH URL, and `<BRANCH>` with the branch you want to track (e.g., `main` or `master`).

```bash
cat <<EOF | kubectl apply -f -
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: my-repo
  namespace: flux-system
spec:
  interval: 1m0s
  url: <REPO_URL>
  ref:
    branch: <BRANCH>
EOF
```

## 2. Verify the Source

Check that the source is ready:

```bash
kubectl get gitrepositories -n flux-system
```

## 3. Use the Source in a Kustomization or HelmRelease

Reference the `GitRepository` in your `Kustomization` or `HelmRelease` resources to deploy manifests or Helm charts from this repo.

---
For more details, see the [FluxCD documentation](https://fluxcd.io/docs/components/source/gitrepositories/).