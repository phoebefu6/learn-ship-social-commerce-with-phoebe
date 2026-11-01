"""The PRE-WRITTEN, CONSTRUCTED gen AI outputs the bench scores live.

A browser cannot run a language model, so these twenty outputs were written by hand to behave the way
draft listing copy and review summaries behave: most are fine, some carry a banned claim, one gets a
number wrong, one is right but in a unit the rubric does not read, one invents a fact the rubric does
not check. The facts they talk about are REAL derived facts (category and weight from the Olist
products table; review counts, mean score and share of 1-2 star reviews recomputed live by the engine
from the review SCORES). No Olist review text is used anywhere.

golden = the hand-labelled verdict a careful reviewer gives each output (True = fit to publish).
"""

GENAI = {
    "banned": [
        {"label": "superlative 'best'", "re": "\\bbest\\b"},
        {"label": "guarantee", "re": "\\bguarantee(d|s)?\\b"},
        {"label": "number one", "re": "#1|\\bnumber one\\b"},
        {"label": "100 percent", "re": "\\b100 ?(%|percent)"},
        {"label": "lowest price", "re": "\\blowest price"},
        {"label": "free shipping", "re": "\\bfree shipping"},
        {"label": "authenticity claim", "re": "\\b(original|authentic|genuine)\\b"},
        {"label": "certification claim", "re": "\\bcertified\\b"},
        {"label": "sentiment scores cannot show", "re": "\\b(love|loves|loved|rave|raves)\\b"},
        {"label": "absolute claim", "re": "\\b(always|never|everyone)\\b"},
    ],
    "length": {"listing": [25, 70], "summary": [20, 60]},
    "items": [
        {"id": "L1", "kind": "listing", "ref": "SKU-01", "golden": True,
         "text": "A sturdy pick for weekend gardeners. This garden tools item weighs 1550 g, so it is solid in the hand "
                 "without tiring the wrist. It ships from a seller in Sao Paulo state (SP). Check the photos for the "
                 "exact fittings before you order."},
        {"id": "L2", "kind": "listing", "ref": "SKU-02", "golden": False,
         "text": "The best piece of furniture decor you will buy this year. At 2600 g it feels substantial and looks "
                 "far more expensive than it is. Free shipping on every order and a finish that turns heads in any "
                 "living room."},
        {"id": "L3", "kind": "listing", "ref": "SKU-03", "golden": True,
         "text": "Built for regular use in small and mid-sized yards. A garden tools item at 1650 g, balanced for "
                 "longer jobs. Sent by a seller based in Sao Paulo state (SP). Measurements and care notes are in the "
                 "photos on this listing."},
        {"id": "L4", "kind": "listing", "ref": "SKU-04", "golden": True,
         "text": "A heavier option in the garden tools range for people who prefer weight behind each stroke. It "
                 "comes in at 1.75 kg and ships from a seller in Sao Paulo state (SP). Compare the handle length in "
                 "the photos with your current tool."},
        {"id": "L5", "kind": "listing", "ref": "SKU-05", "golden": True,
         "text": "A compact add-on for a home or office desk. This computers accessories item weighs 533 g and ships "
                 "from a seller in Pernambuco (PE). Check the connector type and cable length in the photos before "
                 "buying."},
        {"id": "L6", "kind": "listing", "ref": "SKU-06", "golden": False,
         "text": "An authentic watch from our watches gifts collection, guaranteed to impress. It weighs 584 g "
                 "including the presentation box, which makes it ready to give the moment it arrives. Sent from Sao "
                 "Paulo state (SP)."},
        {"id": "L7", "kind": "listing", "ref": "SKU-07", "golden": True,
         "text": "Soft furnishing for everyday use. This bed bath table item weighs 1383 g in its packaging and ships "
                 "from a seller in Sao Paulo state (SP). Sizes and colours are shown in the photos; wash guidance is "
                 "on the label."},
        {"id": "L8", "kind": "listing", "ref": "SKU-08", "golden": False,
         "text": "A gift-ready piece from the watches gifts range, presented in a firm box. Total weight is 1000 g. It "
                 "ships from Sao Paulo the day after payment clears, so most buyers in the south east receive it "
                 "within the week."},
        {"id": "L9", "kind": "listing", "ref": "SKU-09", "golden": True,
         "text": "A dependable all-rounder for planting and weeding. This garden tools item weighs 1500 g and is sent "
                 "by a seller in Sao Paulo state (SP). The photos show the blade width and grip so you can compare it "
                 "with what you own."},
        {"id": "L10", "kind": "listing", "ref": "SKU-10", "golden": True,
         "text": "A light everyday item from the health beauty range. It weighs 200 g, small enough for a travel bag, "
                 "and ships from a seller in Sao Paulo state (SP). Ingredients and usage notes are printed on the "
                 "pack shown in the photos."},
        {"id": "S1", "kind": "summary", "ref": "Store 2", "golden": True,
         "text": "Across 153 reviews this store averages 3.9 out of 5. About 18% of scores are one or two stars, "
                 "higher than most stores in the top ten, so delivery and description checks are worth a look."},
        {"id": "S2", "kind": "summary", "ref": "Store 3", "golden": True,
         "text": "This store has 152 reviews with an average score of 4.0. Roughly 18% are one or two stars; the "
                 "average is solid but the low tail is the place to dig."},
        {"id": "S3", "kind": "summary", "ref": "Store 4", "golden": False,
         "text": "Customers love this store. It has 137 reviews averaging 4.2, and only 14% of scores sit at one or "
                 "two stars, which tells you buyers keep coming back for the quality."},
        {"id": "S4", "kind": "summary", "ref": "Store 1", "golden": True,
         "text": "Store 1 carries 121 reviews and averages 4.3. About 12% of scores are one or two stars, a smaller "
                 "low tail than most of its peers in this group."},
        {"id": "S5", "kind": "summary", "ref": "Store 5", "golden": False,
         "text": "With 210 reviews and an average of 4.3, this store sits near the top of the group. Only 8% of "
                 "scores are one or two stars."},
        {"id": "S6", "kind": "summary", "ref": "Store 8", "golden": True,
         "text": "Store 8 has 112 reviews averaging 4.1. About 16% of scores are one or two stars, close to the "
                 "middle of the group, so no single issue stands out from the scores alone."},
        {"id": "S7", "kind": "summary", "ref": "Store 10", "golden": True,
         "text": "Across 106 reviews the average score is 4.0. Some 16% of scores are one or two stars. The scores "
                 "say how buyers rated orders, not why; read the order notes before acting."},
        {"id": "S8", "kind": "summary", "ref": "Store 6", "golden": True,
         "text": "Store 6 has 101 reviews and the lowest average in the group at 3.5. About 24% of scores are one or "
                 "two stars, the largest low tail here and the first store to review."},
        {"id": "S9", "kind": "summary", "ref": "Store 9", "golden": True,
         "text": "This store has 96 reviews with an average of 4.1. Around 11% of scores are one or two stars, a "
                 "comparatively small low tail for its volume."},
        {"id": "S10", "kind": "summary", "ref": "Store 11", "golden": True,
         "text": "Store 11 holds 91 reviews averaging 4.3, with about 9% of scores at one or two stars. It is one of "
                 "the steadier stores in the group on scores alone."},
    ],
}
