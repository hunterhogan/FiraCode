#! /usr/bin/env python3
import os
import re
import subprocess
import sys

import common


def update_version(version, src):
  print(f"update_version: {version} in {src}")

  match = re.search(r"^(\d+)\.(\d+)(.*)$", version)
  if not match:
      print(f"Could not parse version {version}, falling back to simple split.")
      parts = version.split(".")
      major = parts[0]
      minor = parts[1] if len(parts) > 1 else "0"
  else:
      major = match.group(1)
      minor = match.group(2)

  with open(src, 'r') as f:
    contents = f.read()

  contents = re.sub(r"versionMajor\s+=\s+\d+;",
                    f"versionMajor = {major};",
                    contents)
  contents = re.sub(r"versionMinor\s+=\s+\d+;",
                    f"versionMinor = {minor};",
                    contents)

  # Check for versionString custom parameter and update or insert it
  version_str = f"Version {version}"

  if 'name = "versionString";' in contents:
      # Simple replace for existing value
      contents = re.sub(r'name = "versionString";\s*value = ".*?";',
                        f'name = "versionString";\nvalue = "{version_str}";',
                        contents)
  else:
      # Insert into customParameters
      replacement = f'customParameters = (\n{{\nname = "versionString";\nvalue = "{version_str}";\n}},\n'
      contents = re.sub(r'customParameters\s*=\s*\(', replacement, contents, count=1)

  with open(src, 'w') as f:
    f.write(contents)

if __name__ == '__main__':
  os.chdir(common.root)
  version = common.version()
  update_version(version, 'FiraCode.glyphs')
  sys.exit(0)