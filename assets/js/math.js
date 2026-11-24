// Render LaTeX in posts with KaTeX. Pluto marks its math with class "tex" ($...$ / $$...$$);
// Markdown posts can use $$...$$, \( ... \) or \[ ... \].
document.addEventListener('DOMContentLoaded', function () {
  if (!window.renderMathInElement) return;
  var prose = document.querySelector('.prose');
  if (!prose) return;
  var opts = { throwOnError: false, delimiters: [
    { left: '$$', right: '$$', display: true },
    { left: '\\[', right: '\\]', display: true },
    { left: '\\(', right: '\\)', display: false }
  ] };
  document.querySelectorAll('.prose .tex').forEach(function (el) {
    renderMathInElement(el, { throwOnError: false, delimiters: [
      { left: '$$', right: '$$', display: true },
      { left: '$', right: '$', display: false }
    ] });
  });
  renderMathInElement(prose, opts);
});
