with open("/config/automations.yaml", "r") as f:
    content = f.read()

old = "entity_id: binary_sensor.shelly_buttons_wohnzimmer_input_3\n      to: 'on'\n      trigger: state"
new = "entity_id: binary_sensor.shelly_buttons_wohnzimmer_input_3\n      to: 'on'\n      for:\n        milliseconds: 200\n      trigger: state"

if old in content:
    content = content.replace(old, new)
    with open("/config/automations.yaml", "w") as f:
        f.write(content)
    print("Debounce fixed")
else:
    print("Pattern not found, checking...")
    idx = content.find("govee_knopf_toggle")
    print(repr(content[idx:idx+400]))
