/**
 * OpenClaw Agent using the new ToolRegistry pattern.
 * This demonstrates how an agent can:
 * - Load tool specs from multiple skills
 * - Check permissions
 * - Execute tools and return results
 */

import { GlobalToolRegistry, PermissionMode, mvpToolSpecs } from "@openclaw/tool-registry";

// Demo: Build a registry with built-in tools + a custom plugin
const registry = new GlobalToolRegistry([
  {
    definition: {
      name: "demo_echo",
      description: "Echo back a message (demo plugin tool)",
      inputSchema: {
        type: "object",
        properties: {
          message: { type: "string" },
          times: { type: "number" }
        },
        required: ["message"]
      }
    },
    requiredPermission: () => PermissionMode.ReadOnly,
    execute: async (input) => {
      const msg = input.message as string;
      const times = (input.times as number) || 1;
      return Array(times).fill(msg).join("\n");
    }
  }
]);

// Show all available tool definitions
console.log("Available tools:");
for (const spec of registry.definitions()) {
  console.log(`- ${spec.name}: ${spec.description} (permission: ${spec.requiredPermission})`);
}

// Example: Execute demo_echo
console.log("\nExecuting demo_echo...");
const result = await registry.execute("demo_echo", { message: "Hello from ToolRegistry!", times: 3 });
console.log("Result:", result);

// Example: Normalize allowed tools
console.log("\nNormalized allowed tools from ['read', 'grep', 'bash']:");
const allowed = registry.normalizeAllowedTools(["read", "grep", "bash"]);
if (allowed.isOk()) {
  console.log("Allowed set:", [...allowed.unwrap()]);
} else {
  console.error("Error:", allowed.unwrapErr());
}
