import {
  readFileSync,
  writeFileSync,
  unlinkSync,
  existsSync,
  openSync,
  createReadStream,
  createWriteStream,
} from "fs";
import { createInterface } from "readline/promises";
import { extname, basename, join } from "path";
import { tmpdir } from "os";

const PARK_EXTENSIONS = new Set([".ts", ".py"]);

interface HookInput {
  hook_event_name: string;
  tool_name: string;
  tool_input: { file_path: string };
  session_id: string;
}

function emit(obj: object): never {
  console.log(JSON.stringify(obj));
  process.exit(0);
}

function allow(): never {
  emit({
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "allow",
    },
  });
}

function deny(reason: string): never {
  emit({
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: reason,
    },
  });
}

async function main() {
  const input: HookInput = JSON.parse(readFileSync("/dev/stdin", "utf-8"));
  const { hook_event_name, tool_name, tool_input, session_id } = input;
  const filePath = tool_input?.file_path ?? "";
  const ext = extname(filePath);
  const name = basename(filePath);

  const WAIT_FLAG = join(tmpdir(), `park-wait-${session_id}`);
  const AUTO_FLAG = join(tmpdir(), `park-auto-${session_id}`);

  // Only intercept matched extensions
  if (!PARK_EXTENSIONS.has(ext)) {
    process.exit(0);
  }

  // --- PostToolUse: park if wait flag was set ---
  if (hook_event_name === "PostToolUse") {
    if (existsSync(WAIT_FLAG)) {
      unlinkSync(WAIT_FLAG);
      process.stderr.write(
        `PARK MODE: ${tool_name} on "${name}" done. Waiting for your instructions.`
      );
      process.exit(2);
    }
    process.exit(0);
  }

  // --- PreToolUse ---

  // Auto mode: skip prompt, allow immediately
  if (existsSync(AUTO_FLAG)) {
    allow();
  }

  // Interactive prompt via /dev/tty
  let answer = "y";
  try {
    const fd = openSync("/dev/tty", "r+");
    const rl = createInterface({
      input: createReadStream("", { fd }),
      output: createWriteStream("", { fd }),
    });
    answer = await rl.question(
      `\n[park-mode] ${tool_name} → ${name}\n` +
        `  (y)es / (n)o / (w)ait / (a)uto: `
    );
    rl.close();
  } catch {
    // No TTY available (CI, piped) — default to allow
    answer = "y";
  }

  const choice = answer.trim().toLowerCase();

  switch (choice) {
    case "n":
    case "no":
      deny("User denied via park-mode prompt");
      break;

    case "w":
    case "wait":
      writeFileSync(WAIT_FLAG, "");
      allow();
      break;

    case "a":
    case "auto":
      writeFileSync(AUTO_FLAG, "");
      allow();
      break;

    default:
      allow();
      break;
  }
}

main();
