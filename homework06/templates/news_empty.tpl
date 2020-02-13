<!DOCTYPE html>
<html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/jquery@3.3.1/dist/jquery.min.js"></script>
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/fomantic-ui@2.8.3/dist/semantic.min.css">
        <script src="https://cdn.jsdelivr.net/npm/fomantic-ui@2.8.3/dist/semantic.min.js"></script>
        <style>
            body {
                background: #4079b1;
            }
        </style>
    </head>
    <body>
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

        <div class="ui container" style="padding: 10px 0 20px 0;">
            <div class="ui horizontally fitted inverted placeholder segment">
                <div class="ui icon header">
                    <i class="search icon"></i>
                    Looks like no more news in here
                </div>
                <div class="inline">
                    <a href="/update" class="ui primary button">Add 30 more</a>
                    <a href="/all" class="ui button">Go to all news</a>
                </div>
            </div>
        </div>
    </body>
</html>
