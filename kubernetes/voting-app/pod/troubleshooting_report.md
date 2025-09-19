# Kubernetes Voting App Troubleshooting Report

This document outlines the issues encountered and the steps taken to resolve them when deploying the Kubernetes voting application.

## Summary of Issues

The deployment failed due to a series of YAML configuration errors in the Pod definition files (`voting-app-pod.yml` and `result-app-pod.yml`). The issues were resolved through iterative debugging and correction of the YAML files.

## Detailed Problem and Resolution Steps

### Issue 1: Incorrect `apiVersion` for Pods

*   **Problem:** The initial `kubectl apply` command failed with a "resource mapping not found" error for the `vote` and `result` pods.
*   **Analysis:** The `apiVersion` in `voting-app-pod.yml` and `result-app-pod.yml` was set to `apps/v1`. For `Pod` resources, the correct `apiVersion` is `v1`.
*   **Resolution:** The `apiVersion` in both files was changed from `apps/v1` to `v1`.

### Issue 2: Malformed Container Specification (`env` placement)

*   **Problem:** After fixing the `apiVersion`, the `kubectl apply` command failed with a `BadRequest` error, indicating that the `Pod` resource could not be parsed correctly. The error messages pointed to an issue with an `env` field.
*   **Analysis:** In both `voting-app-pod.yml` and `result-app-pod.yml`, the `env` section (for environment variables) was incorrectly placed as a nested field within the `ports` section. The `env` section should be a direct child of the container specification.
*   **Resolution:** The YAML files were modified to move the `env` block to the correct indentation level, making it a sibling of the `ports` and `image` fields.

### Issue 3: YAML Syntax and Indentation Errors

*   **Problem:** During the process of fixing the `env` placement, further YAML syntax errors were introduced, such as incorrect indentation and a malformed `env` structure in `voting-app-pod.yml`. One of the `replace` operations for `result-app-pod.yml` resulted in incorrect indentation, leading to a "did not find expected '-'" parsing error.
*   **Analysis:** The `replace` operations required very specific `old_string` and `new_string` values to maintain correct YAML indentation. The errors were caused by not precisely matching the existing file content or by providing a replacement string with incorrect whitespace.
*   **Resolution:** The files were read again to get their exact content, and the `replace` operations were performed with carefully crafted strings to ensure the final YAML was valid. This involved correcting the indentation of `ports`, `env`, and their child elements to align with the YAML specification for Pods.

## Final Outcome

After these corrections, the `kubectl apply -f .` command executed successfully, and all pods and services for the voting application were created or updated as expected.
