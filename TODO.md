# Design and project planning document

## List of tasks to do

- [X] Introduce cooldown time for player
- [ ] Introduce path finding for enemys, i.e., to look for you when they see you.
- [ ] Introduce UI with health, items, etc. This will involve changing the current size of the playable screen and posibly entering some conditions for not redrawing the UI while is not changing.
- [ ] Improve Sprite Images
        - [ ] Introduce death animation (I'm looking something like ninja gaiden)
- [ ] Introduce dungeon entering logic, i.e., what tiles do load another set of maps.
- [ ] Introduce text system for reading signs.
- [ ] Introduce layering in map tiles so that player can be drawn between layers, e.g., under the leaves of a tall tree.
- [ ] Introduce Big Boss.
- [ ] Introduce Item picking in, e.g., chests, on the floor leaved by enemies
        - [ ] Introduce new weapons
        - [ ] Introduce currency
- [ ] Designs at least one dungeon.

## Some details to be aware of

- Enemies hitboxes default to the sprite size of the animation. This is automatic and therefor quite nice. To be more flexible think about defining the hitbox size independently.

## Current Issues

- [ ] UI Background is not configurable and defaults to black
- [ ] Change of hearts from 1 to 0.5 is not rendered. Change the hearts to be an integer number, i.e., 2*actual number