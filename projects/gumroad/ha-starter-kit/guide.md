# 📖 Home Assistant Setup Guide 2025

## Quick Start

### 1. Organize Your Entities
Name everything clearly from the start:
- `light.living_room` not `light.entity_123abc`
- Use Areas: assign every device to a room
- Use friendly names that make sense

### 2. Essential HACS Integrations
Install these first:
- **Mushroom Cards** - beautiful modern UI cards
- **Mini Graph Card** - for sensor history
- **Layout Card** - advanced dashboard layouts
- **Browser Mod** - popup cards & more

### 3. Best Free Integrations
- **Google Cast** - control speakers
- **Spotify** - music control
- **Mobile App** - phone battery, location
- **HACS** - community store

### 4. Automation Tips
- Always use `mode: single` to prevent duplicate runs
- Use `input_boolean` for toggleable features
- Use `input_datetime` for times (changeable from UI)
- Test automations manually before trusting them

### 5. Dashboard Best Practices
- One view per room OR per function
- Use grid cards for lights (visual, quick)
- Media control cards for speakers
- Keep status/monitoring on separate view

### 6. Backup!
Set up automatic backups immediately:
Settings → System → Backups → Configure automatic backups

### 7. Naming Convention
```
domain.area_device
light.bedroom_ceiling
switch.kitchen_coffee_machine
sensor.living_room_temperature
```

## Useful Resources
- docs.home-assistant.io (official docs)
- r/homeassistant (community)
- community.home-assistant.io (forum)

---
Made with ❤️ by Clawy Studio
clawy.studio@gmail.com
