# Zero Trust Visibility & Automation Check

> Source: 제로트러스트 가이드라인 2.0 (KISA), CISA Zero Trust Maturity Model
> Checklist refs: Visibility/Automation elements, KISA ZT 8 elements

---

## 1. Centralized Logging Verification

```bash
# Check syslog configuration and forwarding
systemctl status rsyslog 2>/dev/null || systemctl status syslog-ng 2>/dev/null

# Verify log forwarding to SIEM
grep -rn "@@\|action.*forward\|omfwd" /etc/rsyslog.conf /etc/rsyslog.d/ 2>/dev/null

# Check log collection agents
systemctl status filebeat 2>/dev/null
systemctl status fluentd 2>/dev/null
systemctl status fluent-bit 2>/dev/null
systemctl status vector 2>/dev/null

# Verify log rotation is configured
ls -la /etc/logrotate.d/ 2>/dev/null | head -10
```

---

## 2. Audit Trail Completeness Check

```bash
# Check auditd rules
auditctl -l 2>/dev/null | head -20

# Verify critical events are logged
# File access to sensitive paths
auditctl -l 2>/dev/null | grep -E "etc/passwd|etc/shadow|etc/sudoers"

# Verify authentication events are captured
grep -c "authentication\|login\|sshd\|sudo" /var/log/auth.log 2>/dev/null || \
grep -c "authentication\|login\|sshd\|sudo" /var/log/secure 2>/dev/null

# Check log integrity (tamper protection)
ls -la /var/log/audit/audit.log 2>/dev/null
# Logs should be append-only:
lsattr /var/log/audit/audit.log 2>/dev/null | grep "a"
```

---

## 3. SIEM & Threat Detection Status

```bash
# Check SIEM agent connectivity
# Splunk
systemctl status SplunkForwarder 2>/dev/null
/opt/splunkforwarder/bin/splunk list forward-server 2>/dev/null

# Elastic
systemctl status elastic-agent 2>/dev/null
systemctl status filebeat 2>/dev/null

# Wazuh
systemctl status wazuh-agent 2>/dev/null
cat /var/ossec/etc/ossec.conf 2>/dev/null | grep -A2 "server-ip"

# Check alert rules are active
ls /var/ossec/ruleset/rules/ 2>/dev/null | wc -l
```

---

## 4. Automated Response Capability Check (SOAR)

```bash
# Check for SOAR/automation agents
systemctl status soar-agent 2>/dev/null
systemctl status cortex 2>/dev/null

# Verify automated blocking is configured
# Check fail2ban (basic automated response)
systemctl status fail2ban 2>/dev/null
fail2ban-client status 2>/dev/null

# Check automated quarantine rules
iptables -L -n 2>/dev/null | grep -i "drop\|reject" | wc -l
```

---

## 5. Asset Discovery & Inventory

```bash
# Network asset discovery
arp -a 2>/dev/null | wc -l
echo "Known ARP entries: $(arp -a 2>/dev/null | wc -l)"

# Check for asset management agent
systemctl status qualys-cloud-agent 2>/dev/null
systemctl status nessus 2>/dev/null
systemctl status rapid7 2>/dev/null

# List all listening services
ss -tlnp | awk 'NR>1{print $4, $6}' | sort

# Check for unauthorized services
ss -tlnp | awk 'NR>1{print $6}' | sort -u
```

---

## 6. Security Dashboard & Alerting

```bash
# Check monitoring stack
systemctl status prometheus 2>/dev/null
systemctl status grafana-server 2>/dev/null
systemctl status alertmanager 2>/dev/null

# Verify alert notification channels
# Check alertmanager config for notification routes
cat /etc/alertmanager/alertmanager.yml 2>/dev/null | grep -A5 "receivers"

# Check email/SMS/webhook alerting
grep -rn "smtp\|slack\|webhook\|pagerduty" \
  /etc/alertmanager/ /etc/grafana/ 2>/dev/null | head -10
```

---

## 7. Vulnerability Scanning Schedule

```bash
# Check for scheduled vulnerability scans
crontab -l 2>/dev/null | grep -i "scan\|nessus\|openvas\|trivy\|grype"

# Check last scan results
ls -lt /var/log/vulnerability-scan/ 2>/dev/null | head -5
ls -lt /opt/scanner/reports/ 2>/dev/null | head -5

# Verify container image scanning in CI/CD
grep -rn "trivy\|grype\|snyk\|aqua" \
  .github/workflows/ .gitlab-ci.yml Jenkinsfile 2>/dev/null
```

---

## Verification Checklist

| Item | Check | Expected |
|------|-------|----------|
| Log forwarding | Syslog/agent config | Active SIEM integration |
| Audit rules | `auditctl -l` | Critical paths monitored |
| Log integrity | `lsattr` | Append-only attribute set |
| SIEM agent | Service status | Running and connected |
| Fail2ban | `fail2ban-client status` | Active with jails |
| Asset inventory | Discovery agent | Running |
| Alerting | Notification channels | Configured (email/Slack/webhook) |
| Vuln scanning | Cron/CI check | Scheduled regularly |
