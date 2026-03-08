---
id: rli_003_mega_merge_game
name: "RLI: Mega Merge Game"
category: web_development
grading_type: hybrid
timeout_seconds: 600
workspace_files: []
grading_weights:
  automated: 0.4
  llm_judge: 0.6
---

## Prompt

Create a casual, web-based game called "Mega Merge" where players combine falling objects to reach the highest-level item possible. The game should be inspired by the popular Watermelon Game but incorporate unique mechanics and features. It should be designed for accessibility and smooth play on any device, with a responsive layout suitable for both desktop and mobile play.

### Objective

Players will aim to combine objects and score as many points as possible before the box fills up. By merging two identical items, players will create a higher-level item. The goal is to manage space strategically while maximizing the score.

The game should have a brewing theme, with the following objects (in order of merging):
1. Water droplet
2. Barley grain
3. Malt bag
4. Orange
5. Lime
6. Hops
7. Pistachio
8. Honey
9. Beer can with open pull tab
10. Mug of beer
11. Barrel of beer

### Key Features

- Platform: Web-based, compatible with all major browsers (Chrome, Safari, Firefox, Edge).
- Cross-Platform Compatibility: Works seamlessly on desktop and mobile (iOS and Android) with responsive layouts.
- Controls: Supports both touch gestures (tap, swipe) and mouse clicks for flexible gameplay.
- Quick Load Times: Lightweight assets and optimized code to ensure rapid load speeds, even on low-end devices.
- Instant Playability: No downloads required; players can start immediately by opening the game in their browser.

### Technical Requirements

- Implementation: The game should be implemented directly using HTML, CSS, and JavaScript. The developer may use a JavaScript framework such as Phaser.js or Construct 3 if it facilitates development and provides necessary physics capabilities. Vanilla JavaScript is also acceptable if it meets all requirements.
- Physics and Collisions: Objects should obey basic physics. They should fall naturally within a defined "box" and exhibit slight bounce effects when landing or colliding with each other. This behavior can be achieved with a physics engine like matter.js or through Construct 3's physics behavior. The collisions boxes for objects should match the object shapes.
- File Size: The total file size should be kept under 5 MB to ensure fast loading.

### Gameplay Mechanics

- Object Merging: Players combine matching items to generate higher-level objects, aiming to reach the final item. Two items combine to form a higher-level item.
- Score Maximization: Each successful merge scores points. Merging high-level items gives more points.
- Limited Space: Players must manage space carefully within a defined container—if the box fills up, the game ends.
- In general, higher-level items should be physically larger than smaller items, but not always.
- If objects cross the top of the box, the round should end. A screen should appear on top of the game saying "Brewing Results" with an indication of which items were reached this round. There should be a button to start a new round.
- Objects should have non-uniform shapes. The collision boxes should match the object shapes.

### Visual & UI Design

- Container Box: Objects should fall into a clearly defined "box" area with visible boundaries, guiding the player's actions.
- Falling Indicator: The next item should have an indicator at the bottom of the screen to show where it will fall, helping players plan their moves.
- Score Display: The score should be displayed prominently at the top of the screen.
- Minimalist UI: Essential elements only—score display, "Next Item" preview, and basic pause/reset buttons at the top of the screen.
- Cartoon-Style Graphics: Use a cute/kawaii, colorful, and cartoonish visual style with simple lines and vibrant colors, similar to the Watermelon Game, for an approachable and relaxing aesthetic.
- Responsive Layout: The design should adapt seamlessly for both desktop and mobile screens.

### Audio and Sound Design

- Background Music: The game should include relaxing background music that plays continuously during gameplay to create a calm, enjoyable atmosphere.
- Sound Effects:
  - A satisfying sound effect should play when objects are dropped into the container.
  - A distinct, gratifying merging sound should play when two objects combine.
  - These sounds should enhance the feedback of each action, creating an engaging and satisfying player experience.

### Interaction and Controls

- Touch and Mouse Support: The game should support both touch gestures and mouse input to provide a smooth experience on both mobile and desktop platforms.
- Responsive Design: The layout should adjust for screen size changes to ensure accessibility and comfort on any device.

### Deliverables

Game Files: All files (HTML, CSS, JavaScript, images, and audio files) should be organized in a clear folder structure, with folders for assets, icons, images, scripts, styles, and sounds.

## Expected Behavior

The agent should:

1. Create a complete, playable web-based game using HTML, CSS, and JavaScript
2. Implement physics-based merging mechanics (using matter.js or similar)
3. Create 11 distinct item types with a brewing theme
4. Implement score tracking, game over detection, and round restart
5. Include responsive design for desktop and mobile
6. Organize output files in a clear folder structure
7. Generate or use placeholder graphics for the 11 item types

This is a replica of RLI public_003 (Object Merging Game, $1485 budget).

## Grading Criteria

