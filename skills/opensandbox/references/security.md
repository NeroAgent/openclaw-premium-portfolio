# Security Considerations

OpenSandbox uses containers (Docker) or Kubernetes pods to isolate execution.

**Isolation guarantees:**
- Filesystem: Each sandbox gets its own rootfs; host mounts are explicit (`--mount`).
- Network: Egress controlled by server policies; by default may be blocked.
- Resources: CPU/memory limits can be set per image or per request.
- Privileges: Containers run as non-root by default.

**Runtime limits:**
- Timeouts enforced (kill after N seconds)
- Memory limits (configurable)
- Max processes/threads limits

**Threat model:**
- Protects host from malicious code inside sandbox
- Does *not* protect against side-channel attacks or kernel exploits (typical container threat model)
- For high-security, use Kubernetes with additional security contexts (seccomp, AppArmor)

**Best practices:**
- Run server on dedicated host
- Use read-only root filesystem unless writes needed
- Avoid mounting sensitive host paths
- Keep images minimal and patched
- Set resource limits to avoid DoS

---

For advanced security config, see upstream: https://opensandbox.ai/docs/security