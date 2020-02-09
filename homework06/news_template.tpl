<!DOCTYPE html>
<html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/jquery@3.3.1/dist/jquery.min.js"></script>
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/fomantic-ui@2.8.3/dist/semantic.min.css">
        <script src="https://cdn.jsdelivr.net/npm/fomantic-ui@2.8.3/dist/semantic.min.js"></script>
        <!-- 
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link> 
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
        -->
        <style>
            body {
                background: #4079b1;
            }
        </style>

        

        
    </head>
    <body>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled inverted table">
            <thead>
                <th class='center aligned'>Title</th>
                <th class='center aligned'>Author</th>
                <th class='center aligned'>Upvotes</th>
                <th class='center aligned'>Comments</th>
                <th class='center aligned' colspan="3">Label</th>
            </thead>
            <tbody>
                %for row in rows:
                <tr>
                    <td><a href="{{ row.url }}">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td class='right aligned'>{{ row.upvotes }}</td>
                    <td class='right aligned'>{{ row.comments }}</td>
                    <td><a href="/add_label/?label=good&id={{ row.id }}"><em data-emoji=":blue_heart:"></em></a></td>
                    <td><a href="/add_label/?label=maybe&id={{ row.id }}"><em data-emoji=":thinking:"></a></td>
                    <td><a href="/add_label/?label=never&id={{ row.id }}"><em data-emoji=":broken_heart:"></em></a></td>
                </tr>
                %end
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/update" class="ui right floated small primary button">I Wanna more Hacker News!</a>
                    </th>
                </tr>
            </tfoot>
        </table>
        </div>
    </body>
</html>
