# Working in this repo

Two templates in the Decarb-AI style. Put the user's content into them; leave the style files alone unless the user
asks to restyle.

## Poster (`poster/`)

Edit `poster.html` only; the look lives in `decarb.css`. The page is A0 portrait, built from rows of cards.

```html
<div class="row">                              <!-- cards side by side -->
  <section class="card" style="--w: 2">        <!-- --w: relative width, default 1 -->
    <h2><span>Introduction</span></h2>         <!-- section tab: keep the span -->
    <p class="question">The question, in one sentence?</p>
    <p>Text, with <span class="em-1">key words</span> or <span class="em-2">others</span> marked.</p>
  </section>
</div>

<div class="row grow">...</div>                <!-- takes the leftover height; use on one row only -->

<div class="figures" style="--cols: 3">        <!-- grid of figures, 2 columns by default -->
  <figure>
    <img src="figures/fig1.png" alt="What it shows">
    <figcaption><strong>Fig. 1:</strong> What it shows, in one sentence.</figcaption>
  </figure>
</div>

<ol class="steps"><li><strong>Step.</strong> One or two sentences.</li></ol>   <!-- numbered boxes in a row -->
<p class="callout">The one result to remember.</p>
<section class="card filled">...</section>                                     <!-- blue box, for conclusions -->
<section class="card references"><p>Author (2024). Title. <em>Journal</em>.</p></section>
```

- Figures go in `poster/figures/` as PNG (300 dpi) or SVG. Wide figures (about 2:1) use the space best.
- Keep text short; a poster is read from two metres away.
- Use the colour variables in `decarb.css`; don't put hex codes in `poster.html`.
- After every change run `python render.py` and fix each `PROBLEM` line (text overflowing a card or the page, or a
  missing image) before showing the result. If it can't run, open `poster.html` in Chrome to look.

## Slides (`slides/`)

Edit `main.tex` only; the look lives in `beamerthemedecarb.sty`. Build with `latexmk -pdf main.tex` (pdfLaTeX).

- `\maketitleframe` for the title slide; `\begin{frame}{Title}` for content; the `conclusions` environment for the
  closing slide; slides after `\appendix` are backup and not counted.
- Cover photo: `\renewcommand{\titlephoto}{assets/photo-2.jpg}` or the user's own file.
- Chart colours for TikZ and pgfplots: `decarbchart1` to `decarbchart6`.

## Figures

In matplotlib, `plt.style.use("decarb.mplstyle")` applies the chart colours in order. `PALETTE.md` lists every
colour and which are dark enough for text.
