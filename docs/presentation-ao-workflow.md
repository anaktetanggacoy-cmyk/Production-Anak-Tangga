# Presentation AO workflow

Presentation AO (APO) exports saved SketchUp scenes directly to PNG. Its deliverables are checked exports and a manifest containing the model revision, scene name, intended view title, export filename, image dimensions, and verification status.

## Workflow routing

For a complete deck, start with APO for direct views or APR (Presentation Render) for rendered views. Continue through API (Canva Insert), APM (Canva Material), APF (Canva Floor Plan), and APS (Canva Section Plan). Use the same Canva working copy and scene-to-page manifest throughout. A stage can also run on its own with verified inputs. Follow the requested deck order when placing pages.

## APO export


1. **Confirm the brief.** Identify the project, milestone, SketchUp model revision, scene range, and Canva reference or destination. Confirm the live model path, saved scene list, Canva destination, and target page range before editing. Test the SketchUp connector and desktop controls separately.
2. **Check the sources.** Cross-check the current design development and detailed design drawings, drawing schedule, and model for official room names, view titles, drawing codes, levels, key plans, and section or detail references. Verify material codes against the applicable schedule or catalogue. Resolve discrepancies using the source revisions, measured geometry, and approval records.
3. **Prepare the scene manifest.** Read the saved scene names and order from SketchUp. Record the source revision, saved scene, verified view title and drawing code where applicable, output filename, image dimensions, intended destination if known, and verification status. Report gaps in scene numbering.
4. **Export directly from SketchUp.** Test one PNG first. Check camera framing, visibility, image dimensions, and aspect ratio. Export the remaining scenes at consistent settings. Verify the files on disk if an export call times out, since SketchUp may finish writing afterward. Preserve the source model and saved cameras. Restore the originally selected scene. Hand the inspected PNGs and manifest to API.

## Downstream Canva handoff

API places the approved assets. APM verifies material codes and adds legends, callouts, and keyplans. APF exports and annotates the measured floor plan. APS exports and annotates the measured section and verifies the final deck. Apply the following checks when running those stages.

5. **Prepare the Canva design.** Copy the supplied reference or approved milestone template when creating a new presentation. Preserve its page size, typography, borders, and logo. For a new layout without a reference, follow the studio guidelines for Inter typography, a warm white background, and clear page borders.
6. **Place the exports in Canva.** Upload the PNGs directly to Canva and replace the images in the existing frames. Keep the scene labels aligned with the scene-to-page map and check image proportions and crop. Replace sample project text with verified project details.
7. **Add technical annotations.** Derive dimensions and areas from the current model or drawings. Record the source revision, units, measurement endpoints or area basis, and referenced geometry. Use the specified elevation datum and distinguish inferred room labels from official names. Build headings, material codes, descriptions, callout labels, badge shapes, leader lines, and keyplan labels and markers as individual, ungrouped Canva elements. Keep keyplan artwork and circular material swatches as separate replaceable images. Use Inter and distinguish the legend title, category headings, codes, and descriptions through size and weight. Place the room or view title at the upper right, the keyplan on the view, and the legend beside it. Use olive category headings, compact code badges and regular-weight descriptions. Omit empty categories and size swatches to fit without crowding the text. Order categories as Floor, Wall, Openings, Fixtures where applicable, Architectural Detail, and Ceiling. Match each callout to one verified schedule entry. If the connector cannot add native elements, test transferring them from an editable Canva source page using the editor. Verify positions and independent selection before removing the superseded overlay.
8. **Review and deliver.** Check every changed page for the correct view, readable labels, crop, alignment, individually selectable annotations, and duplicate overlays. Preview the draft and get approval where the Canva editing flow requires it. Save the design and verify the page count, order, and preservation of unrelated pages. Deliver the Canva link, scene-to-page map, and screenshots showing the checked layout.
