from receipt_service import CampaignReport, DonorReceipt


def test_campaign_report_counts_only_matching_campaign():
    receipts = [
        DonorReceipt("A", "a@example.org", 1200, "Spring pantry", "p1"),
        DonorReceipt("B", "b@example.org", 800, "School lunch", "p2"),
        DonorReceipt("C", "c@example.org", 500, "Spring pantry", "p3"),
    ]
    assert CampaignReport("Spring pantry", receipts).total_cents == 1700

