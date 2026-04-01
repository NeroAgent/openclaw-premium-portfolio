import { ToolSpec, ToolManifestEntry, ToolSource, PermissionMode, PluginTool, ToolResult } from "./types";

/**
 * Normalize tool name: trim, replace hyphens with underscores, lowercase.
 */
export function normalizeToolName(name: string): string {
  return name.trim().replace(/-/g, "_").toLowerCase();
}

/**
 * Reverses normalization to canonical form (capitalize underscores to hyphens sometimes).
 * For now, we'll keep canonical names using underscores (read_file, write_file).
 */
export function canonicalName(name: string): string {
  return normalizeToolName(name);
}

/**
 * Built-in MVP tool specifications.
 * These mirror the tools in claw-code's tools/src/lib.rs.
 */
export function mvpToolSpecs(): ToolSpec[] {
  return [
    {
      name: "bash",
      description: "Execute a shell command in the current workspace.",
      inputSchema: {
        type: "object",
        properties: {
          command: { type: "string" },
          timeout: { type: "integer" },
          description: { type: "string" },
          run_in_background: { type: "boolean" },
          dangerouslyDisableSandbox: { type: "boolean" },
        },
        required: ["command"],
        additionalProperties: false,
      },
      requiredPermission: PermissionMode.DangerFullAccess,
    },
    {
      name: "read_file",
      description: "Read a text file from the workspace.",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string" },
          offset: { type: "integer" },
          limit: { type: "integer" },
        },
        required: ["path"],
        additionalProperties: false,
      },
      requiredPermission: PermissionMode.ReadOnly,
    },
    {
      name: "write_file",
      description: "Write a text file in the workspace.",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string" },
          content: { type: "string" },
        },
        required: ["path", "content"],
        additionalProperties: false,
      },
      requiredPermission: PermissionMode.WorkspaceWrite,
    },
    {
      name: "edit_file",
      description: "Replace text in a workspace file.",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string" },
          old_string: { type: "string" },
          new_string: { type: "string" },
          replace_all: { type: "boolean" },
        },
        required: ["path", "old_string", "new_string"],
        additionalProperties: false,
      },
      requiredPermission: PermissionMode.WorkspaceWrite,
    },
    {
      name: "glob_search",
      description: "Find files by glob pattern.",
      inputSchema: {
        type: "object",
        properties: {
          pattern: { type: "string" },
          path: { type: "string" },
        },
        required: ["pattern"],
        additionalProperties: false,
      },
      requiredPermission: PermissionMode.ReadOnly,
    },
    {
      name: "grep_search",
      description: "Search file contents with a regex pattern.",
      inputSchema: {
        type: "object",
        properties: {
          pattern: { type: "string" },
          path: { type: "string" },
          glob: { type: "string" },
          count: { type: "boolean" },
        },
        required: ["pattern"],
        additionalProperties: false,
      },
      requiredPermission: PermissionMode.ReadOnly,
    },
  ];
}

/**
 * Registry of tool manifest entries (name + source).
 */
export class ToolRegistry {
  private entries: ToolManifestEntry[];

  constructor(entries: ToolManifestEntry[]) {
    this.entries = entries;
  }

  entriesList(): ToolManifestEntry[] {
    return this.entries;
  }

  /**
   * Check if this registry contains a tool (by normalized name).
   */
  has(name: string): boolean {
    const normalized = normalizeToolName(name);
    return this.entries.some((e) => normalizeToolName(e.name) === normalized);
  }
}

/**
 * Global registry combining built-in tool specs and plugin tools.
 */
export class GlobalToolRegistry {
  private pluginTools: PluginTool[];

  constructor(pluginTools: PluginTool[] = []) {
    this.pluginTools = pluginTools;
  }

  /**
   * Create a registry with only built-in tools.
   */
  static builtin(): GlobalToolRegistry {
    return new GlobalToolRegistry([]);
  }

