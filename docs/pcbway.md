# Splitmac and PCBWay

**Disclosure:** PCBWay sponsors splitmac. This write-up is the project's
GitHub promotion; no social media campaign is planned.

**Coverage status:** The repository contains a MacBook configuration, Voyager
firmware and keymap diagrams. It does not yet contain a PCBWay order record,
manufacturing files, delivered-part photographs or inspection results. The
ordering steps below are a guide; the physical-part sections describe the
evidence still needed to complete the showcase.

## 1. PCBWay's services

[PCBWay](https://www.pcbway.com/) offers PCB fabrication and assembly, plus
[CNC machining, 3D printing, sheet metal fabrication and injection moulding](https://www.pcbway.com/rapid-prototyping/).
These services can help keyboard builders source custom electronics and
mechanical parts such as plates, enclosures and mounts.

## 2. Project background

Splitmac brings a shared ergonomic layout to two keyboards: the MacBook's
built-in keyboard through Karabiner-Elements, and the ZSA Voyager through
QMK firmware. Numbers, symbols and navigation move onto layers so that the
same finger movements work on the laptop and the split keyboard.

The application is everyday typing and programming. The current project
does not require a custom PCB or enclosure to use the keymap. A future
hardware extension could involve a custom mount, case or plate, but no
specific PCBWay part, material or manufacturing process is established in
this repository yet. The Voyager is a commercial ZSA product; it is not
presented here as a PCBWay-manufactured keyboard.

See the [MacBook and Voyager layer diagrams](../README.md#base) and
[interactive MacBook keymap](../keymap.html) for the existing project.

## 3. Ordering walkthrough

For a mechanical part, start with PCBWay's
[CNC / 3D printing quote form](https://www.pcbway.com/rapid-prototyping/manufacture/).
This is a walkthrough of the process, not a record of a completed splitmac
order.

1. Prepare the part's CAD model and a drawing identifying critical dimensions,
   units, mating features and required tolerances.
2. Select the appropriate manufacturing service and upload the design in a
   format accepted by the form. For CNC, the form lists STEP among its CAD
   formats and asks for individual files rather than a ZIP archive.
3. Configure the material, quantity and finish for each part. Include the
   drawing and any fit or surface requirements with the request.
4. Submit the request and resolve any manufacturing questions before
   accepting the quote. PCBWay's [ordering FAQ](https://www.pcbway.com/rapid-prototyping/cnc-faq.html)
   distinguishes instant pricing for supported 3D printing materials from
   services requiring manual quotation. Use the reviewed quote for the
   actual price and lead time.
5. Confirm the specification and delivery details, complete payment when
   ready, and follow production and shipment through the account.

**Project demonstration pending:** Add screenshots of the actual design
upload, selected service/material/quantity/finish, and reviewed order
summary, with captions explaining the choices. Remove addresses, payment
details and other private account information before publishing.

## 4. Unboxing: packaging, quantity and surface quality

**Pending delivered-part photographs and observations.** To complete this
section, document the outer packaging and internal protection, count every
part against the order, and photograph the surfaces under clear lighting.
Record any damage, burrs, visible layer lines or finish variation as well
as what looks good.

The photo sequence should show:

1. The package and internal protection.
2. All delivered parts together, with the received quantity in the caption.
3. Close-ups of surfaces, edges, holes and mating features.
4. The parts installed in their final application.

These images belong in the GitHub write-up. There are no product photographs
in the repository yet; the existing keymap diagrams are not an unboxing.

## 5. Dimensions and precision

**Pending a part drawing and physical measurements.** Record nominal values
from the released design, the tolerances agreed for that order, and actual
measurements using a suitable instrument. Specify units and the measuring
tool. A dimensional check does not establish surface roughness or the
manufacturer's overall process capability.

| Feature | Nominal (mm) | Agreed tolerance (mm) | Measured (mm) | Deviation (mm) | Result |
| --- | --- | --- | --- | --- | --- |
| Overall length / width / thickness, as applicable | Pending design | Pending quote | Pending inspection | Pending | Pending |
| Hole diameter and centre spacing, if applicable | Pending design | Pending quote | Pending inspection | Pending | Pending |
| Critical mating feature, if applicable | Pending design | Pending quote | Pending inspection | Pending | Pending |

For each feature, calculate deviation as measured minus nominal. Report
whether it is within the agreed tolerance and describe the assembled fit.
No numerical accuracy claim can be made from the evidence currently in
this repository.

## 6. Final application

The existing application is an ergonomic typing layout shared between a
MacBook and a ZSA Voyager. The [source and diagrams](../README.md) show how
the same layers map onto both keyboards.

**PCBWay part integration pending:** Once a manufactured part is identified
and fitted, add an installed photograph, explain its function and attachment,
and describe the practical result during use. Include any fit problems or
changes needed. The current software diagrams demonstrate the keymap;
they do not demonstrate a manufactured part's performance.

## 7. Why PCBWay is relevant

PCBWay's service range offers several useful options for a keyboard builder:

- **Electronics and mechanics:** PCB fabrication and assembly are available
  alongside processes for custom plates, cases and mounts.
- **Process choice:** CNC machining and several 3D printing processes give
  builders options to match a part's geometry, material and finish needs.
- **Online quoting:** Uploading a design with the requested specifications
  makes it possible to obtain a quote before committing to production.

These are reasons the services are relevant to keyboard projects. A review
of the actual splitmac order's packaging, precision, finish, delivery and
fit will follow when the supporting evidence is available.

[Back to splitmac](../README.md)
