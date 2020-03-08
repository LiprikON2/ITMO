<div class="fluid ui buttons">
    <button 
        onclick="window.location.href = '/add_label/?label=upvote&id={{ row.id }}&redirected_from=unlabeled';"
        class="ui animated fade medium positive button"
        style="min-width: 5em;">
            <div class="visible content"><i class="arrow up icon"></i></div>
            <div class="hidden content">Upvote</div>
    </button>
    <button 
        onclick="window.location.href = '/add_label/?label=maybe&id={{ row.id }}&redirected_from=unlabeled';" 
        class="ui animated fade medium button">
            <div class="visible content"><i class="meh outline icon"></i></div>
            <div class="hidden content">Maybe</div>
    </button>
    <button 
        onclick="window.location.href = '/add_label/?label=downvote&id={{ row.id }}&redirected_from=unlabeled';" 
        class="ui animated fade medium negative button"
        style="min-width: 5em;">
            <div class="visible content"><i class="arrow down icon"></i></div>
            <div class="hidden content">Downvote</div>
    </button>
</div>