  /**
   * Add plugin tools with conflict detection.
   */
  withPluginTools(pluginTools: PluginTool[]): Result<GlobalToolRegistry, string> {
    const builtinNames = new Set(mvpToolSpecs().map((s) => s.name));
    const seen = new Set<string>();

    for (const tool of pluginTools) {
      const name = canonicalName(tool.definition.name);
      if (builtinNames.has(name)) {
        return Result.err(`plugin tool "${name}" conflicts with a built-in tool`);
      }
      if (!seen.add(name).value) {
        return Result.err(`duplicate plugin tool name "${name}"`);
      }
    }

    return Result.ok(new GlobalToolRegistry(pluginTools));
  }

  /**
   * Build the full list of ToolSpecs, optionally filtering by allowed tools.
   */
  definitions(allowedTools?: Set<string>): ToolSpec[] {
    const builtins = mvpToolSpecs().filter((spec) => !allowedTools || allowedTools.has(spec.name));
    const plugins = this.pluginTools
      .filter((p) => !allowedTools || allowedTools.has(canonicalName(p.definition.name)))
      .map((p) => ({
        name: canonicalName(p.definition.name),
        description: p.definition.description,
        inputSchema: p.definition.inputSchema,
        requiredPermission: PermissionMode.WorkspaceWrite, // plugins opt-in via their requiredPermission()
      } as ToolSpec));
    return builtins.concat(plugins);
  }

  /**
   * Execute a tool by name.
   */
  async execute(name: string, input: Record<string, unknown>): Promise<ToolResult> {
    // Try built-in first
    const spec = mvpToolSpecs().find((s) => s.name === name);
    if (spec) {
      return await this.executeBuiltin(name, input);
    }

    // Try plugin tools
    const plugin = this.pluginTools.find((p) => canonicalName(p.definition.name) === name);
    if (plugin) {
      try {
        const output = await plugin.execute(input);
        return { success: true, output };
      } catch (e) {
        return { success: false, error: String(e) };
      }
    }

    return { success: false, error: `unsupported tool: ${name}` };
  }

  /**
   * Stub for built-in tool execution. To be implemented per-tool.
   */
  private async executeBuiltin(name: string, input: Record<string, unknown>): Promise<ToolResult> {
    switch (name) {
      case "read_file":
        // TODO: implement using OpenClaw file API
        return { success: false, error: "not implemented" };
      case "bash":
        // TODO: integrate with exec tool
        return { success: false, error: "not implemented" };
      default:
        return { success: false, error: `unknown builtin: ${name}` };
    }
  }

  /**
   * Normalize allowed tool list from comma/whitespace separated tokens.
   */
  normalizeAllowedTools(values: string[]): Result<Set<string>, string> {
    if (values.length === 0) {
      return Result.ok(new Set());
    }

    const allSpecs = this.definitions();
    const allNames = new Set(allSpecs.map((s) => s.name));
    const aliasMap: Record<string, string> = {
      read: "read_file",
      write: "write_file",
      edit: "edit_file",
      glob: "glob_search",
      grep: "grep_search",
    };

    const allowed = new Set<string>();
    for (const token of values.flatMap((v) => v.split(/[,\s]+/).filter(Boolean))) {
      const normalized = normalizeToolName(token);
      const canonical = aliasMap[normalized] || (allNames.has(normalized) ? normalized : null);
      if (!canonical) {
        return Result.err(`unsupported tool in allowedTools: ${token}`);
      }
      allowed.add(canonical);
    }
    return Result.ok(allowed);
  }
}

/**
 * Simple Result type for error handling.
 */
export class Result<T, E> {
  constructor(private readonly value: T | null, private readonly error: E | null) {}

  static ok<T, E>(value: T): Result<T, E> {
    return new Result(value, null);
  }

  static err<T, E>(error: E): Result<T, E> {
    return new Result(null, error);
  }

  isOk(): boolean {
    return this.error === null;
  }

  isErr(): boolean {
    return this.error !== null;
  }

  unwrap(): T {
    if (this.error !== null) {
      throw new Error(`unwrap on err: ${this.error}`);
    }
    return this.value as T;
  }

  unwrapErr(): E {
    if (this.value !== null) {
      throw new Error("unwrapErr on ok");
    }
    return this.error as E;
  }
}