- [ ] HTML file loads in a browser without errors
- [ ] Game container/box is visible with clear boundaries
- [ ] Objects fall with physics simulation (gravity, collision)
- [ ] Identical objects merge when colliding to form higher-level item
- [ ] All 11 item levels are defined in the merging hierarchy
- [ ] Score increments on successful merges
- [ ] Game ends when objects cross the top of the box
- [ ] "Brewing Results" screen appears on game over
- [ ] New round can be started after game over
- [ ] Responsive layout adapts to different screen sizes

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    """Grade the Mega Merge game task."""
    from pathlib import Path
    import re

    scores = {}
    workspace = Path(workspace_path)

    # Check for HTML file
    html_files = list(workspace.rglob("*.html"))
    scores["html_exists"] = 1.0 if html_files else 0.0

    # Check for JavaScript file(s)
    js_files = list(workspace.rglob("*.js"))
    scores["js_exists"] = 1.0 if js_files else 0.0

    # Check for CSS file(s)
    css_files = list(workspace.rglob("*.css"))
    scores["css_exists"] = 1.0 if css_files else 0.0

    # Check HTML content for key game elements
    if html_files:
        html_content = ""
        for f in html_files:
            html_content += f.read_text(errors="replace")

        # Check for canvas or game container
        has_canvas = bool(
            re.search(
                r"""(?ix) <canvas | game.?container | game.?box""",
                html_content,
            )
        )
        scores["game_container"] = 1.0 if has_canvas else 0.0

    # Check JS for game mechanics
    all_js = ""
    for f in js_files:
        all_js += f.read_text(errors="replace")

    # Physics engine or gravity
    has_physics = bool(
        re.search(
            r"""(?ix) matter\.js | gravity | physics | velocity | force""",
            all_js,
        )
    )
    scores["physics_implementation"] = 1.0 if has_physics else 0.0

    # Merging logic
    has_merge = bool(
        re.search(
            r"""(?ix) merge | combine | level.?up | upgrade""",
            all_js,
        )
    )
    scores["merge_logic"] = 1.0 if has_merge else 0.0

    # Score tracking
    has_score = bool(
        re.search(
            r"""(?ix) score | points""",
            all_js,
        )
    )
    scores["score_tracking"] = 1.0 if has_score else 0.0

    # Game over detection
    has_game_over = bool(
        re.search(
            r"""(?ix) game.?over | end.?game | brewing.?results""",
            all_js,
        )
    )
    scores["game_over"] = 1.0 if has_game_over else 0.0

    # Item hierarchy (11 items)
    brewing_items = [
        "water", "barley", "malt", "orange", "lime",
        "hops", "pistachio", "honey", "beer", "mug", "barrel",
    ]
    item_count = sum(
        1 for item in brewing_items
        if re.search(
            r"""(?ix)""" + re.escape(item),
            all_js,
        )
    )
    scores["item_hierarchy"] = min(1.0, item_count / 8.0)

    return scores
```

## LLM Judge Rubric

### Criterion 1: Game Functionality (Weight: 35%)

**Score 1.0**: Complete, playable game with physics-based merging, all 11 item levels, score tracking, game over detection, and round restart. Objects fall, collide, and merge correctly.
**Score 0.75**: Game is mostly functional with minor issues. Most mechanics work but may have bugs in edge cases.
**Score 0.5**: Basic game structure exists but significant mechanics are missing or broken. Objects may not merge correctly or physics are unreliable.
**Score 0.25**: Minimal game framework with major functionality gaps. Only basic rendering or placeholder logic.
**Score 0.0**: No functional game or completely broken implementation.

### Criterion 2: Visual Design & UI (Weight: 25%)

**Score 1.0**: Polished, cartoon-style graphics with distinct visuals for all 11 items. Clean UI with score display, next-item preview, and responsive layout. Brewing theme is clear.
**Score 0.75**: Good visual design with most items distinguishable. UI elements present but may lack polish.
**Score 0.5**: Basic visuals with geometric shapes or minimal styling. Some UI elements present.
**Score 0.25**: Very minimal visuals. Hard to distinguish items or understand game state.
**Score 0.0**: No visual design effort or unplayable UI.

### Criterion 3: Technical Quality (Weight: 25%)

**Score 1.0**: Well-structured code, proper physics engine integration, smooth performance, organized file structure with separate folders for assets/scripts/styles.
**Score 0.75**: Good code organization with minor issues. Physics work but may have occasional glitches.
**Score 0.5**: Functional but poorly organized code. Physics are basic or inconsistent.
**Score 0.25**: Disorganized code with significant technical issues.
**Score 0.0**: Non-functional or extremely poor code quality.

### Criterion 4: Responsiveness & Cross-Platform (Weight: 15%)

**Score 1.0**: Works perfectly on both desktop and mobile. Touch and mouse input supported. Layout adapts seamlessly to different screen sizes.
**Score 0.75**: Works on desktop with basic mobile support. Most interactions work on both platforms.
**Score 0.5**: Desktop-only or mobile-only. Input handling is limited.
**Score 0.25**: Fixed layout, no responsive design. Input handling is problematic.
**Score 0.0**: Does not work on any platform or no responsive considerations.
