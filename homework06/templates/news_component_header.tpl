<div class="ui secondary pointing menu inverted">

    <a href="/all" class="item">
        All news
        <div class="ui label">{{ count['all'] }}</div>
    </a>
    <a href="/unlabeled" class="item">
        Unlabeled news
        <div class="ui label">{{ count['unlabeled'] }}</div>
    </a>
    <a href="/upvoted" class="item">
        Upvoted news
        <div class="ui label">{{ count['upvoted'] }}</div>
    </a>
    <a href="/maybe" class="item">
        Maybe'ed news
        <div class="ui label">{{ count['maybe'] }}</div>
    </a>
    <a href="/downvoted" class="item">
        Downvoted news
        <div class="ui label">{{ count['downvoted'] }}</div>
    </a>

    <div class="right menu">
        <div class="item">
            <div class="ui transparent icon input inverted">
                <input type="text" placeholder="Search...">
                <i class="search link icon"></i>
            </div>
        </div>
    </div>
</div>
