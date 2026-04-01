/**
 * Permission modes for tool execution.
 * escalate from least to most privileged.
 */
export enum PermissionMode {
  /** Read-only access to workspace files */
  ReadOnly = "read_only",
  /** Can read and write files, but cannot execute arbitrary commands */
  WorkspaceWrite = "workspace_write",
  /** Full access: can run any command, delete files, etc. */
  DangerFullAccess = "danger_full_access",
}

/**
 * JSON Schema for tool input validation (simplified).
 */
export interface ToolInputSchema {
  type: "object";
  properties: Record<string, { type: string }>;
  required?: string[];
  additionalProperties?: boolean;
}

/**
 * Specification for a single tool.
 */
export interface ToolSpec {
  /** Unique identifier (canonical name, underscores) */
  name: string;
  /** Human-readable description */
  description: string;
  /** JSON Schema for input validation */
  inputSchema: ToolInputSchema;
  /** Required permission level to execute this tool */
  requiredPermission: PermissionMode;
}

/**
 * Source of a tool entry.
 */
export enum ToolSource {
  /** Built-in core tool */
  Base = "base",
  /** Conditionally loaded based on config */
  Conditional = "conditional",
  /** Plugin-provided tool */
  Plugin = "plugin",
}

/**
 * Entry in the tool manifest.
 */
export interface ToolManifestEntry {
  name: string;
  source: ToolSource;
}

/**
 * Result of tool execution.
 */
export interface ToolResult {
  success: boolean;
  output?: string;
  error?: string;
}

/**
 * Plugin tool definition (for external plugins).
 */
export interface PluginTool {
  definition: {
    name: string;
    description: string;
    inputSchema: ToolInputSchema;
  };
  requiredPermission: () => PermissionMode;
  execute(input: Record<string, unknown>): Promise<string>;
}
