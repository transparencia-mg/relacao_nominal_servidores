#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

DATAPACKAGE = Path("datapackage/datapackage.json")

def main():
    dp = json.loads(DATAPACKAGE.read_text(encoding="utf-8"))

    DATAPACKAGE.write_text(
        json.dumps(dp, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("📦 datapackage.json validado e regravado")

if __name__ == "__main__":
    main()
