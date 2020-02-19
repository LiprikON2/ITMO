<!DOCTYPE html>
<html>
    <head>
        <link rel="apple-touch-icon" sizes="180x180" href="static/apple-touch-icon.png">
        <link rel="icon" type="image/png" sizes="32x32" href="static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="static/favicon-16x16.png">
        <link rel="manifest" href="static/site.webmanifest">
        <script src="https://cdn.jsdelivr.net/npm/jquery@3.3.1/dist/jquery.min.js"></script>
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/fomantic-ui@2.8.3/dist/semantic.min.css">
        <script src="https://cdn.jsdelivr.net/npm/fomantic-ui@2.8.3/dist/semantic.min.js"></script>
        <link rel="stylesheet" href="static/styles.css">
        <title>News - nothing in here =(</title>
    </head>
    <body>
        % include('./templates/news_component_header')

        <div class="ui container" style="padding: 10px 0 20px 0;">
            <div style="background-color: #2b2b2b;" class="ui horizontally fitted inverted placeholder segment">
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
        <script type="text/javascript" src="static/script.js"></script>
    </body>
</html>
