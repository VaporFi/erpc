#!/usr/bin/env python3
"""Check the historical block required by V1 startup, with and without transactions.

Usage: python3 scripts/check-avalanche-history.py <RPC URL>
Run against eRPC from its private network after a routing change.
"""
import json
import sys
import urllib.request

for full_transactions in (False, True):
    request = urllib.request.Request(
        sys.argv[1],
        data=json.dumps({
            "jsonrpc": "2.0", "id": 1, "method": "eth_getBlockByNumber",
            "params": ["0x12fd20e", full_transactions],
        }).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        body = json.load(response)
    assert "error" not in body, body.get("error")
    block = body.get("result")
    assert block and block["number"] == "0x12fd20e", "Historical block missing"
    assert block["hash"] == "0x3146c555ae6bb60666a90e0ef61eab163cc25ef2836ca5eefafd4245ee660903"
    print(f"PASS: historical block, full_transactions={full_transactions}")
