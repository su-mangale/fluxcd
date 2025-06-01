# prod Directory Structure

This directory contains the main FluxCD/Kubernetes configuration for the `prod` (production) environment. Below is a description of the subdirectories:

## apps/
Contains application manifests, such as Deployments, Services, and Ingresses for workloads running in production.

## helm/
Contains Helm chart customizations and values files for deploying applications or infrastructure using Helm in the production cluster.

## infrastructure/
Contains Kustomization manifests and GitRepository sources for cluster infrastructure components (e.g., networking, storage, monitoring, ingress controllers, etc.).

---

Each subdirectory is intended to keep production resources organized and manageable for GitOps workflows with FluxCD.
