#!/usr/bin/env bash
set -eu
# Optional reference acquisition; requires network access and git. Does not execute repository software.
target_dir="${1:-resources/upstream}"
mkdir -p "$target_dir"
git clone --depth 1 https://github.com/Leonxlnx/taste-skill.git "$target_dir/taste-skill"
git clone --depth 1 https://github.com/vercel-labs/agent-skills.git "$target_dir/agent-skills"
git clone --depth 1 https://github.com/voltagent/awesome-design-md.git "$target_dir/awesome-design-md"
git clone --depth 1 https://github.com/microsoft/playwright-cli.git "$target_dir/playwright-cli"
for repo in taste-skill agent-skills awesome-design-md playwright-cli; do
 git -C "$target_dir/$repo" rev-parse HEAD > "$target_dir/$repo/ACQUIRED_COMMIT.txt"
done
