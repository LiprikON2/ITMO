<!DOCTYPE html>
<html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/jquery@3.3.1/dist/jquery.min.js"></script>
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/fomantic-ui@2.8.3/dist/semantic.min.css">
        <script src="https://cdn.jsdelivr.net/npm/fomantic-ui@2.8.3/dist/semantic.min.js"></script>
        <link rel="stylesheet" href="static/styles.css">
    </head>
    <body>
        % include('./templates/news_component_header')

        <div class="ui container" style="padding: 10px 0 20px 0;">
            <table class="ui selectable large celled inverted table">
                <thead>
                    <th class='center aligned'>Title</th>
                    <th class='center aligned'>Author</th>
                    <th class='center aligned'>Upvotes</th>
                    <th class='center aligned'>Comments</th>
                    <th class='center aligned' style="width: 6%;">Label</th>
                </thead>
                <tbody>
                    %for row in rows:
                    <tr>
                        <td><div><a href="{{ row.url }}">{{ row.title }}</a></div></td>
                        <td><div>{{ row.author }}</div></td>
                        <td class='right aligned'><div>{{ row.upvotes }}</div></td>
                        <td class='right aligned'><div>{{ row.comments }}</div></td>
                        <td>
                            <button
                                onClick="window.location.href = '/remove_label/?id={{ row.id }}&redirected_from=upvoted'"
                                class="ui animated fade small toggle positive button">
                                <div class="visible content">Upvoted</div>
                                <div class="hidden content"><i class="times icon"></i></div>
                            </button>
                        </td>
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
        <script type="text/javascript" src="static/script.js"></script>
    </body>
</html>
