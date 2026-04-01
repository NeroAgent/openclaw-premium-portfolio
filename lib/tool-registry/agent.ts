#!/usr/bin/env node
/**
 * Tool Registry Agent — Proof of Concept
 *
 * This agent demonstrates Phase 2 integration:
 * - Loads skill definitions from workspace skill_registry.json
 * - Builds a GlobalToolRegistry with built-in + plugin tools
 * - Receives natural language requests, decides which tool to call
 * - Executes tools and returns results
 *
 * This could become the new OpenClaw agent runtime.
 */

import { readFile } from 'fs/promises';
import { join } from 'path';
import { GlobalToolRegistry, PermissionMode, mvpToolSpecs, normalizeToolName } from '@openclaw/tool-registry';

// Simple LLM call placeholder (would use openrouter or local model)
async function callLLM(prompt: string): Promise<string> {
  console.log("[LLM] Would call model with prompt:", prompt.slice(0, 100) + "...");
  return JSON.stringify({ thought: "Use read_file", tool: "read_file", input: { path: "README.md" } });
}

// Permission prompter (simplified)
async function requestPermission(toolName: string, permission: PermissionMode): Promise<boolean> {
  console.log(`[Permission] Requesting ${permission} for tool '${toolName}'`);
  return permission !== PermissionMode.DangerFullAccess;
}

async function discoverPluginTools() {
  const skillRegistryPath = '/root/.openclaw/workspace/skill_registry.json';
  const data = JSON.parse(await readFile(skillRegistryPath, 'utf-8'));
  const plugins: any[] = [];

  for (const [skillName] of Object.entries(data.skills)) {
    const skillDir = join('/root/.openclaw/workspace/skills', skillName);
    const skillFile = join(skillDir, `${skillName}.skill`);
    try {
      const def = JSON.parse(await readFile(skillFile, 'utf-8'));
      if (def.tools) {
        for (const tool of def.tools) {
          plugins.push({
            definition: {
              name: tool.name,
              description: tool.description,
              inputSchema: tool.input_schema
            },
            requiredPermission: () => {
              const map: Record<string, PermissionMode> = {
                read_only: PermissionMode.ReadOnly,
                workspace_write: PermissionMode.WorkspaceWrite,
                danger_full_access: PermissionMode.DangerFullAccess
              };
              return map[tool.permission] || PermissionMode.ReadOnly;
            },
            execute: async (input: any) => {
              const wrapper = join(skillDir, 'scripts', 'run.py');
              const { spawn } = await import('child_process');
              return new Promise((resolve, reject) => {
                const proc = spawn('python3', [wrapper, 'tool-call', tool.name, JSON.stringify(input)]);
                let out = '', err = '';
                proc.stdout.on('data', d => out += d);
                proc.stderr.on('data', d => err += d);
                proc.on('close', code => {
                  if (code === 0) resolve(out.trim());
                  else reject(new Error(err || `exit ${code}`));
                });
              });
            }
          });
        }
      }
    } catch (e) {
      // ignore missing skills
    }
  }

  return plugins;
}

async function main() {
  const pluginTools = await discoverPluginTools();
  const registry = new GlobalToolRegistry([]).withPluginTools(pluginTools).unwrap();
  console.log(`Loaded ${registry.definitions().length} tools`);

  // Demo: Execute read_file via file-reader skill
  const userRequest = "Read the AGENTS.md file";
  console.log(`User: ${userRequest}`);

  const decision = { tool: "read_file", input: { path: "/root/.openclaw/workspace/AGENTS.md", limit: 5 } };
  const toolName = normalizeToolName(decision.tool);
  const spec = registry.definitions().find(s => s.name === toolName);
  if (!spec) throw new Error(`Unknown tool: ${toolName}`);

  if (!(await requestPermission(spec.name, spec.requiredPermission))) {
    throw new Error("Permission denied");
  }

  console.log(`Executing: ${spec.name}`);
  const result = await registry.execute(toolName, decision.input);
  console.log("Result:", result);
}

main().catch(err => {
  console.error("Error:", err.message);
  process.exit(1);
});
