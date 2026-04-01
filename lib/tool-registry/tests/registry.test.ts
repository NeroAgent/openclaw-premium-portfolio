import { describe, it, expect } from "vitest";
import { GlobalToolRegistry, PermissionMode, mvpToolSpecs, normalizeToolName, canonicalName } from "../src/registry";

describe("ToolRegistry", () => {
  it("normalizes tool names", () => {
    expect(normalizeToolName("ReadFile")).toBe("readfile");
    expect(normalizeToolName("read-file")).toBe("read_file");
    expect(normalizeToolName("  GREP  ")).toBe("grep");
  });

  it("returns MVP tool specs", () => {
    const specs = mvpToolSpecs();
    expect(specs.length).toBeGreaterThan(0);
    expect(specs.find((s) => s.name === "read_file")).toBeDefined();
    expect(specs.find((s) => s.name === "bash")).toBeDefined();
  });

  it("creates builtin registry", () => {
    const reg = GlobalToolRegistry.builtin();
    const all = reg.definitions();
    expect(all.some((s) => s.name === "read_file")).toBe(true);
  });

  it("normalizes allowed tools with aliases", () => {
    const reg = GlobalToolRegistry.builtin();
    const result = reg.normalizeAllowedTools(["read", "grep", "bash"]);
    expect(result.isOk()).toBe(true);
    const allowed = result.unwrap();
    expect(allowed.has("read_file")).toBe(true);
    expect(allowed.has("grep_search")).toBe(true);
    expect(allowed.has("bash")).toBe(true);
  });

  it("rejects unknown allowed tool", () => {
    const reg = GlobalToolRegistry.builtin();
    const result = reg.normalizeAllowedTools(["unknown_tool"]);
    expect(result.isErr()).toBe(true);
  });
});
