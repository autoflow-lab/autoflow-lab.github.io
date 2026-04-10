# Security Audit Log

## 2026-04-10 06:04 — Daily Audit

**Status:** ⚠️ WARNUNG (3 warnings, no critical findings)

### Findings

#### OpenClaw Gateway
- **gateway.trusted_proxies_missing**: Reverse proxy headers are not trusted
  - Issue: `gateway.bind` is loopback; `gateway.trustedProxies` is empty
  - Impact: Potential IP spoofing if exposed through a reverse proxy
  - Recommendation: Set `gateway.trustedProxies` to your proxy IPs OR keep Control UI local-only

- **gateway.nodes.denyCommands_ineffective**: Command filtering uses exact name matching only
  - Issue: Unknown command names detected (camera.snap, camera.clip, screen.record, calendar.add, contacts.add, reminders.add)
  - Impact: These commands not properly blocked if listed in denyCommands
  - Recommendation: Use exact command names; remove risky IDs from allowCommands if broader restrictions needed

- **models.weak_tier**: `anthropic/claude-haiku-4-5` below recommended tier
  - Issue: Smaller models more susceptible to prompt injection
  - Recommendation: Use top-tier models (GPT-5+, Claude 4.5+) for any bot with tools/untrusted inboxes

### Home Assistant Access
- **HA API accessible**: ✅ Token-based auth working
- **Logbook accessible**: ✅ Recent 24h logs retrieved successfully
- **Recent activity (last 2h)**:
  - Normal state transitions (lights, media players, automations)
  - Gäste WC automation triggering normally
  - Spotify playback, device presence tracking
  - Hue dimmer interactions
  - Garage door operations (normal)
  - iPhone charging status updates
  - Backup system: automatic backup completed successfully at 03:00 UTC
  
- **Security observations**:
  - No suspicious login attempts in recent logs
  - No unauthorized automations triggered
  - No exposed tokens in visible logs
  - Expected device activity patterns

### Recommendations
1. **Configure reverse proxy security**: If HA is behind a proxy, update `trustedProxies`
2. **Review command allowlist**: Clarify camera/screen/calendar command names in OpenClaw config
3. **Consider model upgrade**: For production deployments with external inputs

### Actions Taken
- Ran `openclaw security audit` successfully
- Verified HA API connectivity
- Reviewed logbook for anomalies
- No critical issues detected

---

**Next audit**: 2026-04-11 06:04 UTC (24h from now)
