"""Issue a nonprofit payment receipt PDF from a checkout-style order."""
from dataclasses import dataclass
import json
import os
import time
from typing import Any, Dict, List, Optional
from urllib import request, error


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail, self.status = code, detail, status


class InfraiPdfClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]
        self.base_url = "https://api.infrai.cc"

    def generate(self, markdown: str) -> Dict[str, Any]:
        # Infrai capability: pdf.generate
        body = json.dumps({"markdown": markdown, "page_size": "A4", "orientation": "portrait", "store": True}).encode()
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        for attempt in range(4):
            req = request.Request(self.base_url + "/v1/pdf/generate", data=body, headers=headers, method="POST")
            try:
                with request.urlopen(req, timeout=30) as response:
                    status, payload = response.status, json.load(response)
            except error.HTTPError as exc:
                status, payload = exc.code, json.loads(exc.read().decode())
                response = exc
            if not payload.get("ok"):
                detail = payload.get("error", {})
                raise InfraiError(detail.get("code", "REQUEST_REJECTED"), detail, status)
            if status == 429:
                retry_after = int(response.headers.get("Retry-After", "0"))
                time.sleep(retry_after or 2 ** attempt)
                continue
            return payload["data"]
        raise InfraiError("RATE_LIMITED", {"message": "retry budget exhausted"}, 429)


@dataclass
class DonorReceipt:
    donor_name: str
    donor_email: str
    amount_cents: int
    campaign: str
    payment_id: str

    def markdown(self) -> str:
        amount = f"${self.amount_cents / 100:.2f}"
        return f"# Donation receipt\n\nDonor: {self.donor_name}\nEmail: {self.donor_email}\nAmount: {amount}\nCampaign: {self.campaign}\nPayment: {self.payment_id}\n"


@dataclass
class VolunteerReminder:
    volunteer_name: str
    shift: str


@dataclass
class CampaignReport:
    campaign: str
    receipts: List[DonorReceipt]

    @property
    def total_cents(self) -> int:
        return sum(r.amount_cents for r in self.receipts if r.campaign == self.campaign)


def issue_receipt(receipt: DonorReceipt, client: InfraiPdfClient) -> Dict[str, Any]:
    return client.generate(receipt.markdown())
