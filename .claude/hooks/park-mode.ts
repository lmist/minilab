import { readFileSync } from "fs";
import { extname } from "path";

interface HookInput {
  tool_name: string;
  tool_input: {
    file_path: string;
    content?: string;
  };
}

const PARK_EXTENSIONS = new Set([".ts", ".py"]);

const input: HookInput = JSON.parse(readFileSync("/dev/stdin", "utf-8"));
const filePath = input.tool_input?.file_path ?? "";
const ext = extname(filePath);

if (PARK_EXTENSIONS.has(ext)) {
  process.stderr.write(
    `PARK MODE: Written file "${filePath}" matches ${[...PARK_EXTENSIONS].join(", ")}. ` +
      `Stop and wait for user instructions before taking any further action.`
  );
  process.exit(2);
}
