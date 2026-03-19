# Overnight Build Log — autoflow-lab.github.io/demo.html

## v6 — 2026-03-14 ~23:00 UTC
- **Floor plan completely rewritten** with SVG texture patterns:
  - Wood grain for living room and office (two directions)
  - Ceramic tile grid for kitchen
  - Hexagonal tile for bathroom
  - Carpet texture for bedroom
  - Grass pattern for garden
- **Room-wide glow illumination**: When light is ON, entire room fills with colored radial gradient (not just dots)
- Light ring indicators added around each ceiling light
- Living room floor lamp added
- Detailed furniture: L-sofa, coffee table, desk+monitor, bathtub, chairs, wardrobe, plants
- Compass rose + scale bar

## v7 — 2026-03-14 ~23:30 UTC
- **Tier showcase** added (3 complexity levels with mini-dashboard previews):
  - Basic $49: room toggle grid
  - Standard $99: full dashboard preview
  - Premium $149: floor plan preview (dark)
- **Social proof section**: 4 review cards + stats bar (47 clients, 98% 5-star, 2.3d delivery)
- **Portfolio gallery**: 3 project previews with different themes
- **Hero device mockup**: floating phone + tablet showing the dashboard

## STILL TODO
- [ ] Dark mode neon glow polish (floor plan in dark)
- [ ] Before/After comparison slider
- [ ] Better mobile layout for floor plan
- [ ] AI tab improvements  
- [ ] Animation / scroll effects polish
- [ ] Loading skeleton or progressive reveal

## v8 — 2026-03-15 ~03:00 UTC
- Before/After comparison slider (drag to compare default HA vs custom)
- Portfolio gallery (3 project mockups with inline CSS previews)
- Hero device mockup (floating phone + tablet)

## v9 — 2026-03-15 ~03:30 UTC
ANIMATIONS:
- Scroll progress bar (top of page, gradient in dark mode)
- Hero particles (floating colored orbs, 18 per hero)
- 3D tilt effect on tier/review/portfolio cards with shine overlay
- Stats counter animation (count up from 0 on scroll-in)
- Live clock in dashboard (HH:MM:SS)
- Light spread animation (expanding ring from bulb when toggled ON)
- Staggered scene transition (rooms light up sequentially)
- Ambient background tint changes per scene (relax=warm, movie=purple)
- Scene button ripple effect on click
- Custom scrollbar (thin, dark-themed)
- wf-node pulse on final "You're notified" step

DESIGN:
- Floor plan dark mode: darker outer walls, neon glow on bulbs
- Glassmorphism on cards in dark mode (rgba backdrop-filter)
- Nav drop shadow in dark mode
- Hero eyebrow icon changes to ⬡ in dark mode
- Tier price gradient text in dark mode
- wf-notify node pulse animation
- Button shine overlay effect

AI TAB:
- Redesigned AI hero with animated workflow diagram (4 nodes + moving dots)
- Live automation ticker (scrolling list of automations)
- "Automations running right now" live indicator

## STILL TODO
- [ ] Floor plan: maybe add room name tooltips on hover
- [ ] Add "What's included" expandable detail per tier
- [ ] Order form UX improvements
- [ ] Better mobile view of floor plan (pinch to zoom?)
- [ ] Testimonial video placeholder
- [ ] SEO meta tags

## v10 — 2026-03-15 ~04:00 UTC
- Room hover tooltips (name, current color, on/off state)
- SEO meta tags (description, og:title, og:description, twitter card, theme-color)
- How it works timeline (AI tab — 4 steps with animated icons)
- Automation ticker (scrolling live automations list)

## v11 — 2026-03-15 ~04:30 UTC
- Trust badges row (48h delivery, guarantee, docs, revision, languages)
- Floating Action Button (💬 Free Quote, bottom right, responsive)
- Better footer with links and email
- Glassmorphism polish across all cards in dark mode

## STILL TODO
- [ ] Add a "FAQ expanded" or contact form in AI tab
- [ ] Test all interactive elements
- [ ] Optimize file size (currently ~248KB)
- [ ] Add keyboard navigation for modals
- [ ] Tab close on Escape key for color picker
