<style type="text/css">
  .cbox {
    font-size: 0.8em;
  }
  #cboxes input {
    position: relative;
    top: 2px;
  }
</style>

<!-- <div class="col-sm-7 mt-2" id="cboxes"> -->
<div class="{{ cls }}" id="cboxes">
  <input type="checkbox" name="icase" id="icase" {{ 'checked' if flags[0] == 'i' else '' }}>
  <label for="icase" class="cbox mr-3">IGNORECASE</label>

  <input type="checkbox" name="dall" id="dall" {{ 'checked' if flags[1] == 's' else '' }}>
  <label for="dall" class="cbox mr-3">DOTALL</label>
  <br class="d-inline d-sm-none">
  <input type="checkbox" name="vbose" id="vbose" {{ 'checked' if flags[2] == 'x' else '' }}>
  <label for="vbose" class="cbox mr-3">VERBOSE</label>
  <br class="d-none d-md-inline {{ 'd-lg-none' if index else '' }}">
  <input type="checkbox" name="ascii" id="ascii" {{ 'checked' if flags[3] == 'a' else '' }}>
  <label for="ascii" class="cbox mr-3">ASCII</label>
  <br class="d-inline d-sm-none">
  <input type="checkbox" name="mline" id="mline" {{ 'checked' if flags[4] == 'm' else '' }}>
  <label for="mline" class="cbox">MULTILINE</label>
</div>
