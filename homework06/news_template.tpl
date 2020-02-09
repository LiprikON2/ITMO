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
        <!--
            table {
                border-collapse: collapse;
            }
            tr, td {
                padding: 0;
            }
            tr td div {
                max-height: 0px;
                padding: 0 10px;
                box-sizing: border-box;
                overflow: hidden;
                transition: max-height 0.3s, padding 0.3s;
            }
            tr.active1 td div {
                max-height: 50px;
                padding: 10px 10px;
                transition: max-height 0.6s, padding 0.6s;
            }
        -->
            
        

        
    </head>
    <body>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui large celled inverted table">
            <thead>
                <th class='center aligned'>Title</th>
                <th class='center aligned'>Author</th>
                <th class='center aligned'>Upvotes</th>
                <th class='center aligned'>Comments</th>
                <th class='center aligned' colspan="1">Label</th>
            </thead>
            <tbody>
                %for row in rows:
                <tr class='active1'>
                    <td><div><a href="{{ row.url }}">{{ row.title }}</a></div></td>
                    <td><div>{{ row.author }}</td>
                    <td class='right aligned'><div>{{ row.upvotes }}</div></td>
                    <td class='right aligned'><div>{{ row.comments }}</div></td>
                    <td>
                        <div class="ui buttons">
                            <button 
                                onclick="
                                    $('tr:nth-child({{ 1 }})').toggleClass('active1'); 
                                    window.location.href = '/add_label/?label=good&id={{ row.id }}';"
                                class="small ui positive button">
                                Upvote
                            </button>
                            <button 
                                onclick="
                                    $('tr:nth-child({{ row.id - 1 }})').toggleClass('active1');
                                    window.location.href = '/add_label/?label=maybe&id={{ row.id }}';" 
                                class="small ui button">
                                Maybe
                            </button>
                            <button 
                                onclick="
                                    $('tr:nth-child({{ row.id - 1 }})').toggleClass('active1');
                                    window.location.href = '/add_label/?label=never&id={{ row.id }}';" 
                                class="small ui negative button">
                                Downvote
                            </button>
                        </div>
                    </td>
                    <!--
                    <td><a href="/add_label/?label=good&id={{ row.id }}"><em data-emoji=":blue_heart:"></em></a></td>
                    <td><a href="/add_label/?label=maybe&id={{ row.id }}"><em data-emoji=":thinking:"></a></td>
                    <td><a href="/add_label/?label=never&id={{ row.id }}"><em data-emoji=":broken_heart:"></em></a></td>
                    -->
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
