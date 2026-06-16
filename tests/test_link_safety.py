from __future__ import annotations

from leftlevel_helix.link_safety import analyze_links, analyze_url, extract_urls


def test_extract_urls_keeps_urls_as_text_only():
    text = "Look at https://example.com/path?q=1, then ignore normal words."
    assert extract_urls(text) == ["https://example.com/path?q=1"]


def test_https_url_gets_review_verdict_not_safe_claim():
    finding = analyze_url("https://example.com/path")
    assert finding.verdict == "review"
    assert finding.scheme == "https"
    assert finding.normalized_url == "https://example.com/path"
    assert finding.reasons == ["no obvious local parsing risk found"]


def test_plain_http_url_warns():
    finding = analyze_url("http://example.com")
    assert finding.verdict == "warning"
    assert "plain HTTP link" in finding.reasons


def test_javascript_url_is_blocked():
    finding = analyze_url("javascript:alert(1)")
    assert finding.verdict == "blocked"
    assert "blocked URL scheme: javascript" in finding.reasons


def test_data_url_is_blocked():
    finding = analyze_url("data:text/html,<script>alert(1)</script>")
    assert finding.verdict == "blocked"
    assert "blocked URL scheme: data" in finding.reasons


def test_private_ip_url_is_blocked():
    finding = analyze_url("https://192.168.1.1/admin")
    assert finding.verdict == "blocked"
    assert "local or private network target" in finding.reasons


def test_localhost_url_is_blocked():
    finding = analyze_url("http://localhost:8080")
    assert finding.verdict == "blocked"
    assert "local or private network target" in finding.reasons


def test_userinfo_link_warns():
    finding = analyze_url("https://login.example.com@evil.example/path")
    assert finding.verdict == "warning"
    assert "URL contains username or password text before the host" in finding.reasons


def test_punycode_link_warns():
    finding = analyze_url("https://xn--pple-43d.com")
    assert finding.verdict == "warning"
    assert "internationalized or punycode hostname needs review" in finding.reasons


def test_analyze_links_returns_multiple_findings():
    findings = analyze_links("One https://example.com and two javascript:alert(1)")
    assert [finding.verdict for finding in findings] == ["review", "blocked"]
