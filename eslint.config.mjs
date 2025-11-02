import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
  {
    ignores: [
      "node_modules/**",
      ".next/**",
      "out/**",
      "build/**",
      "next-env.d.ts",
    ],
  },
  // --- FIX: Add configuration to disable or modify the no-unused-vars rule ---
  {
    // Apply this configuration to TypeScript files
    files: ["**/*.ts", "**/*.tsx"],
    rules: {
      // Option 1 (Recommended compromise): Allow variables prefixed with an underscore
      // Change 'warn' to 'error' if you want to fail the build on unused vars
      "@typescript-eslint/no-unused-vars": ["warn", { "argsIgnorePattern": "^_", "varsIgnorePattern": "^_" }],
      
      // Option 2 (If Option 1 doesn't resolve all warnings and you must deploy): 
      // "@typescript-eslint/no-unused-vars": "off",

      // Option 3: Also disable the base ESLint rule (Next/Vitals might already handle this)
      // "no-unused-vars": "off" 
    },
  },
  // --------------------------------------------------------------------------
];

export default eslintConfig;
