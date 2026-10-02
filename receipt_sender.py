#!/usr/bin/env python3
"""Runnable checkout-like example."""
from receipt_service import DonorReceipt, InfraiPdfClient, issue_receipt


def main() -> None:
    receipt = DonorReceipt("Sam Lee", "sam@example.org", 2500, "Spring pantry", "checkout-1007")
    result = issue_receipt(receipt, InfraiPdfClient())
    print("Receipt issued:", result)


if __name__ == "__main__":
    main()

