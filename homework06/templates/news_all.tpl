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
            a {
                color: #05d8cf;
            }
            a:hover {
                color: #00b5ad;
            }
        </style>
    
    </head>
    <body>
        <div class="ui secondary pointing menu inverted">

            <a href="/all" class="item active">
                All news
                <div class="ui label teal left pointing">{{ count['all'] }}</div>
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
            <table class="ui selectable large celled inverted table">
                <thead>
                    <th class='center aligned'>Title</th>
                    <th class='center aligned'>Author</th>
                    <th class='center aligned'>Upvotes</th>
                    <th class='center aligned'>Comments</th>
                    <th class='center aligned'>Label</th>
                </thead>
                <tbody>
                    %for row in rows:
                    <tr>
                        <td><div><a href="{{ row.url }}">{{ row.title }}</a></div></td>
                        <td><div>{{ row.author }}</td>
                        <td class='right aligned'><div>{{ row.upvotes }}</div></td>
                        <td class='right aligned'><div>{{ row.comments }}</div></td>
                        <td><div>{{ row.label }}</div></td>
                    </tr>
                    %end
                </tbody>
                <tfoot class="full-width">
                    <tr>
                        <th colspan="7">
                            <a href="/drop" class="ui left floated small primary negative button">Drop table</a>
                            <a href="/update" class="ui right floated small primary button">I Wanna 30 more Hacker News!</a>
                        </th>
                    </tr>
                </tfoot>
            </table>
        </div>
    </body>
</html>
