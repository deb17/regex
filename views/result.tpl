% if result == 'error':
<p><strong>Error in re</strong></p>
% elif result:
<h3 class="mb-0 mt-2">Result</h3>
<small>All matches highlighted.</small>
<div class="mb-1 mt-2">The first match:</div>
<p class="resultPara"><b>Group:</b> {{! result[0] }}</p>
<p class="resultPara"><b>Subgroups:</b> {{! result[1] }}</p>
<p class="resultPara"><b>Group Dict:</b> {{! result[2] }}</p>
% end
